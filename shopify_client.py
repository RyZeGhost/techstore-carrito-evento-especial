"""Cliente para la Admin GraphQL API de Shopify usando client credentials.

Variables esperadas en .env:
    SHOPIFY_SHOP=techstore-d8vn3rhk.myshopify.com
    SHOPIFY_CLIENT_ID=...
    SHOPIFY_CLIENT_SECRET=shpss_...

Incluye backoff exponencial ante límites de tasa (HTTP 429 y errores
THROTTLED de GraphQL), según las buenas prácticas del enunciado.
"""

import logging
import os
import re
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# Registro de respuestas fallidas, exigido por el enunciado del agente.
# Se guarda fuera del repo (carpeta ignorada por .gitignore) para no subir datos.
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOGGER = logging.getLogger("shopify")
LOGGER.setLevel(logging.ERROR)
if not LOGGER.handlers:
    _handler = logging.FileHandler(LOG_DIR / "shopify_errores.log", encoding="utf-8")
    _handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    LOGGER.addHandler(_handler)

SHOP = os.getenv("SHOPIFY_SHOP", "").strip()
CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID", "").strip()
CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET", "").strip()
API_VERSION = "2026-01"
INTENTOS = 5

_TOKEN = None


def normalizar_shop(shop: str) -> str:
    """Acepta 'techstore', 'techstore.myshopify.com' o la URL completa con /admin."""
    shop = shop.strip().replace("https://", "").replace("http://", "").rstrip("/")
    if shop.endswith("/admin"):
        shop = shop[: -len("/admin")]
    if "." not in shop:
        shop += ".myshopify.com"
    return shop


def resumen_error(respuesta: requests.Response) -> str:
    """Extrae el mensaje útil de una respuesta de error (JSON o HTML)."""
    try:
        return str(respuesta.json())[:300]
    except ValueError:
        titulo = re.search(r"<title>(.*?)</title>", respuesta.text, re.DOTALL)
        if titulo:
            return titulo.group(1).strip()
        return respuesta.text[:300]


def validar_configuracion() -> None:
    """Verifica que existan las tres credenciales antes de llamar a la API."""
    faltantes = [
        nombre
        for nombre, valor in (
            ("SHOPIFY_SHOP", SHOP),
            ("SHOPIFY_CLIENT_ID", CLIENT_ID),
            ("SHOPIFY_CLIENT_SECRET", CLIENT_SECRET),
        )
        if not valor
    ]
    if faltantes:
        raise RuntimeError("Faltan variables en .env: " + ", ".join(faltantes))


def peticion_con_reintento(constructor, descripcion: str) -> requests.Response:
    """Ejecuta una petición con espera exponencial si Shopify limita la tasa."""
    for intento in range(1, INTENTOS + 1):
        try:
            respuesta = constructor()
        except requests.RequestException as error:
            LOGGER.error("Error de red en %s (intento %s): %s", descripcion, intento, error)
            if intento == INTENTOS:
                raise RuntimeError(f"{descripcion}: {error}") from error
            espera = 2 ** (intento - 1)
            print(f"  {descripcion}: error de red; reintentando en {espera}s...")
            time.sleep(espera)
            continue

        if respuesta.status_code == 429:
            LOGGER.error("HTTP 429 en %s (intento %s)", descripcion, intento)
        if respuesta.status_code == 429 and intento < INTENTOS:
            espera = 2 ** (intento - 1)
            print(f"  Límite de tasa alcanzado ({descripcion}); reintentando en {espera}s...")
            time.sleep(espera)
            continue
        return respuesta
    raise RuntimeError(f"No se pudo completar: {descripcion}")


def rest_request(metodo: str, ruta: str, datos: dict | None = None) -> dict:
    """Llama a la REST Admin API (necesaria para assets de tema)."""
    url = f"https://{normalizar_shop(SHOP)}/admin/api/{API_VERSION}/{ruta.lstrip('/')}"
    respuesta = peticion_con_reintento(
        lambda: requests.request(
            metodo,
            url,
            json=datos,
            headers={
                "X-Shopify-Access-Token": get_shopify_token(),
                "Content-Type": "application/json",
            },
            timeout=30,
        ),
        f"REST {metodo} {ruta}",
    )
    if respuesta.status_code >= 400:
        mensaje = (
            f"Error {respuesta.status_code} en REST {ruta}: {resumen_error(respuesta)}"
        )
        LOGGER.error(mensaje)
        raise RuntimeError(mensaje)
    return respuesta.json() if respuesta.content else {}


def get_shopify_token() -> str:
    """Obtiene (y reutiliza) un access token mediante client_credentials."""
    global _TOKEN
    if _TOKEN:
        return _TOKEN

    validar_configuracion()
    url = f"https://{normalizar_shop(SHOP)}/admin/oauth/access_token"
    respuesta = peticion_con_reintento(
        lambda: requests.post(
            url,
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
            timeout=30,
        ),
        "solicitud de token",
    )
    if respuesta.status_code != 200:
        mensaje = (
            f"Error {respuesta.status_code} al pedir el token: "
            f"{resumen_error(respuesta)}"
        )
        LOGGER.error(mensaje)
        raise RuntimeError(mensaje)
    datos = respuesta.json()
    if "access_token" not in datos:
        mensaje = f"Shopify no devolvió access_token: {datos}"
        LOGGER.error(mensaje)
        raise RuntimeError(mensaje)

    _TOKEN = datos["access_token"]
    return _TOKEN


def graphql_query(query: str, variables: dict | None = None) -> dict:
    """Ejecuta una consulta GraphQL y devuelve el bloque 'data'."""
    url = f"https://{normalizar_shop(SHOP)}/admin/api/{API_VERSION}/graphql.json"

    for intento in range(1, INTENTOS + 1):
        respuesta = peticion_con_reintento(
            lambda: requests.post(
                url,
                json={"query": query, "variables": variables or {}},
                headers={
                    "X-Shopify-Access-Token": get_shopify_token(),
                    "Content-Type": "application/json",
                },
                timeout=30,
            ),
            "consulta GraphQL",
        )
        if respuesta.status_code != 200:
            mensaje = (
                f"Error {respuesta.status_code} en GraphQL: {resumen_error(respuesta)}"
            )
            LOGGER.error(mensaje)
            raise RuntimeError(mensaje)
        resultado = respuesta.json()
        errores = resultado.get("errors") or []

        es_throttled = any(
            error.get("extensions", {}).get("code") == "THROTTLED"
            for error in errores
        )
        if es_throttled and intento < INTENTOS:
            espera = 2 ** (intento - 1)
            print(f"  GraphQL limitó la tasa; reintentando en {espera}s...")
            time.sleep(espera)
            continue
        if errores:
            LOGGER.error("Errores de GraphQL: %s", errores)
            raise RuntimeError(f"Errores de GraphQL: {errores}")
        return resultado.get("data", {})

    raise RuntimeError("La consulta GraphQL agotó los reintentos por límite de tasa")


if __name__ == "__main__":
    try:
        datos = graphql_query("{ shop { name myshopifyDomain } }")
        tienda = datos["shop"]
        print(f"Conectado a: {tienda['name']} ({tienda['myshopifyDomain']})")
    except (RuntimeError, requests.RequestException, KeyError) as error:
        print(f"Error de conexión: {error}")
