"""Puebla el catálogo de Shopify usando la Admin GraphQL API.

Uso desde la raíz del proyecto:
    python -m scripts.poblar_catalogo --dry-run   # solo muestra qué haría
    python -m scripts.poblar_catalogo             # crea productos y colecciones

El script es idempotente: si el SKU ya existe, lo omite.
"""

import argparse
import sys
from pathlib import Path

# Permite importar el módulo de la raíz aunque se ejecute como paquete.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from carrito.datos import cargar_catalogo  # noqa: E402
from shopify_client import graphql_query  # noqa: E402

PRODUCTOS_QUERY = """
{
  products(first: 250) {
    nodes {
      id
      title
      variants(first: 250) { nodes { sku } }
    }
  }
}
"""

LOCATIONS_QUERY = """
{
  locations(first: 10) { nodes { id name } }
}
"""

PRODUCT_CREATE = """
mutation ProductoCrear($input: ProductInput!) {
  productCreate(input: $input) {
    product { id title handle }
    userErrors { field message }
  }
}
"""

COLLECTION_CREATE = """
mutation ColeccionCrear($input: CollectionInput!) {
  collectionCreate(input: $input) {
    collection { id title handle }
    userErrors { field message }
  }
}
"""

COLLECTION_ADD = """
mutation AgregarProductos($id: ID!, $ids: [ID!]!) {
  collectionAddProducts(collectionId: $id, productIds: $ids) {
    collection { id title }
    userErrors { field message }
  }
}
"""


def skus_existentes():
    """Devuelve el conjunto de SKUs ya creados en la tienda."""
    datos = graphql_query(PRODUCTOS_QUERY)
    skus = set()
    for producto in datos["products"]["nodes"]:
        for variante in producto["variants"]["nodes"]:
            if variante["sku"]:
                skus.add(variante["sku"])
    return skus, datos["products"]["nodes"]


def location_principal():
    """Devuelve el ID de la primera ubicación de inventario."""
    datos = graphql_query(LOCATIONS_QUERY)
    ubicaciones = datos["locations"]["nodes"]
    if not ubicaciones:
        raise RuntimeError("No hay ubicaciones de inventario configuradas")
    return ubicaciones[0]["id"]


def crear_producto(producto, location_id):
    """Crea un producto con precio, SKU, stock y etiquetas."""
    entrada = {
        "title": producto["nombre"],
        "descriptionHtml": f"<p>{producto['descripcion']}</p>",
        "productType": producto["categoria"],
        "vendor": "TechStore",
        "status": "ACTIVE",
        "tags": [producto["categoria"], "carrito-evento"],
        "variants": [{
            "sku": producto["sku"],
            "price": str(producto["precio"]),
            "inventoryManagement": "SHOPIFY",
            "inventoryPolicy": "CONTINUE",
            "inventoryQuantities": [{
                "availableQuantity": producto["stock"],
                "locationId": location_id,
            }],
        }],
    }
    respuesta = graphql_query(PRODUCT_CREATE, {"input": entrada})["productCreate"]
    if respuesta["userErrors"]:
        raise RuntimeError(f"Error creando {producto['sku']}: {respuesta['userErrors']}")
    return respuesta["product"]


def crear_colecciones(catalogo, productos_por_sku):
    """Crea una colección por cada categoría y agrega sus productos."""
    categorias = {}
    for producto in catalogo["productos"]:
        categoria = producto["categoria"]
        categorias.setdefault(categoria, []).append(productos_por_sku[producto["sku"]])

    for categoria, ids in categorias.items():
        respuesta = graphql_query(
            COLLECTION_CREATE,
            {"input": {
                "title": categoria,
                "handle": categoria.lower(),
                "descriptionHtml": f"<p>Productos de la categoría {categoria}.</p>",
            }},
        )["collectionCreate"]
        if respuesta["userErrors"]:
            print(f"  Colección {categoria}: {respuesta['userErrors']}")
            continue
        coleccion_id = respuesta["collection"]["id"]
        resultado = graphql_query(
            COLLECTION_ADD, {"id": coleccion_id, "ids": ids}
        )["collectionAddProducts"]
        if resultado["userErrors"]:
            print(f"  Error agregando productos a {categoria}: {resultado['userErrors']}")
        else:
            print(f"  Colección '{categoria}' creada con {len(ids)} productos")


def main():
    """Punto de entrada con modo dry-run."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="no escribe en Shopify")
    args = parser.parse_args()

    catalogo = cargar_catalogo()
    existentes, nodos = skus_existentes()
    print(f"SKUs existentes en la tienda: {len(existentes)}")

    pendientes = [
        p for p in catalogo["productos"] if p["sku"] not in existentes
    ]
    print(f"Productos a crear: {len(pendientes)}")

    if args.dry_run:
        for producto in pendientes:
            print(f"  [DRY RUN] {producto['sku']} - {producto['nombre']}")
        return 0

    location_id = location_principal()
    ids_por_sku = {}
    for nodo in nodos:
        for variante in nodo["variants"]["nodes"]:
            if variante["sku"]:
                ids_por_sku[variante["sku"]] = nodo["id"]

    for producto in pendientes:
        creado = crear_producto(producto, location_id)
        ids_por_sku[producto["sku"]] = creado["id"]
        print(f"  Creado {producto['sku']} -> {creado['handle']}")

    crear_colecciones(catalogo, ids_por_sku)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
