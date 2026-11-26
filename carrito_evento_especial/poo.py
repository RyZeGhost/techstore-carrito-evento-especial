"""Carrito Evento Especial - paradigma Orientado a Objetos.

Este módulo modela el agregado completo del carrito:

* ``Producto``: un SKU del catálogo, con sus datos privados y acceso controlado.
* ``ItemCarrito``: una línea del carrito, con cantidad, precio y descuento privados.
* ``CarritoEventoEspecial``: encapsula la colección de líneas, el estado del
  cliente y ejecuta polimórficamente las reglas de configuración del kit.
* ``RepositorioShopifyJSON``: carga el catálogo como ``Producto`` y persiste el
  estado final en ``resultado_poo.json``.

El encapsulamiento se aplica con atributos ``_precio``, ``_stock`` y
``_cantidad``, expuestos solo mediante propiedades ``@property`` que validan el
dominio antes de asignar. Las validaciones lanzan ``ValueError`` o ``TypeError``
para que ningún objeto quede en un estado inválido.

Los métodos especiales ``__str__``, ``__repr__`` y ``__len__`` permiten imprimir
un desglose legible del kit: ``str`` muestra importes y cantidades, ``repr`` da
una forma inequívoca para depuración y ``len`` devuelve el stock de un
``Producto``, las unidades de un ``ItemCarrito`` y las líneas del carrito.

Las reglas convierten entradas inválidas o falta de stock en
``ParametroKitInvalidoError`` y ``StockInsuficienteError``, las capturan con
``try/except`` y las transforman en avisos, de modo que una regla fallida no
detiene la ejecución de las demás.

Regla de aislamiento: este archivo se escribió sin leer ni copiar los otros
paradigmas (``imperativo.py`` y ``funcional.py``). La información de precios,
stock y etiquetas sale de ``catalogo_shopify.json``.
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path

RUTA_CATALOGO = Path(__file__).resolve().parent / "catalogo_shopify.json"


def _pesos(valor):
    """Formatea un importe como pesos chilenos: $24.990 en vez de $24990."""
    return "$" + format(valor, ",.0f").replace(",", ".")


class StockInsuficienteError(ValueError):
    """No hay unidades suficientes para completar una reserva del kit."""


class ParametroKitInvalidoError(ValueError):
    """Un parámetro de entrada del kit tiene tipo o dominio inválido."""


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
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ParametroKitInvalidoError("cantidad debe ser un entero mayor a cero")
        if not self.hay_stock(cantidad):
            raise StockInsuficienteError(
                "stock insuficiente para reservar la cantidad pedida"
            )
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

    def __str__(self):
        """Descripción de una línea de catálogo para el desglose en consola."""
        texto = self._sku + " | " + self._titulo + " | " + self._categoria
        return texto + " | " + _pesos(self._precio) + " | stock " + str(self._stock)

    def __repr__(self):
        """Representación inequívoca, cercana a la firma del constructor."""
        return (
            "Producto(sku=" + repr(self._sku)
            + ", titulo=" + repr(self._titulo)
            + ", categoria=" + repr(self._categoria)
            + ", precio=" + repr(self._precio)
            + ", stock=" + repr(self._stock)
            + ", etiquetas=" + repr(list(self.etiquetas))
            + ", origen=" + repr(self._origen) + ")"
        )

    def __len__(self):
        """El largo de un producto es su stock disponible."""
        return self._stock


class ItemCarrito:
    """Representa una línea del carrito con importes calculados y validados."""

    def __init__(self, producto, cantidad, precio_unitario=None, descuento=0,
                 es_regalo=False, precio_unitario_original=None):
        self._producto = None
        self._cantidad = 0
        self._precio_unitario = 0
        self._precio_unitario_original = 0
        self._descuento = 0
        self._es_regalo = False

        if not isinstance(producto, Producto):
            raise TypeError("producto debe ser una instancia de Producto")
        self._producto = producto

        if precio_unitario is None:
            precio_unitario = producto.precio
        if precio_unitario_original is None:
            precio_unitario_original = precio_unitario
        # El orden importa: descuento se valida contra subtotal, que depende del
        # precio original y la cantidad, así que esos dos se asignan primero.
        self.precio_unitario_original = precio_unitario_original
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
    def precio_unitario_original(self):
        """Precio de lista antes de descuentos; base del subtotal."""
        return self._precio_unitario_original

    @precio_unitario_original.setter
    def precio_unitario_original(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("precio_unitario_original debe ser un número")
        if valor < 0:
            raise ValueError("precio_unitario_original no puede ser negativo")
        self._precio_unitario_original = valor

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
        """Importe antes de descuento, derivado del precio original."""
        return self._precio_unitario_original * self._cantidad

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
        vista["precio_unitario_original"] = self._precio_unitario_original
        vista["subtotal"] = self.subtotal
        vista["descuento"] = self._descuento
        vista["total"] = self.total
        vista["stock_producto"] = self._producto.stock
        vista["es_regalo"] = self._es_regalo
        return vista

    def __str__(self):
        """Línea legible con unidades, precios, descuento y total neto."""
        texto = self.sku + " | " + self._producto.titulo
        texto += " | " + str(self._cantidad) + " x " + _pesos(self._precio_unitario)
        texto += " | subtotal " + _pesos(self.subtotal)
        texto += " | descuento -" + _pesos(self._descuento)
        texto += " | total " + _pesos(self.total)
        if self._es_regalo:
            texto += " | REGALO"
        return texto

    def __repr__(self):
        """Representación unívoca de la línea, sin depender del ``Producto``."""
        return (
            "ItemCarrito(sku=" + repr(self.sku)
            + ", cantidad=" + repr(self._cantidad)
            + ", precio_unitario=" + repr(self._precio_unitario)
            + ", precio_unitario_original=" + repr(self._precio_unitario_original)
            + ", descuento=" + repr(self._descuento)
            + ", es_regalo=" + repr(self._es_regalo) + ")"
        )

    def __len__(self):
        """El largo de una línea es su cantidad de unidades."""
        return self._cantidad


class ReglaConfiguracionKit(ABC):
    """Base abstracta: define la interfaz común de todas las reglas del kit.

    Cada subclase implementa ``aplicar`` y recibe siempre los mismos tres
    argumentos. El polimorfismo permite al motor iterar una lista de reglas
    sin conocer la clase concreta: todas se llaman igual y todas mutan el
    ``carrito`` que se les pasa.
    """

    @abstractmethod
    def aplicar(self, carrito, catalogo, parametros):
        """Aplica la regla; devuelve el ``ItemCarrito`` agregado o ``None``."""
        raise NotImplementedError

    @staticmethod
    def _entero_no_negativo(parametros, clave):
        """Lee un parámetro entero y lo valida con excepción personalizada."""
        valor = parametros.get(clave, 0)
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ParametroKitInvalidoError(clave + " debe ser un entero")
        if valor < 0:
            raise ParametroKitInvalidoError(clave + " no puede ser negativo")
        return valor

    @staticmethod
    def _productos(catalogo):
        """Acepta el dict del JSON o una lista de ``Producto`` ya instanciados."""
        productos = []
        if isinstance(catalogo, dict):
            for datos in catalogo["productos"]:
                productos.append(Producto.desde_dict(datos))
            return productos
        for producto in catalogo:
            if not isinstance(producto, Producto):
                raise TypeError("catalogo debe contener instancias de Producto")
            productos.append(producto)
        return productos

    @staticmethod
    def _registrar_aviso(parametros, mensaje):
        """Acumula avisos en una lista mutable compartida en ``parametros``."""
        if "avisos" not in parametros or not isinstance(parametros["avisos"], list):
            parametros["avisos"] = []
        parametros["avisos"].append(mensaje)

    def _registrar_error(self, parametros, nombre_regla, error):
        """Convierte una excepción controlada en aviso, sin cortar el flujo."""
        mensaje = nombre_regla + " omitida: " + str(error)
        self._registrar_aviso(parametros, mensaje)

    def _seleccionar(self, catalogo, parametros, etiquetas, cantidad,
                     excluidas=None, mensaje_aviso=""):
        """Filtra por etiquetas, ajusta al stock máximo y elige el SKU más barato."""
        if excluidas is None:
            excluidas = []

        elegibles = []
        for producto in self._productos(catalogo):
            cumple = True
            for etiqueta in etiquetas:
                if not producto.tiene_etiqueta(etiqueta):
                    cumple = False
            for etiqueta in excluidas:
                if producto.tiene_etiqueta(etiqueta):
                    cumple = False
            if cumple:
                elegibles.append(producto)

        stock_max = 0
        for producto in elegibles:
            if producto.stock > stock_max:
                stock_max = producto.stock

        # Stock parcial: si sobra demanda pero hay unidades, se ajusta la
        # cantidad y se avisa. Si no hay unidades, la regla lo maneja con
        # StockInsuficienteError dentro de su propio try/except.
        if cantidad > stock_max and stock_max > 0:
            if mensaje_aviso == "":
                mensaje_aviso = "Cantidad ajustada de"
            texto = mensaje_aviso + " " + str(cantidad) + " a " + str(stock_max)
            self._registrar_aviso(parametros, texto + " por stock disponible.")
            cantidad = stock_max

        if stock_max <= 0 or cantidad <= 0:
            return None, 0

        mejor = None
        for producto in elegibles:
            if producto.stock >= cantidad and (mejor is None or producto.precio < mejor.precio):
                mejor = producto
        return mejor, cantidad


class ReglaSensoresApertura(ReglaConfiguracionKit):
    """Agrega ``puertas + ventanas`` sensores, o avisa y omite la regla."""

    def aplicar(self, carrito, catalogo, parametros):
        try:
            cantidad = self._entero_no_negativo(parametros, "puertas")
            cantidad += self._entero_no_negativo(parametros, "ventanas")
            if cantidad == 0:
                return None

            producto, cantidad = self._seleccionar(
                catalogo,
                parametros,
                ["sensor_apertura"],
                cantidad,
                mensaje_aviso="Sensores de apertura ajustados de",
            )
            if producto is None:
                raise StockInsuficienteError(
                    "No hay sensores de apertura con stock suficiente"
                )
            producto.reservar(cantidad)
        except (ParametroKitInvalidoError, StockInsuficienteError) as error:
            self._registrar_error(parametros, "ReglaSensoresApertura", error)
            return None

        item = ItemCarrito(producto, cantidad)
        carrito.append(item)
        return item


class ReglaSensorMovimientoMascotas(ReglaConfiguracionKit):
    """Elige sensores estándar o ``inmune_mascotas``; avisa si falla."""

    def aplicar(self, carrito, catalogo, parametros):
        try:
            cantidad = self._entero_no_negativo(parametros, "cantidad_sensores_movimiento")
            if cantidad == 0:
                return None

            tiene_mascotas = parametros.get("tiene_mascotas", False)
            if not isinstance(tiene_mascotas, bool):
                raise ParametroKitInvalidoError("tiene_mascotas debe ser booleano")

            etiquetas = ["sensor_movimiento"]
            excluidas = []
            if tiene_mascotas:
                etiquetas.append("inmune_mascotas")
            else:
                excluidas.append("inmune_mascotas")

            producto, cantidad = self._seleccionar(
                catalogo,
                parametros,
                etiquetas,
                cantidad,
                excluidas,
                "Sensores de movimiento ajustados de",
            )
            if producto is None:
                raise StockInsuficienteError(
                    "No hay sensores de movimiento con stock suficiente"
                )
            producto.reservar(cantidad)
        except (ParametroKitInvalidoError, StockInsuficienteError) as error:
            self._registrar_error(parametros, "ReglaSensorMovimientoMascotas", error)
            return None

        item = ItemCarrito(producto, cantidad)
        carrito.append(item)
        return item


class ReglaCamarasDescuentoProgresivo(ReglaConfiguracionKit):
    """Aplica la escala exacta de descuento por volumen de cámaras.

    Tramos: 0% para 0 o 1 cámara, 10% para 2 o 3, y 20% para 4 o más. El
    descuento se calcula sobre el precio de lista de cada cámara y solo afecta
    a las líneas de cámaras; los sensores quedan fuera de esta escala.
    """

    @staticmethod
    def porcentaje_descuento(cantidad):
        """Devuelve 0.0, 0.10 o 0.20 según la cantidad pedida de cámaras."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise ParametroKitInvalidoError("cantidad debe ser un entero")
        if cantidad < 0:
            raise ParametroKitInvalidoError("cantidad no puede ser negativa")
        if cantidad >= 4:
            return 0.20
        if cantidad >= 2:
            return 0.10
        return 0.0

    def aplicar(self, carrito, catalogo, parametros):
        try:
            cantidad = self._entero_no_negativo(parametros, "cantidad_camaras")
            if cantidad == 0:
                return None

            # La escala se resuelve antes de elegir el SKU: el porcentaje depende
            # de la cantidad pedida, no del precio del producto seleccionado.
            porcentaje = self.porcentaje_descuento(cantidad)
            producto, cantidad = self._seleccionar(
                catalogo, parametros, ["camara"], cantidad
            )
            if producto is None:
                raise StockInsuficienteError("No hay cámaras con stock suficiente")

            # Descuento por unidad sobre el precio de lista. Se redondea a entero
            # porque el catálogo trabaja en pesos chilenos sin centavos.
            descuento_unitario = int(round(producto.precio * porcentaje))
            precio_unitario = producto.precio - descuento_unitario
            producto.reservar(cantidad)
        except (ParametroKitInvalidoError, StockInsuficienteError) as error:
            self._registrar_error(parametros, "ReglaCamarasDescuentoProgresivo", error)
            return None

        item = ItemCarrito(
            producto,
            cantidad,
            precio_unitario=precio_unitario,
            descuento=descuento_unitario * cantidad,
            precio_unitario_original=producto.precio,
        )
        carrito.append(item)
        return item


