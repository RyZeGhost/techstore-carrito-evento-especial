"""Carga y acceso al catálogo compartido por las tres implementaciones.

Este módulo es la única fuente de datos: las tres versiones del carrito
reciben el mismo diccionario, por lo que cualquier diferencia de resultado
se debe al paradigma y no a los datos de entrada.
"""

import json
from pathlib import Path

# Ruta por defecto, calculada desde la ubicación de este archivo y no desde
# el directorio de ejecución, para que funcione desde cualquier carpeta.
RUTA_CATALOGO = Path(__file__).resolve().parent.parent / "datos" / "catalogo.json"


def cargar_catalogo(ruta=RUTA_CATALOGO):
    """Lee el JSON y devuelve un diccionario con la configuración del catálogo."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def indice_productos(catalogo):
    """Construye un índice {sku: producto} para búsquedas O(1)."""
    return {producto["sku"]: producto for producto in catalogo["productos"]}
