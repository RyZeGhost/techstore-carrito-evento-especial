"""Cliente simple para la Admin API de Shopify usando client credentials.

Variables esperadas en .env:
    SHOPIFY_SHOP=techstore-d8vn3rhk.myshopify.com
    SHOPIFY_CLIENT_ID=...
    SHOPIFY_CLIENT_SECRET=shpss_...

Nota: el endpoint real de Shopify es https://<shop>.myshopify.com/admin/...
por eso SHOPIFY_SHOP=techstore se normaliza a techstore.myshopify.com.
"""

import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()

SHOP = os.getenv("SHOPIFY_SHOP", "").strip()
CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID", "").strip()
CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET", "").strip()
API_VERSION = "2026-01"

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
        raise RuntimeError(
            "Faltan variables en .env: " + ", ".join(faltantes)
        )


def get_shopify_token() -> str:
    """Obtiene (y reutiliza) un access token mediante client_credentials."""
    global _TOKEN
    if _TOKEN:
        return _TOKEN

    validar_configuracion()
    url = f"https://{normalizar_shop(SHOP)}/admin/oauth/access_token"
    respuesta = requests.post(
        url,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        timeout=30,
    )
    if respuesta.status_code != 200:
        raise RuntimeError(
            f"Error {respuesta.status_code} al pedir el token: "
            f"{resumen_error(respuesta)}"
        )
    datos = respuesta.json()
    if "access_token" not in datos:
        raise RuntimeError(f"Shopify no devolvió access_token: {datos}")

    _TOKEN = datos["access_token"]
    return _TOKEN


def graphql_query(query: str, variables: dict | None = None) -> dict:
    """Ejecuta una consulta en la Admin GraphQL API y devuelve el bloque 'data'."""
    url = (
        f"https://{normalizar_shop(SHOP)}/admin/api/{API_VERSION}/graphql.json"
    )
    respuesta = requests.post(
        url,
        json={"query": query, "variables": variables or {}},
        headers={
            "X-Shopify-Access-Token": get_shopify_token(),
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    if respuesta.status_code != 200:
        raise RuntimeError(
            f"Error {respuesta.status_code} en GraphQL: {resumen_error(respuesta)}"
        )
    resultado = respuesta.json()
    if resultado.get("errors"):
        raise RuntimeError(f"Errores de GraphQL: {resultado['errors']}")
    return resultado.get("data", {})


if __name__ == "__main__":
    try:
        datos = graphql_query("{ shop { name myshopifyDomain } }")
        tienda = datos["shop"]
        print(f"Conectado a: {tienda['name']} ({tienda['myshopifyDomain']})")
    except (RuntimeError, requests.RequestException, KeyError) as error:
        print(f"Error de conexión: {error}")