class ReglaCartelRegalo(ReglaConfiguracionKit):
    """Inserta un ``ItemCarrito`` promocional del cartel a costo $0.

    Solo se activa si el carrito ya tiene artículos y si queda stock del cartel.
    El precio de lista se informa en ``parametros['regalo']``; la línea del
    carrito mantiene subtotal y descuento en 0 para no alterar los totales.
    """

    @staticmethod
    def _item_promocional(cartel):
        """Construye la línea de regalo con precio final 0 y sin descuento."""
        # ``precio_unitario_original`` queda en 0 a propósito: si guardara el
        # precio de lista, el subtotal del carrito incluiría el regalo y habría
        # que descontarlo para que el total volviera a ser 0.
        return ItemCarrito(cartel, 1, precio_unitario=0, descuento=0, es_regalo=True)

    def aplicar(self, carrito, catalogo, parametros):
        if len(carrito) == 0:
            parametros["regalo"] = {"incluido": False}
            return None

        try:
            cartel = None
            for producto in self._productos(catalogo):
                if producto.tiene_etiqueta("cartel_disuasivo") and producto.stock > 0:
                    cartel = producto
                    break
            if cartel is None:
                raise StockInsuficienteError("no hay stock del cartel disuasivo")

            precio_original = cartel.precio
            cartel.reservar(1)
        except (ParametroKitInvalidoError, StockInsuficienteError) as error:
            parametros["regalo"] = {"incluido": False}
            self._registrar_error(parametros, "ReglaCartelRegalo", error)
            return None

        item = self._item_promocional(cartel)
        carrito.append(item)

        parametros["regalo"] = {
            "incluido": True,
            "sku": cartel.sku,
            "titulo": cartel.titulo,
            "cantidad": 1,
            "precio_original": precio_original,
            "precio_final": 0,
            "subtotal": 0,
        }
        return item


