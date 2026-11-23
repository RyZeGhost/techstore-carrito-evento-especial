"""Carga, validación y acceso al catálogo compartido por las tres implementaciones.

Este módulo es la única fuente de datos: las tres versiones del carrito
reciben el mismo diccionario, por lo que cualquier diferencia de resultado
se debe al paradigma y no a los datos de entrada.

La validación del esquema evita enviar datos incompletos a Shopify.
"""

import json
from pathlib import Path

# Ruta por defecto, calculada desde la ubicación de este archivo y no desde
# el directorio de ejecución, para que funcione desde cualquier carpeta.
RUTA_CATALOGO = Path(__file__).resolve().parent.parent / "datos" / "catalogo.json"


def validar_catalogo(catalogo):
    """Comprueba que el JSON tenga las claves y tipos que espera el carrito."""
    if not isinstance(catalogo, dict):
        raise ValueError("El catálogo debe ser un objeto JSON")

    for clave in ("moneda", "envio", "recomendaciones", "segmentos", "sustitutos", "productos", "eventos"):
        if clave not in catalogo:
            raise ValueError(f"Falta la clave obligatoria '{clave}' en el catálogo")

    envio = catalogo["envio"]
    for clave in ("costo", "gratis_desde"):
        if not isinstance(envio.get(clave), int) or envio[clave] < 0:
            raise ValueError(f"envio.{clave} debe ser un entero no negativo")

    recomendaciones = catalogo["recomendaciones"]
    for clave in ("por_categoria", "maximo", "descuento_porcentaje"):
        valor = recomendaciones.get(clave)
        if not isinstance(valor, int) or valor < 0:
            raise ValueError(f"recomendaciones.{clave} debe ser un entero no negativo")
    if not isinstance(recomendaciones.get("eventos_festivos"), list):
        raise ValueError("recomendaciones.eventos_festivos debe ser una lista")

    segmentos = catalogo["segmentos"]
    if not isinstance(segmentos, dict) or not segmentos:
        raise ValueError("segmentos debe ser un objeto no vacío")
    for nombre, segmento in segmentos.items():
        porcentaje = segmento.get("descuento_porcentaje")
        if not isinstance(porcentaje, int) or not 0 <= porcentaje <= 100:
            raise ValueError(f"segmentos.{nombre}.descuento_porcentaje debe estar entre 0 y 100")
        if not isinstance(segmento.get("envio_gratis"), bool):
            raise ValueError(f"segmentos.{nombre}.envio_gratis debe ser booleano")
        if segmento.get("recomendacion") not in ("economica", "premium", "alto_ticket"):
            raise ValueError(f"segmentos.{nombre}.recomendacion no válida")

    if not isinstance(catalogo["productos"], list) or not catalogo["productos"]:
        raise ValueError("productos debe ser una lista no vacía")

    skus = set()
    for producto in catalogo["productos"]:
        for clave in ("sku", "nombre", "precio", "stock", "categoria",
                      "descripcion", "imagen"):
            if clave not in producto:
                raise ValueError(f"Falta '{clave}' en el producto {producto.get('sku')}")
        if producto["sku"] in skus:
            raise ValueError(f"SKU duplicado: {producto['sku']}")
        skus.add(producto["sku"])
        if not isinstance(producto["precio"], int) or producto["precio"] <= 0:
            raise ValueError(f"precio inválido en {producto['sku']}")
        if not isinstance(producto["stock"], int) or producto["stock"] < 0:
            raise ValueError(f"stock inválido en {producto['sku']}")
        if not str(producto["imagen"]).startswith("https://"):
            raise ValueError(f"imagen inválida en {producto['sku']}")

    for sku, sustituto in catalogo["sustitutos"].items():
        if sku not in skus or sustituto not in skus:
            raise ValueError(f"Sustituto inválido: {sku} -> {sustituto}")

    if not isinstance(catalogo["eventos"], dict) or not catalogo["eventos"]:
        raise ValueError("eventos debe ser un objeto no vacío")

    for nombre in recomendaciones["eventos_festivos"]:
        if nombre not in catalogo["eventos"]:
            raise ValueError(f"Evento festivo inexistente: {nombre}")

    for nombre, evento in catalogo["eventos"].items():
        for clave in ("nombre", "cupon", "producto_2x1", "reglas"):
            if clave not in evento:
                raise ValueError(f"Falta '{clave}' en el evento {nombre}")
        if evento["producto_2x1"] not in skus:
            raise ValueError(f"producto_2x1 inexistente en el evento {nombre}")
        for regla in evento["reglas"]:
            if regla["sku"] not in skus:
                raise ValueError(f"SKU de regla inexistente: {regla['sku']}")
            if regla["por_persona"] < 0 or regla["minimo"] < 0:
                raise ValueError(f"Cantidades negativas en el evento {nombre}")

    return True


def cargar_catalogo(ruta=RUTA_CATALOGO):
    """Lee el JSON, valida su esquema y devuelve el diccionario del catálogo."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        catalogo = json.load(archivo)
    validar_catalogo(catalogo)
    return catalogo


def indice_productos(catalogo):
    """Construye un índice {sku: producto} para búsquedas O(1)."""
    return {producto["sku"]: producto for producto in catalogo["productos"]}
