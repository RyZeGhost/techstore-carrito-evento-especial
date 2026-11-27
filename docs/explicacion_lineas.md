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
| 4 | `SHOPIFY_SHOP=games4you-k5xbi4h0.myshopify.com` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 5 | `SHOPIFY_CLIENT_ID=...` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 6 | `SHOPIFY_CLIENT_SECRET=shpss_...` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 7 | `` | Línea en blanco: separa bloques lógicos. |
| 8 | `Incluye backoff exponencial ante límites de tasa (HTTP 429 y errores` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 9 | `THROTTLED de GraphQL), según las buenas prácticas del enunciado.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 10 | `"""` | Docstring: describe el propósito del bloque. |
| 11 | `` | Línea en blanco: separa bloques lógicos. |
| 12 | `import logging` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 13 | `import os` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 14 | `import re` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 15 | `import time` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 16 | `from pathlib import Path` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 17 | `` | Línea en blanco: separa bloques lógicos. |
| 18 | `import requests` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 19 | `from dotenv import load_dotenv` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 20 | `` | Línea en blanco: separa bloques lógicos. |
| 21 | `load_dotenv()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 22 | `` | Línea en blanco: separa bloques lógicos. |
| 23 | `# Registro de respuestas fallidas, exigido por el enunciado del agente.` | Registro de respuestas fallidas, exigido por el enunciado del agente. |
| 24 | `# Se guarda fuera del repo (carpeta ignorada por .gitignore) para no subir datos.` | Se guarda fuera del repo (carpeta ignorada por .gitignore) para no subir datos. |
| 25 | `LOG_DIR = Path(__file__).resolve().parent / "logs"` | Se guarda fuera del repo (carpeta ignorada por .gitignore) para no subir datos. |
| 26 | `LOG_DIR.mkdir(exist_ok=True)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 27 | `LOGGER = logging.getLogger("shopify")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 28 | `LOGGER.setLevel(logging.ERROR)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 29 | `if not LOGGER.handlers:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 30 | `_handler = logging.FileHandler(LOG_DIR / "shopify_errores.log", encoding="utf-8")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 31 | `_handler.setFormatter(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 32 | `logging.Formatter("%(asctime)s \| %(levelname)s \| %(message)s")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 33 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 34 | `LOGGER.addHandler(_handler)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 35 | `` | Línea en blanco: separa bloques lógicos. |
| 36 | `SHOP = os.getenv("SHOPIFY_SHOP", "").strip()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 37 | `CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID", "").strip()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 38 | `CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET", "").strip()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 39 | `API_VERSION = "2026-01"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 40 | `INTENTOS = 5` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 41 | `` | Línea en blanco: separa bloques lógicos. |
| 42 | `_TOKEN = None` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 43 | `` | Línea en blanco: separa bloques lógicos. |
| 44 | `` | Línea en blanco: separa bloques lógicos. |
| 45 | `def normalizar_shop(shop: str) -> str:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 46 | `"""Acepta 'games4you-k5xbi4h0', 'games4you-k5xbi4h0.myshopify.com' o la URL completa con /admin."""` | Docstring: describe el propósito del bloque. |
| 47 | `shop = shop.strip().replace("https://", "").replace("http://", "").rstrip("/")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 48 | `if shop.endswith("/admin"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 49 | `shop = shop[: -len("/admin")]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 50 | `if "." not in shop:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 51 | `shop += ".myshopify.com"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 52 | `return shop` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 53 | `` | Línea en blanco: separa bloques lógicos. |
| 54 | `` | Línea en blanco: separa bloques lógicos. |
| 55 | `def resumen_error(respuesta: requests.Response) -> str:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 56 | `"""Extrae el mensaje útil de una respuesta de error (JSON o HTML)."""` | Docstring: describe el propósito del bloque. |
| 57 | `try:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 58 | `return str(respuesta.json())[:300]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 59 | `except ValueError:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 60 | `titulo = re.search(r"<title>(.*?)</title>", respuesta.text, re.DOTALL)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 61 | `if titulo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 62 | `return titulo.group(1).strip()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 63 | `return respuesta.text[:300]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 64 | `` | Línea en blanco: separa bloques lógicos. |
| 65 | `` | Línea en blanco: separa bloques lógicos. |
| 66 | `def validar_configuracion() -> None:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 67 | `"""Verifica que existan las tres credenciales antes de llamar a la API."""` | Docstring: describe el propósito del bloque. |
| 68 | `faltantes = [` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 69 | `nombre` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 70 | `for nombre, valor in (` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 71 | `("SHOPIFY_SHOP", SHOP),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 72 | `("SHOPIFY_CLIENT_ID", CLIENT_ID),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 73 | `("SHOPIFY_CLIENT_SECRET", CLIENT_SECRET),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 74 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 75 | `if not valor` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 76 | `]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 77 | `if faltantes:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 78 | `raise RuntimeError("Faltan variables en .env: " + ", ".join(faltantes))` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 79 | `` | Línea en blanco: separa bloques lógicos. |
| 80 | `` | Línea en blanco: separa bloques lógicos. |
| 81 | `def peticion_con_reintento(constructor, descripcion: str) -> requests.Response:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 82 | `"""Ejecuta una petición con espera exponencial si Shopify limita la tasa."""` | Docstring: describe el propósito del bloque. |
| 83 | `for intento in range(1, INTENTOS + 1):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 84 | `try:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 85 | `respuesta = constructor()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 86 | `except requests.RequestException as error:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 87 | `LOGGER.error("Error de red en %s (intento %s): %s", descripcion, intento, error)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 88 | `if intento == INTENTOS:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 89 | `raise RuntimeError(f"{descripcion}: {error}") from error` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 90 | `espera = 2 ** (intento - 1)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 91 | `print(f"  {descripcion}: error de red; reintentando en {espera}s...")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 92 | `time.sleep(espera)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 93 | `continue` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 94 | `` | Línea en blanco: separa bloques lógicos. |
| 95 | `if respuesta.status_code == 429:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 96 | `LOGGER.error("HTTP 429 en %s (intento %s)", descripcion, intento)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 97 | `if respuesta.status_code == 429 and intento < INTENTOS:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 98 | `espera = 2 ** (intento - 1)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 99 | `print(f"  Límite de tasa alcanzado ({descripcion}); reintentando en {espera}s...")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 100 | `time.sleep(espera)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 101 | `continue` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 102 | `return respuesta` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 103 | `raise RuntimeError(f"No se pudo completar: {descripcion}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 104 | `` | Línea en blanco: separa bloques lógicos. |
| 105 | `` | Línea en blanco: separa bloques lógicos. |
| 106 | `def rest_request(metodo: str, ruta: str, datos: dict \| None = None) -> dict:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 107 | `"""Llama a la REST Admin API (necesaria para assets de tema)."""` | Docstring: describe el propósito del bloque. |
| 108 | `url = f"https://{normalizar_shop(SHOP)}/admin/api/{API_VERSION}/{ruta.lstrip('/')}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 109 | `respuesta = peticion_con_reintento(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 110 | `lambda: requests.request(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 111 | `metodo,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 112 | `url,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 113 | `json=datos,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 114 | `headers={` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 115 | `"X-Shopify-Access-Token": get_shopify_token(),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 116 | `"Content-Type": "application/json",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 117 | `},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 118 | `timeout=30,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 119 | `),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 120 | `f"REST {metodo} {ruta}",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 121 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 122 | `if respuesta.status_code >= 400:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 123 | `mensaje = (` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 124 | `f"Error {respuesta.status_code} en REST {ruta}: {resumen_error(respuesta)}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 125 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 126 | `LOGGER.error(mensaje)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 127 | `raise RuntimeError(mensaje)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 128 | `return respuesta.json() if respuesta.content else {}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 129 | `` | Línea en blanco: separa bloques lógicos. |
| 130 | `` | Línea en blanco: separa bloques lógicos. |
| 131 | `def get_shopify_token() -> str:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 132 | `"""Obtiene (y reutiliza) un access token mediante client_credentials."""` | Docstring: describe el propósito del bloque. |
| 133 | `global _TOKEN` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 134 | `if _TOKEN:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 135 | `return _TOKEN` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 136 | `` | Línea en blanco: separa bloques lógicos. |
| 137 | `validar_configuracion()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 138 | `url = f"https://{normalizar_shop(SHOP)}/admin/oauth/access_token"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 139 | `respuesta = peticion_con_reintento(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 140 | `lambda: requests.post(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 141 | `url,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 142 | `data={` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 143 | `"grant_type": "client_credentials",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 144 | `"client_id": CLIENT_ID,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 145 | `"client_secret": CLIENT_SECRET,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 146 | `},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 147 | `timeout=30,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 148 | `),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 149 | `"solicitud de token",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 150 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 151 | `if respuesta.status_code != 200:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 152 | `mensaje = (` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 153 | `f"Error {respuesta.status_code} al pedir el token: "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 154 | `f"{resumen_error(respuesta)}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 155 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 156 | `LOGGER.error(mensaje)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 157 | `raise RuntimeError(mensaje)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 158 | `datos = respuesta.json()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 159 | `if "access_token" not in datos:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 160 | `mensaje = f"Shopify no devolvió access_token: {datos}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 161 | `LOGGER.error(mensaje)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 162 | `raise RuntimeError(mensaje)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 163 | `` | Línea en blanco: separa bloques lógicos. |
| 164 | `_TOKEN = datos["access_token"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 165 | `return _TOKEN` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 166 | `` | Línea en blanco: separa bloques lógicos. |
| 167 | `` | Línea en blanco: separa bloques lógicos. |
| 168 | `def graphql_query(query: str, variables: dict \| None = None) -> dict:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 169 | `"""Ejecuta una consulta GraphQL y devuelve el bloque 'data'."""` | Docstring: describe el propósito del bloque. |
| 170 | `url = f"https://{normalizar_shop(SHOP)}/admin/api/{API_VERSION}/graphql.json"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 171 | `` | Línea en blanco: separa bloques lógicos. |
| 172 | `for intento in range(1, INTENTOS + 1):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 173 | `respuesta = peticion_con_reintento(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 174 | `lambda: requests.post(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 175 | `url,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 176 | `json={"query": query, "variables": variables or {}},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 177 | `headers={` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 178 | `"X-Shopify-Access-Token": get_shopify_token(),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 179 | `"Content-Type": "application/json",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 180 | `},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 181 | `timeout=30,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 182 | `),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 183 | `"consulta GraphQL",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 184 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 185 | `if respuesta.status_code != 200:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 186 | `mensaje = (` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 187 | `f"Error {respuesta.status_code} en GraphQL: {resumen_error(respuesta)}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 188 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 189 | `LOGGER.error(mensaje)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 190 | `raise RuntimeError(mensaje)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 191 | `resultado = respuesta.json()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 192 | `errores = resultado.get("errors") or []` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 193 | `` | Línea en blanco: separa bloques lógicos. |
| 194 | `es_throttled = any(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 195 | `error.get("extensions", {}).get("code") == "THROTTLED"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 196 | `for error in errores` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 197 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 198 | `if es_throttled and intento < INTENTOS:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 199 | `espera = 2 ** (intento - 1)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 200 | `print(f"  GraphQL limitó la tasa; reintentando en {espera}s...")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 201 | `time.sleep(espera)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 202 | `continue` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 203 | `if errores:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 204 | `LOGGER.error("Errores de GraphQL: %s", errores)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 205 | `raise RuntimeError(f"Errores de GraphQL: {errores}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 206 | `return resultado.get("data", {})` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 207 | `` | Línea en blanco: separa bloques lógicos. |
| 208 | `raise RuntimeError("La consulta GraphQL agotó los reintentos por límite de tasa")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 209 | `` | Línea en blanco: separa bloques lógicos. |
| 210 | `` | Línea en blanco: separa bloques lógicos. |
| 211 | `if __name__ == "__main__":` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 212 | `try:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 213 | `datos = graphql_query("{ shop { name myshopifyDomain } }")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 214 | `tienda = datos["shop"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 215 | `print(f"Conectado a: {tienda['name']} ({tienda['myshopifyDomain']})")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 216 | `except (RuntimeError, requests.RequestException, KeyError) as error:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 217 | `print(f"Error de conexión: {error}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

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
| 23 | `for clave in ("moneda", "envio", "recomendaciones", "sustitutos", "productos", "eventos"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 24 | `if clave not in catalogo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 25 | `raise ValueError(f"Falta la clave obligatoria '{clave}' en el catálogo")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 26 | `` | Línea en blanco: separa bloques lógicos. |
| 27 | `envio = catalogo["envio"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 28 | `for clave in ("costo", "gratis_desde"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 29 | `if not isinstance(envio.get(clave), int) or envio[clave] < 0:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 30 | `raise ValueError(f"envio.{clave} debe ser un entero no negativo")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 31 | `` | Línea en blanco: separa bloques lógicos. |
| 32 | `recomendaciones = catalogo["recomendaciones"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 33 | `for clave in ("por_categoria", "maximo", "descuento_porcentaje"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 34 | `valor = recomendaciones.get(clave)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 35 | `if not isinstance(valor, int) or valor < 0:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 36 | `raise ValueError(f"recomendaciones.{clave} debe ser un entero no negativo")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 37 | `if not isinstance(recomendaciones.get("eventos_festivos"), list):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 38 | `raise ValueError("recomendaciones.eventos_festivos debe ser una lista")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 39 | `` | Línea en blanco: separa bloques lógicos. |
| 40 | `if not isinstance(catalogo["productos"], list) or not catalogo["productos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 41 | `raise ValueError("productos debe ser una lista no vacía")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 42 | `` | Línea en blanco: separa bloques lógicos. |
| 43 | `skus = set()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 44 | `for producto in catalogo["productos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 45 | `for clave in ("sku", "nombre", "precio", "stock", "categoria",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 46 | `"descripcion", "imagen"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 47 | `if clave not in producto:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 48 | `raise ValueError(f"Falta '{clave}' en el producto {producto.get('sku')}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 49 | `if producto["sku"] in skus:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 50 | `raise ValueError(f"SKU duplicado: {producto['sku']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 51 | `skus.add(producto["sku"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 52 | `if not isinstance(producto["precio"], int) or producto["precio"] <= 0:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 53 | `raise ValueError(f"precio inválido en {producto['sku']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 54 | `if not isinstance(producto["stock"], int) or producto["stock"] < 0:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 55 | `raise ValueError(f"stock inválido en {producto['sku']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 56 | `if not str(producto["imagen"]).startswith("https://"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 57 | `raise ValueError(f"imagen inválida en {producto['sku']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 58 | `` | Línea en blanco: separa bloques lógicos. |
| 59 | `for sku, sustituto in catalogo["sustitutos"].items():` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 60 | `if sku not in skus or sustituto not in skus:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 61 | `raise ValueError(f"Sustituto inválido: {sku} -> {sustituto}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 62 | `` | Línea en blanco: separa bloques lógicos. |
| 63 | `if not isinstance(catalogo["eventos"], dict) or not catalogo["eventos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 64 | `raise ValueError("eventos debe ser un objeto no vacío")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 65 | `` | Línea en blanco: separa bloques lógicos. |
| 66 | `for nombre in recomendaciones["eventos_festivos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 67 | `if nombre not in catalogo["eventos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 68 | `raise ValueError(f"Evento festivo inexistente: {nombre}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 69 | `` | Línea en blanco: separa bloques lógicos. |
| 70 | `for nombre, evento in catalogo["eventos"].items():` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 71 | `for clave in ("nombre", "cupon", "producto_2x1", "reglas"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 72 | `if clave not in evento:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 73 | `raise ValueError(f"Falta '{clave}' en el evento {nombre}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 74 | `if evento["producto_2x1"] not in skus:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 75 | `raise ValueError(f"producto_2x1 inexistente en el evento {nombre}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 76 | `for regla in evento["reglas"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 77 | `if regla["sku"] not in skus:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 78 | `raise ValueError(f"SKU de regla inexistente: {regla['sku']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 79 | `if regla["por_persona"] < 0 or regla["minimo"] < 0:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 80 | `raise ValueError(f"Cantidades negativas en el evento {nombre}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 81 | `` | Línea en blanco: separa bloques lógicos. |
| 82 | `return True` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 83 | `` | Línea en blanco: separa bloques lógicos. |
| 84 | `` | Línea en blanco: separa bloques lógicos. |
| 85 | `def cargar_catalogo(ruta=RUTA_CATALOGO):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 86 | `"""Lee el JSON, valida su esquema y devuelve el diccionario del catálogo."""` | Docstring: describe el propósito del bloque. |
| 87 | `with open(ruta, "r", encoding="utf-8") as archivo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 88 | `catalogo = json.load(archivo)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 89 | `validar_catalogo(catalogo)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 90 | `return catalogo` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 91 | `` | Línea en blanco: separa bloques lógicos. |
| 92 | `` | Línea en blanco: separa bloques lógicos. |
| 93 | `def indice_productos(catalogo):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 94 | `"""Construye un índice {sku: producto} para búsquedas O(1)."""` | Docstring: describe el propósito del bloque. |
| 95 | `return {producto["sku"]: producto for producto in catalogo["productos"]}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

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
| 12 | `from carrito.recomendaciones import sugerir` | Regla transversal de sugerencias. |
| 13 | `` | Línea en blanco: separa bloques lógicos. |
| 14 | `` | Línea en blanco: separa bloques lógicos. |
| 15 | `def armar_carrito(evento, personas, catalogo, cupon=None):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 16 | `"""Devuelve el carrito armado como diccionario (misma forma en los 3 paradigmas)."""` | Docstring: describe el propósito del bloque. |
| 17 | `` | Línea en blanco: separa bloques lógicos. |
| 18 | `# Validación temprana: evita trabajar con entradas sin sentido.` | Validación temprana: evita trabajar con entradas sin sentido. |
| 19 | `if personas <= 0:` | Una persona o menos no define un evento. |
| 20 | `raise ValueError("personas debe ser mayor que cero")` | Error explícito. |
| 21 | `` | Línea en blanco: separa bloques lógicos. |
| 22 | `if evento not in catalogo["eventos"]:` | El evento debe existir en el JSON. |
| 23 | `raise ValueError(f"Evento desconocido: {evento}")` | Mensaje útil. |
| 24 | `` | Línea en blanco: separa bloques lógicos. |
| 25 | `productos = indice_productos(catalogo)` | {sku: producto}, acceso O(1). |
| 26 | `config = catalogo["eventos"][evento]` | Reglas propias del evento elegido. |
| 27 | `items = []` | Acumulador mutable de líneas del carrito. |
| 28 | `faltantes = []` | Acumulador mutable de productos sin stock suficiente. |
| 29 | `` | Línea en blanco: separa bloques lógicos. |
| 30 | `# --- Paso 1: calcular cantidades y resolver stock ---` | --- Paso 1: calcular cantidades y resolver stock --- |
| 31 | `for regla in config["reglas"]:` | Recorre las reglas en orden estable. |
| 32 | `sku = regla["sku"]` | SKU del producto sugerido por la regla. |
| 33 | `producto = productos[sku]` | Datos del producto (precio, stock, nombre). |
| 34 | `` | Línea en blanco: separa bloques lógicos. |
| 35 | `# ceil() porque no se pueden vender fracciones; max() aplica el mínimo.` | ceil() porque no se pueden vender fracciones; max() aplica el mínimo. |
| 36 | `cantidad = max(regla["minimo"], math.ceil(personas * regla["por_persona"]))` | ceil() porque no se pueden vender fracciones; max() aplica el mínimo. |
| 37 | `` | Línea en blanco: separa bloques lógicos. |
| 38 | `if cantidad > producto["stock"]:` | No hay stock suficiente. |
| 39 | `sku_sustituto = catalogo["sustitutos"].get(sku)` | Busca alternativa. |
| 40 | `sustituto = productos.get(sku_sustituto)` | Puede no existir. |
| 41 | `` | Línea en blanco: separa bloques lógicos. |
| 42 | `if sustituto and sustituto["stock"] >= cantidad:` | El sustituto alcanza. |
| 43 | `# Se agrega el sustituto, dejando registro del producto original.` | Se agrega el sustituto, dejando registro del producto original. |
| 44 | `items.append({` | Se agrega el sustituto, dejando registro del producto original. |
| 45 | `"sku": sustituto["sku"],` | SKU que finalmente se vende. |
| 46 | `"nombre": sustituto["nombre"],` | Nombre del sustituto. |
| 47 | `"cantidad": cantidad,` | Cantidad calculada originalmente. |
| 48 | `"precio_unitario": sustituto["precio"],` | Precio del sustituto. |
| 49 | `"subtotal": cantidad * sustituto["precio"],` | Línea * precio. |
| 50 | `"sustituto_de": sku,` | Trazabilidad del cambio. |
| 51 | `})` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 52 | `continue` | Ya resolvimos esta regla; pasamos a la siguiente. |
| 53 | `` | Línea en blanco: separa bloques lógicos. |
| 54 | `disponible = producto["stock"]` | Stock real que sí se puede vender. |
| 55 | `if disponible > 0:` | Solo agregamos la línea si hay algo disponible. |
| 56 | `items.append({` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 57 | `"sku": sku,` | SKU original. |
| 58 | `"nombre": producto["nombre"],` | Nombre original. |
| 59 | `"cantidad": disponible,` | Se limita al stock disponible. |
| 60 | `"precio_unitario": producto["precio"],` | Precio original. |
| 61 | `"subtotal": disponible * producto["precio"],` | Subtotal de la línea. |
| 62 | `"sustituto_de": None,` | No hubo sustitución. |
| 63 | `})` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 64 | `` | Línea en blanco: separa bloques lógicos. |
| 65 | `falta = cantidad - disponible` | Diferencia no cubierta. |
| 66 | `if falta > 0:` | Solo se registra si realmente falta stock. |
| 67 | `faltantes.append({"sku": sku, "cantidad": falta})` | Reporte. |
| 68 | `else:` | Hay stock suficiente. |
| 69 | `items.append({` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 70 | `"sku": sku,` | SKU original. |
| 71 | `"nombre": producto["nombre"],` | Nombre original. |
| 72 | `"cantidad": cantidad,` | Cantidad calculada. |
| 73 | `"precio_unitario": producto["precio"],` | Precio original. |
| 74 | `"subtotal": cantidad * producto["precio"],` | Subtotal de la línea. |
| 75 | `"sustituto_de": None,` | Sin sustitución. |
| 76 | `})` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 77 | `` | Línea en blanco: separa bloques lógicos. |
| 78 | `# --- Paso 2: aplicar promoción 2x1 ---` | --- Paso 2: aplicar promoción 2x1 --- |
| 79 | `descuento_2x1 = 0` | Acumulador del descuento. |
| 80 | `sku_promo = config["producto_2x1"]` | Producto con 2x1 en este evento. |
| 81 | `for item in items:` | Revisa cada línea ya construida. |
| 82 | `# Se considera también el sustituto para no perder la promoción.` | Se considera también el sustituto para no perder la promoción. |
| 83 | `if item["sku"] == sku_promo or item["sustituto_de"] == sku_promo:` | Se considera también el sustituto para no perder la promoción. |
| 84 | `pares = item["cantidad"] // 2` | Cada par equivale a una unidad gratis. |
| 85 | `descuento_2x1 += pares * item["precio_unitario"]` | Acumula el descuento. |
| 86 | `` | Línea en blanco: separa bloques lógicos. |
| 87 | `# --- Paso 3: subtotal, cupón y envío ---` | --- Paso 3: subtotal, cupón y envío --- |
| 88 | `subtotal = 0` | Acumulador del subtotal sin descuentos. |
| 89 | `for item in items:` | Recorre las líneas. |
| 90 | `subtotal += item["subtotal"]` | Suma el subtotal de cada línea. |
| 91 | `` | Línea en blanco: separa bloques lógicos. |
| 92 | `base = subtotal - descuento_2x1` | Subtotal después del 2x1. |
| 93 | `descuento_cupon = 0` | Valor por defecto: sin cupón. |
| 94 | `if cupon == config["cupon"]:` | Solo si el cupón coincide con el del evento. |
| 95 | `descuento_cupon = base * 10 // 100` | 10% redondeado hacia abajo (enteros). |
| 96 | `` | Línea en blanco: separa bloques lógicos. |
| 97 | `envio = catalogo["envio"]` | Configuración de envío del JSON. |
| 98 | `if base - descuento_cupon >= envio["gratis_desde"]:` | Supera el umbral. |
| 99 | `costo_envio = 0` | Envío gratis. |
| 100 | `else:` | No supera el umbral. |
| 101 | `costo_envio = envio["costo"]` | Se cobra el envío. |
| 102 | `` | Línea en blanco: separa bloques lógicos. |
| 103 | `total = base - descuento_cupon + costo_envio` | Resultado final. |
| 104 | `` | Línea en blanco: separa bloques lógicos. |
| 105 | `# --- Paso 4: sugerencias personalizadas según el carrito y la festividad ---` | --- Paso 4: sugerencias personalizadas según el carrito y la festividad --- |
| 106 | `# Se calculan al final porque dependen de las líneas ya resueltas.` | Se calculan al final porque dependen de las líneas ya resueltas. |
| 107 | `recomendaciones = sugerir(items, catalogo, evento)` | Se calculan al final porque dependen de las líneas ya resueltas. |
| 108 | `` | Línea en blanco: separa bloques lógicos. |
| 109 | `# --- Paso 5: devolver estructura común a los tres paradigmas ---` | --- Paso 5: devolver estructura común a los tres paradigmas --- |
| 110 | `return {` | --- Paso 5: devolver estructura común a los tres paradigmas --- |
| 111 | `"evento": evento,` | Evento solicitado. |
| 112 | `"personas": personas,` | Cantidad de personas solicitada. |
| 113 | `"items": items,` | Líneas del carrito. |
| 114 | `"faltantes": faltantes,` | Productos sin stock. |
| 115 | `"descuentos": {"2x1": descuento_2x1, "cupon": descuento_cupon},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 116 | `"envio": costo_envio,` | Costo de envío aplicado. |
| 117 | `"total": total,` | Total a pagar. |
| 118 | `"recomendaciones": recomendaciones,` | Ofertas similares; no cambian el total. |
| 119 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

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
| 15 | `from carrito.recomendaciones import sugerir` | Regla pura compartida. |
| 16 | `` | Línea en blanco: separa bloques lógicos. |
| 17 | `` | Línea en blanco: separa bloques lógicos. |
| 18 | `# --- Modelo de datos ---` | --- Modelo de datos --- |
| 19 | `` | Línea en blanco: separa bloques lógicos. |
| 20 | `@dataclass(frozen=True)` | frozen=True => objetos inmutables. |
| 21 | `class Producto:` | --- Modelo de datos --- |
| 22 | `"""Representa un producto del catálogo."""` | Docstring: describe el propósito del bloque. |
| 23 | `` | Línea en blanco: separa bloques lógicos. |
| 24 | `sku: str` | Identificador único. |
| 25 | `nombre: str` | Nombre visible. |
| 26 | `precio: int` | Precio en pesos enteros. |
| 27 | `stock: int` | Unidades disponibles. |
| 28 | `` | Línea en blanco: separa bloques lógicos. |
| 29 | `def crear_item(self, cantidad, sustituto_de=None):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 30 | `"""Fábrica de líneas de carrito a partir del producto."""` | Docstring: describe el propósito del bloque. |
| 31 | `return Item(` | Devuelve un objeto Item. |
| 32 | `sku=self.sku,` | SKU del producto vendido. |
| 33 | `nombre=self.nombre,` | Nombre del producto vendido. |
| 34 | `cantidad=cantidad,` | Unidades calculadas. |
| 35 | `precio_unitario=self.precio,` | Precio unitario. |
| 36 | `subtotal=cantidad * self.precio,` | Precio total de la línea. |
| 37 | `sustituto_de=sustituto_de,` | SKU original si hubo sustitución. |
| 38 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 39 | `` | Línea en blanco: separa bloques lógicos. |
| 40 | `` | Línea en blanco: separa bloques lógicos. |
| 41 | `@dataclass(frozen=True)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 42 | `class Item:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 43 | `"""Una línea del carrito; también inmutable."""` | Docstring: describe el propósito del bloque. |
| 44 | `` | Línea en blanco: separa bloques lógicos. |
| 45 | `sku: str` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 46 | `nombre: str` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 47 | `cantidad: int` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 48 | `precio_unitario: int` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 49 | `subtotal: int` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 50 | `sustituto_de: str \| None` | None cuando no hubo sustitución. |
| 51 | `` | Línea en blanco: separa bloques lógicos. |
| 52 | `def como_dict(self):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 53 | `"""Convierte el objeto en diccionario para igualar a los otros paradigmas."""` | Docstring: describe el propósito del bloque. |
| 54 | `return {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 55 | `"sku": self.sku,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 56 | `"nombre": self.nombre,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 57 | `"cantidad": self.cantidad,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 58 | `"precio_unitario": self.precio_unitario,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 59 | `"subtotal": self.subtotal,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 60 | `"sustituto_de": self.sustituto_de,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 61 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 62 | `` | Línea en blanco: separa bloques lógicos. |
| 63 | `` | Línea en blanco: separa bloques lógicos. |
| 64 | `@dataclass(frozen=True)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 65 | `class Regla:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 66 | `"""Regla que define cuántas unidades se sugieren por persona."""` | Docstring: describe el propósito del bloque. |
| 67 | `` | Línea en blanco: separa bloques lógicos. |
| 68 | `sku: str` | Producto al que aplica. |
| 69 | `por_persona: float` | Unidades (o fracción) por persona. |
| 70 | `minimo: int` | Mínimo absoluto de unidades. |
| 71 | `` | Línea en blanco: separa bloques lógicos. |
| 72 | `def cantidad_para(self, personas):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 73 | `"""Calcula la cantidad redondeada hacia arriba, con mínimo."""` | Docstring: describe el propósito del bloque. |
| 74 | `return max(self.minimo, math.ceil(personas * self.por_persona))` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 75 | `` | Línea en blanco: separa bloques lógicos. |
| 76 | `` | Línea en blanco: separa bloques lógicos. |
| 77 | `@dataclass(frozen=True)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 78 | `class Evento:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 79 | `"""Configuración de un evento: reglas, cupón y producto en 2x1."""` | Docstring: describe el propósito del bloque. |
| 80 | `` | Línea en blanco: separa bloques lógicos. |
| 81 | `nombre: str` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 82 | `cupon: str` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 83 | `producto_2x1: str` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 84 | `reglas: tuple` | Tupla de Regla (inmutable). |
| 85 | `` | Línea en blanco: separa bloques lógicos. |
| 86 | `@classmethod` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 87 | `def desde_dict(cls, datos):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 88 | `"""Construye un Evento desde el diccionario del JSON."""` | Docstring: describe el propósito del bloque. |
| 89 | `reglas = tuple(` | Comprensión que crea objetos Regla. |
| 90 | `Regla(r["sku"], r["por_persona"], r["minimo"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 91 | `for r in datos["reglas"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 92 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 93 | `return cls(datos["nombre"], datos["cupon"], datos["producto_2x1"], reglas)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 94 | `` | Línea en blanco: separa bloques lógicos. |
| 95 | `` | Línea en blanco: separa bloques lógicos. |
| 96 | `# --- Estrategias de descuento (herencia y polimorfismo) ---` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 97 | `` | Línea en blanco: separa bloques lógicos. |
| 98 | `class Descuento(ABC):` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 99 | `"""Interfaz común: toda estrategia debe saber calcular un descuento."""` | Docstring: describe el propósito del bloque. |
| 100 | `` | Línea en blanco: separa bloques lógicos. |
| 101 | `@abstractmethod` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 102 | `def calcular(self, items, evento, cupon):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 103 | `"""Devuelve el monto de descuento (entero)."""` | Docstring: describe el propósito del bloque. |
| 104 | `raise NotImplementedError` | Obliga a las subclases a implementarlo. |
| 105 | `` | Línea en blanco: separa bloques lógicos. |
| 106 | `` | Línea en blanco: separa bloques lógicos. |
| 107 | `class Descuento2x1(Descuento):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 108 | `"""Descuento 2x1 sobre el producto configurado en el evento."""` | Docstring: describe el propósito del bloque. |
| 109 | `` | Línea en blanco: separa bloques lógicos. |
| 110 | `def calcular(self, items, evento, cupon):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 111 | `total = 0` | Acumulador local. |
| 112 | `for item in items:` | Polimorfismo: Item expone los mismos atributos. |
| 113 | `es_promo = item.sku == evento.producto_2x1` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 114 | `es_sustituto = item.sustituto_de == evento.producto_2x1` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 115 | `if es_promo or es_sustituto:` | Aplica también al sustituto. |
| 116 | `total += (item.cantidad // 2) * item.precio_unitario` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 117 | `return total` | Cumple el contrato de Descuento. |
| 118 | `` | Línea en blanco: separa bloques lógicos. |
| 119 | `` | Línea en blanco: separa bloques lógicos. |
| 120 | `class DescuentoPorcentaje(Descuento):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 121 | `"""Descuento por cupón: porcentaje sobre la base ya descontada."""` | Docstring: describe el propósito del bloque. |
| 122 | `` | Línea en blanco: separa bloques lógicos. |
| 123 | `def __init__(self, porcentaje):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 124 | `self.porcentaje = porcentaje` | Estado interno encapsulado. |
| 125 | `` | Línea en blanco: separa bloques lógicos. |
| 126 | `def calcular(self, items, evento, cupon, base=0):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 127 | `# Firma extendida con `base`; se usa desde el carrito de forma explícita.` | Firma extendida con `base`; se usa desde el carrito de forma explícita. |
| 128 | `if cupon != evento.cupon:` | Cupón incorrecto o ausente. |
| 129 | `return 0` | Sin descuento. |
| 130 | `return base * self.porcentaje // 100` | Entero, redondeo hacia abajo. |
| 131 | `` | Línea en blanco: separa bloques lógicos. |
| 132 | `` | Línea en blanco: separa bloques lógicos. |
| 133 | `class Recomendador:` | Firma extendida con `base`; se usa desde el carrito de forma explícita. |
| 134 | `"""Encapsula la regla de sugerencias por similitud y festividad."""` | Docstring: describe el propósito del bloque. |
| 135 | `` | Línea en blanco: separa bloques lógicos. |
| 136 | `def __init__(self, catalogo):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 137 | `self.catalogo = catalogo` | Configuración de recomendaciones y productos. |
| 138 | `` | Línea en blanco: separa bloques lógicos. |
| 139 | `def sugerir_para(self, items, evento):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 140 | `"""Devuelve sugerencias para las líneas ya armadas del carrito."""` | Docstring: describe el propósito del bloque. |
| 141 | `return sugerir(items, self.catalogo, evento)` | Delega en la función pura. |
| 142 | `` | Línea en blanco: separa bloques lógicos. |
| 143 | `` | Línea en blanco: separa bloques lógicos. |
| 144 | `class PoliticaEnvio:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 145 | `"""Define cuándo el envío es gratis."""` | Docstring: describe el propósito del bloque. |
| 146 | `` | Línea en blanco: separa bloques lógicos. |
| 147 | `def __init__(self, costo, gratis_desde):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 148 | `self.costo = costo` | Costo normal. |
| 149 | `self.gratis_desde = gratis_desde` | Umbral para envío gratis. |
| 150 | `` | Línea en blanco: separa bloques lógicos. |
| 151 | `def calcular(self, monto):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 152 | `"""Devuelve el costo de envío según el monto después de descuentos."""` | Docstring: describe el propósito del bloque. |
| 153 | `return 0 if monto >= self.gratis_desde else self.costo` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 154 | `` | Línea en blanco: separa bloques lógicos. |
| 155 | `` | Línea en blanco: separa bloques lógicos. |
| 156 | `# --- Orquestación ---` | --- Orquestación --- |
| 157 | `` | Línea en blanco: separa bloques lógicos. |
| 158 | `class Carrito:` | --- Orquestación --- |
| 159 | `"""Coordina productos, reglas y descuentos para armar el carrito."""` | Docstring: describe el propósito del bloque. |
| 160 | `` | Línea en blanco: separa bloques lógicos. |
| 161 | `def __init__(self, evento, personas, catalogo, cupon=None):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 162 | `if personas <= 0:` | Validación de entrada. |
| 163 | `raise ValueError("personas debe ser mayor que cero")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 164 | `if evento not in catalogo["eventos"]:` | Validación de evento. |
| 165 | `raise ValueError(f"Evento desconocido: {evento}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 166 | `` | Línea en blanco: separa bloques lógicos. |
| 167 | `self.evento = Evento.desde_dict(catalogo["eventos"][evento])` | Config. |
| 168 | `self.clave_evento = evento` | Clave exacta del JSON, para las sugerencias. |
| 169 | `self.personas = personas` | Cantidad de personas. |
| 170 | `self.productos = {` | Dict de objetos Producto. |
| 171 | `sku: Producto(p["sku"], p["nombre"], p["precio"], p["stock"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 172 | `for sku, p in indice_productos(catalogo).items()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 173 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 174 | `self.sustitutos = catalogo["sustitutos"]` | Mapa de reemplazos. |
| 175 | `self.cupon = cupon` | Cupón ingresado por el usuario. |
| 176 | `self.envio = PoliticaEnvio(` | Política de envío del catálogo. |
| 177 | `catalogo["envio"]["costo"], catalogo["envio"]["gratis_desde"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 178 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 179 | `self.descuentos = [Descuento2x1()]` | Estrategias polimórficas. |
| 180 | `self.recomendador = Recomendador(catalogo)` | Sugerencias personalizadas. |
| 181 | `` | Línea en blanco: separa bloques lógicos. |
| 182 | `def _resolver_regla(self, regla):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 183 | `"""Aplica una regla; devuelve (item o None, faltante o None)."""` | Docstring: describe el propósito del bloque. |
| 184 | `producto = self.productos[regla.sku]` | Producto sugerido. |
| 185 | `cantidad = regla.cantidad_para(self.personas)` | Cantidad calculada. |
| 186 | `` | Línea en blanco: separa bloques lógicos. |
| 187 | `if cantidad <= producto.stock:` | Caso simple: hay stock. |
| 188 | `return producto.crear_item(cantidad), None` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 189 | `` | Línea en blanco: separa bloques lógicos. |
| 190 | `# Sin stock suficiente: intenta sustituto.` | Sin stock suficiente: intenta sustituto. |
| 191 | `sku_alt = self.sustitutos.get(regla.sku)` | SKU alternativo. |
| 192 | `alternativo = self.productos.get(sku_alt)` | Objeto alternativo. |
| 193 | `if alternativo and alternativo.stock >= cantidad:` | El sustituto alcanza. |
| 194 | `return alternativo.crear_item(cantidad, regla.sku), None` | Sin stock suficiente: intenta sustituto. |
| 195 | `` | Línea en blanco: separa bloques lógicos. |
| 196 | `# No hay sustituto válido: se vende lo disponible y se reporta el falta.` | No hay sustituto válido: se vende lo disponible y se reporta el falta. |
| 197 | `disponible = producto.stock` | No hay sustituto válido: se vende lo disponible y se reporta el falta. |
| 198 | `item = producto.crear_item(disponible) if disponible > 0 else None` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 199 | `faltante = {"sku": regla.sku, "cantidad": cantidad - disponible}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 200 | `return item, faltante` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 201 | `` | Línea en blanco: separa bloques lógicos. |
| 202 | `def armar(self):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 203 | `"""Ejecuta el algoritmo completo y devuelve el diccionario resultado."""` | Docstring: describe el propósito del bloque. |
| 204 | `items = []` | Lista mutable de objetos Item. |
| 205 | `faltantes = []` | Lista mutable de reportes de stock. |
| 206 | `` | Línea en blanco: separa bloques lógicos. |
| 207 | `for regla in self.evento.reglas:` | Iteración sobre reglas del evento. |
| 208 | `item, faltante = self._resolver_regla(regla)` | Delegación. |
| 209 | `if item is not None:` | Puede no haber item si stock = 0. |
| 210 | `items.append(item)` | Acumula el objeto. |
| 211 | `if faltante is not None:` | Puede no haber faltante. |
| 212 | `faltantes.append(faltante)` | Acumula el reporte. |
| 213 | `` | Línea en blanco: separa bloques lógicos. |
| 214 | `subtotal = sum(item.subtotal for item in items)` | Suma de líneas. |
| 215 | `` | Línea en blanco: separa bloques lógicos. |
| 216 | `# Polimorfismo: ambas estrategias responden a `calcular`.` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 217 | `desc_2x1 = self.descuentos[0].calcular(items, self.evento, self.cupon)` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 218 | `desc_cupon = DescuentoPorcentaje(10).calcular(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 219 | `items, self.evento, self.cupon, base=subtotal - desc_2x1` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 220 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 221 | `` | Línea en blanco: separa bloques lógicos. |
| 222 | `base = subtotal - desc_2x1 - desc_cupon` | Monto para evaluar envío. |
| 223 | `costo_envio = self.envio.calcular(base)` | Política de envío. |
| 224 | `total = base + costo_envio` | Total final. |
| 225 | `` | Línea en blanco: separa bloques lógicos. |
| 226 | `# El recomendador es un colaborador más del carrito, como la política de envío.` | El recomendador es un colaborador más del carrito, como la política de envío. |
| 227 | `items_dict = [item.como_dict() for item in items]` | El recomendador es un colaborador más del carrito, como la política de envío. |
| 228 | `recomendaciones = self.recomendador.sugerir_para(items_dict, self.clave_evento)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 229 | `` | Línea en blanco: separa bloques lógicos. |
| 230 | `return {` | Misma estructura que en el paradigma imperativo. |
| 231 | `"evento": self.evento.nombre.lower().replace(" ", "_"),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 232 | `"personas": self.personas,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 233 | `"items": items_dict,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 234 | `"faltantes": faltantes,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 235 | `"descuentos": {"2x1": desc_2x1, "cupon": desc_cupon},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 236 | `"envio": costo_envio,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 237 | `"total": total,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 238 | `"recomendaciones": recomendaciones,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 239 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 240 | `` | Línea en blanco: separa bloques lógicos. |
| 241 | `` | Línea en blanco: separa bloques lógicos. |
| 242 | `def armar_carrito(evento, personas, catalogo, cupon=None):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 243 | `"""API pública equivalente a la de los otros dos módulos."""` | Docstring: describe el propósito del bloque. |
| 244 | `# El evento devuelto por la clase se normaliza al nombre de la clave JSON.` | El evento devuelto por la clase se normaliza al nombre de la clave JSON. |
| 245 | `carrito = Carrito(evento, personas, catalogo, cupon)` | El evento devuelto por la clase se normaliza al nombre de la clave JSON. |
| 246 | `resultado = carrito.armar()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 247 | `resultado["evento"] = evento` | Garantiza igualdad exacta entre versiones. |
| 248 | `return resultado` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

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
| 14 | `from carrito.recomendaciones import sugerir` | Función pura compartida. |
| 15 | `` | Línea en blanco: separa bloques lógicos. |
| 16 | `` | Línea en blanco: separa bloques lógicos. |
| 17 | `def validar(evento, personas, catalogo):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 18 | `"""Función pura de validación: devuelve la configuración del evento."""` | Docstring: describe el propósito del bloque. |
| 19 | `if personas <= 0:` | Condición de error. |
| 20 | `raise ValueError("personas debe ser mayor que cero")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 21 | `if evento not in catalogo["eventos"]:` | El evento debe existir. |
| 22 | `raise ValueError(f"Evento desconocido: {evento}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 23 | `return catalogo["eventos"][evento]` | Devuelve un dict existente (no lo muta). |
| 24 | `` | Línea en blanco: separa bloques lógicos. |
| 25 | `` | Línea en blanco: separa bloques lógicos. |
| 26 | `def cantidad_para(personas, regla):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 27 | `"""Calcula unidades de una regla: techo y mínimo."""` | Docstring: describe el propósito del bloque. |
| 28 | `return max(regla["minimo"], math.ceil(personas * regla["por_persona"]))` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 29 | `` | Línea en blanco: separa bloques lógicos. |
| 30 | `` | Línea en blanco: separa bloques lógicos. |
| 31 | `def crear_item(producto, cantidad, sustituto_de=None):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 32 | `"""Construye un diccionario nuevo para una línea del carrito."""` | Docstring: describe el propósito del bloque. |
| 33 | `return {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 34 | `"sku": producto["sku"],` | SKU vendido. |
| 35 | `"nombre": producto["nombre"],` | Nombre del producto. |
| 36 | `"cantidad": cantidad,` | Unidades. |
| 37 | `"precio_unitario": producto["precio"],` | Precio unitario. |
| 38 | `"subtotal": cantidad * producto["precio"],` | Total de la línea. |
| 39 | `"sustituto_de": sustituto_de,` | SKU original si se sustituyó. |
| 40 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 41 | `` | Línea en blanco: separa bloques lógicos. |
| 42 | `` | Línea en blanco: separa bloques lógicos. |
| 43 | `def resolver(regla, personas, catalogo, productos):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 44 | `"""Devuelve el par (item, faltante); uno de los dos puede ser None."""` | Docstring: describe el propósito del bloque. |
| 45 | `producto = productos[regla["sku"]]` | Producto de la regla. |
| 46 | `cantidad = cantidad_para(personas, regla)` | Cantidad calculada. |
| 47 | `` | Línea en blanco: separa bloques lógicos. |
| 48 | `if cantidad <= producto["stock"]:` | Hay stock. |
| 49 | `return crear_item(producto, cantidad), None` | Par sin faltante. |
| 50 | `` | Línea en blanco: separa bloques lógicos. |
| 51 | `# Sin stock: buscar sustituto con stock suficiente.` | Sin stock: buscar sustituto con stock suficiente. |
| 52 | `sku_alternativo = catalogo["sustitutos"].get(regla["sku"])` | Puede no existir. |
| 53 | `alternativo = productos.get(sku_alternativo)` | Puede no existir. |
| 54 | `` | Línea en blanco: separa bloques lógicos. |
| 55 | `if alternativo and alternativo["stock"] >= cantidad:` | Sustituto válido. |
| 56 | `return crear_item(alternativo, cantidad, regla["sku"]), None` | Sin stock: buscar sustituto con stock suficiente. |
| 57 | `` | Línea en blanco: separa bloques lógicos. |
| 58 | `# Sin sustituto válido: vender lo disponible y reportar la diferencia.` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 59 | `disponible = producto["stock"]` | Stock disponible. |
| 60 | `item = crear_item(producto, disponible) if disponible > 0 else None` | Item opcional. |
| 61 | `faltante = {"sku": regla["sku"], "cantidad": cantidad - disponible}` | Reporte. |
| 62 | `return item, faltante` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 63 | `` | Línea en blanco: separa bloques lógicos. |
| 64 | `` | Línea en blanco: separa bloques lógicos. |
| 65 | `def construir_lineas(config, personas, catalogo, productos):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 66 | `"""Aplica `resolver` a todas las reglas con map y separa resultados."""` | Docstring: describe el propósito del bloque. |
| 67 | `pares = tuple(` | Tupla inmutable de resultados. |
| 68 | `map(` | map aplica resolver a cada regla. |
| 69 | `lambda regla: resolver(regla, personas, catalogo, productos),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 70 | `config["reglas"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 71 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 72 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 73 | `items = tuple(filter(None, map(lambda par: par[0], pares)))` | Solo items. |
| 74 | `faltantes = tuple(filter(None, map(lambda par: par[1], pares)))` | Solo faltantes. |
| 75 | `return items, faltantes` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 76 | `` | Línea en blanco: separa bloques lógicos. |
| 77 | `` | Línea en blanco: separa bloques lógicos. |
| 78 | `def sumar_subtotal(items):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 79 | `"""Reduce los subtotales de las líneas en un entero."""` | Docstring: describe el propósito del bloque. |
| 80 | `return reduce(lambda total, item: total + item["subtotal"], items, 0)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 81 | `` | Línea en blanco: separa bloques lógicos. |
| 82 | `` | Línea en blanco: separa bloques lógicos. |
| 83 | `def descuento_2x1(items, sku_promo):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 84 | `"""Descuento 2x1 usando reduce sobre las líneas promocionadas."""` | Docstring: describe el propósito del bloque. |
| 85 | `promocionados = filter(` | filter conserva solo las líneas que cumplen. |
| 86 | `lambda item: item["sku"] == sku_promo or item["sustituto_de"] == sku_promo,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 87 | `items,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 88 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 89 | `return reduce(` | Acumula pares * precio. |
| 90 | `lambda total, item: total + (item["cantidad"] // 2) * item["precio_unitario"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 91 | `promocionados,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 92 | `0,` | Valor inicial del acumulador. |
| 93 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 94 | `` | Línea en blanco: separa bloques lógicos. |
| 95 | `` | Línea en blanco: separa bloques lógicos. |
| 96 | `def descuento_cupon(cupon, config, base):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 97 | `"""Descuento de 10% solo si el cupón coincide con el del evento."""` | Docstring: describe el propósito del bloque. |
| 98 | `return base * 10 // 100 if cupon == config["cupon"] else 0` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 99 | `` | Línea en blanco: separa bloques lógicos. |
| 100 | `` | Línea en blanco: separa bloques lógicos. |
| 101 | `def costo_envio(catalogo, monto):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 102 | `"""Costo de envío según el umbral configurado."""` | Docstring: describe el propósito del bloque. |
| 103 | `envio = catalogo["envio"]` | Configuración de envío. |
| 104 | `return 0 if monto >= envio["gratis_desde"] else envio["costo"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 105 | `` | Línea en blanco: separa bloques lógicos. |
| 106 | `` | Línea en blanco: separa bloques lógicos. |
| 107 | `def recomendaciones_para(items, catalogo, evento):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 108 | `"""Envuelve la regla compartida como una función pura más de la composición."""` | Docstring: describe el propósito del bloque. |
| 109 | `return sugerir(items, catalogo, evento)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 110 | `` | Línea en blanco: separa bloques lógicos. |
| 111 | `` | Línea en blanco: separa bloques lógicos. |
| 112 | `def armar_carrito(evento, personas, catalogo, cupon=None):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 113 | `"""Compone todas las funciones puras y devuelve el resultado final."""` | Docstring: describe el propósito del bloque. |
| 114 | `config = validar(evento, personas, catalogo)` | 1) Validar entradas. |
| 115 | `productos = indice_productos(catalogo)` | 2) Indexar productos. |
| 116 | `` | Línea en blanco: separa bloques lógicos. |
| 117 | `items, faltantes = construir_lineas(config, personas, catalogo, productos)` | 3) |
| 118 | `` | Línea en blanco: separa bloques lógicos. |
| 119 | `subtotal = sumar_subtotal(items)` | 4) Suma funcional de líneas. |
| 120 | `desc_2x1 = descuento_2x1(items, config["producto_2x1"])` | 5) Promoción. |
| 121 | `desc_cupon = descuento_cupon(cupon, config, subtotal - desc_2x1)` | 6) Cupón. |
| 122 | `` | Línea en blanco: separa bloques lógicos. |
| 123 | `base = subtotal - desc_2x1 - desc_cupon` | 7) Base para envío. |
| 124 | `envio = costo_envio(catalogo, base)` | 8) Envío. |
| 125 | `total = base + envio` | 9) Total. |
| 126 | `sugerencias = recomendaciones_para(list(items), catalogo, evento)` | 10) |
| 127 | `` | Línea en blanco: separa bloques lógicos. |
| 128 | `return {` | 11) Diccionario nuevo; equivalente a los otros paradigmas. |
| 129 | `"evento": evento,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 130 | `"personas": personas,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 131 | `"items": list(items),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 132 | `"faltantes": list(faltantes),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 133 | `"descuentos": {"2x1": desc_2x1, "cupon": desc_cupon},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 134 | `"envio": envio,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 135 | `"total": total,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 136 | `"recomendaciones": sugerencias,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 137 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

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
| 38 | `f"envio=${resultado['envio']}, total=${resultado['total']}, "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 39 | `f"recs={len(resultado['recomendaciones'])}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 40 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 41 | `` | Línea en blanco: separa bloques lógicos. |
| 42 | `` | Línea en blanco: separa bloques lógicos. |
| 43 | `def main():` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 44 | `"""Ejecuta todos los casos y verifica que los tres resultados sean iguales."""` | Docstring: describe el propósito del bloque. |
| 45 | `catalogo = cargar_catalogo()` | Misma fuente de datos para todos. |
| 46 | `todos_iguales = True` | Bandera global del resultado de la comparación. |
| 47 | `` | Línea en blanco: separa bloques lógicos. |
| 48 | `for evento, personas, cupon in CASOS:` | Recorre los escenarios. |
| 49 | `print(f"\n=== {evento} \| {personas} personas \| cupón={cupon} ===")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 50 | `resultados = []` | Resultados de las tres implementaciones. |
| 51 | `` | Línea en blanco: separa bloques lógicos. |
| 52 | `for nombre, funcion in IMPLEMENTACIONES:` | Recorre los paradigmas. |
| 53 | `resultado = funcion(evento, personas, catalogo, cupon)` | Ejecuta. |
| 54 | `resultados.append(resultado)` | Guarda para comparar. |
| 55 | `print(f"  {nombre:<20} {formatear(resultado)}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 56 | `` | Línea en blanco: separa bloques lógicos. |
| 57 | `# Comparación estricta: los tres dict deben ser exactamente iguales.` | Comparación estricta: los tres dict deben ser exactamente iguales. |
| 58 | `iguales = resultados[0] == resultados[1] == resultados[2]` | Comparación estricta: los tres dict deben ser exactamente iguales. |
| 59 | `todos_iguales = todos_iguales and iguales` | Actualiza la bandera. |
| 60 | `print(f"  >>> Paridad: {'OK' if iguales else 'FALLO'}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 61 | `` | Línea en blanco: separa bloques lógicos. |
| 62 | `# Detalle de las sugerencias personalizadas calculadas para el caso.` | Detalle de las sugerencias personalizadas calculadas para el caso. |
| 63 | `for recom in resultados[0]["recomendaciones"]:` | Detalle de las sugerencias personalizadas calculadas para el caso. |
| 64 | `print(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 65 | `f"    Recomendado: {recom['nombre']} ({recom['categoria']}) "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 66 | `f"${recom['precio']} -> ${recom['precio_final']} "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 67 | `f"[{recom['motivo']}]"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 68 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 69 | `` | Línea en blanco: separa bloques lógicos. |
| 70 | `# Detalle del caso de stock agotado para hacer visible la sustitución.` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 71 | `if personas == 200:` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 72 | `for item in resultados[0]["items"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 73 | `if item["sustituto_de"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 74 | `print(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 75 | `f"    Sustituto: {item['sustituto_de']} -> "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 76 | `f"{item['sku']} x{item['cantidad']}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 77 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 78 | `for falta in resultados[0]["faltantes"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 79 | `print(f"    Faltante: {falta['sku']} x{falta['cantidad']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 80 | `` | Línea en blanco: separa bloques lógicos. |
| 81 | `print(f"\nResultado global: {'TODOS LOS CASOS COINCIDEN' if todos_iguales else 'HAY DIFERENCIAS'}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 82 | `return 0 if todos_iguales else 1` | Código de salida para CI. |
| 83 | `` | Línea en blanco: separa bloques lógicos. |
| 84 | `` | Línea en blanco: separa bloques lógicos. |
| 85 | `if __name__ == "__main__":` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 86 | `raise SystemExit(main())` | Permite usar el demo en scripts y tests. |

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
| 140 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 141 | `# La API 2026-01 no acepta `media` dentro de ProductInput: el producto se` | La API 2026-01 no acepta `media` dentro de ProductInput: el producto se |
| 142 | `# crea primero y la imagen se asocia después con productCreateMedia.` | crea primero y la imagen se asocia después con productCreateMedia. |
| 143 | `respuesta = graphql_query(PRODUCT_CREATE, {"input": entrada})["productCreate"]` | crea primero y la imagen se asocia después con productCreateMedia. |
| 144 | `if respuesta["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 145 | `raise RuntimeError(f"Error creando {producto['sku']}: {respuesta['userErrors']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 146 | `` | Línea en blanco: separa bloques lógicos. |
| 147 | `producto_id = respuesta["product"]["id"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 148 | `variante = {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 149 | `"price": str(producto["precio"]),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 150 | `"inventoryItem": {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 151 | `"sku": producto["sku"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 152 | `"tracked": True,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 153 | `"requiresShipping": True,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 154 | `},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 155 | `"inventoryPolicy": "CONTINUE",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 156 | `"inventoryQuantities": [{` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 157 | `"availableQuantity": producto["stock"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 158 | `"locationId": location_id,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 159 | `}],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 160 | `"optionValues": [{` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 161 | `"optionName": "Title",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 162 | `"name": producto["nombre"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 163 | `}],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 164 | `}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 165 | `respuesta_variante = graphql_query(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 166 | `VARIANT_CREATE, {"productId": producto_id, "variants": [variante]}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 167 | `)["productVariantsBulkCreate"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 168 | `if respuesta_variante["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 169 | `raise RuntimeError(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 170 | `f"Error creando variante de {producto['sku']}: "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 171 | `f"{respuesta_variante['userErrors']}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 172 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 173 | `` | Línea en blanco: separa bloques lógicos. |
| 174 | `# La imagen se sube en una mutación independiente (igual que en` | La imagen se sube en una mutación independiente (igual que en |
| 175 | `# `sincronizar_producto`) porque no forma parte de `ProductInput`.` | `sincronizar_producto`) porque no forma parte de `ProductInput`. |
| 176 | `respuesta_media = graphql_query(MEDIA_CREATE, {` | `sincronizar_producto`) porque no forma parte de `ProductInput`. |
| 177 | `"productId": producto_id,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 178 | `"media": [{` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 179 | `"alt": producto["nombre"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 180 | `"mediaContentType": "IMAGE",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 181 | `"originalSource": producto["imagen"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 182 | `}],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 183 | `})["productCreateMedia"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 184 | `if respuesta_media["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 185 | `raise RuntimeError(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 186 | `f"Error agregando imagen a {producto['sku']}: "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 187 | `f"{respuesta_media['userErrors']}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 188 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 189 | `` | Línea en blanco: separa bloques lógicos. |
| 190 | `return respuesta["product"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 191 | `` | Línea en blanco: separa bloques lógicos. |
| 192 | `` | Línea en blanco: separa bloques lógicos. |
| 193 | `def sincronizar_producto(producto, nodo):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 194 | `"""Ajusta precio e imagen de un producto que ya existe en Shopify."""` | Docstring: describe el propósito del bloque. |
| 195 | `cambios = []` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 196 | `variante = next(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 197 | `(v for v in nodo["variants"]["nodes"] if v["sku"] == producto["sku"]), None` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 198 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 199 | `if variante and variante["price"] != str(producto["precio"]):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 200 | `respuesta = graphql_query(VARIANT_UPDATE, {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 201 | `"productId": nodo["id"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 202 | `"variants": [{"id": variante["id"], "price": str(producto["precio"])}],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 203 | `})["productVariantsBulkUpdate"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 204 | `if respuesta["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 205 | `raise RuntimeError(f"Error actualizando precio: {respuesta['userErrors']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 206 | `cambios.append("precio")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 207 | `` | Línea en blanco: separa bloques lógicos. |
| 208 | `if not nodo["media"]["nodes"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 209 | `respuesta = graphql_query(MEDIA_CREATE, {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 210 | `"productId": nodo["id"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 211 | `"media": [{` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 212 | `"alt": producto["nombre"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 213 | `"mediaContentType": "IMAGE",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 214 | `"originalSource": producto["imagen"],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 215 | `}],` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 216 | `})["productCreateMedia"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 217 | `if respuesta["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 218 | `raise RuntimeError(f"Error agregando imagen: {respuesta['userErrors']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 219 | `cambios.append("imagen")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 220 | `` | Línea en blanco: separa bloques lógicos. |
| 221 | `return cambios` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 222 | `` | Línea en blanco: separa bloques lógicos. |
| 223 | `` | Línea en blanco: separa bloques lógicos. |
| 224 | `def handle_de(texto):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 225 | `"""Convierte un texto a handle Shopify (minúsculas, sin tildes)."""` | Docstring: describe el propósito del bloque. |
| 226 | `sin_tildes = unicodedata.normalize("NFKD", texto)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 227 | `return "".join(c for c in sin_tildes if not unicodedata.combining(c)).lower()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 228 | `` | Línea en blanco: separa bloques lógicos. |
| 229 | `` | Línea en blanco: separa bloques lógicos. |
| 230 | `def crear_colecciones(catalogo, productos_por_sku):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 231 | `"""Crea una colección por cada categoría y agrega sus productos."""` | Docstring: describe el propósito del bloque. |
| 232 | `categorias = {}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 233 | `for producto in catalogo["productos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 234 | `categoria = producto["categoria"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 235 | `categorias.setdefault(categoria, []).append(productos_por_sku[producto["sku"]])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 236 | `` | Línea en blanco: separa bloques lógicos. |
| 237 | `existentes = graphql_query(COLECCIONES_QUERY)["collections"]["nodes"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 238 | `por_handle = {nodo["handle"]: nodo for nodo in existentes}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 239 | `` | Línea en blanco: separa bloques lógicos. |
| 240 | `for categoria, ids in categorias.items():` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 241 | `handle = handle_de(categoria)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 242 | `nodo = por_handle.get(handle)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 243 | `if nodo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 244 | `coleccion_id = nodo["id"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 245 | `ya_agregados = {p["id"] for p in nodo["products"]["nodes"]}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 246 | `por_agregar = [i for i in ids if i not in ya_agregados]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 247 | `if not por_agregar:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 248 | `print(f"  Colección '{categoria}' ya estaba completa")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 249 | `continue` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 250 | `else:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 251 | `respuesta = graphql_query(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 252 | `COLLECTION_CREATE,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 253 | `{"input": {` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 254 | `"title": categoria,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 255 | `"handle": handle,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 256 | `"descriptionHtml": f"<p>Productos de la categoría {categoria}.</p>",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 257 | `}},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 258 | `)["collectionCreate"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 259 | `if respuesta["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 260 | `print(f"  Colección {categoria}: {respuesta['userErrors']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 261 | `continue` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 262 | `coleccion_id = respuesta["collection"]["id"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 263 | `por_agregar = ids` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 264 | `` | Línea en blanco: separa bloques lógicos. |
| 265 | `resultado = graphql_query(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 266 | `COLLECTION_ADD, {"id": coleccion_id, "productIds": por_agregar}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 267 | `)["collectionAddProducts"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 268 | `if resultado["userErrors"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 269 | `print(f"  Error agregando productos a {categoria}: {resultado['userErrors']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 270 | `else:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 271 | `print(f"  Colección '{categoria}' con {len(por_agregar)} productos agregados")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 272 | `` | Línea en blanco: separa bloques lógicos. |
| 273 | `` | Línea en blanco: separa bloques lógicos. |
| 274 | `def main():` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 275 | `"""Punto de entrada con modo dry-run."""` | Docstring: describe el propósito del bloque. |
| 276 | `parser = argparse.ArgumentParser(description=__doc__)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 277 | `parser.add_argument("--dry-run", action="store_true", help="no escribe en Shopify")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 278 | `args = parser.parse_args()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 279 | `` | Línea en blanco: separa bloques lógicos. |
| 280 | `catalogo = cargar_catalogo()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 281 | `existentes, nodos = skus_existentes()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 282 | `print(f"SKUs existentes en la tienda: {len(existentes)}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 283 | `` | Línea en blanco: separa bloques lógicos. |
| 284 | `nodos_por_sku = {}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 285 | `for nodo in nodos:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 286 | `for variante in nodo["variants"]["nodes"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 287 | `if variante["sku"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 288 | `nodos_por_sku[variante["sku"]] = nodo` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 289 | `` | Línea en blanco: separa bloques lógicos. |
| 290 | `pendientes = [` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 291 | `p for p in catalogo["productos"] if p["sku"] not in existentes` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 292 | `]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 293 | `print(f"Productos a crear: {len(pendientes)}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 294 | `` | Línea en blanco: separa bloques lógicos. |
| 295 | `if args.dry_run:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 296 | `for producto in pendientes:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 297 | `print(f"  [DRY RUN] Crear {producto['sku']} - {producto['nombre']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 298 | `for producto in catalogo["productos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 299 | `nodo = nodos_por_sku.get(producto["sku"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 300 | `if nodo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 301 | `sin_precio = any(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 302 | `v["sku"] == producto["sku"] and v["price"] != str(producto["precio"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 303 | `for v in nodo["variants"]["nodes"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 304 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 305 | `if sin_precio or not nodo["media"]["nodes"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 306 | `print(f"  [DRY RUN] Sincronizar {producto['sku']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 307 | `return 0` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 308 | `` | Línea en blanco: separa bloques lógicos. |
| 309 | `location_id = location_principal() if pendientes else None` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 310 | `ids_por_sku = {sku: nodo["id"] for sku, nodo in nodos_por_sku.items()}` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 311 | `` | Línea en blanco: separa bloques lógicos. |
| 312 | `for producto in pendientes:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 313 | `creado = crear_producto(producto, location_id)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 314 | `ids_por_sku[producto["sku"]] = creado["id"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 315 | `print(f"  Creado {producto['sku']} -> {creado['handle']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 316 | `` | Línea en blanco: separa bloques lógicos. |
| 317 | `for producto in catalogo["productos"]:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 318 | `nodo = nodos_por_sku.get(producto["sku"])` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 319 | `if nodo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 320 | `cambios = sincronizar_producto(producto, nodo)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 321 | `if cambios:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 322 | `print(f"  Actualizado {producto['sku']}: {', '.join(cambios)}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 323 | `` | Línea en blanco: separa bloques lógicos. |
| 324 | `crear_colecciones(catalogo, ids_por_sku)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 325 | `return 0` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 326 | `` | Línea en blanco: separa bloques lógicos. |
| 327 | `` | Línea en blanco: separa bloques lógicos. |
| 328 | `if __name__ == "__main__":` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 329 | `raise SystemExit(main())` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

