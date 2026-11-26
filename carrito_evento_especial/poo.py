"""Carrito Evento Especial - paradigma Orientado a Objetos.

Este módulo modela las dos entidades base del carrito:

* ``Producto``: un SKU del catálogo, con sus datos privados y acceso controlado.
* ``ItemCarrito``: una línea del carrito, con cantidad, precio y descuento privados.

El encapsulamiento se aplica con atributos ``_precio``, ``_stock`` y
``_cantidad``, expuestos solo mediante propiedades ``@property`` que validan el
dominio antes de asignar. Las validaciones lanzan ``ValueError`` o ``TypeError``
para que ningún objeto quede en un estado inválido.

Regla de aislamiento: este archivo se escribió sin leer ni copiar los otros
paradigmas (``imperativo.py`` y ``funcional.py``). La información de precios,
stock y etiquetas sale de ``catalogo_shopify.json``.
"""

import json
from pathlib import Path

RUTA_CATALOGO = Path(__file__).resolve().parent / "catalogo_shopify.json"


class Producto:
    """Representa un producto del catálogo con acceso controlado a sus datos."""

    def __init__(self, sku, titulo, categoria, precio, stock, etiquetas=None, origen=""):
        # Se crean todos los atributos privados antes de usar los setters, para
        # que las validaciones de las propiedades encuentren un estado coherente.
        self._sku = ""
        self._titulo = ""
        self._categoria = ""
        self._precio = 0
        self._stock = 0
        self._etiquetas = []
        self._origen = ""

        self.sku = sku
        self.titulo = titulo
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.etiquetas = etiquetas
        self.origen = origen

    @property
    def sku(self):
        """Identificador del producto; solo se acepta una cadena no vacía."""
        return self._sku

    @sku.setter
    def sku(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("sku debe ser una cadena no vacía")
        self._sku = valor.strip()

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("titulo debe ser una cadena no vacía")
        self._titulo = valor.strip()

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("categoria debe ser una cadena no vacía")
        self._categoria = valor.strip()

    @property
    def precio(self):
        """Precio unitario; se rechazan booleanos, no numéricos y negativos."""
        return self._precio

    @precio.setter
    def precio(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("precio debe ser un número")
        if valor < 0:
            raise ValueError("precio no puede ser negativo")
        self._precio = valor

    @property
    def stock(self):
        """Unidades disponibles; entero no negativo."""
        return self._stock

    @stock.setter
    def stock(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("stock debe ser un entero")
        if valor < 0:
            raise ValueError("stock no puede ser negativo")
        self._stock = valor

    @property
    def etiquetas(self):
        """Devuelve una copia en tupla: el exterior no puede alterar la lista interna."""
        return tuple(self._etiquetas)

    @etiquetas.setter
    def etiquetas(self, valores):
        if valores is None:
            self._etiquetas = []
            return
        if isinstance(valores, str):
            raise TypeError("etiquetas debe ser una colección de cadenas")
        lista = []
        for valor in valores:
            if not isinstance(valor, str):
                raise TypeError("cada etiqueta debe ser una cadena")
            if valor not in lista:
                lista.append(valor)
        self._etiquetas = lista

    @property
    def origen(self):
        return self._origen

    @origen.setter
    def origen(self, valor):
        if not isinstance(valor, str):
            raise TypeError("origen debe ser una cadena")
        self._origen = valor

    def tiene_etiqueta(self, etiqueta):
        """Indica si el producto posee una etiqueta funcional concreta."""
        for propia in self._etiquetas:
            if propia == etiqueta:
                return True
        return False

    def hay_stock(self, cantidad):
        """Comprueba si hay unidades suficientes sin modificar el objeto."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise TypeError("cantidad debe ser un entero")
        if cantidad <= 0:
            raise ValueError("cantidad debe ser mayor a cero")
        return self._stock >= cantidad

    def reservar(self, cantidad):
        """Descuenta unidades del stock interno usando el setter validado."""
        if not self.hay_stock(cantidad):
            raise ValueError("stock insuficiente para reservar la cantidad pedida")
        self.stock = self._stock - cantidad
        return self._stock

    @classmethod
    def desde_dict(cls, datos):
        """Construye un Producto a partir de un elemento del catálogo JSON."""
        return cls(
            sku=datos["sku"],
            titulo=datos["titulo"],
            categoria=datos["categoria"],
            precio=datos["precio"],
            stock=datos["stock"],
            etiquetas=datos.get("tags_funcionales", []),
            origen=datos.get("origen", ""),
        )

    def a_dict(self):
        """Exporta una vista plana del objeto, sin exponer sus atributos privados."""
        vista = {}
        vista["sku"] = self._sku
        vista["titulo"] = self._titulo
        vista["categoria"] = self._categoria
        vista["precio"] = self._precio
        vista["stock"] = self._stock
        vista["etiquetas"] = list(self.etiquetas)
        vista["origen"] = self._origen
        return vista


class ItemCarrito:
    """Representa una línea del carrito con importes calculados y validados."""

    def __init__(self, producto, cantidad, precio_unitario=None, descuento=0, es_regalo=False):
        self._producto = None
        self._cantidad = 0
        self._precio_unitario = 0
        self._descuento = 0
        self._es_regalo = False

        if not isinstance(producto, Producto):
            raise TypeError("producto debe ser una instancia de Producto")
        self._producto = producto

        if precio_unitario is None:
            precio_unitario = producto.precio
        # El orden importa: descuento se valida contra subtotal, que depende de
        # precio_unitario y cantidad, así que esos dos se asignan primero.
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
        self.descuento = descuento
        self._es_regalo = bool(es_regalo)

    @property
    def producto(self):
        return self._producto

    @property
    def sku(self):
        return self._producto.sku

    @property
    def cantidad(self):
        """Unidades de la línea; entero positivo."""
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("cantidad debe ser un entero")
        if valor <= 0:
            raise ValueError("cantidad debe ser mayor a cero")
        self._cantidad = valor

    @property
    def precio_unitario(self):
        """Precio aplicado en la línea; se rechazan negativos y no numéricos."""
        return self._precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("precio_unitario debe ser un número")
        if valor < 0:
            raise ValueError("precio_unitario no puede ser negativo")
        self._precio_unitario = valor

    @property
    def descuento(self):
        """Monto descontado; no puede ser negativo ni mayor que el subtotal."""
        return self._descuento

    @descuento.setter
    def descuento(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("descuento debe ser un número")
        if valor < 0:
            raise ValueError("descuento no puede ser negativo")
        if valor > self.subtotal:
            raise ValueError("descuento no puede superar el subtotal de la línea")
        self._descuento = valor

    @property
    def subtotal(self):
        """Importe antes de descuento, derivado de los atributos privados."""
        return self._precio_unitario * self._cantidad

    @property
    def total(self):
        """Importe final de la línea, derivado del subtotal y el descuento."""
        return self.subtotal - self._descuento

    @property
    def es_regalo(self):
        return self._es_regalo

    def a_dict(self):
        """Exporta la línea como diccionario plano para el JSON de resultado."""
        vista = {}
        vista["sku"] = self.sku
        vista["titulo"] = self._producto.titulo
        vista["categoria"] = self._producto.categoria
        vista["etiquetas"] = list(self._producto.etiquetas)
        vista["cantidad"] = self._cantidad
        vista["precio_unitario"] = self._precio_unitario
        vista["subtotal"] = self.subtotal
        vista["descuento"] = self._descuento
        vista["total"] = self.total
        vista["stock_producto"] = self._producto.stock
        vista["es_regalo"] = self._es_regalo
        return vista


if __name__ == "__main__":
    # Demostración mínima de encapsulamiento con datos reales del catálogo.
    with RUTA_CATALOGO.open(encoding="utf-8") as archivo:
        catalogo = json.load(archivo)

    producto = Producto.desde_dict(catalogo["productos"][0])
    item = ItemCarrito(producto, 2)

    demostracion = {}
    demostracion["producto"] = producto.a_dict()
    demostracion["item"] = item.a_dict()
    print(json.dumps(demostracion, ensure_ascii=False, indent=2))
