"""Puebla el catálogo de Shopify usando la Admin GraphQL API.

Uso desde la raíz del proyecto:
    python -m scripts.poblar_catalogo --dry-run   # solo muestra qué haría
    python -m scripts.poblar_catalogo             # crea productos y colecciones

El script es idempotente: si el SKU ya existe, lo omite.
"""

import argparse
import sys
import unicodedata
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
      variants(first: 250) { nodes { id sku price } }
      media(first: 20) { nodes { id } }
    }
  }
}
"""

LOCATIONS_QUERY = """
{
  locations(first: 10) { nodes { id } }
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

VARIANT_CREATE = """
mutation VarianteCrear($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkCreate(
    productId: $productId,
    variants: $variants,
    strategy: DEFAULT
  ) {
    productVariants { id sku }
    userErrors { field message }
  }
}
"""

VARIANT_UPDATE = """
mutation VarianteActualizar($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    productVariants { id sku price }
    userErrors { field message }
  }
}
"""

MEDIA_CREATE = """
mutation ImagenAgregar($productId: ID!, $media: [CreateMediaInput!]!) {
  productCreateMedia(productId: $productId, media: $media) {
    media { id mediaContentType }
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

COLECCIONES_QUERY = """
{
  collections(first: 250) {
    nodes {
      id
      handle
      products(first: 250) { nodes { id } }
    }
  }
}
"""

COLLECTION_ADD = """
mutation AgregarProductos($id: ID!, $productIds: [ID!]!) {
  collectionAddProducts(id: $id, productIds: $productIds) {
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
        "media": [{
            "alt": producto["nombre"],
            "mediaContentType": "IMAGE",
            "originalSource": producto["imagen"],
        }],
    }
    respuesta = graphql_query(PRODUCT_CREATE, {"input": entrada})["productCreate"]
    if respuesta["userErrors"]:
        raise RuntimeError(f"Error creando {producto['sku']}: {respuesta['userErrors']}")

    producto_id = respuesta["product"]["id"]
    variante = {
        "price": str(producto["precio"]),
        "inventoryItem": {
            "sku": producto["sku"],
            "tracked": True,
            "requiresShipping": True,
        },
        "inventoryPolicy": "CONTINUE",
        "inventoryQuantities": [{
            "availableQuantity": producto["stock"],
            "locationId": location_id,
        }],
        "optionValues": [{
            "optionName": "Title",
            "name": producto["nombre"],
        }],
    }
    respuesta_variante = graphql_query(
        VARIANT_CREATE, {"productId": producto_id, "variants": [variante]}
    )["productVariantsBulkCreate"]
    if respuesta_variante["userErrors"]:
        raise RuntimeError(
            f"Error creando variante de {producto['sku']}: "
            f"{respuesta_variante['userErrors']}"
        )
    return respuesta["product"]


def sincronizar_producto(producto, nodo):
    """Ajusta precio e imagen de un producto que ya existe en Shopify."""
    cambios = []
    variante = next(
        (v for v in nodo["variants"]["nodes"] if v["sku"] == producto["sku"]), None
    )
    if variante and variante["price"] != str(producto["precio"]):
        respuesta = graphql_query(VARIANT_UPDATE, {
            "productId": nodo["id"],
            "variants": [{"id": variante["id"], "price": str(producto["precio"])}],
        })["productVariantsBulkUpdate"]
        if respuesta["userErrors"]:
            raise RuntimeError(f"Error actualizando precio: {respuesta['userErrors']}")
        cambios.append("precio")

    if not nodo["media"]["nodes"]:
        respuesta = graphql_query(MEDIA_CREATE, {
            "productId": nodo["id"],
            "media": [{
                "alt": producto["nombre"],
                "mediaContentType": "IMAGE",
                "originalSource": producto["imagen"],
            }],
        })["productCreateMedia"]
        if respuesta["userErrors"]:
            raise RuntimeError(f"Error agregando imagen: {respuesta['userErrors']}")
        cambios.append("imagen")

    return cambios


def handle_de(texto):
    """Convierte un texto a handle Shopify (minúsculas, sin tildes)."""
    sin_tildes = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in sin_tildes if not unicodedata.combining(c)).lower()


def crear_colecciones(catalogo, productos_por_sku):
    """Crea una colección por cada categoría y agrega sus productos."""
    categorias = {}
    for producto in catalogo["productos"]:
        categoria = producto["categoria"]
        categorias.setdefault(categoria, []).append(productos_por_sku[producto["sku"]])

    existentes = graphql_query(COLECCIONES_QUERY)["collections"]["nodes"]
    por_handle = {nodo["handle"]: nodo for nodo in existentes}

    for categoria, ids in categorias.items():
        handle = handle_de(categoria)
        nodo = por_handle.get(handle)
        if nodo:
            coleccion_id = nodo["id"]
            ya_agregados = {p["id"] for p in nodo["products"]["nodes"]}
            por_agregar = [i for i in ids if i not in ya_agregados]
            if not por_agregar:
                print(f"  Colección '{categoria}' ya estaba completa")
                continue
        else:
            respuesta = graphql_query(
                COLLECTION_CREATE,
                {"input": {
                    "title": categoria,
                    "handle": handle,
                    "descriptionHtml": f"<p>Productos de la categoría {categoria}.</p>",
                }},
            )["collectionCreate"]
            if respuesta["userErrors"]:
                print(f"  Colección {categoria}: {respuesta['userErrors']}")
                continue
            coleccion_id = respuesta["collection"]["id"]
            por_agregar = ids

        resultado = graphql_query(
            COLLECTION_ADD, {"id": coleccion_id, "productIds": por_agregar}
        )["collectionAddProducts"]
        if resultado["userErrors"]:
            print(f"  Error agregando productos a {categoria}: {resultado['userErrors']}")
        else:
            print(f"  Colección '{categoria}' con {len(por_agregar)} productos agregados")


def main():
    """Punto de entrada con modo dry-run."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="no escribe en Shopify")
    args = parser.parse_args()

    catalogo = cargar_catalogo()
    existentes, nodos = skus_existentes()
    print(f"SKUs existentes en la tienda: {len(existentes)}")

    nodos_por_sku = {}
    for nodo in nodos:
        for variante in nodo["variants"]["nodes"]:
            if variante["sku"]:
                nodos_por_sku[variante["sku"]] = nodo

    pendientes = [
        p for p in catalogo["productos"] if p["sku"] not in existentes
    ]
    print(f"Productos a crear: {len(pendientes)}")

    if args.dry_run:
        for producto in pendientes:
            print(f"  [DRY RUN] Crear {producto['sku']} - {producto['nombre']}")
        for producto in catalogo["productos"]:
            nodo = nodos_por_sku.get(producto["sku"])
            if nodo:
                sin_precio = any(
                    v["sku"] == producto["sku"] and v["price"] != str(producto["precio"])
                    for v in nodo["variants"]["nodes"]
                )
                if sin_precio or not nodo["media"]["nodes"]:
                    print(f"  [DRY RUN] Sincronizar {producto['sku']}")
        return 0

    location_id = location_principal() if pendientes else None
    ids_por_sku = {sku: nodo["id"] for sku, nodo in nodos_por_sku.items()}

    for producto in pendientes:
        creado = crear_producto(producto, location_id)
        ids_por_sku[producto["sku"]] = creado["id"]
        print(f"  Creado {producto['sku']} -> {creado['handle']}")

    for producto in catalogo["productos"]:
        nodo = nodos_por_sku.get(producto["sku"])
        if nodo:
            cambios = sincronizar_producto(producto, nodo)
            if cambios:
                print(f"  Actualizado {producto['sku']}: {', '.join(cambios)}")

    crear_colecciones(catalogo, ids_por_sku)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
