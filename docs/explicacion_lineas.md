# Explicación línea por línea del código

Documento generado automáticamente desde los comentarios del código fuente.
La columna **Explicación** corresponde al comentario de la línea o al
comentario del bloque que le precede inmediatamente.

## `shopify_client.py`

| Línea | Código | Explicación |
|---:|---|---|
| 1 | `"""Cliente para la Admin GraphQL API de Shopify usando client credentials.` | Docstring: describe el propósito del bloque. |
| 2 | `` | Línea en blanco: separa bloques lógicos. |
| 3 | `Variables esperadas en .env:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 4 | `SHOPIFY_SHOP=techstore-d8vn3rhk.myshopify.com` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 5 | `SHOPIFY_CLIENT_ID=...` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 6 | `SHOPIFY_CLIENT_SECRET=shpss_...` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 7 | `` | Línea en blanco: separa bloques lógicos. |
| 8 | `Incluye backoff exponencial ante límites de tasa (HTTP 429 y errores` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 9 | `THROTTLED de GraphQL), según las buenas prácticas del enunciado.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 10 | `"""` | Docstring: describe el propósito del bloque. |
| 11 | `` | Línea en blanco: separa bloques lógicos. |
| 12 | `import os` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 13 | `import re` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 14 | `import time` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 15 | `` | Línea en blanco: separa bloques lógicos. |
| 16 | `import requests` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 17 | `from dotenv import load_dotenv` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 18 | `` | Línea en blanco: separa bloques lógicos. |
| 19 | `load_dotenv()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 20 | `` | Línea en blanco: separa bloques lógicos. |
| 21 | `SHOP = os.getenv("SHOPIFY_SHOP", "").strip()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 22 | `CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID", "").strip()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 23 | `CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET", "").strip()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 24 | `API_VERSION = "2026-01"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 25 | `INTENTOS = 5` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 26 | `` | Línea en blanco: separa bloques lógicos. |
| 27 | `_TOKEN = None` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 28 | `` | Línea en blanco: separa bloques lógicos. |
| 29 | `` | Línea en blanco: separa bloques lógicos. |
| 30 | `def normalizar_shop(shop: str) -> str:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 31 | `"""Acepta 'techstore', 'techstore.myshopify.com' o la URL completa con /admin."""` | Docstring: describe el propósito del bloque. |
| 32 | `shop = shop.strip().replace("https://", "").replace("http://", "").rstrip("/")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 33 | `if shop.endswith("/admin"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 34 | `shop = shop[: -len("/admin")]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 35 | `if "." not in shop:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 36 | `shop += ".myshopify.com"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 37 | `return shop` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 38 | `` | Línea en blanco: separa bloques lógicos. |
| 39 | `` | Línea en blanco: separa bloques lógicos. |
| 40 | `def resumen_error(respuesta: requests.Response) -> str:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 41 | `"""Extrae el mensaje útil de una respuesta de error (JSON o HTML)."""` | Docstring: describe el propósito del bloque. |
| 42 | `try:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 43 | `return str(respuesta.json())[:300]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 44 | `except ValueError:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 45 | `titulo = re.search(r"<title>(.*?)</title>", respuesta.text, re.DOTALL)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 46 | `if titulo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 47 | `return titulo.group(1).strip()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 48 | `return respuesta.text[:300]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 49 | `` | Línea en blanco: separa bloques lógicos. |
| 50 | `` | Línea en blanco: separa bloques lógicos. |
| 51 | `def validar_configuracion() -> None:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 52 | `"""Verifica que existan las tres credenciales antes de llamar a la API."""` | Docstring: describe el propósito del bloque. |
| 53 | `faltantes = [` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 54 | `nombre` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 55 | `for nombre, valor in (` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 56 | `("SHOPIFY_SHOP", SHOP),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 57 | `("SHOPIFY_CLIENT_ID", CLIENT_ID),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 58 | `("SHOPIFY_CLIENT_SECRET", CLIENT_SECRET),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 59 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 60 | `if not valor` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 61 | `]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 62 | `if faltantes:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 63 | `raise RuntimeError("Faltan variables en .env: " + ", ".join(faltantes))` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 64 | `` | Línea en blanco: separa bloques lógicos. |
| 65 | `` | Línea en blanco: separa bloques lógicos. |
| 66 | `def peticion_con_reintento(constructor, descripcion: str) -> requests.Response:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 67 | `"""Ejecuta una petición con espera exponencial si Shopify limita la tasa."""` | Docstring: describe el propósito del bloque. |
| 68 | `for intento in range(1, INTENTOS + 1):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 69 | `try:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 70 | `respuesta = constructor()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 71 | `except requests.RequestException as error:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 72 | `if intento == INTENTOS:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 73 | `raise RuntimeError(f"{descripcion}: {error}") from error` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 74 | `espera = 2 ** (intento - 1)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 75 | `print(f"  {descripcion}: error de red; reintentando en {espera}s...")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 76 | `time.sleep(espera)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 77 | `continue` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 78 | `` | Línea en blanco: separa bloques lógicos. |
| 79 | `if respuesta.status_code == 429 and intento < INTENTOS:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 80 | `espera = 2 ** (intento - 1)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 81 | `print(f"  Límite de tasa alcanzado ({descripcion}); reintentando en {espera}s...")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 82 | `time.sleep(espera)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 83 | `continue` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 84 | `return respuesta` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 85 | `raise RuntimeError(f"No se pudo completar: {descripcion}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 86 | `` | Línea en blanco: separa bloques lógicos. |
| 87 | `` | Línea en blanco: separa bloques lógicos. |
| 88 | `def get_shopify_token() -> str:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 89 | `"""Obtiene (y reutiliza) un access token mediante client_credentials."""` | Docstring: describe el propósito del bloque. |
| 90 | `global _TOKEN` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 91 | `if _TOKEN:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 92 | `return _TOKEN` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 93 | `` | Línea en blanco: separa bloques lógicos. |
| 94 | `validar_configuracion()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 95 | `url = f"https://{normalizar_shop(SHOP)}/admin/oauth/access_token"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 96 | `respuesta = peticion_con_reintento(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 97 | `lambda: requests.post(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 98 | `url,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 99 | `data={` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 100 | `"grant_type": "client_credentials",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 101 | `"client_id": CLIENT_ID,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 102 | `"client_secret": CLIENT_SECRET,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 103 | `},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 104 | `timeout=30,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 105 | `),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 106 | `"solicitud de token",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 107 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 108 | `if respuesta.status_code != 200:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 109 | `raise RuntimeError(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 110 | `f"Error {respuesta.status_code} al pedir el token: "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 111 | `f"{resumen_error(respuesta)}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 112 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 113 | `datos = respuesta.json()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 114 | `if "access_token" not in datos:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 115 | `raise RuntimeError(f"Shopify no devolvió access_token: {datos}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 116 | `` | Línea en blanco: separa bloques lógicos. |
| 117 | `_TOKEN = datos["access_token"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 118 | `return _TOKEN` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 119 | `` | Línea en blanco: separa bloques lógicos. |
| 120 | `` | Línea en blanco: separa bloques lógicos. |
| 121 | `def graphql_query(query: str, variables: dict \| None = None) -> dict:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 122 | `"""Ejecuta una consulta GraphQL y devuelve el bloque 'data'."""` | Docstring: describe el propósito del bloque. |
| 123 | `url = f"https://{normalizar_shop(SHOP)}/admin/api/{API_VERSION}/graphql.json"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 124 | `` | Línea en blanco: separa bloques lógicos. |
| 125 | `for intento in range(1, INTENTOS + 1):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 126 | `respuesta = peticion_con_reintento(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 127 | `lambda: requests.post(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 128 | `url,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 129 | `json={"query": query, "variables": variables or {}},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 130 | `headers={` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 131 | `"X-Shopify-Access-Token": get_shopify_token(),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 132 | `"Content-Type": "application/json",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 133 | `},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 134 | `timeout=30,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 135 | `),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 136 | `"consulta GraphQL",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 137 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 138 | `if respuesta.status_code != 200:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 139 | `raise RuntimeError(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 140 | `f"Error {respuesta.status_code} en GraphQL: {resumen_error(respuesta)}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 141 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 142 | `resultado = respuesta.json()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 143 | `errores = resultado.get("errors") or []` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 144 | `` | Línea en blanco: separa bloques lógicos. |
| 145 | `es_throttled = any(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 146 | `error.get("extensions", {}).get("code") == "THROTTLED"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 147 | `for error in errores` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 148 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 149 | `if es_throttled and intento < INTENTOS:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 150 | `espera = 2 ** (intento - 1)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 151 | `print(f"  GraphQL limitó la tasa; reintentando en {espera}s...")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 152 | `time.sleep(espera)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 153 | `continue` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 154 | `if errores:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 155 | `raise RuntimeError(f"Errores de GraphQL: {errores}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 156 | `return resultado.get("data", {})` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 157 | `` | Línea en blanco: separa bloques lógicos. |
| 158 | `raise RuntimeError("La consulta GraphQL agotó los reintentos por límite de tasa")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 159 | `` | Línea en blanco: separa bloques lógicos. |
| 160 | `` | Línea en blanco: separa bloques lógicos. |
| 161 | `if __name__ == "__main__":` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 162 | `try:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 163 | `datos = graphql_query("{ shop { name myshopifyDomain } }")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 164 | `tienda = datos["shop"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 165 | `print(f"Conectado a: {tienda['name']} ({tienda['myshopifyDomain']})")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 166 | `except (RuntimeError, requests.RequestException, KeyError) as error:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 167 | `print(f"Error de conexión: {error}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

## `carrito/datos.py`

| Línea | Código | Explicación |
|---:|---|---|
| 1 | `"""Carga, validación y acceso al catálogo compartido por las tres implementaciones.` | Docstring: describe el propósito del bloque. |
| 2 | `` | Línea en blanco: separa bloques lógicos. |
| 3 | `Este módulo es la única fuente de datos: las tres versiones del carrito` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 4 | `reciben el mismo diccionario, por lo que cualquier diferencia de resultado` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 5 | `se debe al paradigma y no a los datos de entrada.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 6 | `` | Línea en blanco: separa bloques lógicos. |
| 7 | `La validación del esquema evita enviar datos incompletos a Shopify.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 8 | `"""` | Docstring: describe el propósito del bloque. |
| 9 | `` | Línea en blanco: separa bloques lógicos. |
| 10 | `import json` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 11 | `from pathlib import Path` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 12 | `` | Línea en blanco: separa bloques lógicos. |
| 13 | `# Ruta por defecto, calculada desde la ubicación de este archivo y no desde` | Ruta por defecto, calculada desde la ubicación de este archivo y no desde |
| 14 | `# el directorio de ejecución, para que funcione desde cualquier carpeta.` | el directorio de ejecución, para que funcione desde cualquier carpeta. |
| 15 | `RUTA_CATALOGO = Path(__file__).resolve().parent.parent / "datos" / "catalogo.json"` | el directorio de ejecución, para que funcione desde cualquier carpeta. |
| 16 | `` | Línea en blanco: separa bloques lógicos. |
| 17 | `` | Línea en blanco: separa bloques lógicos. |
| 18 | `def validar_catalogo(catalogo):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 19 | `"""Comprueba que el JSON tenga las claves y tipos que espera el carrito."""` | Docstring: describe el propósito del bloque. |
| 20 | `if not isinstance(catalogo, dict):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 21 | `raise ValueError("El catálogo debe ser un objeto JSON")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 22 | `` | Línea en blanco: separa bloques lógicos. |
| 23 | `for clave in ("moneda", "envio", "sustitutos", "productos", "eventos"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 24 | `if clave not in catalogo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 25 | `raise ValueError(f"Falta la clave obligatoria '{clave}' en el catálogo")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 26 | `` | Línea en blanco: separa bloques lógicos. |
| 27 | `envio = catalogo["envio"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 28 | `for clave in ("costo", "gratis_desde"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 29 | `if not isinstance(envio.get(clave), int) or envio[clave] < 0:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 30 | `raise ValueError(f"envio.{clave} debe ser un entero no negativo")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 31 | `` | Línea en blanco: separa bloques lógicos. |
| 32 | `if not isinstance(catalogo["productos"], list) or not catalogo["productos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 33 | `raise ValueError("productos debe ser una lista no vacía")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 34 | `` | Línea en blanco: separa bloques lógicos. |
| 35 | `skus = set()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 36 | `for producto in catalogo["productos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 37 | `for clave in ("sku", "nombre", "precio", "stock", "categoria",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 38 | `"descripcion", "imagen"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 39 | `if clave not in producto:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 40 | `raise ValueError(f"Falta '{clave}' en el producto {producto.get('sku')}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 41 | `if producto["sku"] in skus:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 42 | `raise ValueError(f"SKU duplicado: {producto['sku']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 43 | `skus.add(producto["sku"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 44 | `if not isinstance(producto["precio"], int) or producto["precio"] <= 0:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 45 | `raise ValueError(f"precio inválido en {producto['sku']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 46 | `if not isinstance(producto["stock"], int) or producto["stock"] < 0:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 47 | `raise ValueError(f"stock inválido en {producto['sku']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 48 | `if not str(producto["imagen"]).startswith("https://"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 49 | `raise ValueError(f"imagen inválida en {producto['sku']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 50 | `` | Línea en blanco: separa bloques lógicos. |
| 51 | `for sku, sustituto in catalogo["sustitutos"].items():` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 52 | `if sku not in skus or sustituto not in skus:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 53 | `raise ValueError(f"Sustituto inválido: {sku} -> {sustituto}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 54 | `` | Línea en blanco: separa bloques lógicos. |
| 55 | `if not isinstance(catalogo["eventos"], dict) or not catalogo["eventos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 56 | `raise ValueError("eventos debe ser un objeto no vacío")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 57 | `` | Línea en blanco: separa bloques lógicos. |
| 58 | `for nombre, evento in catalogo["eventos"].items():` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 59 | `for clave in ("nombre", "cupon", "producto_2x1", "reglas"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 60 | `if clave not in evento:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 61 | `raise ValueError(f"Falta '{clave}' en el evento {nombre}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 62 | `if evento["producto_2x1"] not in skus:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 63 | `raise ValueError(f"producto_2x1 inexistente en el evento {nombre}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 64 | `for regla in evento["reglas"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 65 | `if regla["sku"] not in skus:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 66 | `raise ValueError(f"SKU de regla inexistente: {regla['sku']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 67 | `if regla["por_persona"] < 0 or regla["minimo"] < 0:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 68 | `raise ValueError(f"Cantidades negativas en el evento {nombre}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 69 | `` | Línea en blanco: separa bloques lógicos. |
| 70 | `return True` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 71 | `` | Línea en blanco: separa bloques lógicos. |
| 72 | `` | Línea en blanco: separa bloques lógicos. |
| 73 | `def cargar_catalogo(ruta=RUTA_CATALOGO):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 74 | `"""Lee el JSON, valida su esquema y devuelve el diccionario del catálogo."""` | Docstring: describe el propósito del bloque. |
| 75 | `with open(ruta, "r", encoding="utf-8") as archivo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 76 | `catalogo = json.load(archivo)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 77 | `validar_catalogo(catalogo)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 78 | `return catalogo` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 79 | `` | Línea en blanco: separa bloques lógicos. |
| 80 | `` | Línea en blanco: separa bloques lógicos. |
| 81 | `def indice_productos(catalogo):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 82 | `"""Construye un índice {sku: producto} para búsquedas O(1)."""` | Docstring: describe el propósito del bloque. |
| 83 | `return {producto["sku"]: producto for producto in catalogo["productos"]}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

## `carrito/imperativo.py`

| Línea | Código | Explicación |
|---:|---|---|
| 1 | `"""Versión IMPERATIVA del Carrito Evento Especial.` | Docstring: describe el propósito del bloque. |
| 2 | `` | Línea en blanco: separa bloques lógicos. |
| 3 | `Características del paradigma usadas aquí:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 4 | `- Variables mutables (`items`, `faltantes`, `total`).` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 5 | `- Estructuras de control explícitas (`for`, `if`).` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 6 | `- Estado construido paso a paso con asignaciones.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 7 | `"""` | Docstring: describe el propósito del bloque. |
| 8 | `` | Línea en blanco: separa bloques lógicos. |
| 9 | `import math` | ceil() redondea siempre hacia arriba. |
| 10 | `` | Línea en blanco: separa bloques lógicos. |
| 11 | `from carrito.datos import indice_productos` | Convierte la lista de productos en un dict. |
| 12 | `` | Línea en blanco: separa bloques lógicos. |
| 13 | `` | Línea en blanco: separa bloques lógicos. |
| 14 | `def armar_carrito(evento, personas, catalogo, cupon=None):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 15 | `"""Devuelve el carrito armado como diccionario (misma forma en los 3 paradigmas)."""` | Docstring: describe el propósito del bloque. |
| 16 | `` | Línea en blanco: separa bloques lógicos. |
| 17 | `# Validación temprana: evita trabajar con entradas sin sentido.` | Validación temprana: evita trabajar con entradas sin sentido. |
| 18 | `if personas <= 0:` | Una persona o menos no define un evento. |
| 19 | `raise ValueError("personas debe ser mayor que cero")` | Error explícito. |
| 20 | `` | Línea en blanco: separa bloques lógicos. |
| 21 | `if evento not in catalogo["eventos"]:` | El evento debe existir en el JSON. |
| 22 | `raise ValueError(f"Evento desconocido: {evento}")` | Mensaje útil. |
| 23 | `` | Línea en blanco: separa bloques lógicos. |
| 24 | `productos = indice_productos(catalogo)` | {sku: producto}, acceso O(1). |
| 25 | `config = catalogo["eventos"][evento]` | Reglas propias del evento elegido. |
| 26 | `items = []` | Acumulador mutable de líneas del carrito. |
| 27 | `faltantes = []` | Acumulador mutable de productos sin stock suficiente. |
| 28 | `` | Línea en blanco: separa bloques lógicos. |
| 29 | `# --- Paso 1: calcular cantidades y resolver stock ---` | --- Paso 1: calcular cantidades y resolver stock --- |
| 30 | `for regla in config["reglas"]:` | Recorre las reglas en orden estable. |
| 31 | `sku = regla["sku"]` | SKU del producto sugerido por la regla. |
| 32 | `producto = productos[sku]` | Datos del producto (precio, stock, nombre). |
| 33 | `` | Línea en blanco: separa bloques lógicos. |
| 34 | `# ceil() porque no se pueden vender fracciones; max() aplica el mínimo.` | ceil() porque no se pueden vender fracciones; max() aplica el mínimo. |
| 35 | `cantidad = max(regla["minimo"], math.ceil(personas * regla["por_persona"]))` | ceil() porque no se pueden vender fracciones; max() aplica el mínimo. |
| 36 | `` | Línea en blanco: separa bloques lógicos. |
| 37 | `if cantidad > producto["stock"]:` | No hay stock suficiente. |
| 38 | `sku_sustituto = catalogo["sustitutos"].get(sku)` | Busca alternativa. |
| 39 | `sustituto = productos.get(sku_sustituto)` | Puede no existir. |
| 40 | `` | Línea en blanco: separa bloques lógicos. |
| 41 | `if sustituto and sustituto["stock"] >= cantidad:` | El sustituto alcanza. |
| 42 | `# Se agrega el sustituto, dejando registro del producto original.` | Se agrega el sustituto, dejando registro del producto original. |
| 43 | `items.append({` | Se agrega el sustituto, dejando registro del producto original. |
| 44 | `"sku": sustituto["sku"],` | SKU que finalmente se vende. |
| 45 | `"nombre": sustituto["nombre"],` | Nombre del sustituto. |
| 46 | `"cantidad": cantidad,` | Cantidad calculada originalmente. |
| 47 | `"precio_unitario": sustituto["precio"],` | Precio del sustituto. |
| 48 | `"subtotal": cantidad * sustituto["precio"],` | Línea * precio. |
| 49 | `"sustituto_de": sku,` | Trazabilidad del cambio. |
| 50 | `})` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 51 | `continue` | Ya resolvimos esta regla; pasamos a la siguiente. |
| 52 | `` | Línea en blanco: separa bloques lógicos. |
| 53 | `disponible = producto["stock"]` | Stock real que sí se puede vender. |
| 54 | `if disponible > 0:` | Solo agregamos la línea si hay algo disponible. |
| 55 | `items.append({` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 56 | `"sku": sku,` | SKU original. |
| 57 | `"nombre": producto["nombre"],` | Nombre original. |
| 58 | `"cantidad": disponible,` | Se limita al stock disponible. |
| 59 | `"precio_unitario": producto["precio"],` | Precio original. |
| 60 | `"subtotal": disponible * producto["precio"],` | Subtotal de la línea. |
| 61 | `"sustituto_de": None,` | No hubo sustitución. |
| 62 | `})` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 63 | `` | Línea en blanco: separa bloques lógicos. |
| 64 | `falta = cantidad - disponible` | Diferencia no cubierta. |
| 65 | `if falta > 0:` | Solo se registra si realmente falta stock. |
| 66 | `faltantes.append({"sku": sku, "cantidad": falta})` | Reporte. |
| 67 | `else:` | Hay stock suficiente. |
| 68 | `items.append({` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 69 | `"sku": sku,` | SKU original. |
| 70 | `"nombre": producto["nombre"],` | Nombre original. |
| 71 | `"cantidad": cantidad,` | Cantidad calculada. |
| 72 | `"precio_unitario": producto["precio"],` | Precio original. |
| 73 | `"subtotal": cantidad * producto["precio"],` | Subtotal de la línea. |
| 74 | `"sustituto_de": None,` | Sin sustitución. |
| 75 | `})` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 76 | `` | Línea en blanco: separa bloques lógicos. |
| 77 | `# --- Paso 2: aplicar promoción 2x1 ---` | --- Paso 2: aplicar promoción 2x1 --- |
| 78 | `descuento_2x1 = 0` | Acumulador del descuento. |
| 79 | `sku_promo = config["producto_2x1"]` | Producto con 2x1 en este evento. |
| 80 | `for item in items:` | Revisa cada línea ya construida. |
| 81 | `# Se considera también el sustituto para no perder la promoción.` | Se considera también el sustituto para no perder la promoción. |
| 82 | `if item["sku"] == sku_promo or item["sustituto_de"] == sku_promo:` | Se considera también el sustituto para no perder la promoción. |
| 83 | `pares = item["cantidad"] // 2` | Cada par equivale a una unidad gratis. |
| 84 | `descuento_2x1 += pares * item["precio_unitario"]` | Acumula el descuento. |
| 85 | `` | Línea en blanco: separa bloques lógicos. |
| 86 | `# --- Paso 3: subtotal, cupón y envío ---` | --- Paso 3: subtotal, cupón y envío --- |
| 87 | `subtotal = 0` | Acumulador del subtotal sin descuentos. |
| 88 | `for item in items:` | Recorre las líneas. |
| 89 | `subtotal += item["subtotal"]` | Suma el subtotal de cada línea. |
| 90 | `` | Línea en blanco: separa bloques lógicos. |
| 91 | `base = subtotal - descuento_2x1` | Subtotal después del 2x1. |
| 92 | `descuento_cupon = 0` | Valor por defecto: sin cupón. |
| 93 | `if cupon == config["cupon"]:` | Solo si el cupón coincide con el del evento. |
| 94 | `descuento_cupon = base * 10 // 100` | 10% redondeado hacia abajo (enteros). |
| 95 | `` | Línea en blanco: separa bloques lógicos. |
| 96 | `envio = catalogo["envio"]` | Configuración de envío del JSON. |
| 97 | `if base - descuento_cupon >= envio["gratis_desde"]:` | Supera el umbral. |
| 98 | `costo_envio = 0` | Envío gratis. |
| 99 | `else:` | No supera el umbral. |
| 100 | `costo_envio = envio["costo"]` | Se cobra el envío. |
| 101 | `` | Línea en blanco: separa bloques lógicos. |
| 102 | `total = base - descuento_cupon + costo_envio` | Resultado final. |
| 103 | `` | Línea en blanco: separa bloques lógicos. |
| 104 | `# --- Paso 4: devolver estructura común a los tres paradigmas ---` | --- Paso 4: devolver estructura común a los tres paradigmas --- |
| 105 | `return {` | --- Paso 4: devolver estructura común a los tres paradigmas --- |
| 106 | `"evento": evento,` | Evento solicitado. |
| 107 | `"personas": personas,` | Cantidad de personas solicitada. |
| 108 | `"items": items,` | Líneas del carrito. |
| 109 | `"faltantes": faltantes,` | Productos sin stock. |
| 110 | `"descuentos": {"2x1": descuento_2x1, "cupon": descuento_cupon},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 111 | `"envio": costo_envio,` | Costo de envío aplicado. |
| 112 | `"total": total,` | Total a pagar. |
| 113 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

## `carrito/orientado_objetos.py`

| Línea | Código | Explicación |
|---:|---|---|
| 1 | `"""Versión ORIENTADA A OBJETOS del Carrito Evento Especial.` | Docstring: describe el propósito del bloque. |
| 2 | `` | Línea en blanco: separa bloques lógicos. |
| 3 | `Características del paradigma usadas aquí:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 4 | `- Clases e instancias que modelan Producto, Regla, Evento, Item y Carrito.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 5 | `- Encapsulamiento: cada clase conoce solo su propia responsabilidad.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 6 | `- Herencia y polimorfismo: `Descuento2x1` y `DescuentoPorcentaje` derivan de` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 7 | ``Descuento` y se tratan de la misma forma desde el carrito.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 8 | `"""` | Docstring: describe el propósito del bloque. |
| 9 | `` | Línea en blanco: separa bloques lógicos. |
| 10 | `import math` | Para ceil(). |
| 11 | `from abc import ABC, abstractmethod` | ABC = clase abstracta. |
| 12 | `from dataclasses import dataclass` | Reduce el código repetitivo de __init__. |
| 13 | `` | Línea en blanco: separa bloques lógicos. |
| 14 | `from carrito.datos import indice_productos` | Índice compartido de productos. |
| 15 | `` | Línea en blanco: separa bloques lógicos. |
| 16 | `` | Línea en blanco: separa bloques lógicos. |
| 17 | `# --- Modelo de datos ---` | --- Modelo de datos --- |
| 18 | `` | Línea en blanco: separa bloques lógicos. |
| 19 | `@dataclass(frozen=True)` | frozen=True => objetos inmutables. |
| 20 | `class Producto:` | --- Modelo de datos --- |
| 21 | `"""Representa un producto del catálogo."""` | Docstring: describe el propósito del bloque. |
| 22 | `` | Línea en blanco: separa bloques lógicos. |
| 23 | `sku: str` | Identificador único. |
| 24 | `nombre: str` | Nombre visible. |
| 25 | `precio: int` | Precio en pesos enteros. |
| 26 | `stock: int` | Unidades disponibles. |
| 27 | `` | Línea en blanco: separa bloques lógicos. |
| 28 | `def crear_item(self, cantidad, sustituto_de=None):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 29 | `"""Fábrica de líneas de carrito a partir del producto."""` | Docstring: describe el propósito del bloque. |
| 30 | `return Item(` | Devuelve un objeto Item. |
| 31 | `sku=self.sku,` | SKU del producto vendido. |
| 32 | `nombre=self.nombre,` | Nombre del producto vendido. |
| 33 | `cantidad=cantidad,` | Unidades calculadas. |
| 34 | `precio_unitario=self.precio,` | Precio unitario. |
| 35 | `subtotal=cantidad * self.precio,` | Precio total de la línea. |
| 36 | `sustituto_de=sustituto_de,` | SKU original si hubo sustitución. |
| 37 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 38 | `` | Línea en blanco: separa bloques lógicos. |
| 39 | `` | Línea en blanco: separa bloques lógicos. |
| 40 | `@dataclass(frozen=True)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 41 | `class Item:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 42 | `"""Una línea del carrito; también inmutable."""` | Docstring: describe el propósito del bloque. |
| 43 | `` | Línea en blanco: separa bloques lógicos. |
| 44 | `sku: str` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 45 | `nombre: str` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 46 | `cantidad: int` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 47 | `precio_unitario: int` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 48 | `subtotal: int` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 49 | `sustituto_de: str \| None` | None cuando no hubo sustitución. |
| 50 | `` | Línea en blanco: separa bloques lógicos. |
| 51 | `def como_dict(self):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 52 | `"""Convierte el objeto en diccionario para igualar a los otros paradigmas."""` | Docstring: describe el propósito del bloque. |
| 53 | `return {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 54 | `"sku": self.sku,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 55 | `"nombre": self.nombre,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 56 | `"cantidad": self.cantidad,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 57 | `"precio_unitario": self.precio_unitario,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 58 | `"subtotal": self.subtotal,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 59 | `"sustituto_de": self.sustituto_de,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 60 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 61 | `` | Línea en blanco: separa bloques lógicos. |
| 62 | `` | Línea en blanco: separa bloques lógicos. |
| 63 | `@dataclass(frozen=True)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 64 | `class Regla:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 65 | `"""Regla que define cuántas unidades se sugieren por persona."""` | Docstring: describe el propósito del bloque. |
| 66 | `` | Línea en blanco: separa bloques lógicos. |
| 67 | `sku: str` | Producto al que aplica. |
| 68 | `por_persona: float` | Unidades (o fracción) por persona. |
| 69 | `minimo: int` | Mínimo absoluto de unidades. |
| 70 | `` | Línea en blanco: separa bloques lógicos. |
| 71 | `def cantidad_para(self, personas):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 72 | `"""Calcula la cantidad redondeada hacia arriba, con mínimo."""` | Docstring: describe el propósito del bloque. |
| 73 | `return max(self.minimo, math.ceil(personas * self.por_persona))` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 74 | `` | Línea en blanco: separa bloques lógicos. |
| 75 | `` | Línea en blanco: separa bloques lógicos. |
| 76 | `@dataclass(frozen=True)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 77 | `class Evento:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 78 | `"""Configuración de un evento: reglas, cupón y producto en 2x1."""` | Docstring: describe el propósito del bloque. |
| 79 | `` | Línea en blanco: separa bloques lógicos. |
| 80 | `nombre: str` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 81 | `cupon: str` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 82 | `producto_2x1: str` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 83 | `reglas: tuple` | Tupla de Regla (inmutable). |
| 84 | `` | Línea en blanco: separa bloques lógicos. |
| 85 | `@classmethod` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 86 | `def desde_dict(cls, datos):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 87 | `"""Construye un Evento desde el diccionario del JSON."""` | Docstring: describe el propósito del bloque. |
| 88 | `reglas = tuple(` | Comprensión que crea objetos Regla. |
| 89 | `Regla(r["sku"], r["por_persona"], r["minimo"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 90 | `for r in datos["reglas"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 91 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 92 | `return cls(datos["nombre"], datos["cupon"], datos["producto_2x1"], reglas)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 93 | `` | Línea en blanco: separa bloques lógicos. |
| 94 | `` | Línea en blanco: separa bloques lógicos. |
| 95 | `# --- Estrategias de descuento (herencia y polimorfismo) ---` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 96 | `` | Línea en blanco: separa bloques lógicos. |
| 97 | `class Descuento(ABC):` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 98 | `"""Interfaz común: toda estrategia debe saber calcular un descuento."""` | Docstring: describe el propósito del bloque. |
| 99 | `` | Línea en blanco: separa bloques lógicos. |
| 100 | `@abstractmethod` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 101 | `def calcular(self, items, evento, cupon):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 102 | `"""Devuelve el monto de descuento (entero)."""` | Docstring: describe el propósito del bloque. |
| 103 | `raise NotImplementedError` | Obliga a las subclases a implementarlo. |
| 104 | `` | Línea en blanco: separa bloques lógicos. |
| 105 | `` | Línea en blanco: separa bloques lógicos. |
| 106 | `class Descuento2x1(Descuento):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 107 | `"""Descuento 2x1 sobre el producto configurado en el evento."""` | Docstring: describe el propósito del bloque. |
| 108 | `` | Línea en blanco: separa bloques lógicos. |
| 109 | `def calcular(self, items, evento, cupon):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 110 | `total = 0` | Acumulador local. |
| 111 | `for item in items:` | Polimorfismo: Item expone los mismos atributos. |
| 112 | `es_promo = item.sku == evento.producto_2x1` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 113 | `es_sustituto = item.sustituto_de == evento.producto_2x1` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 114 | `if es_promo or es_sustituto:` | Aplica también al sustituto. |
| 115 | `total += (item.cantidad // 2) * item.precio_unitario` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 116 | `return total` | Cumple el contrato de Descuento. |
| 117 | `` | Línea en blanco: separa bloques lógicos. |
| 118 | `` | Línea en blanco: separa bloques lógicos. |
| 119 | `class DescuentoPorcentaje(Descuento):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 120 | `"""Descuento por cupón: porcentaje sobre la base ya descontada."""` | Docstring: describe el propósito del bloque. |
| 121 | `` | Línea en blanco: separa bloques lógicos. |
| 122 | `def __init__(self, porcentaje):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 123 | `self.porcentaje = porcentaje` | Estado interno encapsulado. |
| 124 | `` | Línea en blanco: separa bloques lógicos. |
| 125 | `def calcular(self, items, evento, cupon, base=0):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 126 | `# Firma extendida con `base`; se usa desde el carrito de forma explícita.` | Firma extendida con `base`; se usa desde el carrito de forma explícita. |
| 127 | `if cupon != evento.cupon:` | Cupón incorrecto o ausente. |
| 128 | `return 0` | Sin descuento. |
| 129 | `return base * self.porcentaje // 100` | Entero, redondeo hacia abajo. |
| 130 | `` | Línea en blanco: separa bloques lógicos. |
| 131 | `` | Línea en blanco: separa bloques lógicos. |
| 132 | `class PoliticaEnvio:` | Firma extendida con `base`; se usa desde el carrito de forma explícita. |
| 133 | `"""Define cuándo el envío es gratis."""` | Docstring: describe el propósito del bloque. |
| 134 | `` | Línea en blanco: separa bloques lógicos. |
| 135 | `def __init__(self, costo, gratis_desde):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 136 | `self.costo = costo` | Costo normal. |
| 137 | `self.gratis_desde = gratis_desde` | Umbral para envío gratis. |
| 138 | `` | Línea en blanco: separa bloques lógicos. |
| 139 | `def calcular(self, monto):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 140 | `"""Devuelve el costo de envío según el monto después de descuentos."""` | Docstring: describe el propósito del bloque. |
| 141 | `return 0 if monto >= self.gratis_desde else self.costo` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 142 | `` | Línea en blanco: separa bloques lógicos. |
| 143 | `` | Línea en blanco: separa bloques lógicos. |
| 144 | `# --- Orquestación ---` | --- Orquestación --- |
| 145 | `` | Línea en blanco: separa bloques lógicos. |
| 146 | `class Carrito:` | --- Orquestación --- |
| 147 | `"""Coordina productos, reglas y descuentos para armar el carrito."""` | Docstring: describe el propósito del bloque. |
| 148 | `` | Línea en blanco: separa bloques lógicos. |
| 149 | `def __init__(self, evento, personas, catalogo, cupon=None):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 150 | `if personas <= 0:` | Validación de entrada. |
| 151 | `raise ValueError("personas debe ser mayor que cero")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 152 | `if evento not in catalogo["eventos"]:` | Validación de evento. |
| 153 | `raise ValueError(f"Evento desconocido: {evento}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 154 | `` | Línea en blanco: separa bloques lógicos. |
| 155 | `self.evento = Evento.desde_dict(catalogo["eventos"][evento])` | Config. |
| 156 | `self.personas = personas` | Cantidad de personas. |
| 157 | `self.productos = {` | Dict de objetos Producto. |
| 158 | `sku: Producto(p["sku"], p["nombre"], p["precio"], p["stock"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 159 | `for sku, p in indice_productos(catalogo).items()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 160 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 161 | `self.sustitutos = catalogo["sustitutos"]` | Mapa de reemplazos. |
| 162 | `self.cupon = cupon` | Cupón ingresado por el usuario. |
| 163 | `self.envio = PoliticaEnvio(` | Política de envío del catálogo. |
| 164 | `catalogo["envio"]["costo"], catalogo["envio"]["gratis_desde"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 165 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 166 | `self.descuentos = [Descuento2x1()]` | Estrategias polimórficas. |
| 167 | `` | Línea en blanco: separa bloques lógicos. |
| 168 | `def _resolver_regla(self, regla):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 169 | `"""Aplica una regla; devuelve (item o None, faltante o None)."""` | Docstring: describe el propósito del bloque. |
| 170 | `producto = self.productos[regla.sku]` | Producto sugerido. |
| 171 | `cantidad = regla.cantidad_para(self.personas)` | Cantidad calculada. |
| 172 | `` | Línea en blanco: separa bloques lógicos. |
| 173 | `if cantidad <= producto.stock:` | Caso simple: hay stock. |
| 174 | `return producto.crear_item(cantidad), None` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 175 | `` | Línea en blanco: separa bloques lógicos. |
| 176 | `# Sin stock suficiente: intenta sustituto.` | Sin stock suficiente: intenta sustituto. |
| 177 | `sku_alt = self.sustitutos.get(regla.sku)` | SKU alternativo. |
| 178 | `alternativo = self.productos.get(sku_alt)` | Objeto alternativo. |
| 179 | `if alternativo and alternativo.stock >= cantidad:` | El sustituto alcanza. |
| 180 | `return alternativo.crear_item(cantidad, regla.sku), None` | Sin stock suficiente: intenta sustituto. |
| 181 | `` | Línea en blanco: separa bloques lógicos. |
| 182 | `# No hay sustituto válido: se vende lo disponible y se reporta el falta.` | No hay sustituto válido: se vende lo disponible y se reporta el falta. |
| 183 | `disponible = producto.stock` | No hay sustituto válido: se vende lo disponible y se reporta el falta. |
| 184 | `item = producto.crear_item(disponible) if disponible > 0 else None` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 185 | `faltante = {"sku": regla.sku, "cantidad": cantidad - disponible}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 186 | `return item, faltante` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 187 | `` | Línea en blanco: separa bloques lógicos. |
| 188 | `def armar(self):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 189 | `"""Ejecuta el algoritmo completo y devuelve el diccionario resultado."""` | Docstring: describe el propósito del bloque. |
| 190 | `items = []` | Lista mutable de objetos Item. |
| 191 | `faltantes = []` | Lista mutable de reportes de stock. |
| 192 | `` | Línea en blanco: separa bloques lógicos. |
| 193 | `for regla in self.evento.reglas:` | Iteración sobre reglas del evento. |
| 194 | `item, faltante = self._resolver_regla(regla)` | Delegación. |
| 195 | `if item is not None:` | Puede no haber item si stock = 0. |
| 196 | `items.append(item)` | Acumula el objeto. |
| 197 | `if faltante is not None:` | Puede no haber faltante. |
| 198 | `faltantes.append(faltante)` | Acumula el reporte. |
| 199 | `` | Línea en blanco: separa bloques lógicos. |
| 200 | `subtotal = sum(item.subtotal for item in items)` | Suma de líneas. |
| 201 | `` | Línea en blanco: separa bloques lógicos. |
| 202 | `# Polimorfismo: ambas estrategias responden a `calcular`.` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 203 | `desc_2x1 = self.descuentos[0].calcular(items, self.evento, self.cupon)` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 204 | `desc_cupon = DescuentoPorcentaje(10).calcular(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 205 | `items, self.evento, self.cupon, base=subtotal - desc_2x1` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 206 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 207 | `` | Línea en blanco: separa bloques lógicos. |
| 208 | `base = subtotal - desc_2x1 - desc_cupon` | Monto para evaluar envío. |
| 209 | `costo_envio = self.envio.calcular(base)` | Política de envío. |
| 210 | `total = base + costo_envio` | Total final. |
| 211 | `` | Línea en blanco: separa bloques lógicos. |
| 212 | `return {` | Misma estructura que en el paradigma imperativo. |
| 213 | `"evento": self.evento.nombre.lower().replace(" ", "_"),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 214 | `"personas": self.personas,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 215 | `"items": [item.como_dict() for item in items],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 216 | `"faltantes": faltantes,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 217 | `"descuentos": {"2x1": desc_2x1, "cupon": desc_cupon},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 218 | `"envio": costo_envio,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 219 | `"total": total,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 220 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 221 | `` | Línea en blanco: separa bloques lógicos. |
| 222 | `` | Línea en blanco: separa bloques lógicos. |
| 223 | `def armar_carrito(evento, personas, catalogo, cupon=None):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 224 | `"""API pública equivalente a la de los otros dos módulos."""` | Docstring: describe el propósito del bloque. |
| 225 | `# El evento devuelto por la clase se normaliza al nombre de la clave JSON.` | El evento devuelto por la clase se normaliza al nombre de la clave JSON. |
| 226 | `carrito = Carrito(evento, personas, catalogo, cupon)` | El evento devuelto por la clase se normaliza al nombre de la clave JSON. |
| 227 | `resultado = carrito.armar()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 228 | `resultado["evento"] = evento` | Garantiza igualdad exacta entre versiones. |
| 229 | `return resultado` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

## `carrito/funcional.py`

| Línea | Código | Explicación |
|---:|---|---|
| 1 | `"""Versión FUNCIONAL del Carrito Evento Especial.` | Docstring: describe el propósito del bloque. |
| 2 | `` | Línea en blanco: separa bloques lógicos. |
| 3 | `Características del paradigma usadas aquí:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 4 | `- Funciones puras: misma entrada => misma salida, sin efectos secundarios.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 5 | `- Inmutabilidad: se usan tuplas y diccionarios nuevos, nunca se mutan los de entrada.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 6 | `- Funciones de orden superior: `map`, `filter` y `functools.reduce`.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 7 | `- Composición: `armar_carrito` encadena funciones pequeñas.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 8 | `"""` | Docstring: describe el propósito del bloque. |
| 9 | `` | Línea en blanco: separa bloques lógicos. |
| 10 | `import math` | ceil(). |
| 11 | `from functools import reduce` | reduce() acumula una secuencia en un solo valor. |
| 12 | `` | Línea en blanco: separa bloques lógicos. |
| 13 | `from carrito.datos import indice_productos` | Índice de productos compartido. |
| 14 | `` | Línea en blanco: separa bloques lógicos. |
| 15 | `` | Línea en blanco: separa bloques lógicos. |
| 16 | `def validar(evento, personas, catalogo):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 17 | `"""Función pura de validación: devuelve la configuración del evento."""` | Docstring: describe el propósito del bloque. |
| 18 | `if personas <= 0:` | Condición de error. |
| 19 | `raise ValueError("personas debe ser mayor que cero")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 20 | `if evento not in catalogo["eventos"]:` | El evento debe existir. |
| 21 | `raise ValueError(f"Evento desconocido: {evento}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 22 | `return catalogo["eventos"][evento]` | Devuelve un dict existente (no lo muta). |
| 23 | `` | Línea en blanco: separa bloques lógicos. |
| 24 | `` | Línea en blanco: separa bloques lógicos. |
| 25 | `def cantidad_para(personas, regla):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 26 | `"""Calcula unidades de una regla: techo y mínimo."""` | Docstring: describe el propósito del bloque. |
| 27 | `return max(regla["minimo"], math.ceil(personas * regla["por_persona"]))` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 28 | `` | Línea en blanco: separa bloques lógicos. |
| 29 | `` | Línea en blanco: separa bloques lógicos. |
| 30 | `def crear_item(producto, cantidad, sustituto_de=None):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 31 | `"""Construye un diccionario nuevo para una línea del carrito."""` | Docstring: describe el propósito del bloque. |
| 32 | `return {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 33 | `"sku": producto["sku"],` | SKU vendido. |
| 34 | `"nombre": producto["nombre"],` | Nombre del producto. |
| 35 | `"cantidad": cantidad,` | Unidades. |
| 36 | `"precio_unitario": producto["precio"],` | Precio unitario. |
| 37 | `"subtotal": cantidad * producto["precio"],` | Total de la línea. |
| 38 | `"sustituto_de": sustituto_de,` | SKU original si se sustituyó. |
| 39 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 40 | `` | Línea en blanco: separa bloques lógicos. |
| 41 | `` | Línea en blanco: separa bloques lógicos. |
| 42 | `def resolver(regla, personas, catalogo, productos):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 43 | `"""Devuelve el par (item, faltante); uno de los dos puede ser None."""` | Docstring: describe el propósito del bloque. |
| 44 | `producto = productos[regla["sku"]]` | Producto de la regla. |
| 45 | `cantidad = cantidad_para(personas, regla)` | Cantidad calculada. |
| 46 | `` | Línea en blanco: separa bloques lógicos. |
| 47 | `if cantidad <= producto["stock"]:` | Hay stock. |
| 48 | `return crear_item(producto, cantidad), None` | Par sin faltante. |
| 49 | `` | Línea en blanco: separa bloques lógicos. |
| 50 | `# Sin stock: buscar sustituto con stock suficiente.` | Sin stock: buscar sustituto con stock suficiente. |
| 51 | `sku_alternativo = catalogo["sustitutos"].get(regla["sku"])` | Puede no existir. |
| 52 | `alternativo = productos.get(sku_alternativo)` | Puede no existir. |
| 53 | `` | Línea en blanco: separa bloques lógicos. |
| 54 | `if alternativo and alternativo["stock"] >= cantidad:` | Sustituto válido. |
| 55 | `return crear_item(alternativo, cantidad, regla["sku"]), None` | Sin stock: buscar sustituto con stock suficiente. |
| 56 | `` | Línea en blanco: separa bloques lógicos. |
| 57 | `# Sin sustituto válido: vender lo disponible y reportar la diferencia.` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 58 | `disponible = producto["stock"]` | Stock disponible. |
| 59 | `item = crear_item(producto, disponible) if disponible > 0 else None` | Item opcional. |
| 60 | `faltante = {"sku": regla["sku"], "cantidad": cantidad - disponible}` | Reporte. |
| 61 | `return item, faltante` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 62 | `` | Línea en blanco: separa bloques lógicos. |
| 63 | `` | Línea en blanco: separa bloques lógicos. |
| 64 | `def construir_lineas(config, personas, catalogo, productos):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 65 | `"""Aplica `resolver` a todas las reglas con map y separa resultados."""` | Docstring: describe el propósito del bloque. |
| 66 | `pares = tuple(` | Tupla inmutable de resultados. |
| 67 | `map(` | map aplica resolver a cada regla. |
| 68 | `lambda regla: resolver(regla, personas, catalogo, productos),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 69 | `config["reglas"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 70 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 71 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 72 | `items = tuple(filter(None, map(lambda par: par[0], pares)))` | Solo items. |
| 73 | `faltantes = tuple(filter(None, map(lambda par: par[1], pares)))` | Solo faltantes. |
| 74 | `return items, faltantes` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 75 | `` | Línea en blanco: separa bloques lógicos. |
| 76 | `` | Línea en blanco: separa bloques lógicos. |
| 77 | `def sumar_subtotal(items):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 78 | `"""Reduce los subtotales de las líneas en un entero."""` | Docstring: describe el propósito del bloque. |
| 79 | `return reduce(lambda total, item: total + item["subtotal"], items, 0)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 80 | `` | Línea en blanco: separa bloques lógicos. |
| 81 | `` | Línea en blanco: separa bloques lógicos. |
| 82 | `def descuento_2x1(items, sku_promo):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 83 | `"""Descuento 2x1 usando reduce sobre las líneas promocionadas."""` | Docstring: describe el propósito del bloque. |
| 84 | `promocionados = filter(` | filter conserva solo las líneas que cumplen. |
| 85 | `lambda item: item["sku"] == sku_promo or item["sustituto_de"] == sku_promo,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 86 | `items,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 87 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 88 | `return reduce(` | Acumula pares * precio. |
| 89 | `lambda total, item: total + (item["cantidad"] // 2) * item["precio_unitario"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 90 | `promocionados,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 91 | `0,` | Valor inicial del acumulador. |
| 92 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 93 | `` | Línea en blanco: separa bloques lógicos. |
| 94 | `` | Línea en blanco: separa bloques lógicos. |
| 95 | `def descuento_cupon(cupon, config, base):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 96 | `"""Descuento de 10% solo si el cupón coincide con el del evento."""` | Docstring: describe el propósito del bloque. |
| 97 | `return base * 10 // 100 if cupon == config["cupon"] else 0` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 98 | `` | Línea en blanco: separa bloques lógicos. |
| 99 | `` | Línea en blanco: separa bloques lógicos. |
| 100 | `def costo_envio(catalogo, monto):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 101 | `"""Costo de envío según el umbral configurado."""` | Docstring: describe el propósito del bloque. |
| 102 | `envio = catalogo["envio"]` | Configuración de envío. |
| 103 | `return 0 if monto >= envio["gratis_desde"] else envio["costo"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 104 | `` | Línea en blanco: separa bloques lógicos. |
| 105 | `` | Línea en blanco: separa bloques lógicos. |
| 106 | `def armar_carrito(evento, personas, catalogo, cupon=None):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 107 | `"""Compone todas las funciones puras y devuelve el resultado final."""` | Docstring: describe el propósito del bloque. |
| 108 | `config = validar(evento, personas, catalogo)` | 1) Validar entradas. |
| 109 | `productos = indice_productos(catalogo)` | 2) Indexar productos. |
| 110 | `` | Línea en blanco: separa bloques lógicos. |
| 111 | `items, faltantes = construir_lineas(config, personas, catalogo, productos)` | 3) |
| 112 | `` | Línea en blanco: separa bloques lógicos. |
| 113 | `subtotal = sumar_subtotal(items)` | 4) Suma funcional de líneas. |
| 114 | `desc_2x1 = descuento_2x1(items, config["producto_2x1"])` | 5) Promoción. |
| 115 | `desc_cupon = descuento_cupon(cupon, config, subtotal - desc_2x1)` | 6) Cupón. |
| 116 | `` | Línea en blanco: separa bloques lógicos. |
| 117 | `base = subtotal - desc_2x1 - desc_cupon` | 7) Base para envío. |
| 118 | `envio = costo_envio(catalogo, base)` | 8) Envío. |
| 119 | `total = base + envio` | 9) Total. |
| 120 | `` | Línea en blanco: separa bloques lógicos. |
| 121 | `return {` | 10) Diccionario nuevo; equivalente a los otros paradigmas. |
| 122 | `"evento": evento,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 123 | `"personas": personas,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 124 | `"items": list(items),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 125 | `"faltantes": list(faltantes),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 126 | `"descuentos": {"2x1": desc_2x1, "cupon": desc_cupon},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 127 | `"envio": envio,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 128 | `"total": total,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 129 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

## `carrito/demo.py`

| Línea | Código | Explicación |
|---:|---|---|
| 1 | `"""Demostración: ejecuta las tres versiones con las mismas entradas y las compara.` | Docstring: describe el propósito del bloque. |
| 2 | `` | Línea en blanco: separa bloques lógicos. |
| 3 | `Uso desde la raíz del proyecto:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 4 | `python -m carrito.demo` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 5 | `"""` | Docstring: describe el propósito del bloque. |
| 6 | `` | Línea en blanco: separa bloques lógicos. |
| 7 | `from carrito import (` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 8 | `armar_funcional,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 9 | `armar_imperativo,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 10 | `armar_objetos,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 11 | `cargar_catalogo,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 12 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 13 | `` | Línea en blanco: separa bloques lógicos. |
| 14 | `# Casos de prueba definidos una sola vez para las tres implementaciones.` | Casos de prueba definidos una sola vez para las tres implementaciones. |
| 15 | `CASOS = [` | Casos de prueba definidos una sola vez para las tres implementaciones. |
| 16 | `("cumpleanos", 10, "FIESTA10"),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 17 | `("trabajo_remoto", 12, "HOME10"),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 18 | `("vuelta_a_clases", 12, "ESCUELA10"),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 19 | `("cumpleanos", 200, None),` | Fuerza sustituciones y faltantes por stock. |
| 20 | `("accesorios_basicos", 1, None),` | Monto bajo: debe cobrar envío. |
| 21 | `]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 22 | `` | Línea en blanco: separa bloques lógicos. |
| 23 | `# Las tres funciones se agrupan en una tupla para iterarlas por igual.` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 24 | `IMPLEMENTACIONES = (` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 25 | `("Imperativo", armar_imperativo),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 26 | `("Orientado a objetos", armar_objetos),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 27 | `("Funcional", armar_funcional),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 28 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 29 | `` | Línea en blanco: separa bloques lógicos. |
| 30 | `` | Línea en blanco: separa bloques lógicos. |
| 31 | `def formatear(resultado):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 32 | `"""Resume un resultado para mostrarlo en pantalla."""` | Docstring: describe el propósito del bloque. |
| 33 | `return (` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 34 | `f"items={len(resultado['items'])}, "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 35 | `f"faltantes={len(resultado['faltantes'])}, "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 36 | `f"2x1=${resultado['descuentos']['2x1']}, "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 37 | `f"cupon=${resultado['descuentos']['cupon']}, "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 38 | `f"envio=${resultado['envio']}, total=${resultado['total']}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 39 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 40 | `` | Línea en blanco: separa bloques lógicos. |
| 41 | `` | Línea en blanco: separa bloques lógicos. |
| 42 | `def main():` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 43 | `"""Ejecuta todos los casos y verifica que los tres resultados sean iguales."""` | Docstring: describe el propósito del bloque. |
| 44 | `catalogo = cargar_catalogo()` | Misma fuente de datos para todos. |
| 45 | `todos_iguales = True` | Bandera global del resultado de la comparación. |
| 46 | `` | Línea en blanco: separa bloques lógicos. |
| 47 | `for evento, personas, cupon in CASOS:` | Recorre los escenarios. |
| 48 | `print(f"\n=== {evento} \| {personas} personas \| cupón={cupon} ===")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 49 | `resultados = []` | Resultados de las tres implementaciones. |
| 50 | `` | Línea en blanco: separa bloques lógicos. |
| 51 | `for nombre, funcion in IMPLEMENTACIONES:` | Recorre los paradigmas. |
| 52 | `resultado = funcion(evento, personas, catalogo, cupon)` | Ejecuta. |
| 53 | `resultados.append(resultado)` | Guarda para comparar. |
| 54 | `print(f"  {nombre:<20} {formatear(resultado)}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 55 | `` | Línea en blanco: separa bloques lógicos. |
| 56 | `# Comparación estricta: los tres dict deben ser exactamente iguales.` | Comparación estricta: los tres dict deben ser exactamente iguales. |
| 57 | `iguales = resultados[0] == resultados[1] == resultados[2]` | Comparación estricta: los tres dict deben ser exactamente iguales. |
| 58 | `todos_iguales = todos_iguales and iguales` | Actualiza la bandera. |
| 59 | `print(f"  >>> Paridad: {'OK' if iguales else 'FALLO'}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 60 | `` | Línea en blanco: separa bloques lógicos. |
| 61 | `# Detalle del caso de stock agotado para hacer visible la sustitución.` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 62 | `if personas == 200:` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 63 | `for item in resultados[0]["items"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 64 | `if item["sustituto_de"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 65 | `print(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 66 | `f"    Sustituto: {item['sustituto_de']} -> "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 67 | `f"{item['sku']} x{item['cantidad']}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 68 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 69 | `for falta in resultados[0]["faltantes"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 70 | `print(f"    Faltante: {falta['sku']} x{falta['cantidad']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 71 | `` | Línea en blanco: separa bloques lógicos. |
| 72 | `print(f"\nResultado global: {'TODOS LOS CASOS COINCIDEN' if todos_iguales else 'HAY DIFERENCIAS'}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 73 | `return 0 if todos_iguales else 1` | Código de salida para CI. |
| 74 | `` | Línea en blanco: separa bloques lógicos. |
| 75 | `` | Línea en blanco: separa bloques lógicos. |
| 76 | `if __name__ == "__main__":` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 77 | `raise SystemExit(main())` | Permite usar el demo en scripts y tests. |

## `scripts/poblar_catalogo.py`

| Línea | Código | Explicación |
|---:|---|---|
| 1 | `"""Puebla el catálogo de Shopify usando la Admin GraphQL API.` | Docstring: describe el propósito del bloque. |
| 2 | `` | Línea en blanco: separa bloques lógicos. |
| 3 | `Uso desde la raíz del proyecto:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 4 | `python -m scripts.poblar_catalogo --dry-run` | solo muestra qué haría |
| 5 | `python -m scripts.poblar_catalogo` | crea productos y colecciones |
| 6 | `` | Línea en blanco: separa bloques lógicos. |
| 7 | `El script es idempotente: si el SKU ya existe, lo omite.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 8 | `"""` | Docstring: describe el propósito del bloque. |
| 9 | `` | Línea en blanco: separa bloques lógicos. |
| 10 | `import argparse` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 11 | `import sys` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 12 | `import unicodedata` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 13 | `from pathlib import Path` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 14 | `` | Línea en blanco: separa bloques lógicos. |
| 15 | `# Permite importar el módulo de la raíz aunque se ejecute como paquete.` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 16 | `sys.path.insert(0, str(Path(__file__).resolve().parent.parent))` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 17 | `` | Línea en blanco: separa bloques lógicos. |
| 18 | `from carrito.datos import cargar_catalogo` | noqa: E402 |
| 19 | `from shopify_client import graphql_query` | noqa: E402 |
| 20 | `` | Línea en blanco: separa bloques lógicos. |
| 21 | `PRODUCTOS_QUERY = """` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 22 | `{` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 23 | `products(first: 250) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 24 | `nodes {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 25 | `id` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 26 | `title` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 27 | `variants(first: 250) { nodes { id sku price } }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 28 | `media(first: 20) { nodes { id } }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 29 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 30 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 31 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 32 | `"""` | Docstring: describe el propósito del bloque. |
| 33 | `` | Línea en blanco: separa bloques lógicos. |
| 34 | `LOCATIONS_QUERY = """` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 35 | `{` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 36 | `locations(first: 10) { nodes { id } }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 37 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 38 | `"""` | Docstring: describe el propósito del bloque. |
| 39 | `` | Línea en blanco: separa bloques lógicos. |
| 40 | `PRODUCT_CREATE = """` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 41 | `mutation ProductoCrear($input: ProductInput!) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 42 | `productCreate(input: $input) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 43 | `product { id title handle }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 44 | `userErrors { field message }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 45 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 46 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 47 | `"""` | Docstring: describe el propósito del bloque. |
| 48 | `` | Línea en blanco: separa bloques lógicos. |
| 49 | `VARIANT_CREATE = """` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 50 | `mutation VarianteCrear($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 51 | `productVariantsBulkCreate(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 52 | `productId: $productId,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 53 | `variants: $variants,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 54 | `strategy: DEFAULT` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 55 | `) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 56 | `productVariants { id sku }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 57 | `userErrors { field message }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 58 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 59 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 60 | `"""` | Docstring: describe el propósito del bloque. |
| 61 | `` | Línea en blanco: separa bloques lógicos. |
| 62 | `VARIANT_UPDATE = """` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 63 | `mutation VarianteActualizar($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 64 | `productVariantsBulkUpdate(productId: $productId, variants: $variants) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 65 | `productVariants { id sku price }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 66 | `userErrors { field message }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 67 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 68 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 69 | `"""` | Docstring: describe el propósito del bloque. |
| 70 | `` | Línea en blanco: separa bloques lógicos. |
| 71 | `MEDIA_CREATE = """` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 72 | `mutation ImagenAgregar($productId: ID!, $media: [CreateMediaInput!]!) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 73 | `productCreateMedia(productId: $productId, media: $media) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 74 | `media { id mediaContentType }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 75 | `userErrors { field message }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 76 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 77 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 78 | `"""` | Docstring: describe el propósito del bloque. |
| 79 | `` | Línea en blanco: separa bloques lógicos. |
| 80 | `COLLECTION_CREATE = """` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 81 | `mutation ColeccionCrear($input: CollectionInput!) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 82 | `collectionCreate(input: $input) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 83 | `collection { id title handle }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 84 | `userErrors { field message }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 85 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 86 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 87 | `"""` | Docstring: describe el propósito del bloque. |
| 88 | `` | Línea en blanco: separa bloques lógicos. |
| 89 | `COLECCIONES_QUERY = """` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 90 | `{` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 91 | `collections(first: 250) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 92 | `nodes {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 93 | `id` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 94 | `handle` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 95 | `products(first: 250) { nodes { id } }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 96 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 97 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 98 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 99 | `"""` | Docstring: describe el propósito del bloque. |
| 100 | `` | Línea en blanco: separa bloques lógicos. |
| 101 | `COLLECTION_ADD = """` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 102 | `mutation AgregarProductos($id: ID!, $productIds: [ID!]!) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 103 | `collectionAddProducts(id: $id, productIds: $productIds) {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 104 | `collection { id title }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 105 | `userErrors { field message }` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 106 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 107 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 108 | `"""` | Docstring: describe el propósito del bloque. |
| 109 | `` | Línea en blanco: separa bloques lógicos. |
| 110 | `` | Línea en blanco: separa bloques lógicos. |
| 111 | `def skus_existentes():` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 112 | `"""Devuelve el conjunto de SKUs ya creados en la tienda."""` | Docstring: describe el propósito del bloque. |
| 113 | `datos = graphql_query(PRODUCTOS_QUERY)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 114 | `skus = set()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 115 | `for producto in datos["products"]["nodes"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 116 | `for variante in producto["variants"]["nodes"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 117 | `if variante["sku"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 118 | `skus.add(variante["sku"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 119 | `return skus, datos["products"]["nodes"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 120 | `` | Línea en blanco: separa bloques lógicos. |
| 121 | `` | Línea en blanco: separa bloques lógicos. |
| 122 | `def location_principal():` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 123 | `"""Devuelve el ID de la primera ubicación de inventario."""` | Docstring: describe el propósito del bloque. |
| 124 | `datos = graphql_query(LOCATIONS_QUERY)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 125 | `ubicaciones = datos["locations"]["nodes"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 126 | `if not ubicaciones:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 127 | `raise RuntimeError("No hay ubicaciones de inventario configuradas")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 128 | `return ubicaciones[0]["id"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 129 | `` | Línea en blanco: separa bloques lógicos. |
| 130 | `` | Línea en blanco: separa bloques lógicos. |
| 131 | `def crear_producto(producto, location_id):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 132 | `"""Crea un producto con precio, SKU, stock y etiquetas."""` | Docstring: describe el propósito del bloque. |
| 133 | `entrada = {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 134 | `"title": producto["nombre"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 135 | `"descriptionHtml": f"<p>{producto['descripcion']}</p>",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 136 | `"productType": producto["categoria"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 137 | `"vendor": "TechStore",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 138 | `"status": "ACTIVE",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 139 | `"tags": [producto["categoria"], "carrito-evento"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 140 | `"media": [{` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 141 | `"alt": producto["nombre"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 142 | `"mediaContentType": "IMAGE",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 143 | `"originalSource": producto["imagen"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 144 | `}],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 145 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 146 | `respuesta = graphql_query(PRODUCT_CREATE, {"input": entrada})["productCreate"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 147 | `if respuesta["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 148 | `raise RuntimeError(f"Error creando {producto['sku']}: {respuesta['userErrors']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 149 | `` | Línea en blanco: separa bloques lógicos. |
| 150 | `producto_id = respuesta["product"]["id"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 151 | `variante = {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 152 | `"price": str(producto["precio"]),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 153 | `"inventoryItem": {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 154 | `"sku": producto["sku"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 155 | `"tracked": True,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 156 | `"requiresShipping": True,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 157 | `},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 158 | `"inventoryPolicy": "CONTINUE",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 159 | `"inventoryQuantities": [{` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 160 | `"availableQuantity": producto["stock"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 161 | `"locationId": location_id,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 162 | `}],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 163 | `"optionValues": [{` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 164 | `"optionName": "Title",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 165 | `"name": producto["nombre"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 166 | `}],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 167 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 168 | `respuesta_variante = graphql_query(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 169 | `VARIANT_CREATE, {"productId": producto_id, "variants": [variante]}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 170 | `)["productVariantsBulkCreate"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 171 | `if respuesta_variante["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 172 | `raise RuntimeError(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 173 | `f"Error creando variante de {producto['sku']}: "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 174 | `f"{respuesta_variante['userErrors']}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 175 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 176 | `return respuesta["product"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 177 | `` | Línea en blanco: separa bloques lógicos. |
| 178 | `` | Línea en blanco: separa bloques lógicos. |
| 179 | `def sincronizar_producto(producto, nodo):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 180 | `"""Ajusta precio e imagen de un producto que ya existe en Shopify."""` | Docstring: describe el propósito del bloque. |
| 181 | `cambios = []` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 182 | `variante = next(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 183 | `(v for v in nodo["variants"]["nodes"] if v["sku"] == producto["sku"]), None` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 184 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 185 | `if variante and variante["price"] != str(producto["precio"]):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 186 | `respuesta = graphql_query(VARIANT_UPDATE, {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 187 | `"productId": nodo["id"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 188 | `"variants": [{"id": variante["id"], "price": str(producto["precio"])}],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 189 | `})["productVariantsBulkUpdate"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 190 | `if respuesta["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 191 | `raise RuntimeError(f"Error actualizando precio: {respuesta['userErrors']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 192 | `cambios.append("precio")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 193 | `` | Línea en blanco: separa bloques lógicos. |
| 194 | `if not nodo["media"]["nodes"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 195 | `respuesta = graphql_query(MEDIA_CREATE, {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 196 | `"productId": nodo["id"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 197 | `"media": [{` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 198 | `"alt": producto["nombre"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 199 | `"mediaContentType": "IMAGE",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 200 | `"originalSource": producto["imagen"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 201 | `}],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 202 | `})["productCreateMedia"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 203 | `if respuesta["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 204 | `raise RuntimeError(f"Error agregando imagen: {respuesta['userErrors']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 205 | `cambios.append("imagen")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 206 | `` | Línea en blanco: separa bloques lógicos. |
| 207 | `return cambios` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 208 | `` | Línea en blanco: separa bloques lógicos. |
| 209 | `` | Línea en blanco: separa bloques lógicos. |
| 210 | `def handle_de(texto):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 211 | `"""Convierte un texto a handle Shopify (minúsculas, sin tildes)."""` | Docstring: describe el propósito del bloque. |
| 212 | `sin_tildes = unicodedata.normalize("NFKD", texto)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 213 | `return "".join(c for c in sin_tildes if not unicodedata.combining(c)).lower()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 214 | `` | Línea en blanco: separa bloques lógicos. |
| 215 | `` | Línea en blanco: separa bloques lógicos. |
| 216 | `def crear_colecciones(catalogo, productos_por_sku):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 217 | `"""Crea una colección por cada categoría y agrega sus productos."""` | Docstring: describe el propósito del bloque. |
| 218 | `categorias = {}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 219 | `for producto in catalogo["productos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 220 | `categoria = producto["categoria"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 221 | `categorias.setdefault(categoria, []).append(productos_por_sku[producto["sku"]])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 222 | `` | Línea en blanco: separa bloques lógicos. |
| 223 | `existentes = graphql_query(COLECCIONES_QUERY)["collections"]["nodes"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 224 | `por_handle = {nodo["handle"]: nodo for nodo in existentes}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 225 | `` | Línea en blanco: separa bloques lógicos. |
| 226 | `for categoria, ids in categorias.items():` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 227 | `handle = handle_de(categoria)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 228 | `nodo = por_handle.get(handle)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 229 | `if nodo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 230 | `coleccion_id = nodo["id"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 231 | `ya_agregados = {p["id"] for p in nodo["products"]["nodes"]}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 232 | `por_agregar = [i for i in ids if i not in ya_agregados]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 233 | `if not por_agregar:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 234 | `print(f"  Colección '{categoria}' ya estaba completa")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 235 | `continue` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 236 | `else:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 237 | `respuesta = graphql_query(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 238 | `COLLECTION_CREATE,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 239 | `{"input": {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 240 | `"title": categoria,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 241 | `"handle": handle,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 242 | `"descriptionHtml": f"<p>Productos de la categoría {categoria}.</p>",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 243 | `}},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 244 | `)["collectionCreate"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 245 | `if respuesta["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 246 | `print(f"  Colección {categoria}: {respuesta['userErrors']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 247 | `continue` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 248 | `coleccion_id = respuesta["collection"]["id"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 249 | `por_agregar = ids` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 250 | `` | Línea en blanco: separa bloques lógicos. |
| 251 | `resultado = graphql_query(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 252 | `COLLECTION_ADD, {"id": coleccion_id, "productIds": por_agregar}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 253 | `)["collectionAddProducts"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 254 | `if resultado["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 255 | `print(f"  Error agregando productos a {categoria}: {resultado['userErrors']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 256 | `else:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 257 | `print(f"  Colección '{categoria}' con {len(por_agregar)} productos agregados")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 258 | `` | Línea en blanco: separa bloques lógicos. |
| 259 | `` | Línea en blanco: separa bloques lógicos. |
| 260 | `def main():` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 261 | `"""Punto de entrada con modo dry-run."""` | Docstring: describe el propósito del bloque. |
| 262 | `parser = argparse.ArgumentParser(description=__doc__)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 263 | `parser.add_argument("--dry-run", action="store_true", help="no escribe en Shopify")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 264 | `args = parser.parse_args()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 265 | `` | Línea en blanco: separa bloques lógicos. |
| 266 | `catalogo = cargar_catalogo()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 267 | `existentes, nodos = skus_existentes()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 268 | `print(f"SKUs existentes en la tienda: {len(existentes)}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 269 | `` | Línea en blanco: separa bloques lógicos. |
| 270 | `nodos_por_sku = {}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 271 | `for nodo in nodos:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 272 | `for variante in nodo["variants"]["nodes"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 273 | `if variante["sku"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 274 | `nodos_por_sku[variante["sku"]] = nodo` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 275 | `` | Línea en blanco: separa bloques lógicos. |
| 276 | `pendientes = [` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 277 | `p for p in catalogo["productos"] if p["sku"] not in existentes` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 278 | `]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 279 | `print(f"Productos a crear: {len(pendientes)}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 280 | `` | Línea en blanco: separa bloques lógicos. |
| 281 | `if args.dry_run:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 282 | `for producto in pendientes:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 283 | `print(f"  [DRY RUN] Crear {producto['sku']} - {producto['nombre']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 284 | `for producto in catalogo["productos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 285 | `nodo = nodos_por_sku.get(producto["sku"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 286 | `if nodo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 287 | `sin_precio = any(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 288 | `v["sku"] == producto["sku"] and v["price"] != str(producto["precio"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 289 | `for v in nodo["variants"]["nodes"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 290 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 291 | `if sin_precio or not nodo["media"]["nodes"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 292 | `print(f"  [DRY RUN] Sincronizar {producto['sku']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 293 | `return 0` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 294 | `` | Línea en blanco: separa bloques lógicos. |
| 295 | `location_id = location_principal() if pendientes else None` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 296 | `ids_por_sku = {sku: nodo["id"] for sku, nodo in nodos_por_sku.items()}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 297 | `` | Línea en blanco: separa bloques lógicos. |
| 298 | `for producto in pendientes:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 299 | `creado = crear_producto(producto, location_id)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 300 | `ids_por_sku[producto["sku"]] = creado["id"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 301 | `print(f"  Creado {producto['sku']} -> {creado['handle']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 302 | `` | Línea en blanco: separa bloques lógicos. |
| 303 | `for producto in catalogo["productos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 304 | `nodo = nodos_por_sku.get(producto["sku"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 305 | `if nodo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 306 | `cambios = sincronizar_producto(producto, nodo)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 307 | `if cambios:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 308 | `print(f"  Actualizado {producto['sku']}: {', '.join(cambios)}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 309 | `` | Línea en blanco: separa bloques lógicos. |
| 310 | `crear_colecciones(catalogo, ids_por_sku)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 311 | `return 0` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 312 | `` | Línea en blanco: separa bloques lógicos. |
| 313 | `` | Línea en blanco: separa bloques lógicos. |
| 314 | `if __name__ == "__main__":` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 315 | `raise SystemExit(main())` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