class CarritoEventoEspecial:
    """Agregado que encapsula el carrito, el estado del cliente y las reglas.

    El exterior no manipula la lista de líneas ni el catálogo interno: solo
    interactúa mediante propiedades y métodos. Al ejecutar reglas envía el mismo
    mensaje ``aplicar(carrito, catalogo, parametros)`` a cada objeto, sin conocer
    su clase concreta; por eso el motor es polimórfico.
    """

    def __init__(self, catalogo, puertas=0, ventanas=0, tiene_mascotas=False,
                 cantidad_camaras=0, cantidad_sensores_movimiento=0):
        self._items = []
        self._catalogo = []
        self._puertas = 0
        self._ventanas = 0
        self._tiene_mascotas = False
        self._cantidad_camaras = 0
        self._cantidad_sensores_movimiento = 0
        self._avisos = []
        self._regalo = {"incluido": False}

        self.catalogo = catalogo
        self.puertas = puertas
        self.ventanas = ventanas
        self.tiene_mascotas = tiene_mascotas
        self.cantidad_camaras = cantidad_camaras
        self.cantidad_sensores_movimiento = cantidad_sensores_movimiento

    @staticmethod
    def _validar_entero(nombre, valor):
        """Centraliza la validación de dominio de los enteros del cliente."""
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError(nombre + " debe ser un entero")
        if valor < 0:
            raise ValueError(nombre + " no puede ser negativo")
        return valor

    @property
    def items(self):
        """Copia en tupla de las líneas: el exterior no puede agregar ni quitar."""
        return tuple(self._items)

    @property
    def cantidad_items(self):
        return len(self._items)

    @property
    def catalogo(self):
        """Copia en tupla de los ``Producto`` internos, con su stock ya reservado."""
        return tuple(self._catalogo)

    @catalogo.setter
    def catalogo(self, valor):
        """Acepta el dict del JSON o ``Producto`` y guarda copias privadas.

        Al clonar cada producto, las reservas de stock de las reglas quedan
        confinadas al carrito y no alteran el diccionario original del JSON ni
        los objetos que el llamador pudiera conservar fuera de la clase.
        """
        productos = []
        if isinstance(valor, dict):
            datos_productos = valor.get("productos")
            if not isinstance(datos_productos, list):
                raise TypeError("catalogo debe tener una lista 'productos'")
            for datos in datos_productos:
                productos.append(Producto.desde_dict(datos))
        else:
            if isinstance(valor, (str, bytes)):
                raise TypeError("catalogo debe ser un dict o una colección de Producto")
            for producto in valor:
                if not isinstance(producto, Producto):
                    raise TypeError("catalogo debe contener instancias de Producto")
                productos.append(Producto(
                    sku=producto.sku,
                    titulo=producto.titulo,
                    categoria=producto.categoria,
                    precio=producto.precio,
                    stock=producto.stock,
                    etiquetas=producto.etiquetas,
                    origen=producto.origen,
                ))
        self._catalogo = productos

    @property
    def puertas(self):
        return self._puertas

    @puertas.setter
    def puertas(self, valor):
        self._puertas = self._validar_entero("puertas", valor)

    @property
    def ventanas(self):
        return self._ventanas

    @ventanas.setter
    def ventanas(self, valor):
        self._ventanas = self._validar_entero("ventanas", valor)

    @property
    def tiene_mascotas(self):
        return self._tiene_mascotas

    @tiene_mascotas.setter
    def tiene_mascotas(self, valor):
        if not isinstance(valor, bool):
            raise TypeError("tiene_mascotas debe ser booleano")
        self._tiene_mascotas = valor

    @property
    def cantidad_camaras(self):
        return self._cantidad_camaras

    @cantidad_camaras.setter
    def cantidad_camaras(self, valor):
        self._cantidad_camaras = self._validar_entero("cantidad_camaras", valor)

    @property
    def cantidad_sensores_movimiento(self):
        return self._cantidad_sensores_movimiento

    @cantidad_sensores_movimiento.setter
    def cantidad_sensores_movimiento(self, valor):
        self._cantidad_sensores_movimiento = self._validar_entero(
            "cantidad_sensores_movimiento", valor
        )

    @property
    def avisos(self):
        return list(self._avisos)

    @property
    def regalo(self):
        return dict(self._regalo)

    @property
    def subtotal(self):
        """Suma derivada de las líneas; no se almacena para evitar duplicar estado."""
        total = 0
        for item in self._items:
            total += item.subtotal
        return total

    @property
    def descuento_total(self):
        total = 0
        for item in self._items:
            total += item.descuento
        return total

    @property
    def total_final(self):
        return self.subtotal - self.descuento_total

    def agregar_item(self, item):
        """Incorpora una línea validada a la colección privada."""
        if not isinstance(item, ItemCarrito):
            raise TypeError("item debe ser una instancia de ItemCarrito")
        self._items.append(item)
        return item

    def _parametros(self):
        """Traduce el estado privado al dict que espera ``ReglaConfiguracionKit``."""
        parametros = {}
        parametros["puertas"] = self._puertas
        parametros["ventanas"] = self._ventanas
        parametros["tiene_mascotas"] = self._tiene_mascotas
        parametros["cantidad_camaras"] = self._cantidad_camaras
        parametros["cantidad_sensores_movimiento"] = self._cantidad_sensores_movimiento
        # Se comparte la lista real para que los avisos de las reglas queden en
        # el estado del carrito; el dict de regalo se vuelve a leer tras cada regla.
        parametros["avisos"] = self._avisos
        parametros["regalo"] = self._regalo
        return parametros

    def ejecutar_reglas(self, reglas):
        """Aplica cada regla con el mismo mensaje y devuelve las que se ejecutaron.

        El ``carrito`` y el ``catalogo`` que se pasan son los objetos privados
        reales: las reglas agregan líneas y descuentan stock sobre el estado del
        agregado, no sobre copias desechables.
        """
        if isinstance(reglas, (str, bytes)):
            raise TypeError("reglas debe ser una colección de ReglaConfiguracionKit")

        aplicadas = []
        for regla in reglas:
            if not isinstance(regla, ReglaConfiguracionKit):
                raise TypeError(
                    "cada regla debe ser una instancia de ReglaConfiguracionKit"
                )
            parametros = self._parametros()
            regla.aplicar(self._items, self._catalogo, parametros)
            self._regalo = parametros.get("regalo", self._regalo)
            aplicadas.append(regla)
        return tuple(aplicadas)

    def a_dict(self):
        """Exporta una vista completa y plana del estado del agregado."""
        vista = {}

        cliente = {}
        cliente["puertas"] = self._puertas
        cliente["ventanas"] = self._ventanas
        cliente["tiene_mascotas"] = self._tiene_mascotas
        cliente["cantidad_camaras"] = self._cantidad_camaras
        cliente["cantidad_sensores_movimiento"] = self._cantidad_sensores_movimiento
        vista["cliente"] = cliente

        lineas = []
        for item in self._items:
            lineas.append(item.a_dict())
        vista["carrito"] = lineas
        vista["regalo"] = dict(self._regalo)

        resumen = {}
        resumen["cantidad_items"] = self.cantidad_items
        resumen["subtotal"] = self.subtotal
        resumen["descuento_total"] = self.descuento_total
        resumen["total_final"] = self.total_final
        vista["resumen"] = resumen

        inventario = {}
        for producto in self._catalogo:
            inventario[producto.sku] = producto.stock
        vista["inventario"] = inventario
        vista["avisos"] = list(self._avisos)
        return vista

    def __str__(self):
        """Desglose completo del kit, listo para imprimir en consola."""
        lineas = []
        lineas.append("Kit de Seguridad Residencial")
        cliente = "Cliente: " + str(self._puertas) + " puertas, " + str(self._ventanas)
        cliente += " ventanas, mascotas: " + ("si" if self._tiene_mascotas else "no")
        cliente += ", camaras: " + str(self._cantidad_camaras)
        cliente += ", sensores movimiento: " + str(self._cantidad_sensores_movimiento)
        lineas.append(cliente)
        lineas.append("-" * 68)

        numero = 0
        for item in self._items:
            numero += 1
            lineas.append(str(numero) + ". " + str(item))

        lineas.append("-" * 68)
        lineas.append("Subtotal: " + _pesos(self.subtotal))
        lineas.append("Descuento: -" + _pesos(self.descuento_total))
        lineas.append("Total final: " + _pesos(self.total_final))
        if self._regalo.get("incluido"):
            precio = self._regalo.get("precio_original") or 0
            lineas.append("Regalo: " + str(self._regalo.get("sku"))
                          + " (normalmente " + _pesos(precio) + ")")
        else:
            lineas.append("Regalo: no incluido")

        if self._avisos:
            for aviso in self._avisos:
                lineas.append("Aviso: " + aviso)
        else:
            lineas.append("Avisos: ninguno")
        return "\n".join(lineas)

    def __repr__(self):
        """Representación unívoca del estado del cliente y del total."""
        return (
            "CarritoEventoEspecial(puertas=" + repr(self._puertas)
            + ", ventanas=" + repr(self._ventanas)
            + ", tiene_mascotas=" + repr(self._tiene_mascotas)
            + ", cantidad_camaras=" + repr(self._cantidad_camaras)
            + ", cantidad_sensores_movimiento=" + repr(self._cantidad_sensores_movimiento)
            + ", items=" + repr(self.cantidad_items)
            + ", total_final=" + repr(self.total_final) + ")"
        )

    def __len__(self):
        """El largo del carrito es la cantidad de líneas que contiene."""
        return self.cantidad_items


