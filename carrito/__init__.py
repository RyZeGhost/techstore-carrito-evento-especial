"""Paquete con las tres implementaciones del Carrito Evento Especial."""

from carrito.datos import cargar_catalogo
from carrito.funcional import armar_carrito as armar_funcional
from carrito.imperativo import armar_carrito as armar_imperativo
from carrito.orientado_objetos import armar_carrito as armar_objetos

__all__ = [
    "cargar_catalogo",
    "armar_imperativo",
    "armar_objetos",
    "armar_funcional",
]
