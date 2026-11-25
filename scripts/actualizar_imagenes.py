"""Reemplaza las imágenes del catálogo por fotos limpias de producto.

Las imágenes generadas se guardan en `datos/imagenes/<SKU>.<ext>`, se suben
como assets del tema y se asocian a cada producto con `productCreateMedia`.
La URL pública devuelta por Shopify se guarda en `datos/catalogo.json`.

Uso desde la raíz del proyecto:
    python -m scripts.actualizar_imagenes --sku AURICULARES --dry-run
    python -m scripts.actualizar_imagenes --sku AURICULARES
    python -m scripts.actualizar_imagenes
"""

import argparse
import base64
import json
import mimetypes
import sys
from pathlib import Path

# Permite importar el módulo de la raíz aunque se ejecute como paquete.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shopify_client import graphql_query, rest_request  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
CATALOGO = RAIZ / "datos" / "catalogo.json"
IMAGENES = RAIZ / "datos" / "imagenes"

PRODUCTOS_MEDIA = """
{
  products(first: 250, query: "tag:carrito-evento") {
    nodes {
      id
      title
      variants(first: 1) { nodes { sku } }
      media(first: 20) { nodes { id } }
    }
  }
}
"""

MEDIA_BORRAR = """
mutation BorrarMedia($productId: ID!, $mediaIds: [ID!]!) {
  productDeleteMedia(productId: $productId, mediaIds: $mediaIds) {
    deletedMediaIds
    userErrors { field message }
  }
}
"""

MEDIA_CREAR = """
mutation ImagenAgregar($productId: ID!, $media: [CreateMediaInput!]!) {
  productCreateMedia(productId: $productId, media: $media) {
    media { id mediaContentType }
    userErrors { field message }
  }
}
"""


def tema_activo():
    """Devuelve el tema publicado."""
    temas = rest_request("GET", "themes.json")["themes"]
    activo = next((t for t in temas if t.get("role") == "main"), None)
    if not activo:
        raise RuntimeError("No hay un tema publicado (role=main)")
    return activo


def ruta_imagen(sku):
    """Busca el archivo generado para un SKU (png, jpg, webp...)."""
    encontradas = [p for p in IMAGENES.glob(f"{sku}.*") if p.is_file()]
    return max(encontradas, key=lambda p: p.stat().st_mtime) if encontradas else None


def subir_asset(tema_id, ruta):
    """Sube una imagen al tema y devuelve su URL pública en el CDN."""
    # Los assets del tema no aceptan subcarpetas: se usa un prefijo plano.
    clave = f"assets/productos_{ruta.stem}{ruta.suffix}"
    tipo = mimetypes.guess_type(ruta.name)[0] or "image/png"
    codificado = base64.b64encode(ruta.read_bytes()).decode("ascii")
    respuesta = rest_request(
        "PUT",
        f"themes/{tema_id}/assets.json",
        {"asset": {"key": clave, "content_type": tipo, "attachment": codificado}},
    )["asset"]
    url = respuesta.get("public_url")
    if not url:
        raise RuntimeError(f"Shopify no devolvió public_url para {clave}")
    return url


def reemplazar_media(producto_id, media_actual, url):
    """Borra la imagen anterior y asocia la nueva al producto."""
    ids = [medio["id"] for medio in media_actual]
    if ids:
        borrado = graphql_query(
            MEDIA_BORRAR, {"productId": producto_id, "mediaIds": ids}
        )["productDeleteMedia"]
        if borrado["userErrors"]:
            raise RuntimeError(f"Error borrando imágenes: {borrado['userErrors']}")

    creado = graphql_query(MEDIA_CREAR, {
        "productId": producto_id,
        "media": [{
            "alt": "Producto TechStore sobre fondo blanco",
            "mediaContentType": "IMAGE",
            "originalSource": url,
        }],
    })["productCreateMedia"]
    if creado["userErrors"]:
        raise RuntimeError(f"Error agregando imagen: {creado['userErrors']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sku", help="actualiza solo un SKU")
    parser.add_argument("--dry-run", action="store_true", help="no escribe en Shopify")
    args = parser.parse_args()

    datos = json.loads(CATALOGO.read_text(encoding="utf-8"))
    productos = {p["sku"]: p for p in datos["productos"]}
    seleccion = [args.sku] if args.sku else list(productos)
    desconocidos = [sku for sku in seleccion if sku not in productos]
    if desconocidos:
        raise SystemExit(f"SKU no encontrados en el catálogo: {desconocidos}")

    nodos = graphql_query(PRODUCTOS_MEDIA)["products"]["nodes"]
    por_sku = {
        variante["sku"]: nodo
        for nodo in nodos
        for variante in nodo["variants"]["nodes"]
        if variante["sku"]
    }
    tema = tema_activo() if not args.dry_run else {"id": "dry-run"}
    actualizados = []

    for sku in seleccion:
        ruta = ruta_imagen(sku)
        if not ruta:
            print(f"  Sin imagen generada para {sku}; se omite")
            continue
        nodo = por_sku.get(sku)
        if not nodo:
            print(f"  Producto {sku} no encontrado en Shopify; se omite")
            continue
        if args.dry_run:
            print(f"  [DRY RUN] {sku}: {ruta.name} -> {nodo['title']}")
            continue

        url = subir_asset(tema["id"], ruta)
        reemplazar_media(nodo["id"], nodo["media"]["nodes"], url)
        productos[sku]["imagen"] = url
        actualizados.append(sku)
        print(f"  Actualizado {sku} -> {url}")

    if actualizados:
        CATALOGO.write_text(
            json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Catálogo actualizado con {len(actualizados)} imágenes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