class RepositorioShopifyJSON:
    """Persistencia JSON: carga el catálogo y guarda el resultado del carrito.

    Mantiene privadas las rutas y expone solo dos operaciones: ``cargar_catalogo``
    devuelve ``Producto`` ya instanciados y ``exportar_resultado`` escribe el
    estado final del agregado con el mismo formato determinista en todas las
    ejecuciones.
    """

    def __init__(self, ruta_catalogo=None, ruta_resultado=None):
        self._ruta_catalogo = RUTA_CATALOGO
        self._ruta_resultado = RUTA_CATALOGO.parent / "resultado_poo.json"
        if ruta_catalogo is not None:
            self.ruta_catalogo = ruta_catalogo
        if ruta_resultado is not None:
            self.ruta_resultado = ruta_resultado

    @staticmethod
    def _validar_ruta(nombre, valor):
        """Acepta ``str`` o ``Path`` y exige extensión JSON."""
        if isinstance(valor, Path):
            ruta = valor
        elif isinstance(valor, str) and valor.strip():
            ruta = Path(valor)
        else:
            raise TypeError(nombre + " debe ser una cadena o pathlib.Path")
        if ruta.suffix.lower() != ".json":
            raise ValueError(nombre + " debe terminar en .json")
        return ruta

    @property
    def ruta_catalogo(self):
        return self._ruta_catalogo

    @ruta_catalogo.setter
    def ruta_catalogo(self, valor):
        self._ruta_catalogo = self._validar_ruta("ruta_catalogo", valor)

    @property
    def ruta_resultado(self):
        return self._ruta_resultado

    @ruta_resultado.setter
    def ruta_resultado(self, valor):
        self._ruta_resultado = self._validar_ruta("ruta_resultado", valor)

    def cargar_catalogo(self):
        """Lee el archivo JSON y devuelve una lista de ``Producto``."""
        with self._ruta_catalogo.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if not isinstance(datos, dict) or not isinstance(datos.get("productos"), list):
            raise ValueError("catalogo_shopify.json debe contener una lista 'productos'")

        productos = []
        for fila in datos["productos"]:
            productos.append(Producto.desde_dict(fila))
        return productos

    def exportar_resultado(self, carrito):
        """Serializa el estado final del agregado y devuelve la ruta escrita."""
        if not isinstance(carrito, CarritoEventoEspecial):
            raise TypeError("carrito debe ser una instancia de CarritoEventoEspecial")

        contenido = carrito.a_dict()
        # newline="\n" evita que Windows convierta los saltos en CRLF: el JSON
        # resultante es byte-idéntico en cualquier sistema operativo.
        with self._ruta_resultado.open("w", encoding="utf-8", newline="\n") as archivo:
            json.dump(contenido, archivo, ensure_ascii=False, indent=2)
            archivo.write("\n")
        return self._ruta_resultado


if __name__ == "__main__":
    # El repositorio entrega ``Producto`` instanciados; el agregado los clona
    # para que las reservas de stock no modifiquen los objetos cargados.
    repositorio = RepositorioShopifyJSON()
    productos = repositorio.cargar_catalogo()

    carrito = CarritoEventoEspecial(
        catalogo=productos,
        puertas=2,
        ventanas=4,
        tiene_mascotas=True,
        cantidad_camaras=3,
        cantidad_sensores_movimiento=2,
    )

    reglas = []
    reglas.append(ReglaSensoresApertura())
    reglas.append(ReglaSensorMovimientoMascotas())
    reglas.append(ReglaCamarasDescuentoProgresivo())
    reglas.append(ReglaCartelRegalo())

    carrito.ejecutar_reglas(reglas)
    repositorio.exportar_resultado(carrito)
    # str(carrito) imprime el desglose; el JSON ya quedó en resultado_poo.json.
    print(carrito)
