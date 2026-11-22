# Explicación línea por línea del código

Documento generado automáticamente desde los comentarios del código fuente.
La columna **Explicación** corresponde al comentario de la línea o al
comentario del bloque que le precede inmediatamente.

## `shopify_client.py`

| Línea | Código | Explicación |
|---:|---|---|
| 1 | `"""Cliente simple para la Admin API de Shopify usando client credentials.` | Docstring: describe el propósito del bloque. |
| 2 | `` | Línea en blanco: separa bloques lógicos. |
| 3 | `Variables esperadas en .env:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 4 | `SHOPIFY_SHOP=techstore-d8vn3rhk.myshopify.com` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 5 | `SHOPIFY_CLIENT_ID=...` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 6 | `SHOPIFY_CLIENT_SECRET=shpss_...` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 7 | `` | Línea en blanco: separa bloques lógicos. |
| 8 | `Nota: el endpoint real de Shopify es https://<shop>.myshopify.com/admin/...` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 9 | `por eso SHOPIFY_SHOP=techstore se normaliza a techstore.myshopify.com.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 10 | `"""` | Docstring: describe el propósito del bloque. |
| 11 | `` | Línea en blanco: separa bloques lógicos. |
| 12 | `import os` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 13 | `import re` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 14 | `` | Línea en blanco: separa bloques lógicos. |
| 15 | `import requests` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 16 | `from dotenv import load_dotenv` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 17 | `` | Línea en blanco: separa bloques lógicos. |
| 18 | `load_dotenv()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 19 | `` | Línea en blanco: separa bloques lógicos. |
| 20 | `SHOP = os.getenv("SHOPIFY_SHOP", "").strip()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 21 | `CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID", "").strip()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 22 | `CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET", "").strip()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 23 | `API_VERSION = "2026-01"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 24 | `` | Línea en blanco: separa bloques lógicos. |
| 25 | `_TOKEN = None` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 26 | `` | Línea en blanco: separa bloques lógicos. |
| 27 | `` | Línea en blanco: separa bloques lógicos. |
| 28 | `def normalizar_shop(shop: str) -> str:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 29 | `"""Acepta 'techstore', 'techstore.myshopify.com' o la URL completa con /admin."""` | Docstring: describe el propósito del bloque. |
| 30 | `shop = shop.strip().replace("https://", "").replace("http://", "").rstrip("/")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 31 | `if shop.endswith("/admin"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 32 | `shop = shop[: -len("/admin")]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 33 | `if "." not in shop:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 34 | `shop += ".myshopify.com"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 35 | `return shop` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 36 | `` | Línea en blanco: separa bloques lógicos. |
| 37 | `` | Línea en blanco: separa bloques lógicos. |
| 38 | `def resumen_error(respuesta: requests.Response) -> str:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 39 | `"""Extrae el mensaje útil de una respuesta de error (JSON o HTML)."""` | Docstring: describe el propósito del bloque. |
| 40 | `try:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 41 | `return str(respuesta.json())[:300]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 42 | `except ValueError:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 43 | `titulo = re.search(r"<title>(.*?)</title>", respuesta.text, re.DOTALL)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 44 | `if titulo:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 45 | `return titulo.group(1).strip()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 46 | `return respuesta.text[:300]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 47 | `` | Línea en blanco: separa bloques lógicos. |
| 48 | `` | Línea en blanco: separa bloques lógicos. |
| 49 | `def validar_configuracion() -> None:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 50 | `faltantes = [` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 51 | `nombre` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 52 | `for nombre, valor in (` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 53 | `("SHOPIFY_SHOP", SHOP),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 54 | `("SHOPIFY_CLIENT_ID", CLIENT_ID),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 55 | `("SHOPIFY_CLIENT_SECRET", CLIENT_SECRET),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 56 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 57 | `if not valor` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 58 | `]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 59 | `if faltantes:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 60 | `raise RuntimeError(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 61 | `"Faltan variables en .env: " + ", ".join(faltantes)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 62 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 63 | `` | Línea en blanco: separa bloques lógicos. |
| 64 | `` | Línea en blanco: separa bloques lógicos. |
| 65 | `def get_shopify_token() -> str:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 66 | `"""Obtiene (y reutiliza) un access token mediante client_credentials."""` | Docstring: describe el propósito del bloque. |
| 67 | `global _TOKEN` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 68 | `if _TOKEN:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 69 | `return _TOKEN` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 70 | `` | Línea en blanco: separa bloques lógicos. |
| 71 | `validar_configuracion()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 72 | `url = f"https://{normalizar_shop(SHOP)}/admin/oauth/access_token"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 73 | `respuesta = requests.post(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 74 | `url,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 75 | `data={` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 76 | `"grant_type": "client_credentials",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 77 | `"client_id": CLIENT_ID,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 78 | `"client_secret": CLIENT_SECRET,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 79 | `},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 80 | `timeout=30,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 81 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 82 | `if respuesta.status_code != 200:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 83 | `raise RuntimeError(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 84 | `f"Error {respuesta.status_code} al pedir el token: "` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 85 | `f"{resumen_error(respuesta)}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 86 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 87 | `datos = respuesta.json()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 88 | `if "access_token" not in datos:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 89 | `raise RuntimeError(f"Shopify no devolvió access_token: {datos}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 90 | `` | Línea en blanco: separa bloques lógicos. |
| 91 | `_TOKEN = datos["access_token"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 92 | `return _TOKEN` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 93 | `` | Línea en blanco: separa bloques lógicos. |
| 94 | `` | Línea en blanco: separa bloques lógicos. |
| 95 | `def graphql_query(query: str, variables: dict \| None = None) -> dict:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 96 | `"""Ejecuta una consulta en la Admin GraphQL API y devuelve el bloque 'data'."""` | Docstring: describe el propósito del bloque. |
| 97 | `url = (` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 98 | `f"https://{normalizar_shop(SHOP)}/admin/api/{API_VERSION}/graphql.json"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 99 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 100 | `respuesta = requests.post(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 101 | `url,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 102 | `json={"query": query, "variables": variables or {}},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 103 | `headers={` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 104 | `"X-Shopify-Access-Token": get_shopify_token(),` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 105 | `"Content-Type": "application/json",` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 106 | `},` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 107 | `timeout=30,` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 108 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 109 | `if respuesta.status_code != 200:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 110 | `raise RuntimeError(` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 111 | `f"Error {respuesta.status_code} en GraphQL: {resumen_error(respuesta)}"` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 112 | `)` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 113 | `resultado = respuesta.json()` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 114 | `if resultado.get("errors"):` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 115 | `raise RuntimeError(f"Errores de GraphQL: {resultado['errors']}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 116 | `return resultado.get("data", {})` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 117 | `` | Línea en blanco: separa bloques lógicos. |
| 118 | `` | Línea en blanco: separa bloques lógicos. |
| 119 | `if __name__ == "__main__":` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 120 | `try:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 121 | `datos = graphql_query("{ shop { name myshopifyDomain } }")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 122 | `tienda = datos["shop"]` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 123 | `print(f"Conectado a: {tienda['name']} ({tienda['myshopifyDomain']})")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 124 | `except (RuntimeError, requests.RequestException, KeyError) as error:` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 125 | `print(f"Error de conexión: {error}")` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |

## `carrito/datos.py`

| Línea | Código | Explicación |
|---:|---|---|
| 1 | `"""Carga y acceso al catálogo compartido por las tres implementaciones.` | Docstring: describe el propósito del bloque. |
| 2 | `` | Línea en blanco: separa bloques lógicos. |
| 3 | `Este módulo es la única fuente de datos: las tres versiones del carrito` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 4 | `reciben el mismo diccionario, por lo que cualquier diferencia de resultado` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 5 | `se debe al paradigma y no a los datos de entrada.` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 6 | `"""` | Docstring: describe el propósito del bloque. |
| 7 | `` | Línea en blanco: separa bloques lógicos. |
| 8 | `import json` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 9 | `from pathlib import Path` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 10 | `` | Línea en blanco: separa bloques lógicos. |
| 11 | `# Ruta por defecto, calculada desde la ubicación de este archivo y no desde` | Ruta por defecto, calculada desde la ubicación de este archivo y no desde |
| 12 | `# el directorio de ejecución, para que funcione desde cualquier carpeta.` | el directorio de ejecución, para que funcione desde cualquier carpeta. |
| 13 | `RUTA_CATALOGO = Path(__file__).resolve().parent.parent / "datos" / "catalogo.json"` | el directorio de ejecución, para que funcione desde cualquier carpeta. |
| 14 | `` | Línea en blanco: separa bloques lógicos. |
| 15 | `` | Línea en blanco: separa bloques lógicos. |
| 16 | `def cargar_catalogo(ruta=RUTA_CATALOGO):` | el directorio de ejecución, para que funcione desde cualquier carpeta. |
| 17 | `"""Lee el JSON y devuelve un diccionario con la configuración del catálogo."""` | Docstring: describe el propósito del bloque. |
| 18 | `with open(ruta, "r", encoding="utf-8") as archivo:` | el directorio de ejecución, para que funcione desde cualquier carpeta. |
| 19 | `return json.load(archivo)` | el directorio de ejecución, para que funcione desde cualquier carpeta. |
| 20 | `` | Línea en blanco: separa bloques lógicos. |
| 21 | `` | Línea en blanco: separa bloques lógicos. |
| 22 | `def indice_productos(catalogo):` | el directorio de ejecución, para que funcione desde cualquier carpeta. |
| 23 | `"""Construye un índice {sku: producto} para búsquedas O(1)."""` | Docstring: describe el propósito del bloque. |
| 24 | `return {producto["sku"]: producto for producto in catalogo["productos"]}` | el directorio de ejecución, para que funcione desde cualquier carpeta. |

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
| 50 | `})` | Se agrega el sustituto, dejando registro del producto original. |
| 51 | `continue` | Ya resolvimos esta regla; pasamos a la siguiente. |
| 52 | `` | Línea en blanco: separa bloques lógicos. |
| 53 | `disponible = producto["stock"]` | Stock real que sí se puede vender. |
| 54 | `if disponible > 0:` | Solo agregamos la línea si hay algo disponible. |
| 55 | `items.append({` | Se agrega el sustituto, dejando registro del producto original. |
| 56 | `"sku": sku,` | SKU original. |
| 57 | `"nombre": producto["nombre"],` | Nombre original. |
| 58 | `"cantidad": disponible,` | Se limita al stock disponible. |
| 59 | `"precio_unitario": producto["precio"],` | Precio original. |
| 60 | `"subtotal": disponible * producto["precio"],` | Subtotal de la línea. |
| 61 | `"sustituto_de": None,` | No hubo sustitución. |
| 62 | `})` | Se agrega el sustituto, dejando registro del producto original. |
| 63 | `` | Línea en blanco: separa bloques lógicos. |
| 64 | `falta = cantidad - disponible` | Diferencia no cubierta. |
| 65 | `if falta > 0:` | Solo se registra si realmente falta stock. |
| 66 | `faltantes.append({"sku": sku, "cantidad": falta})` | Reporte. |
| 67 | `else:` | Hay stock suficiente. |
| 68 | `items.append({` | Se agrega el sustituto, dejando registro del producto original. |
| 69 | `"sku": sku,` | SKU original. |
| 70 | `"nombre": producto["nombre"],` | Nombre original. |
| 71 | `"cantidad": cantidad,` | Cantidad calculada. |
| 72 | `"precio_unitario": producto["precio"],` | Precio original. |
| 73 | `"subtotal": cantidad * producto["precio"],` | Subtotal de la línea. |
| 74 | `"sustituto_de": None,` | Sin sustitución. |
| 75 | `})` | Se agrega el sustituto, dejando registro del producto original. |
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
| 110 | `"descuentos": {"2x1": descuento_2x1, "cupon": descuento_cupon},` | --- Paso 4: devolver estructura común a los tres paradigmas --- |
| 111 | `"envio": costo_envio,` | Costo de envío aplicado. |
| 112 | `"total": total,` | Total a pagar. |
| 113 | `}` | --- Paso 4: devolver estructura común a los tres paradigmas --- |

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
| 28 | `def crear_item(self, cantidad, sustituto_de=None):` | --- Modelo de datos --- |
| 29 | `"""Fábrica de líneas de carrito a partir del producto."""` | Docstring: describe el propósito del bloque. |
| 30 | `return Item(` | Devuelve un objeto Item. |
| 31 | `sku=self.sku,` | SKU del producto vendido. |
| 32 | `nombre=self.nombre,` | Nombre del producto vendido. |
| 33 | `cantidad=cantidad,` | Unidades calculadas. |
| 34 | `precio_unitario=self.precio,` | Precio unitario. |
| 35 | `subtotal=cantidad * self.precio,` | Precio total de la línea. |
| 36 | `sustituto_de=sustituto_de,` | SKU original si hubo sustitución. |
| 37 | `)` | --- Modelo de datos --- |
| 38 | `` | Línea en blanco: separa bloques lógicos. |
| 39 | `` | Línea en blanco: separa bloques lógicos. |
| 40 | `@dataclass(frozen=True)` | --- Modelo de datos --- |
| 41 | `class Item:` | --- Modelo de datos --- |
| 42 | `"""Una línea del carrito; también inmutable."""` | Docstring: describe el propósito del bloque. |
| 43 | `` | Línea en blanco: separa bloques lógicos. |
| 44 | `sku: str` | --- Modelo de datos --- |
| 45 | `nombre: str` | --- Modelo de datos --- |
| 46 | `cantidad: int` | --- Modelo de datos --- |
| 47 | `precio_unitario: int` | --- Modelo de datos --- |
| 48 | `subtotal: int` | --- Modelo de datos --- |
| 49 | `sustituto_de: str \| None` | None cuando no hubo sustitución. |
| 50 | `` | Línea en blanco: separa bloques lógicos. |
| 51 | `def como_dict(self):` | --- Modelo de datos --- |
| 52 | `"""Convierte el objeto en diccionario para igualar a los otros paradigmas."""` | Docstring: describe el propósito del bloque. |
| 53 | `return {` | --- Modelo de datos --- |
| 54 | `"sku": self.sku,` | --- Modelo de datos --- |
| 55 | `"nombre": self.nombre,` | --- Modelo de datos --- |
| 56 | `"cantidad": self.cantidad,` | --- Modelo de datos --- |
| 57 | `"precio_unitario": self.precio_unitario,` | --- Modelo de datos --- |
| 58 | `"subtotal": self.subtotal,` | --- Modelo de datos --- |
| 59 | `"sustituto_de": self.sustituto_de,` | --- Modelo de datos --- |
| 60 | `}` | --- Modelo de datos --- |
| 61 | `` | Línea en blanco: separa bloques lógicos. |
| 62 | `` | Línea en blanco: separa bloques lógicos. |
| 63 | `@dataclass(frozen=True)` | --- Modelo de datos --- |
| 64 | `class Regla:` | --- Modelo de datos --- |
| 65 | `"""Regla que define cuántas unidades se sugieren por persona."""` | Docstring: describe el propósito del bloque. |
| 66 | `` | Línea en blanco: separa bloques lógicos. |
| 67 | `sku: str` | Producto al que aplica. |
| 68 | `por_persona: float` | Unidades (o fracción) por persona. |
| 69 | `minimo: int` | Mínimo absoluto de unidades. |
| 70 | `` | Línea en blanco: separa bloques lógicos. |
| 71 | `def cantidad_para(self, personas):` | --- Modelo de datos --- |
| 72 | `"""Calcula la cantidad redondeada hacia arriba, con mínimo."""` | Docstring: describe el propósito del bloque. |
| 73 | `return max(self.minimo, math.ceil(personas * self.por_persona))` | --- Modelo de datos --- |
| 74 | `` | Línea en blanco: separa bloques lógicos. |
| 75 | `` | Línea en blanco: separa bloques lógicos. |
| 76 | `@dataclass(frozen=True)` | --- Modelo de datos --- |
| 77 | `class Evento:` | --- Modelo de datos --- |
| 78 | `"""Configuración de un evento: reglas, cupón y producto en 2x1."""` | Docstring: describe el propósito del bloque. |
| 79 | `` | Línea en blanco: separa bloques lógicos. |
| 80 | `nombre: str` | --- Modelo de datos --- |
| 81 | `cupon: str` | --- Modelo de datos --- |
| 82 | `producto_2x1: str` | --- Modelo de datos --- |
| 83 | `reglas: tuple` | Tupla de Regla (inmutable). |
| 84 | `` | Línea en blanco: separa bloques lógicos. |
| 85 | `@classmethod` | --- Modelo de datos --- |
| 86 | `def desde_dict(cls, datos):` | --- Modelo de datos --- |
| 87 | `"""Construye un Evento desde el diccionario del JSON."""` | Docstring: describe el propósito del bloque. |
| 88 | `reglas = tuple(` | Comprensión que crea objetos Regla. |
| 89 | `Regla(r["sku"], r["por_persona"], r["minimo"])` | --- Modelo de datos --- |
| 90 | `for r in datos["reglas"]` | --- Modelo de datos --- |
| 91 | `)` | --- Modelo de datos --- |
| 92 | `return cls(datos["nombre"], datos["cupon"], datos["producto_2x1"], reglas)` | --- Modelo de datos --- |
| 93 | `` | Línea en blanco: separa bloques lógicos. |
| 94 | `` | Línea en blanco: separa bloques lógicos. |
| 95 | `# --- Estrategias de descuento (herencia y polimorfismo) ---` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 96 | `` | Línea en blanco: separa bloques lógicos. |
| 97 | `class Descuento(ABC):` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 98 | `"""Interfaz común: toda estrategia debe saber calcular un descuento."""` | Docstring: describe el propósito del bloque. |
| 99 | `` | Línea en blanco: separa bloques lógicos. |
| 100 | `@abstractmethod` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 101 | `def calcular(self, items, evento, cupon):` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 102 | `"""Devuelve el monto de descuento (entero)."""` | Docstring: describe el propósito del bloque. |
| 103 | `raise NotImplementedError` | Obliga a las subclases a implementarlo. |
| 104 | `` | Línea en blanco: separa bloques lógicos. |
| 105 | `` | Línea en blanco: separa bloques lógicos. |
| 106 | `class Descuento2x1(Descuento):` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 107 | `"""Descuento 2x1 sobre el producto configurado en el evento."""` | Docstring: describe el propósito del bloque. |
| 108 | `` | Línea en blanco: separa bloques lógicos. |
| 109 | `def calcular(self, items, evento, cupon):` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 110 | `total = 0` | Acumulador local. |
| 111 | `for item in items:` | Polimorfismo: Item expone los mismos atributos. |
| 112 | `es_promo = item.sku == evento.producto_2x1` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 113 | `es_sustituto = item.sustituto_de == evento.producto_2x1` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 114 | `if es_promo or es_sustituto:` | Aplica también al sustituto. |
| 115 | `total += (item.cantidad // 2) * item.precio_unitario` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 116 | `return total` | Cumple el contrato de Descuento. |
| 117 | `` | Línea en blanco: separa bloques lógicos. |
| 118 | `` | Línea en blanco: separa bloques lógicos. |
| 119 | `class DescuentoPorcentaje(Descuento):` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 120 | `"""Descuento por cupón: porcentaje sobre la base ya descontada."""` | Docstring: describe el propósito del bloque. |
| 121 | `` | Línea en blanco: separa bloques lógicos. |
| 122 | `def __init__(self, porcentaje):` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 123 | `self.porcentaje = porcentaje` | Estado interno encapsulado. |
| 124 | `` | Línea en blanco: separa bloques lógicos. |
| 125 | `def calcular(self, items, evento, cupon, base=0):` | --- Estrategias de descuento (herencia y polimorfismo) --- |
| 126 | `# Firma extendida con `base`; se usa desde el carrito de forma explícita.` | Firma extendida con `base`; se usa desde el carrito de forma explícita. |
| 127 | `if cupon != evento.cupon:` | Cupón incorrecto o ausente. |
| 128 | `return 0` | Sin descuento. |
| 129 | `return base * self.porcentaje // 100` | Entero, redondeo hacia abajo. |
| 130 | `` | Línea en blanco: separa bloques lógicos. |
| 131 | `` | Línea en blanco: separa bloques lógicos. |
| 132 | `class PoliticaEnvio:` | Firma extendida con `base`; se usa desde el carrito de forma explícita. |
| 133 | `"""Define cuándo el envío es gratis."""` | Docstring: describe el propósito del bloque. |
| 134 | `` | Línea en blanco: separa bloques lógicos. |
| 135 | `def __init__(self, costo, gratis_desde):` | Firma extendida con `base`; se usa desde el carrito de forma explícita. |
| 136 | `self.costo = costo` | Costo normal. |
| 137 | `self.gratis_desde = gratis_desde` | Umbral para envío gratis. |
| 138 | `` | Línea en blanco: separa bloques lógicos. |
| 139 | `def calcular(self, monto):` | Firma extendida con `base`; se usa desde el carrito de forma explícita. |
| 140 | `"""Devuelve el costo de envío según el monto después de descuentos."""` | Docstring: describe el propósito del bloque. |
| 141 | `return 0 if monto >= self.gratis_desde else self.costo` | Firma extendida con `base`; se usa desde el carrito de forma explícita. |
| 142 | `` | Línea en blanco: separa bloques lógicos. |
| 143 | `` | Línea en blanco: separa bloques lógicos. |
| 144 | `# --- Orquestación ---` | --- Orquestación --- |
| 145 | `` | Línea en blanco: separa bloques lógicos. |
| 146 | `class Carrito:` | --- Orquestación --- |
| 147 | `"""Coordina productos, reglas y descuentos para armar el carrito."""` | Docstring: describe el propósito del bloque. |
| 148 | `` | Línea en blanco: separa bloques lógicos. |
| 149 | `def __init__(self, evento, personas, catalogo, cupon=None):` | --- Orquestación --- |
| 150 | `if personas <= 0:` | Validación de entrada. |
| 151 | `raise ValueError("personas debe ser mayor que cero")` | --- Orquestación --- |
| 152 | `if evento not in catalogo["eventos"]:` | Validación de evento. |
| 153 | `raise ValueError(f"Evento desconocido: {evento}")` | --- Orquestación --- |
| 154 | `` | Línea en blanco: separa bloques lógicos. |
| 155 | `self.evento = Evento.desde_dict(catalogo["eventos"][evento])` | Config. |
| 156 | `self.personas = personas` | Cantidad de personas. |
| 157 | `self.productos = {` | Dict de objetos Producto. |
| 158 | `sku: Producto(p["sku"], p["nombre"], p["precio"], p["stock"])` | --- Orquestación --- |
| 159 | `for sku, p in indice_productos(catalogo).items()` | --- Orquestación --- |
| 160 | `}` | --- Orquestación --- |
| 161 | `self.sustitutos = catalogo["sustitutos"]` | Mapa de reemplazos. |
| 162 | `self.cupon = cupon` | Cupón ingresado por el usuario. |
| 163 | `self.envio = PoliticaEnvio(` | Política de envío del catálogo. |
| 164 | `catalogo["envio"]["costo"], catalogo["envio"]["gratis_desde"]` | --- Orquestación --- |
| 165 | `)` | --- Orquestación --- |
| 166 | `self.descuentos = [Descuento2x1()]` | Estrategias polimórficas. |
| 167 | `` | Línea en blanco: separa bloques lógicos. |
| 168 | `def _resolver_regla(self, regla):` | --- Orquestación --- |
| 169 | `"""Aplica una regla; devuelve (item o None, faltante o None)."""` | Docstring: describe el propósito del bloque. |
| 170 | `producto = self.productos[regla.sku]` | Producto sugerido. |
| 171 | `cantidad = regla.cantidad_para(self.personas)` | Cantidad calculada. |
| 172 | `` | Línea en blanco: separa bloques lógicos. |
| 173 | `if cantidad <= producto.stock:` | Caso simple: hay stock. |
| 174 | `return producto.crear_item(cantidad), None` | --- Orquestación --- |
| 175 | `` | Línea en blanco: separa bloques lógicos. |
| 176 | `# Sin stock suficiente: intenta sustituto.` | Sin stock suficiente: intenta sustituto. |
| 177 | `sku_alt = self.sustitutos.get(regla.sku)` | SKU alternativo. |
| 178 | `alternativo = self.productos.get(sku_alt)` | Objeto alternativo. |
| 179 | `if alternativo and alternativo.stock >= cantidad:` | El sustituto alcanza. |
| 180 | `return alternativo.crear_item(cantidad, regla.sku), None` | Sin stock suficiente: intenta sustituto. |
| 181 | `` | Línea en blanco: separa bloques lógicos. |
| 182 | `# No hay sustituto válido: se vende lo disponible y se reporta el falta.` | No hay sustituto válido: se vende lo disponible y se reporta el falta. |
| 183 | `disponible = producto.stock` | No hay sustituto válido: se vende lo disponible y se reporta el falta. |
| 184 | `item = producto.crear_item(disponible) if disponible > 0 else None` | No hay sustituto válido: se vende lo disponible y se reporta el falta. |
| 185 | `faltante = {"sku": regla.sku, "cantidad": cantidad - disponible}` | No hay sustituto válido: se vende lo disponible y se reporta el falta. |
| 186 | `return item, faltante` | No hay sustituto válido: se vende lo disponible y se reporta el falta. |
| 187 | `` | Línea en blanco: separa bloques lógicos. |
| 188 | `def armar(self):` | No hay sustituto válido: se vende lo disponible y se reporta el falta. |
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
| 204 | `desc_cupon = DescuentoPorcentaje(10).calcular(` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 205 | `items, self.evento, self.cupon, base=subtotal - desc_2x1` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 206 | `)` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 207 | `` | Línea en blanco: separa bloques lógicos. |
| 208 | `base = subtotal - desc_2x1 - desc_cupon` | Monto para evaluar envío. |
| 209 | `costo_envio = self.envio.calcular(base)` | Política de envío. |
| 210 | `total = base + costo_envio` | Total final. |
| 211 | `` | Línea en blanco: separa bloques lógicos. |
| 212 | `return {` | Misma estructura que en el paradigma imperativo. |
| 213 | `"evento": self.evento.nombre.lower().replace(" ", "_"),` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 214 | `"personas": self.personas,` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 215 | `"items": [item.como_dict() for item in items],` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 216 | `"faltantes": faltantes,` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 217 | `"descuentos": {"2x1": desc_2x1, "cupon": desc_cupon},` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 218 | `"envio": costo_envio,` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 219 | `"total": total,` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 220 | `}` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 221 | `` | Línea en blanco: separa bloques lógicos. |
| 222 | `` | Línea en blanco: separa bloques lógicos. |
| 223 | `def armar_carrito(evento, personas, catalogo, cupon=None):` | Polimorfismo: ambas estrategias responden a `calcular`. |
| 224 | `"""API pública equivalente a la de los otros dos módulos."""` | Docstring: describe el propósito del bloque. |
| 225 | `# El evento devuelto por la clase se normaliza al nombre de la clave JSON.` | El evento devuelto por la clase se normaliza al nombre de la clave JSON. |
| 226 | `carrito = Carrito(evento, personas, catalogo, cupon)` | El evento devuelto por la clase se normaliza al nombre de la clave JSON. |
| 227 | `resultado = carrito.armar()` | El evento devuelto por la clase se normaliza al nombre de la clave JSON. |
| 228 | `resultado["evento"] = evento` | Garantiza igualdad exacta entre versiones. |
| 229 | `return resultado` | El evento devuelto por la clase se normaliza al nombre de la clave JSON. |

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
| 64 | `def construir_lineas(config, personas, catalogo, productos):` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 65 | `"""Aplica `resolver` a todas las reglas con map y separa resultados."""` | Docstring: describe el propósito del bloque. |
| 66 | `pares = tuple(` | Tupla inmutable de resultados. |
| 67 | `map(` | map aplica resolver a cada regla. |
| 68 | `lambda regla: resolver(regla, personas, catalogo, productos),` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 69 | `config["reglas"],` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 70 | `)` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 71 | `)` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 72 | `items = tuple(filter(None, map(lambda par: par[0], pares)))` | Solo items. |
| 73 | `faltantes = tuple(filter(None, map(lambda par: par[1], pares)))` | Solo faltantes. |
| 74 | `return items, faltantes` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 75 | `` | Línea en blanco: separa bloques lógicos. |
| 76 | `` | Línea en blanco: separa bloques lógicos. |
| 77 | `def sumar_subtotal(items):` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 78 | `"""Reduce los subtotales de las líneas en un entero."""` | Docstring: describe el propósito del bloque. |
| 79 | `return reduce(lambda total, item: total + item["subtotal"], items, 0)` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 80 | `` | Línea en blanco: separa bloques lógicos. |
| 81 | `` | Línea en blanco: separa bloques lógicos. |
| 82 | `def descuento_2x1(items, sku_promo):` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 83 | `"""Descuento 2x1 usando reduce sobre las líneas promocionadas."""` | Docstring: describe el propósito del bloque. |
| 84 | `promocionados = filter(` | filter conserva solo las líneas que cumplen. |
| 85 | `lambda item: item["sku"] == sku_promo or item["sustituto_de"] == sku_promo,` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 86 | `items,` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 87 | `)` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 88 | `return reduce(` | Acumula pares * precio. |
| 89 | `lambda total, item: total + (item["cantidad"] // 2) * item["precio_unitario"],` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 90 | `promocionados,` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 91 | `0,` | Valor inicial del acumulador. |
| 92 | `)` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 93 | `` | Línea en blanco: separa bloques lógicos. |
| 94 | `` | Línea en blanco: separa bloques lógicos. |
| 95 | `def descuento_cupon(cupon, config, base):` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 96 | `"""Descuento de 10% solo si el cupón coincide con el del evento."""` | Docstring: describe el propósito del bloque. |
| 97 | `return base * 10 // 100 if cupon == config["cupon"] else 0` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 98 | `` | Línea en blanco: separa bloques lógicos. |
| 99 | `` | Línea en blanco: separa bloques lógicos. |
| 100 | `def costo_envio(catalogo, monto):` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 101 | `"""Costo de envío según el umbral configurado."""` | Docstring: describe el propósito del bloque. |
| 102 | `envio = catalogo["envio"]` | Configuración de envío. |
| 103 | `return 0 if monto >= envio["gratis_desde"] else envio["costo"]` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 104 | `` | Línea en blanco: separa bloques lógicos. |
| 105 | `` | Línea en blanco: separa bloques lógicos. |
| 106 | `def armar_carrito(evento, personas, catalogo, cupon=None):` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
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
| 122 | `"evento": evento,` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 123 | `"personas": personas,` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 124 | `"items": list(items),` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 125 | `"faltantes": list(faltantes),` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 126 | `"descuentos": {"2x1": desc_2x1, "cupon": desc_cupon},` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 127 | `"envio": envio,` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 128 | `"total": total,` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |
| 129 | `}` | Sin sustituto válido: vender lo disponible y reportar la diferencia. |

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
| 16 | `("cumpleanos", 10, "FIESTA10"),` | Casos de prueba definidos una sola vez para las tres implementaciones. |
| 17 | `("trabajo_remoto", 12, "HOME10"),` | Casos de prueba definidos una sola vez para las tres implementaciones. |
| 18 | `("vuelta_a_clases", 12, "ESCUELA10"),` | Casos de prueba definidos una sola vez para las tres implementaciones. |
| 19 | `("cumpleanos", 200, None),` | Fuerza sustituciones y faltantes por stock. |
| 20 | `("accesorios_basicos", 1, None),` | Monto bajo: debe cobrar envío. |
| 21 | `]` | Casos de prueba definidos una sola vez para las tres implementaciones. |
| 22 | `` | Línea en blanco: separa bloques lógicos. |
| 23 | `# Las tres funciones se agrupan en una tupla para iterarlas por igual.` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 24 | `IMPLEMENTACIONES = (` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 25 | `("Imperativo", armar_imperativo),` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 26 | `("Orientado a objetos", armar_objetos),` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 27 | `("Funcional", armar_funcional),` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 28 | `)` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 29 | `` | Línea en blanco: separa bloques lógicos. |
| 30 | `` | Línea en blanco: separa bloques lógicos. |
| 31 | `def formatear(resultado):` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 32 | `"""Resume un resultado para mostrarlo en pantalla."""` | Docstring: describe el propósito del bloque. |
| 33 | `return (` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 34 | `f"items={len(resultado['items'])}, "` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 35 | `f"faltantes={len(resultado['faltantes'])}, "` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 36 | `f"2x1=${resultado['descuentos']['2x1']}, "` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 37 | `f"cupon=${resultado['descuentos']['cupon']}, "` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 38 | `f"envio=${resultado['envio']}, total=${resultado['total']}"` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 39 | `)` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 40 | `` | Línea en blanco: separa bloques lógicos. |
| 41 | `` | Línea en blanco: separa bloques lógicos. |
| 42 | `def main():` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 43 | `"""Ejecuta todos los casos y verifica que los tres resultados sean iguales."""` | Docstring: describe el propósito del bloque. |
| 44 | `catalogo = cargar_catalogo()` | Misma fuente de datos para todos. |
| 45 | `todos_iguales = True` | Bandera global del resultado de la comparación. |
| 46 | `` | Línea en blanco: separa bloques lógicos. |
| 47 | `for evento, personas, cupon in CASOS:` | Recorre los escenarios. |
| 48 | `print(f"\n=== {evento} \| {personas} personas \| cupón={cupon} ===")` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 49 | `resultados = []` | Resultados de las tres implementaciones. |
| 50 | `` | Línea en blanco: separa bloques lógicos. |
| 51 | `for nombre, funcion in IMPLEMENTACIONES:` | Recorre los paradigmas. |
| 52 | `resultado = funcion(evento, personas, catalogo, cupon)` | Ejecuta. |
| 53 | `resultados.append(resultado)` | Guarda para comparar. |
| 54 | `print(f"  {nombre:<20} {formatear(resultado)}")` | Las tres funciones se agrupan en una tupla para iterarlas por igual. |
| 55 | `` | Línea en blanco: separa bloques lógicos. |
| 56 | `# Comparación estricta: los tres dict deben ser exactamente iguales.` | Comparación estricta: los tres dict deben ser exactamente iguales. |
| 57 | `iguales = resultados[0] == resultados[1] == resultados[2]` | Comparación estricta: los tres dict deben ser exactamente iguales. |
| 58 | `todos_iguales = todos_iguales and iguales` | Actualiza la bandera. |
| 59 | `print(f"  >>> Paridad: {'OK' if iguales else 'FALLO'}")` | Comparación estricta: los tres dict deben ser exactamente iguales. |
| 60 | `` | Línea en blanco: separa bloques lógicos. |
| 61 | `# Detalle del caso de stock agotado para hacer visible la sustitución.` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 62 | `if personas == 200:` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 63 | `for item in resultados[0]["items"]:` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 64 | `if item["sustituto_de"]:` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 65 | `print(` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 66 | `f"    Sustituto: {item['sustituto_de']} -> "` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 67 | `f"{item['sku']} x{item['cantidad']}"` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 68 | `)` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 69 | `for falta in resultados[0]["faltantes"]:` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 70 | `print(f"    Faltante: {falta['sku']} x{falta['cantidad']}")` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 71 | `` | Línea en blanco: separa bloques lógicos. |
| 72 | `print(f"\nResultado global: {'TODOS LOS CASOS COINCIDEN' if todos_iguales else 'HAY DIFERENCIAS'}")` | Detalle del caso de stock agotado para hacer visible la sustitución. |
| 73 | `return 0 if todos_iguales else 1` | Código de salida para CI. |
| 74 | `` | Línea en blanco: separa bloques lógicos. |
| 75 | `` | Línea en blanco: separa bloques lógicos. |
| 76 | `if __name__ == "__main__":` | Detalle del caso de stock agotado para hacer visible la sustitución. |
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
| 12 | `from pathlib import Path` | Declaración o expresión del algoritmo; ver el bloque comentado anterior. |
| 13 | `` | Línea en blanco: separa bloques lógicos. |
| 14 | `# Permite importar el módulo de la raíz aunque se ejecute como paquete.` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 15 | `sys.path.insert(0, str(Path(__file__).resolve().parent.parent))` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 16 | `` | Línea en blanco: separa bloques lógicos. |
| 17 | `from carrito.datos import cargar_catalogo` | noqa: E402 |
| 18 | `from shopify_client import graphql_query` | noqa: E402 |
| 19 | `` | Línea en blanco: separa bloques lógicos. |
| 20 | `PRODUCTOS_QUERY = """` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 21 | `{` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 22 | `products(first: 250) {` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 23 | `nodes {` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 24 | `id` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 25 | `title` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 26 | `variants(first: 250) { nodes { sku } }` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 27 | `}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 28 | `}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 29 | `}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 30 | `"""` | Docstring: describe el propósito del bloque. |
| 31 | `` | Línea en blanco: separa bloques lógicos. |
| 32 | `LOCATIONS_QUERY = """` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 33 | `{` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 34 | `locations(first: 10) { nodes { id name } }` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 35 | `}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 36 | `"""` | Docstring: describe el propósito del bloque. |
| 37 | `` | Línea en blanco: separa bloques lógicos. |
| 38 | `PRODUCT_CREATE = """` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 39 | `mutation ProductoCrear($input: ProductInput!) {` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 40 | `productCreate(input: $input) {` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 41 | `product { id title handle }` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 42 | `userErrors { field message }` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 43 | `}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 44 | `}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 45 | `"""` | Docstring: describe el propósito del bloque. |
| 46 | `` | Línea en blanco: separa bloques lógicos. |
| 47 | `COLLECTION_CREATE = """` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 48 | `mutation ColeccionCrear($input: CollectionInput!) {` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 49 | `collectionCreate(input: $input) {` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 50 | `collection { id title handle }` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 51 | `userErrors { field message }` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 52 | `}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 53 | `}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 54 | `"""` | Docstring: describe el propósito del bloque. |
| 55 | `` | Línea en blanco: separa bloques lógicos. |
| 56 | `COLLECTION_ADD = """` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 57 | `mutation AgregarProductos($id: ID!, $ids: [ID!]!) {` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 58 | `collectionAddProducts(collectionId: $id, productIds: $ids) {` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 59 | `collection { id title }` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 60 | `userErrors { field message }` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 61 | `}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 62 | `}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 63 | `"""` | Docstring: describe el propósito del bloque. |
| 64 | `` | Línea en blanco: separa bloques lógicos. |
| 65 | `` | Línea en blanco: separa bloques lógicos. |
| 66 | `def skus_existentes():` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 67 | `"""Devuelve el conjunto de SKUs ya creados en la tienda."""` | Docstring: describe el propósito del bloque. |
| 68 | `datos = graphql_query(PRODUCTOS_QUERY)` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 69 | `skus = set()` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 70 | `for producto in datos["products"]["nodes"]:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 71 | `for variante in producto["variants"]["nodes"]:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 72 | `if variante["sku"]:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 73 | `skus.add(variante["sku"])` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 74 | `return skus, datos["products"]["nodes"]` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 75 | `` | Línea en blanco: separa bloques lógicos. |
| 76 | `` | Línea en blanco: separa bloques lógicos. |
| 77 | `def location_principal():` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 78 | `"""Devuelve el ID de la primera ubicación de inventario."""` | Docstring: describe el propósito del bloque. |
| 79 | `datos = graphql_query(LOCATIONS_QUERY)` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 80 | `ubicaciones = datos["locations"]["nodes"]` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 81 | `if not ubicaciones:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 82 | `raise RuntimeError("No hay ubicaciones de inventario configuradas")` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 83 | `return ubicaciones[0]["id"]` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 84 | `` | Línea en blanco: separa bloques lógicos. |
| 85 | `` | Línea en blanco: separa bloques lógicos. |
| 86 | `def crear_producto(producto, location_id):` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 87 | `"""Crea un producto con precio, SKU, stock y etiquetas."""` | Docstring: describe el propósito del bloque. |
| 88 | `entrada = {` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 89 | `"title": producto["nombre"],` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 90 | `"descriptionHtml": f"<p>{producto['descripcion']}</p>",` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 91 | `"productType": producto["categoria"],` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 92 | `"vendor": "TechStore",` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 93 | `"status": "ACTIVE",` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 94 | `"tags": [producto["categoria"], "carrito-evento"],` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 95 | `"variants": [{` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 96 | `"sku": producto["sku"],` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 97 | `"price": str(producto["precio"]),` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 98 | `"inventoryManagement": "SHOPIFY",` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 99 | `"inventoryPolicy": "CONTINUE",` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 100 | `"inventoryQuantities": [{` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 101 | `"availableQuantity": producto["stock"],` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 102 | `"locationId": location_id,` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 103 | `}],` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 104 | `}],` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 105 | `}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 106 | `respuesta = graphql_query(PRODUCT_CREATE, {"input": entrada})["productCreate"]` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 107 | `if respuesta["userErrors"]:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 108 | `raise RuntimeError(f"Error creando {producto['sku']}: {respuesta['userErrors']}")` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 109 | `return respuesta["product"]` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 110 | `` | Línea en blanco: separa bloques lógicos. |
| 111 | `` | Línea en blanco: separa bloques lógicos. |
| 112 | `def crear_colecciones(catalogo, productos_por_sku):` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 113 | `"""Crea una colección por cada categoría y agrega sus productos."""` | Docstring: describe el propósito del bloque. |
| 114 | `categorias = {}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 115 | `for producto in catalogo["productos"]:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 116 | `categoria = producto["categoria"]` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 117 | `categorias.setdefault(categoria, []).append(productos_por_sku[producto["sku"]])` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 118 | `` | Línea en blanco: separa bloques lógicos. |
| 119 | `for categoria, ids in categorias.items():` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 120 | `respuesta = graphql_query(` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 121 | `COLLECTION_CREATE,` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 122 | `{"input": {` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 123 | `"title": categoria,` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 124 | `"handle": categoria.lower(),` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 125 | `"descriptionHtml": f"<p>Productos de la categoría {categoria}.</p>",` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 126 | `}},` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 127 | `)["collectionCreate"]` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 128 | `if respuesta["userErrors"]:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 129 | `print(f"  Colección {categoria}: {respuesta['userErrors']}")` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 130 | `continue` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 131 | `coleccion_id = respuesta["collection"]["id"]` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 132 | `resultado = graphql_query(` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 133 | `COLLECTION_ADD, {"id": coleccion_id, "ids": ids}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 134 | `)["collectionAddProducts"]` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 135 | `if resultado["userErrors"]:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 136 | `print(f"  Error agregando productos a {categoria}: {resultado['userErrors']}")` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 137 | `else:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 138 | `print(f"  Colección '{categoria}' creada con {len(ids)} productos")` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 139 | `` | Línea en blanco: separa bloques lógicos. |
| 140 | `` | Línea en blanco: separa bloques lógicos. |
| 141 | `def main():` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 142 | `"""Punto de entrada con modo dry-run."""` | Docstring: describe el propósito del bloque. |
| 143 | `parser = argparse.ArgumentParser(description=__doc__)` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 144 | `parser.add_argument("--dry-run", action="store_true", help="no escribe en Shopify")` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 145 | `args = parser.parse_args()` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 146 | `` | Línea en blanco: separa bloques lógicos. |
| 147 | `catalogo = cargar_catalogo()` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 148 | `existentes, nodos = skus_existentes()` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 149 | `print(f"SKUs existentes en la tienda: {len(existentes)}")` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 150 | `` | Línea en blanco: separa bloques lógicos. |
| 151 | `pendientes = [` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 152 | `p for p in catalogo["productos"] if p["sku"] not in existentes` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 153 | `]` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 154 | `print(f"Productos a crear: {len(pendientes)}")` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 155 | `` | Línea en blanco: separa bloques lógicos. |
| 156 | `if args.dry_run:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 157 | `for producto in pendientes:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 158 | `print(f"  [DRY RUN] {producto['sku']} - {producto['nombre']}")` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 159 | `return 0` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 160 | `` | Línea en blanco: separa bloques lógicos. |
| 161 | `location_id = location_principal()` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 162 | `ids_por_sku = {}` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 163 | `for nodo in nodos:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 164 | `for variante in nodo["variants"]["nodes"]:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 165 | `if variante["sku"]:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 166 | `ids_por_sku[variante["sku"]] = nodo["id"]` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 167 | `` | Línea en blanco: separa bloques lógicos. |
| 168 | `for producto in pendientes:` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 169 | `creado = crear_producto(producto, location_id)` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 170 | `ids_por_sku[producto["sku"]] = creado["id"]` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 171 | `print(f"  Creado {producto['sku']} -> {creado['handle']}")` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 172 | `` | Línea en blanco: separa bloques lógicos. |
| 173 | `crear_colecciones(catalogo, ids_por_sku)` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 174 | `return 0` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 175 | `` | Línea en blanco: separa bloques lógicos. |
| 176 | `` | Línea en blanco: separa bloques lógicos. |
| 177 | `if __name__ == "__main__":` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |
| 178 | `raise SystemExit(main())` | Permite importar el módulo de la raíz aunque se ejecute como paquete. |

