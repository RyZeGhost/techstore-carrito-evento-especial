"""Conexión con la Shopify Admin API y utilidades básicas.

Uso:
    python main.py                  # comprueba la conexión (no modifica nada)
    python main.py --crear-ejemplo  # crea un producto de prueba
    python main.py --crear-ejemplo --dry-run  # solo muestra qué se crearía
"""

import argparse
import os
import time

import shopify
from dotenv import load_dotenv
from pyactiveresource.connection import UnauthorizedAccess

load_dotenv()


def normalizar_url(url: str) -> str:
    """Deja la URL en formato 'tienda.myshopify.com'."""
    url = url.strip().replace("https://", "").replace("http://", "").rstrip("/")
    if url.endswith("/admin"):
        url = url[: -len("/admin")]
    return url


SHOP_URL = normalizar_url(os.getenv("SHOPIFY_STORE_URL", ""))
API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2026-10").strip() or "2026-10"
ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "").strip()


def validar_configuracion() -> None:
    """Verifica que existan las credenciales antes de llamar a la API."""
    faltantes = []
    if not SHOP_URL:
        faltantes.append("SHOPIFY_STORE_URL")
    if not ACCESS_TOKEN or ACCESS_TOKEN.startswith("shpat_xxx"):
        faltantes.append("SHOPIFY_ACCESS_TOKEN")

    if faltantes:
        raise RuntimeError(
            "Faltan credenciales en el archivo .env: " + ", ".join(faltantes)
            + ". Copia .env.example como .env y rellénalo."
        )

    if ACCESS_TOKEN.startswith("shpss_"):
        raise RuntimeError(
            "SHOPIFY_ACCESS_TOKEN contiene el secreto de la app (shpss_...). "
            "Necesitas el Admin API access token, que empieza por shpat_."
        )


def con_reintento(funcion, intentos: int = 5):
    """Reintenta con backoff exponencial si Shopify limita la tasa de peticiones."""
    for intento in range(1, intentos + 1):
        try:
            return funcion()
        except Exception as error:
            mensaje = str(error).lower()
            es_throttling = "429" in mensaje or "throttl" in mensaje
            if not es_throttling or intento == intentos:
                raise
            espera = 2 ** (intento - 1)
            print(f"  Límite de tasa alcanzado; reintentando en {espera}s...")
            time.sleep(espera)
    return None


def iniciar_sesion() -> None:
    validar_configuracion()
    session = shopify.Session(SHOP_URL, API_VERSION, ACCESS_TOKEN)
    shopify.ShopifyResource.activate_session(session)


def verificar_conexion() -> shopify.Shop:
    """Devuelve la tienda conectada o lanza un error con el motivo."""
    iniciar_sesion()
    try:
        tienda = con_reintento(shopify.Shop.current)
    except UnauthorizedAccess as error:
        raise RuntimeError(
            f"Credenciales rechazadas por '{SHOP_URL}' (401). Comprueba que el token "
            "sea el Admin API access token (shpat_...) y que la app esté instalada "
            "en la tienda con los scopes necesarios."
        ) from error
    except Exception as error:
        raise RuntimeError(f"No se pudo conectar a '{SHOP_URL}': {error}") from error

    print(f"Conectado exitosamente a: {tienda.name} ({tienda.myshopify_domain})")
    print(f"  API version: {API_VERSION}")
    print(f"  Plan: {getattr(tienda, 'plan_display_name', 'N/A')}")
    return tienda


def crear_producto(titulo, descripcion, precio, sku, tipo_producto="General", dry_run=False):
    """Crea un producto, o solo muestra el payload si dry_run=True."""
    if not titulo or not precio or not sku:
        raise ValueError("titulo, precio y sku son obligatorios")

    variante = shopify.Variant({
        "price": str(precio),
        "sku": sku,
        "inventory_management": "shopify",
    })
    producto = shopify.Product()
    producto.title = titulo
    producto.body_html = descripcion
    producto.product_type = tipo_producto
    producto.variants = [variante]

    if dry_run:
        print(f"[DRY RUN] Se crearía el producto '{titulo}' (SKU {sku}, ${precio})")
        return None

    guardado = con_reintento(producto.save)
    if guardado:
        print(f"Producto '{titulo}' creado con ID: {producto.id}")
        return producto

    print(f"Error al crear '{titulo}': {producto.errors.full_messages()}")
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crear-ejemplo", action="store_true", help="crea un producto de prueba")
    parser.add_argument("--dry-run", action="store_true", help="no escribe en la tienda")
    args = parser.parse_args()

    try:
        verificar_conexion()
    except RuntimeError as error:
        print(f"Error: {error}")
        raise SystemExit(1) from None

    if args.crear_ejemplo:
        crear_producto(
            titulo="Camiseta de Prueba Python",
            descripcion="<p>Producto creado automáticamente desde Python.</p>",
            precio="19.99",
            sku="TSHIRT-PY-001",
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    main()
