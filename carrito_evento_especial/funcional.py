"""Carrito Evento Especial - paradigma estrictamente funcional.

Reglas cumplidas:

* Todas las estructuras de dominio son ``@dataclass(frozen=True)`` o
  ``NamedTuple``, y sus colecciones son ``tuple``.
* No hay ``.append()``, ni asignación de atributos: cada regla devuelve un
  ``Estado`` nuevo con ``dataclasses.replace``.
* No hay diccionarios mutables en la lógica: el catálogo entrante se envuelve
  en ``MappingProxyType`` y el resultado se modela con ``ResultadoKit``.
* ``map``, ``filter``, ``reduce`` y ``componer`` resuelven selección, stock,
  totales y composición del pipeline.

Los únicos contenedores mutables se materializan en la frontera de E/S:
``desbloquear`` crea dicts/listas planos para que ``json.dump`` pueda escribir
``resultado_funcional.json``. Ninguna función de negocio los recibe ni los
modifica.

Regla de aislamiento: este archivo se escribió sin leer ni copiar los otros
paradigmas (``imperativo.py`` y ``poo.py``). Los datos salen de
``catalogo_shopify.json``.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from functools import partial, reduce
from pathlib import Path
from types import MappingProxyType
from typing import Callable, NamedTuple

RUTA_CATALOGO = Path(__file__).resolve().parent / "catalogo_shopify.json"
RUTA_RESULTADO = Path(__file__).resolve().parent / "resultado_funcional.json"


# ---------------------------------------------------------------------------
# Utilidades funcionales
# ---------------------------------------------------------------------------


def componer(*funciones: Callable) -> Callable:
    """
    Firma: componer(*funciones: Callable) -> Callable

    Descripción: compone funciones de derecha a izquierda;
    componer(f, g)(x) equivale a f(g(x)).
    Pureza referencial: con las mismas funciones devuelve siempre el mismo
    cierre y no consulta estado externo.
    Inmutabilidad: no altera las funciones recibidas; cada paso de reduce
    crea un cierre nuevo sin mutar el acumulador.
    Orden superior: reduce sobre la tupla de funciones.
    """
    return reduce(
        lambda acumulada, siguiente: lambda valor: acumulada(siguiente(valor)),
        funciones,
        lambda valor: valor,
    )


# Alias conservado para el código que ya usaba el nombre en inglés.
compose = componer


def pesos(valor: int) -> str:
    """
    Firma: pesos(valor: int) -> str

    Descripción: formatea un entero como peso chileno con punto de miles.
    Pureza referencial: el mismo valor produce siempre la misma cadena;
    no hay lectura de archivos ni de estado global.
    Inmutabilidad: solo construye cadenas nuevas con format y replace.
    Orden superior: componer encadena dos funciones puras de formato.
    """
    return componer(
        lambda texto: "$" + texto.replace(",", "."),
        lambda numero: format(numero, ",.0f"),
    )(valor)


# ---------------------------------------------------------------------------
# Estructuras inmutables del catálogo, los ítems y el estado
# ---------------------------------------------------------------------------


class TramoDescuento(NamedTuple):
    """Tramo de descuento por volumen; ``maximo=None`` es sin límite."""

    minimo: int
    maximo: int | None
    porcentaje: float


@dataclass(frozen=True)
class Producto:
    """SKU del catálogo; etiquetas inmutables como tupla."""

    sku: str
    titulo: str
    categoria: str
    precio: int
    stock: int
    etiquetas: tuple[str, ...]
    origen: str = ""

    def tiene_etiqueta(self, etiqueta: str) -> bool:
        """
        Firma: tiene_etiqueta(self, etiqueta: str) -> bool

        Descripción: indica si el producto lleva una etiqueta dada.
        Pureza referencial: la respuesta depende solo de self y del argumento.
        Inmutabilidad: lee la tupla etiquetas congelada sin exponerla ni cambiarla.
        Orden superior: ninguna; usa la pertenencia directa en la tupla.
        """
        return etiqueta in self.etiquetas

    def con_stock(self, cantidad: int) -> "Producto":
        """
        Firma: con_stock(self, cantidad: int) -> "Producto"

        Descripción: produce un producto con otro stock reservado.
        Pureza referencial: los mismos self y cantidad dan el mismo producto.
        Inmutabilidad: dataclasses.replace crea otra instancia; self queda intacto.
        Orden superior: ninguna; delega en replace.
        """
        return replace(self, stock=cantidad)


@dataclass(frozen=True)
class ItemCarrito:
    """Línea inmutable con importes derivados como propiedades."""

    producto: Producto
    cantidad: int
    precio_unitario: int
    precio_unitario_original: int
    descuento: int
    es_regalo: bool = False

    @property
    def sku(self) -> str:
        """
        Firma: sku(self) -> str

        Descripción: expone el SKU del producto contenido en la línea.
        Pureza referencial: lee solo un campo determinista del producto.
        Inmutabilidad: propiedad de solo lectura sobre una instancia congelada.
        Orden superior: ninguna.
        """
        return self.producto.sku

    @property
    def subtotal(self) -> int:
        """
        Firma: subtotal(self) -> int

        Descripción: calcula precio_unitario_original por cantidad.
        Pureza referencial: dos campos inmutables fijan siempre el mismo valor.
        Inmutabilidad: el importe se deriva, no se almacena ni se escribe.
        Orden superior: ninguna.
        """
        return self.precio_unitario_original * self.cantidad

    @property
    def total(self) -> int:
        """
        Firma: total(self) -> int

        Descripción: calcula subtotal menos descuento de la línea.
        Pureza referencial: compone dos propiedades puras sin efectos externos.
        Inmutabilidad: solo lectura; no modifica el item.
        Orden superior: ninguna.
        """
        return self.subtotal - self.descuento


@dataclass(frozen=True)
class Cliente:
    """Entradas del cliente que alimentan las reglas del kit."""

    puertas: int
    ventanas: int
    tiene_mascotas: bool
    cantidad_camaras: int
    cantidad_sensores_movimiento: int


def cantidad_positiva(valor: int) -> int:
    """
    Firma: cantidad_positiva(valor: int) -> int

    Descripción: normaliza una entrada a entero positivo o cero.
    Pureza referencial: valida solo el argumento y es determinista.
    Inmutabilidad: devuelve el propio entero o cero; no hay escritura.
    Orden superior: ninguna.
    """
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        return 0
    return valor


def normalizar_cliente(cliente: Cliente) -> Cliente:
    """
    Firma: normalizar_cliente(cliente: Cliente) -> Cliente

    Descripción: sanea las cantidades no positivas del cliente.
    Pureza referencial: el cliente saneado depende solo del recibido.
    Inmutabilidad: replace crea un Cliente nuevo; el original no se toca.
    Orden superior: ninguna; aplica cantidad_positiva campo por campo.
    """
    return replace(
        cliente,
        puertas=cantidad_positiva(cliente.puertas),
        ventanas=cantidad_positiva(cliente.ventanas),
        cantidad_camaras=cantidad_positiva(cliente.cantidad_camaras),
        cantidad_sensores_movimiento=cantidad_positiva(
            cliente.cantidad_sensores_movimiento
        ),
    )


@dataclass(frozen=True)
class Regalo:
    """Estado del obsequio; la instancia vacía es el valor neutral."""

    incluido: bool = False
    sku: str = ""
    titulo: str = ""
    cantidad: int = 0
    precio_original: int = 0
    precio_final: int = 0
    subtotal: int = 0


@dataclass(frozen=True)
class ReglasKit:
    """Parámetros congelados de las reglas."""

    etiqueta_apertura: str = "sensor_apertura"
    etiqueta_movimiento: str = "sensor_movimiento"
    etiqueta_inmune: str = "inmune_mascotas"
    etiqueta_camara: str = "camara"
    etiqueta_regalo: str = "cartel_disuasivo"
    tramos_camaras: tuple[TramoDescuento, ...] = (
        TramoDescuento(2, 3, 0.10),
        TramoDescuento(4, None, 0.20),
    )


@dataclass(frozen=True)
class Estado:
    """Estado completo del kit; cada regla devuelve una copia nueva."""

    catalogo: tuple[Producto, ...]
    cliente: Cliente
    items: tuple[ItemCarrito, ...] = ()
    avisos: tuple[str, ...] = ()
    regalo: Regalo = field(default_factory=Regalo)


# ---------------------------------------------------------------------------
# Estructuras inmutables del resultado
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MapeoInmutable(Mapping):
    """Mapeo de solo lectura respaldado por una tupla de pares, sin dicts."""

    pares: tuple[tuple[str, object], ...]

    def __getitem__(self, clave: str) -> object:
        """
        Firma: __getitem__(self, clave: str) -> object

        Descripción: busca una clave recorriendo la tupla de pares.
        Pureza referencial: la misma clave da siempre el mismo valor o KeyError.
        Inmutabilidad: recorre pares sin construir ni mutar un dict.
        Orden superior: ninguna; bucle de lectura directa.
        """
        for nombre, valor in self.pares:
            if nombre == clave:
                return valor
        raise KeyError(clave)

    def __iter__(self):
        """
        Firma: __iter__(self)

        Descripción: itera las claves en el orden original de la tupla.
        Pureza referencial: el orden de claves está fijado por pares.
        Inmutabilidad: el generador lee la tupla y no la modifica.
        Orden superior: expresión generadora; no usa map, filter ni reduce.
        """
        return (nombre for nombre, _ in self.pares)

    def __len__(self) -> int:
        """
        Firma: __len__(self) -> int

        Descripción: devuelve la cantidad de pares del mapeo.
        Pureza referencial: len de una tupla inmutable es determinista.
        Inmutabilidad: operación de solo lectura.
        Orden superior: ninguna.
        """
        return len(self.pares)


@dataclass(frozen=True)
class LineaResultado:
    """Vista plana e inmutable de una línea del carrito."""

    sku: str
    titulo: str
    categoria: str
    etiquetas: tuple[str, ...]
    cantidad: int
    precio_unitario: int
    precio_unitario_original: int
    subtotal: int
    descuento: int
    total: int
    stock_producto: int
    es_regalo: bool


@dataclass(frozen=True)
class ResumenCarrito:
    """Totales financieros consolidados de los ítems del carrito."""

    subtotal: int = 0
    descuento_total: int = 0
    total_final: int = 0


def resumen_carrito_desde_items(
    items: tuple[ItemCarrito, ...],
) -> ResumenCarrito:
    """
    Firma: resumen_carrito_desde_items(
        items: tuple[ItemCarrito, ...],
    ) -> ResumenCarrito

    Descripción: consolida la tupla final de ítems en un ResumenCarrito.
    Pureza referencial: la suma de propiedades fijas da el mismo resumen.
    Inmutabilidad: replace produce otro acumulador en cada paso; los ítems
    de entrada quedan intactos.
    Orden superior: reduce con valor inicial ResumenCarrito().
    """
    return reduce(
        lambda acumulado, item: replace(
            acumulado,
            subtotal=acumulado.subtotal + item.subtotal,
            descuento_total=acumulado.descuento_total + item.descuento,
            total_final=acumulado.total_final + item.total,
        ),
        items,
        ResumenCarrito(),
    )


@dataclass(frozen=True)
class Resumen:
    """Totales derivados, calculados con ``reduce``."""

    cantidad_items: int
    subtotal: int
    descuento_total: int
    total_final: int


@dataclass(frozen=True)
class ResultadoKit:
    """Resultado completo del kit sin un solo diccionario mutable."""

    cliente: Cliente
    carrito: tuple[LineaResultado, ...]
    regalo: Regalo
    resumen: Resumen
    inventario: tuple[tuple[str, int], ...]
    avisos: tuple[str, ...]


REGLAS = ReglasKit()
CLIENTE_PRUEBA = Cliente(
    puertas=2,
    ventanas=4,
    tiene_mascotas=True,
    cantidad_camaras=3,
    cantidad_sensores_movimiento=2,
)


# ---------------------------------------------------------------------------
# Funciones puras de apoyo
# ---------------------------------------------------------------------------


def producto_desde_dict(datos: Mapping) -> Producto:
    """
    Firma: producto_desde_dict(datos: Mapping) -> Producto

    Descripción: construye un Producto desde un mapeo de solo lectura.
    Pureza referencial: los mismos datos producen el mismo producto.
    Inmutabilidad: convierte etiquetas en tuple y crea una instancia nueva.
    Orden superior: ninguna.
    """
    return Producto(
        sku=datos["sku"],
        titulo=datos["titulo"],
        categoria=datos["categoria"],
        precio=int(datos["precio"]),
        stock=int(datos["stock"]),
        etiquetas=tuple(datos.get("tags_funcionales", ())),
        origen=datos.get("origen", ""),
    )


def catalogo_desde_dict(datos: Mapping) -> tuple[Producto, ...]:
    """
    Firma: catalogo_desde_dict(datos: Mapping) -> tuple[Producto, ...]

    Descripción: convierte la lista de productos del JSON en una tupla.
    Pureza referencial: mapea cada entrada de forma determinista.
    Inmutabilidad: tuple(map(...)) crea una colección nueva; datos intactos.
    Orden superior: map con producto_desde_dict.
    """
    return tuple(map(producto_desde_dict, tuple(datos["productos"])))


def filtrar_por_etiquetas(
    productos: tuple[Producto, ...],
    incluidas: tuple[str, ...],
    excluidas: tuple[str, ...] = (),
) -> tuple[Producto, ...]:
    """
    Firma: filtrar_por_etiquetas(
        productos: tuple[Producto, ...],
        incluidas: tuple[str, ...],
        excluidas: tuple[str, ...] = (),
    ) -> tuple[Producto, ...]

    Descripción: filtra productos por etiquetas incluidas y excluidas.
    Pureza referencial: el predicado depende solo de etiquetas y producto.
    Inmutabilidad: devuelve una tupla nueva; la entrada no se altera.
    Orden superior: filter con predicado que usa map sobre ambas tuplas.
    """
    return tuple(
        filter(
            lambda producto: (
                all(map(lambda e: producto.tiene_etiqueta(e), incluidas))
                and not any(map(lambda e: producto.tiene_etiqueta(e), excluidas))
            ),
            productos,
        )
    )


def _cumple_mascotas(
    producto: Producto, tiene_mascotas: bool, reglas: ReglasKit
) -> bool:
    """
    Firma: _cumple_mascotas(
        producto: Producto, tiene_mascotas: bool, reglas: ReglasKit
    ) -> bool

    Descripción: exige inmunidad si hay mascotas y la excluye si no.
    Pureza referencial: depende solo de la etiqueta y de la bandera.
    Inmutabilidad: consulta etiquetas sin modificar producto ni reglas.
    Orden superior: ninguna.
    """
    inmune = producto.tiene_etiqueta(reglas.etiqueta_inmune)
    return inmune if tiene_mascotas else not inmune


def sensores_apertura_disponibles(
    catalogo: tuple[Producto, ...], reglas: ReglasKit = REGLAS
) -> tuple[Producto, ...]:
    """
    Firma: sensores_apertura_disponibles(
        catalogo: tuple[Producto, ...], reglas: ReglasKit = REGLAS
    ) -> tuple[Producto, ...]

    Descripción: extrae sensores de apertura con stock positivo.
    Pureza referencial: filtra por etiqueta y stock sin estado oculto.
    Inmutabilidad: filter sobre generadora devuelve una tupla nueva.
    Orden superior: filter aplicado a una expresión generadora.
    """
    return tuple(
        filter(
            lambda producto: producto.stock > 0,
            (
                producto
                for producto in catalogo
                if producto.tiene_etiqueta(reglas.etiqueta_apertura)
            ),
        )
    )


def sensores_movimiento_disponibles(
    catalogo: tuple[Producto, ...],
    tiene_mascotas: bool,
    reglas: ReglasKit = REGLAS,
) -> tuple[Producto, ...]:
    """
    Firma: sensores_movimiento_disponibles(
        catalogo: tuple[Producto, ...],
        tiene_mascotas: bool,
        reglas: ReglasKit = REGLAS,
    ) -> tuple[Producto, ...]

    Descripción: extrae sensores de movimiento según tiene_mascotas.
    Pureza referencial: la bandera y las etiquetas fijan el resultado.
    Inmutabilidad: solo lectura del catálogo; devuelve tupla nueva.
    Orden superior: filter sobre generadora con _cumple_mascotas.
    """
    return tuple(
        filter(
            lambda producto: producto.stock > 0,
            (
                producto
                for producto in catalogo
                if producto.tiene_etiqueta(reglas.etiqueta_movimiento)
                and _cumple_mascotas(producto, tiene_mascotas, reglas)
            ),
        )
    )


def camaras_disponibles(
    catalogo: tuple[Producto, ...], reglas: ReglasKit = REGLAS
) -> tuple[Producto, ...]:
    """
    Firma: camaras_disponibles(
        catalogo: tuple[Producto, ...], reglas: ReglasKit = REGLAS
    ) -> tuple[Producto, ...]

    Descripción: extrae cámaras con stock positivo del catálogo.
    Pureza referencial: depende solo de etiqueta camara y stock.
    Inmutabilidad: devuelve tupla nueva sin tocar el catálogo.
    Orden superior: filter sobre una expresión generadora.
    """
    return tuple(
        filter(
            lambda producto: producto.stock > 0,
            (
                producto
                for producto in catalogo
                if producto.tiene_etiqueta(reglas.etiqueta_camara)
            ),
        )
    )


def cartel_disuasivo_disponible(
    catalogo: tuple[Producto, ...], reglas: ReglasKit = REGLAS
) -> Producto | None:
    """
    Firma: cartel_disuasivo_disponible(
        catalogo: tuple[Producto, ...], reglas: ReglasKit = REGLAS
    ) -> Producto | None

    Descripción: devuelve el primer cartel con stock o None.
    Pureza referencial: next sobre el mismo iterable da el mismo resultado.
    Inmutabilidad: no modifica productos; entrega una referencia congelada.
    Orden superior: filter sobre generadora, seguido de next.
    """
    return next(
        filter(
            lambda producto: producto.stock > 0,
            (
                producto
                for producto in catalogo
                if producto.tiene_etiqueta(reglas.etiqueta_regalo)
            ),
        ),
        None,
    )


def seleccionar(
    productos: tuple[Producto, ...],
    cantidad: int,
    incluidas: tuple[str, ...],
    excluidas: tuple[str, ...] = (),
    mensaje_aviso: str = "",
) -> tuple[Producto | None, int, tuple[str, ...]]:
    """
    Firma: seleccionar(
        productos: tuple[Producto, ...],
        cantidad: int,
        incluidas: tuple[str, ...],
        excluidas: tuple[str, ...] = (),
        mensaje_aviso: str = "",
    ) -> tuple[Producto | None, int, tuple[str, ...]]

    Descripción: elige el SKU más barato con stock y ajusta stock parcial.
    Pureza referencial: min por precio y SKU es determinista; avisa si ajusta.
    Inmutabilidad: no cambia stocks; devuelve producto y tuplas nuevas.
    Orden superior: filter de candidatos y map para calcular stock máximo.
    """
    if cantidad_positiva(cantidad) == 0:
        return None, 0, ()
    elegibles = filtrar_por_etiquetas(productos, incluidas, excluidas)
    stock_maximo = max(map(lambda p: p.stock, elegibles), default=0)
    if stock_maximo <= 0:
        return None, 0, ()

    avisos: tuple[str, ...] = ()
    if cantidad > stock_maximo:
        prefijo = mensaje_aviso or "Cantidad ajustada de"
        avisos = (
            prefijo + " " + str(cantidad) + " a " + str(stock_maximo)
            + " por stock disponible.",
        )
        cantidad = stock_maximo

    if cantidad <= 0:
        return None, 0, avisos

    candidatos = tuple(filter(lambda p: p.stock >= cantidad, elegibles))
    if not candidatos:
        return None, 0, avisos

    elegido = min(candidatos, key=lambda p: (p.precio, p.sku))
    return elegido, cantidad, avisos


def reemplazar_producto(
    catalogo: tuple[Producto, ...], producto: Producto
) -> tuple[Producto, ...]:
    """
    Firma: reemplazar_producto(
        catalogo: tuple[Producto, ...], producto: Producto
    ) -> tuple[Producto, ...]

    Descripción: sustituye en el catálogo el producto con el mismo SKU.
    Pureza referencial: la comparación por SKU fija la salida.
    Inmutabilidad: map construye una tupla nueva; catálogo intacto.
    Orden superior: map sobre el catálogo.
    """
    return tuple(
        map(lambda actual: producto if actual.sku == producto.sku else actual,
            catalogo)
    )


def porcentaje_camaras(cantidad: int, reglas: ReglasKit = REGLAS) -> float:
    """
    Firma: porcentaje_camaras(cantidad: int, reglas: ReglasKit = REGLAS) -> float

    Descripción: resuelve el tramo de descuento 10 o 20 por cámara.
    Pureza referencial: cantidad y reglas fijan el porcentaje o 0.0.
    Inmutabilidad: lee la tupla tramos_camaras sin modificarla.
    Orden superior: filter sobre los tramos con next.
    """
    if isinstance(cantidad, bool) or not isinstance(cantidad, int):
        raise ValueError("cantidad de cámaras debe ser un entero no negativo")
    if cantidad <= 0:
        return 0.0
    tramo = next(
        filter(
            lambda t: cantidad >= t.minimo
            and (t.maximo is None or cantidad <= t.maximo),
            reglas.tramos_camaras,
        ),
        None,
    )
    return tramo.porcentaje if tramo is not None else 0.0


# ---------------------------------------------------------------------------
# Transformaciones puras con map: productos filtrados -> tupla de ítems
# ---------------------------------------------------------------------------


def item_desde_producto(producto: Producto, cantidad: int) -> ItemCarrito:
    """
    Firma: item_desde_producto(producto: Producto, cantidad: int) -> ItemCarrito

    Descripción: construye un ItemCarrito con el stock ya reservado.
    Pureza referencial: producto y cantidad determinan el mismo ítem.
    Inmutabilidad: con_stock crea otro Producto; el original no cambia.
    Orden superior: ninguna.
    """
    return ItemCarrito(
        producto=producto.con_stock(producto.stock - cantidad),
        cantidad=cantidad,
        precio_unitario=producto.precio,
        precio_unitario_original=producto.precio,
        descuento=0,
    )


def items_sensores_apertura(
    productos_filtrados: tuple[Producto, ...],
    parametros: Cliente,
    mensaje_aviso: str = "Sensores de apertura ajustados de",
) -> tuple[tuple[ItemCarrito, ...], tuple[str, ...]]:
    """
    Firma: items_sensores_apertura(
        productos_filtrados: tuple[Producto, ...],
        parametros: Cliente,
        mensaje_aviso: str = "Sensores de apertura ajustados de",
    ) -> tuple[tuple[ItemCarrito, ...], tuple[str, ...]]

    Descripción: devuelve ítems con exactamente puertas más ventanas.
    Pureza referencial: normaliza, selecciona y transforma sin estado oculto.
    Inmutabilidad: las tuplas de entrada quedan intactas; map crea la salida.
    Orden superior: map con item_desde_producto y seleccionar/filter internos.
    """
    solicitada = (
        cantidad_positiva(parametros.puertas)
        + cantidad_positiva(parametros.ventanas)
    )
    if solicitada <= 0:
        return (), ()

    producto, cantidad, avisos = seleccionar(
        productos_filtrados, solicitada, (), mensaje_aviso=mensaje_aviso
    )
    if producto is None:
        return (), avisos
    return tuple(map(lambda p: item_desde_producto(p, cantidad), (producto,))), avisos


def items_sensores_movimiento(
    productos_filtrados: tuple[Producto, ...],
    parametros: Cliente,
    mensaje_aviso: str = "Sensores de movimiento ajustados de",
) -> tuple[tuple[ItemCarrito, ...], tuple[str, ...]]:
    """
    Firma: items_sensores_movimiento(
        productos_filtrados: tuple[Producto, ...],
        parametros: Cliente,
        mensaje_aviso: str = "Sensores de movimiento ajustados de",
    ) -> tuple[tuple[ItemCarrito, ...], tuple[str, ...]]

    Descripción: devuelve ítems con la cantidad de sensores de movimiento.
    Pureza referencial: cantidad positiva y stock fijan el resultado.
    Inmutabilidad: devuelve tuplas nuevas; entradas sin cambios.
    Orden superior: map con item_desde_producto y seleccionar/filter internos.
    """
    solicitada = cantidad_positiva(parametros.cantidad_sensores_movimiento)
    if solicitada <= 0:
        return (), ()

    producto, cantidad, avisos = seleccionar(
        productos_filtrados, solicitada, (), mensaje_aviso=mensaje_aviso
    )
    if producto is None:
        return (), avisos
    return tuple(map(lambda p: item_desde_producto(p, cantidad), (producto,))), avisos


# ---------------------------------------------------------------------------
# Reglas de negocio como transformadores: tupla de ítems -> tupla de ítems
# ---------------------------------------------------------------------------


def _es_camara(item: ItemCarrito, reglas: ReglasKit = REGLAS) -> bool:
    """
    Firma: _es_camara(item: ItemCarrito, reglas: ReglasKit = REGLAS) -> bool

    Descripción: indica si el ítem corresponde a una cámara.
    Pureza referencial: consulta solo la etiqueta del producto.
    Inmutabilidad: lectura de campos congelados.
    Orden superior: ninguna.
    """
    return item.producto.tiene_etiqueta(reglas.etiqueta_camara)


def _item_con_descuento(item: ItemCarrito, porcentaje: float) -> ItemCarrito:
    """
    Firma: _item_con_descuento(item: ItemCarrito, porcentaje: float) -> ItemCarrito

    Descripción: devuelve un ítem con descuento sobre el precio original.
    Pureza referencial: porcentaje y precio fijan el mismo importe.
    Inmutabilidad: replace crea otro ItemCarrito; el recibido no cambia.
    Orden superior: ninguna.
    """
    unitario = int(round(item.precio_unitario_original * porcentaje))
    return replace(
        item,
        precio_unitario=item.precio_unitario_original - unitario,
        descuento=unitario * item.cantidad,
    )


def aplicar_descuento_camaras(
    items: tuple[ItemCarrito, ...], reglas: ReglasKit = REGLAS
) -> tuple[ItemCarrito, ...]:
    """
    Firma: aplicar_descuento_camaras(
        items: tuple[ItemCarrito, ...], reglas: ReglasKit = REGLAS
    ) -> tuple[ItemCarrito, ...]

    Descripción: aplica 10 o 20 por ciento solo a las cámaras.
    Pureza referencial: la cantidad de cámaras fija el tramo y el resultado.
    Inmutabilidad: map produce otra tupla; los ítems de entrada intactos.
    Orden superior: map sobre items; generadora con if para contar cámaras.
    """
    cantidad = sum(item.cantidad for item in items if _es_camara(item, reglas))
    porcentaje = porcentaje_camaras(cantidad, reglas)
    if porcentaje == 0.0:
        return items
    return tuple(
        map(
            lambda item: (
                _item_con_descuento(item, porcentaje)
                if _es_camara(item, reglas)
                else item
            ),
            items,
        )
    )


def agregar_cartel_regalo(
    items: tuple[ItemCarrito, ...],
    cartel: Producto | None,
    reglas: ReglasKit = REGLAS,
) -> tuple[ItemCarrito, ...]:
    """
    Firma: agregar_cartel_regalo(
        items: tuple[ItemCarrito, ...],
        cartel: Producto | None,
        reglas: ReglasKit = REGLAS,
    ) -> tuple[ItemCarrito, ...]

    Descripción: agrega el cartel a cero pesos si aún no hay regalo.
    Pureza referencial: es idempotente y depende solo de items y cartel.
    Inmutabilidad: items + (item,) crea otra tupla; con_stock no muta.
    Orden superior: ninguna; usa any sobre generadora para el idempotente.
    """
    if cartel is None or not items:
        return items
    if any(item.es_regalo for item in items):
        return items
    item = ItemCarrito(
        producto=cartel.con_stock(cartel.stock - 1),
        cantidad=1,
        precio_unitario=0,
        precio_unitario_original=0,
        descuento=0,
        es_regalo=True,
    )
    return items + (item,)


def aplicar_transformaciones(
    estado: Estado, reglas: ReglasKit = REGLAS
) -> Estado:
    """
    Firma: aplicar_transformaciones(
        estado: Estado, reglas: ReglasKit = REGLAS
    ) -> Estado

    Descripción: encadena descuento de cámaras y regalo sobre los ítems.
    Pureza referencial: los mismos estado y reglas dan el mismo estado.
    Inmutabilidad: replace crea un Estado nuevo; partial no modifica nada.
    Orden superior: componer con partial para encadenar transformadores.
    """
    cartel = cartel_disuasivo_disponible(estado.catalogo, reglas)
    if cartel is None and len(estado.items) > 0:
        return replace(
            estado,
            avisos=estado.avisos + (
                "ReglaCartelRegalo omitida: no hay stock del cartel disuasivo",
            ),
        )

    transformar = componer(
        partial(agregar_cartel_regalo, cartel=cartel, reglas=reglas),
        partial(aplicar_descuento_camaras, reglas=reglas),
    )
    items = transformar(estado.items)
    if len(items) == len(estado.items):
        return estado

    regalo = Regalo(
        incluido=True,
        sku=cartel.sku,
        titulo=cartel.titulo,
        cantidad=1,
        precio_original=cartel.precio,
        precio_final=0,
        subtotal=0,
    )
    return replace(
        estado,
        catalogo=reemplazar_producto(estado.catalogo, items[-1].producto),
        items=items,
        regalo=regalo,
    )


# ---------------------------------------------------------------------------
# Reglas puras: Estado -> Estado
# ---------------------------------------------------------------------------


def regla_apertura(estado: Estado, reglas: ReglasKit = REGLAS) -> Estado:
    """
    Firma: regla_apertura(estado: Estado, reglas: ReglasKit = REGLAS) -> Estado

    Descripción: agrega o ajusta sensores de apertura del kit.
    Pureza referencial: cliente y catálogo determinan el estado resultante.
    Inmutabilidad: replace y reemplazar_producto construyen valores nuevos.
    Orden superior: delega filter/generadoras y map en funciones de apoyo.
    """
    cantidad = (
        cantidad_positiva(estado.cliente.puertas)
        + cantidad_positiva(estado.cliente.ventanas)
    )
    if cantidad == 0:
        return estado

    items, avisos = items_sensores_apertura(
        sensores_apertura_disponibles(estado.catalogo, reglas),
        estado.cliente,
    )
    if not items:
        return replace(
            estado,
            avisos=estado.avisos + (
                "ReglaSensoresApertura omitida: no hay sensores de apertura "
                "con stock suficiente",
            ),
        )

    return replace(
        estado,
        catalogo=reemplazar_producto(estado.catalogo, items[0].producto),
        items=estado.items + items,
        avisos=estado.avisos + avisos,
    )


def regla_movimiento(estado: Estado, reglas: ReglasKit = REGLAS) -> Estado:
    """
    Firma: regla_movimiento(estado: Estado, reglas: ReglasKit = REGLAS) -> Estado

    Descripción: agrega sensores de movimiento inmunes o estándar.
    Pureza referencial: bandera de mascotas y stock fijan el resultado.
    Inmutabilidad: devuelve Estado nuevo; catálogo e ítems se reconstruyen.
    Orden superior: delega filter/generadoras y map en funciones de apoyo.
    """
    cantidad = cantidad_positiva(estado.cliente.cantidad_sensores_movimiento)
    if cantidad == 0:
        return estado

    items, avisos = items_sensores_movimiento(
        sensores_movimiento_disponibles(
            estado.catalogo, estado.cliente.tiene_mascotas, reglas
        ),
        estado.cliente,
    )
    if not items:
        return replace(
            estado,
            avisos=estado.avisos + (
                "ReglaSensorMovimientoMascotas omitida: no hay sensores de "
                "movimiento con stock suficiente",
            ),
        )

    return replace(
        estado,
        catalogo=reemplazar_producto(estado.catalogo, items[0].producto),
        items=estado.items + items,
        avisos=estado.avisos + avisos,
    )


def regla_camaras(estado: Estado, reglas: ReglasKit = REGLAS) -> Estado:
    """
    Firma: regla_camaras(estado: Estado, reglas: ReglasKit = REGLAS) -> Estado

    Descripción: agrega cámaras a precio de lista para descontar después.
    Pureza referencial: selección por precio y SKU es determinista.
    Inmutabilidad: reserva stock con replace; Estado e ítems son nuevos.
    Orden superior: delega filter y map en extracción y reemplazo.
    """
    cantidad = cantidad_positiva(estado.cliente.cantidad_camaras)
    if cantidad == 0:
        return estado

    producto, cantidad, avisos = seleccionar(
        camaras_disponibles(estado.catalogo, reglas),
        cantidad,
        (),
        mensaje_aviso="Cámaras ajustadas de",
    )
    if producto is None:
        return replace(
            estado,
            avisos=estado.avisos + (
                "ReglaCamarasDescuentoProgresivo omitida: no hay cámaras "
                "con stock suficiente",
            ),
        )

    reservado = producto.con_stock(producto.stock - cantidad)
    item = ItemCarrito(
        producto=reservado,
        cantidad=cantidad,
        precio_unitario=producto.precio,
        precio_unitario_original=producto.precio,
        descuento=0,
    )
    return replace(
        estado,
        catalogo=reemplazar_producto(estado.catalogo, reservado),
        items=estado.items + (item,),
        avisos=estado.avisos + avisos,
    )


PIPELINE: tuple[Callable[..., Estado], ...] = (
    regla_apertura,
    regla_movimiento,
    regla_camaras,
    aplicar_transformaciones,
)


def inicializar(
    catalogo: tuple[Producto, ...], cliente: Cliente = CLIENTE_PRUEBA
) -> Estado:
    """
    Firma: inicializar(
        catalogo: tuple[Producto, ...], cliente: Cliente = CLIENTE_PRUEBA
    ) -> Estado

    Descripción: crea el estado inicial con regalo neutral y entradas saneadas.
    Pureza referencial: catálogo y cliente fijan el mismo Estado inicial.
    Inmutabilidad: tuple(catalogo) y normalizar_cliente producen valores nuevos.
    Orden superior: ninguna directa; normalizar_cliente usa replace.
    """
    return Estado(
        catalogo=tuple(catalogo), cliente=normalizar_cliente(cliente)
    )


def resolver(estado: Estado) -> Estado:
    """
    Firma: resolver(estado: Estado) -> Estado

    Descripción: aplica el pipeline de reglas con reduce.
    Pureza referencial: catálogo vacío es estado vacío; si no, reduce es
    determinista sobre el mismo pipeline.
    Inmutabilidad: cada regla devuelve un Estado nuevo; nunca se muta uno.
    Orden superior: reduce sobre la tupla PIPELINE.
    """
    if not estado.catalogo:
        return estado
    return reduce(lambda acumulado, regla: regla(acumulado), PIPELINE, estado)


# ---------------------------------------------------------------------------
# Proyección a estructuras inmutables de resultado
# ---------------------------------------------------------------------------


def linea_desde_item(item: ItemCarrito) -> LineaResultado:
    """
    Firma: linea_desde_item(item: ItemCarrito) -> LineaResultado

    Descripción: proyecta un ItemCarrito a una LineaResultado plana.
    Pureza referencial: todos los campos salen del item inmutable.
    Inmutabilidad: crea una LineaResultado congelada nueva.
    Orden superior: ninguna.
    """
    return LineaResultado(
        sku=item.sku,
        titulo=item.producto.titulo,
        categoria=item.producto.categoria,
        etiquetas=item.producto.etiquetas,
        cantidad=item.cantidad,
        precio_unitario=item.precio_unitario,
        precio_unitario_original=item.precio_unitario_original,
        subtotal=item.subtotal,
        descuento=item.descuento,
        total=item.total,
        stock_producto=item.producto.stock,
        es_regalo=item.es_regalo,
    )


def estado_a_resultado(estado: Estado) -> ResultadoKit:
    """
    Firma: estado_a_resultado(estado: Estado) -> ResultadoKit

    Descripción: convierte el Estado final en ResultadoKit sin dicts.
    Pureza referencial: proyección y resumen dependen solo del estado.
    Inmutabilidad: map y generadoras construyen tuplas nuevas.
    Orden superior: map para líneas y reduce indirecto en el resumen.
    """
    lineas = tuple(map(linea_desde_item, estado.items))
    consolidado = resumen_carrito_desde_items(estado.items)
    return ResultadoKit(
        cliente=estado.cliente,
        carrito=lineas,
        regalo=estado.regalo,
        resumen=Resumen(
            cantidad_items=len(lineas),
            subtotal=consolidado.subtotal,
            descuento_total=consolidado.descuento_total,
            total_final=consolidado.total_final,
        ),
        inventario=tuple((p.sku, p.stock) for p in estado.catalogo),
        avisos=estado.avisos,
    )


def cliente_a_mapping(cliente: Cliente) -> Mapping:
    """
    Firma: cliente_a_mapping(cliente: Cliente) -> Mapping

    Descripción: proyecta el cliente a un mapeo de solo lectura.
    Pureza referencial: los cinco campos son fijos para el mismo cliente.
    Inmutabilidad: MapeoInmutable guarda una tupla de pares, no un dict.
    Orden superior: ninguna.
    """
    return MapeoInmutable(
        tuple((
            ("puertas", cliente.puertas),
            ("ventanas", cliente.ventanas),
            ("tiene_mascotas", cliente.tiene_mascotas),
            ("cantidad_camaras", cliente.cantidad_camaras),
            ("cantidad_sensores_movimiento",
             cliente.cantidad_sensores_movimiento),
        ))
    )


def linea_a_mapping(linea: LineaResultado) -> Mapping:
    """
    Firma: linea_a_mapping(linea: LineaResultado) -> Mapping

    Descripción: proyecta una línea a un mapeo de solo lectura.
    Pureza referencial: cada campo sale de la línea congelada.
    Inmutabilidad: convierte etiquetas en tupla y construye pares nuevos.
    Orden superior: ninguna; usa línea_sku como delegado puro.
    """
    return MapeoInmutable(
        tuple((
            ("sku", línea_sku(linea)),
            ("titulo", linea.titulo),
            ("categoria", linea.categoria),
            ("etiquetas", tuple(linea.etiquetas)),
            ("cantidad", linea.cantidad),
            ("precio_unitario", linea.precio_unitario),
            ("precio_unitario_original", linea.precio_unitario_original),
            ("subtotal", linea.subtotal),
            ("descuento", linea.descuento),
            ("total", linea.total),
            ("stock_producto", linea.stock_producto),
            ("es_regalo", linea.es_regalo),
        ))
    )


def línea_sku(linea: LineaResultado) -> str:
    """
    Firma: línea_sku(linea: LineaResultado) -> str

    Descripción: devuelve el SKU de una línea del resultado.
    Pureza referencial: lee un único campo inmutable.
    Inmutabilidad: operación de solo lectura.
    Orden superior: ninguna.
    """
    return linea.sku


def regalo_a_mapping(regalo: Regalo) -> Mapping:
    """
    Firma: regalo_a_mapping(regalo: Regalo) -> Mapping

    Descripción: proyecta el regalo a un mapeo de solo lectura.
    Pureza referencial: campos fijos para el mismo Regalo.
    Inmutabilidad: MapeoInmutable sobre tupla de pares nueva.
    Orden superior: ninguna.
    """
    return MapeoInmutable(
        tuple((
            ("incluido", regalo.incluido),
            ("sku", regalo.sku),
            ("titulo", regalo.titulo),
            ("cantidad", regalo.cantidad),
            ("precio_original", regalo.precio_original),
            ("precio_final", regalo.precio_final),
            ("subtotal", regalo.subtotal),
        ))
    )


def resumen_a_mapping(resumen: Resumen) -> Mapping:
    """
    Firma: resumen_a_mapping(resumen: Resumen) -> Mapping

    Descripción: proyecta el resumen a un mapeo de solo lectura.
    Pureza referencial: cuatro totales deterministas del Resumen.
    Inmutabilidad: tupla de pares nueva; ningún dict mutable.
    Orden superior: ninguna.
    """
    return MapeoInmutable(
        tuple((
            ("cantidad_items", resumen.cantidad_items),
            ("subtotal", resumen.subtotal),
            ("descuento_total", resumen.descuento_total),
            ("total_final", resumen.total_final),
        ))
    )


def resultado_a_mapping(resultado: ResultadoKit) -> Mapping:
    """
    Firma: resultado_a_mapping(resultado: ResultadoKit) -> Mapping

    Descripción: proyecta el ResultadoKit completo a mapeos inmutables.
    Pureza referencial: cada subproyección es pura y determinista.
    Inmutabilidad: map y tuplas nuevas; el resultado original no cambia.
    Orden superior: map sobre el carrito y composición vía procesar.
    """
    return MapeoInmutable(
        tuple((
            ("cliente", cliente_a_mapping(resultado.cliente)),
            ("carrito", tuple(map(linea_a_mapping, resultado.carrito))),
            ("regalo", regalo_a_mapping(resultado.regalo)),
            ("resumen", resumen_a_mapping(resultado.resumen)),
            ("inventario", MapeoInmutable(tuple(resultado.inventario))),
            ("avisos", tuple(resultado.avisos)),
        ))
    )


procesar = componer(resultado_a_mapping, estado_a_resultado, resolver)


# ---------------------------------------------------------------------------
# Frontera de E/S: aquí sí se materializan contenedores mutables para JSON
# ---------------------------------------------------------------------------


def desbloquear(valor: object) -> object:
    """
    Firma: desbloquear(valor: object) -> object

    Descripción: convierte mapeos y tuplas en dicts y listas para JSON.
    Pureza referencial: conversión recursiva determinista, sin I/O propio.
    Inmutabilidad: construye copias nuevas; las entradas quedan intactas.
    Orden superior: ninguna; usa comprensiones recursivas en la frontera.
    """
    if isinstance(valor, Mapping):
        return {clave: desbloquear(item) for clave, item in valor.items()}
    if isinstance(valor, tuple):
        return [desbloquear(item) for item in valor]
    return valor


def cargar_catalogo_inmutable(
    ruta: Path = RUTA_CATALOGO,
) -> tuple[Producto, ...]:
    """
    Firma: cargar_catalogo_inmutable(
        ruta: Path = RUTA_CATALOGO,
    ) -> tuple[Producto, ...]

    Descripción: función impura de entrada; lee el JSON del catálogo.
    Pureza referencial: es E/S, pero con igual ruta y contenido da igual tupla.
    Inmutabilidad: MappingProxyType y catalogo_desde_dict devuelven tuplas
    de Producto congelados.
    Orden superior: map indirecto mediante catalogo_desde_dict.
    """
    with Path(ruta).open("r", encoding="utf-8") as archivo:
        datos = MappingProxyType(json.load(archivo))
    return catalogo_desde_dict(datos)


# Alias conservado para el codigo que ya usaba el nombre anterior.
cargar_catalogo = cargar_catalogo_inmutable


def guardar_resultado_json(
    resultado: Mapping, ruta: Path = RUTA_RESULTADO
) -> Path:
    """
    Firma: guardar_resultado_json(
        resultado: Mapping, ruta: Path = RUTA_RESULTADO
    ) -> Path

    Descripción: función impura de salida; escribe el resultado en JSON.
    Pureza referencial: es E/S; la serialización es determinista para el
    mismo resultado y la misma ruta.
    Inmutabilidad: desbloquear construye una copia; resultado no se muta.
    Orden superior: comprensiones de desbloquear; map indirecto del resultado.
    """
    destino = Path(ruta)
    with destino.open("w", encoding="utf-8", newline="\n") as archivo:
        json.dump(desbloquear(resultado), archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")
    return destino


# Alias conservado para el codigo que ya usaba el nombre anterior.
exportar_resultado = guardar_resultado_json


def imprimir_desglose(resultado: Mapping) -> None:
    """
    Firma: imprimir_desglose(resultado: Mapping) -> None

    Descripción: función impura de presentación; imprime el desglose.
    Pureza referencial: es E/S de consola; solo lee mapeos inmutables.
    Inmutabilidad: no escribe en el resultado ni en estructuras de dominio.
    Orden superior: componer indirecto a través de pesos para el formato.
    """
    cliente = resultado["cliente"]
    print("Kit de Seguridad Residencial")
    print(
        "Cliente: {puertas} puertas, {ventanas} ventanas, mascotas: {mascotas}, "
        "camaras: {camaras}, sensores movimiento: {movimiento}".format(
            puertas=cliente["puertas"],
            ventanas=cliente["ventanas"],
            mascotas="si" if cliente["tiene_mascotas"] else "no",
            camaras=cliente["cantidad_camaras"],
            movimiento=cliente["cantidad_sensores_movimiento"],
        )
    )
    print("-" * 68)
    for numero, item in enumerate(resultado["carrito"], 1):
        texto = (
            "{numero}. {sku} | {titulo} | {cantidad} x {precio} | "
            "subtotal {subtotal} | descuento -{descuento} | total {total}"
        ).format(
            numero=numero,
            sku=item["sku"],
            titulo=item["titulo"],
            cantidad=item["cantidad"],
            precio=pesos(item["precio_unitario"]),
            subtotal=pesos(item["subtotal"]),
            descuento=pesos(item["descuento"]),
            total=pesos(item["total"]),
        )
        if item["es_regalo"]:
            texto = texto + " | REGALO"
        print(texto)
    print("-" * 68)
    resumen = resultado["resumen"]
    print("Subtotal:", pesos(resumen["subtotal"]))
    print("Descuento: -" + pesos(resumen["descuento_total"]))
    print("Total final:", pesos(resumen["total_final"]))
    regalo = resultado["regalo"]
    if regalo["incluido"]:
        print(
            "Regalo: " + regalo["sku"] + " (normalmente "
            + pesos(regalo["precio_original"]) + ")"
        )
    avisos = resultado["avisos"]
    print("Avisos:", ", ".join(avisos) if avisos else "ninguno")


def ejecutar(
    ruta_catalogo: Path = RUTA_CATALOGO,
    ruta_resultado: Path = RUTA_RESULTADO,
) -> Mapping:
    """
    Firma: ejecutar(
        ruta_catalogo: Path = RUTA_CATALOGO,
        ruta_resultado: Path = RUTA_RESULTADO,
    ) -> Mapping

    Descripción: envoltorio impuro que coordina lectura, pipeline y escritura.
    Pureza referencial: la E/S está en los bordes; procesar es puro.
    Inmutabilidad: catálogo y resultado son estructuras inmutables.
    Orden superior: composición indirecta vía procesar = componer(...).
    """
    catalogo = cargar_catalogo_inmutable(ruta_catalogo)
    resultado = procesar(inicializar(catalogo))
    guardar_resultado_json(resultado, ruta_resultado)
    return resultado


def main() -> Mapping:
    """
    Firma: main() -> Mapping

    Descripción: punto de entrada; ejecuta el borde y muestra el desglose.
    Pureza referencial: delega la E/S en ejecutar e imprimir_desglose.
    Inmutabilidad: solo lee el mapping devuelto por ejecutar.
    Orden superior: indirecta mediante ejecutar y pesos.
    """
    resultado = ejecutar()
    imprimir_desglose(resultado)
    return resultado


if __name__ == "__main__":
    main()
