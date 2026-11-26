"""Carrito Evento Especial - paradigma estrictamente funcional.

Reglas cumplidas:

* Todas las estructuras de dominio son ``@dataclass(frozen=True)`` o
  ``NamedTuple``, y sus colecciones son ``tuple``.
* No hay ``.append()``, ni asignación de atributos: cada regla devuelve un
  ``Estado`` nuevo con ``dataclasses.replace``.
* No hay diccionarios mutables en la lógica: el catálogo entrante se envuelve
  en ``MappingProxyType`` y el resultado se modela con ``ResultadoKit``.
* ``map``, ``filter``, ``reduce`` y ``compose`` resuelven selección, stock,
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
from functools import reduce
from pathlib import Path
from types import MappingProxyType
from typing import Callable, NamedTuple

RUTA_CATALOGO = Path(__file__).resolve().parent / "catalogo_shopify.json"
RUTA_RESULTADO = Path(__file__).resolve().parent / "resultado_funcional.json"


# ---------------------------------------------------------------------------
# Utilidades funcionales
# ---------------------------------------------------------------------------


def compose(*funciones: Callable) -> Callable:
    """Compone funciones de derecha a izquierda mediante ``reduce``."""
    return reduce(
        lambda acumulada, siguiente: lambda valor: acumulada(siguiente(valor)),
        funciones,
        lambda valor: valor,
    )


def sumar_atributo(items: tuple, atributo: str) -> int:
    """Suma un atributo entero de una tupla de ítems usando ``reduce``."""
    return reduce(lambda total, item: total + getattr(item, atributo), items, 0)


def pesos(valor: int) -> str:
    """Formatea pesos chilenos con la composición de dos funciones puras."""
    return compose(
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
        """Indica si lleva una etiqueta sin exponer la tupla interna."""
        return etiqueta in self.etiquetas

    def con_stock(self, cantidad: int) -> "Producto":
        """Devuelve otro ``Producto`` con distinto stock; no se auto-modifica."""
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
        """SKU delegado al producto contenido."""
        return self.producto.sku

    @property
    def subtotal(self) -> int:
        """Subtotal sobre el precio original, sin estado duplicado."""
        return self.precio_unitario_original * self.cantidad

    @property
    def total(self) -> int:
        """Neto de la línea: subtotal menos descuento."""
        return self.subtotal - self.descuento


@dataclass(frozen=True)
class Cliente:
    """Entradas del cliente que alimentan las reglas del kit."""

    puertas: int
    ventanas: int
    tiene_mascotas: bool
    cantidad_camaras: int
    cantidad_sensores_movimiento: int


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
        """Busca una clave recorriendo la tupla, sin construir un dict."""
        for nombre, valor in self.pares:
            if nombre == clave:
                return valor
        raise KeyError(clave)

    def __iter__(self):
        """Itera las claves en el orden original de la tupla."""
        return (nombre for nombre, _ in self.pares)

    def __len__(self) -> int:
        """Devuelve la cantidad de pares."""
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
    """Construye un ``Producto`` desde un mapeo de solo lectura del JSON."""
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
    """Mapea los productos del JSON a una tupla inmutable."""
    return tuple(map(producto_desde_dict, tuple(datos["productos"])))


def filtrar_por_etiquetas(
    productos: tuple[Producto, ...],
    incluidas: tuple[str, ...],
    excluidas: tuple[str, ...] = (),
) -> tuple[Producto, ...]:
    """Filtra por etiquetas incluidas y excluidas con ``filter``."""
    return tuple(
        filter(
            lambda producto: (
                all(map(lambda e: producto.tiene_etiqueta(e), incluidas))
                and not any(map(lambda e: producto.tiene_etiqueta(e), excluidas))
            ),
            productos,
        )
    )


def seleccionar(
    productos: tuple[Producto, ...],
    cantidad: int,
    incluidas: tuple[str, ...],
    excluidas: tuple[str, ...] = (),
    mensaje_aviso: str = "",
) -> tuple[Producto | None, int, tuple[str, ...]]:
    """Elige el SKU más barato con stock y ajusta stock parcial sin mutar."""
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
    """Devuelve un catálogo nuevo con el producto sustituido por su SKU."""
    return tuple(
        map(lambda actual: producto if actual.sku == producto.sku else actual,
            catalogo)
    )


def porcentaje_camaras(cantidad: int, reglas: ReglasKit = REGLAS) -> float:
    """Resuelve el tramo de descuento aplicable con ``filter``."""
    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 0:
        raise ValueError("cantidad de cámaras debe ser un entero no negativo")
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
# Reglas puras: Estado -> Estado
# ---------------------------------------------------------------------------


def regla_apertura(estado: Estado, reglas: ReglasKit = REGLAS) -> Estado:
    """Agrega ``puertas + ventanas`` sensores o registra un aviso."""
    cantidad = estado.cliente.puertas + estado.cliente.ventanas
    if cantidad == 0:
        return estado

    producto, cantidad, avisos = seleccionar(
        estado.catalogo,
        cantidad,
        (reglas.etiqueta_apertura,),
        mensaje_aviso="Sensores de apertura ajustados de",
    )
    if producto is None:
        return replace(
            estado,
            avisos=estado.avisos + (
                "ReglaSensoresApertura omitida: no hay sensores de apertura "
                "con stock suficiente",
            ),
        )

    reservado = producto.con_stock(producto.stock - cantidad)
    item = ItemCarrito(reservado, cantidad, producto.precio, producto.precio, 0)
    return replace(
        estado,
        catalogo=reemplazar_producto(estado.catalogo, reservado),
        items=estado.items + (item,),
        avisos=estado.avisos + avisos,
    )


def regla_movimiento(estado: Estado, reglas: ReglasKit = REGLAS) -> Estado:
    """Elige sensores inmunes a mascotas o estándar según la bandera."""
    cantidad = estado.cliente.cantidad_sensores_movimiento
    if cantidad == 0:
        return estado

    incluidas = (reglas.etiqueta_movimiento,)
    excluidas: tuple[str, ...] = ()
    if estado.cliente.tiene_mascotas:
        incluidas = incluidas + (reglas.etiqueta_inmune,)
    else:
        excluidas = excluidas + (reglas.etiqueta_inmune,)

    producto, cantidad, avisos = seleccionar(
        estado.catalogo,
        cantidad,
        incluidas,
        excluidas,
        mensaje_aviso="Sensores de movimiento ajustados de",
    )
    if producto is None:
        return replace(
            estado,
            avisos=estado.avisos + (
                "ReglaSensorMovimientoMascotas omitida: no hay sensores de "
                "movimiento con stock suficiente",
            ),
        )

    reservado = producto.con_stock(producto.stock - cantidad)
    item = ItemCarrito(reservado, cantidad, producto.precio, producto.precio, 0)
    return replace(
        estado,
        catalogo=reemplazar_producto(estado.catalogo, reservado),
        items=estado.items + (item,),
        avisos=estado.avisos + avisos,
    )


def regla_camaras(estado: Estado, reglas: ReglasKit = REGLAS) -> Estado:
    """Aplica 10% o 20% solo a cámaras, conservando el precio original."""
    cantidad = estado.cliente.cantidad_camaras
    if cantidad == 0:
        return estado

    porcentaje = porcentaje_camaras(cantidad, reglas)
    producto, cantidad, avisos = seleccionar(
        estado.catalogo,
        cantidad,
        (reglas.etiqueta_camara,),
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

    descuento_unitario = int(round(producto.precio * porcentaje))
    reservado = producto.con_stock(producto.stock - cantidad)
    item = ItemCarrito(
        producto=reservado,
        cantidad=cantidad,
        precio_unitario=producto.precio - descuento_unitario,
        precio_unitario_original=producto.precio,
        descuento=descuento_unitario * cantidad,
    )
    return replace(
        estado,
        catalogo=reemplazar_producto(estado.catalogo, reservado),
        items=estado.items + (item,),
        avisos=estado.avisos + avisos,
    )


def regla_regalo(estado: Estado, reglas: ReglasKit = REGLAS) -> Estado:
    """Regala un cartel a $0 si hay artículos y stock del cartel."""
    if len(estado.items) == 0:
        return estado

    carteles = filtrar_por_etiquetas(
        estado.catalogo, (reglas.etiqueta_regalo,)
    )
    cartel = next(filter(lambda p: p.stock > 0, carteles), None)
    if cartel is None:
        return replace(
            estado,
            avisos=estado.avisos + (
                "ReglaCartelRegalo omitida: no hay stock del cartel disuasivo",
            ),
        )

    reservado = cartel.con_stock(cartel.stock - 1)
    item = ItemCarrito(
        producto=reservado,
        cantidad=1,
        precio_unitario=0,
        precio_unitario_original=0,
        descuento=0,
        es_regalo=True,
    )
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
        catalogo=reemplazar_producto(estado.catalogo, reservado),
        items=estado.items + (item,),
        regalo=regalo,
    )


PIPELINE: tuple[Callable[..., Estado], ...] = (
    regla_apertura,
    regla_movimiento,
    regla_camaras,
    regla_regalo,
)


def inicializar(
    catalogo: tuple[Producto, ...], cliente: Cliente = CLIENTE_PRUEBA
) -> Estado:
    """Crea el estado inicial con tuplas vacías y regalo neutral."""
    return Estado(catalogo=catalogo, cliente=cliente)


def resolver(estado: Estado) -> Estado:
    """Aplica el pipeline de reglas con ``reduce``."""
    return reduce(lambda acumulado, regla: regla(acumulado), PIPELINE, estado)


# ---------------------------------------------------------------------------
# Proyección a estructuras inmutables de resultado
# ---------------------------------------------------------------------------


def linea_desde_item(item: ItemCarrito) -> LineaResultado:
    """Proyecta una línea del carrito a un registro congelado."""
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
    """Convierte el estado final en ``ResultadoKit``, sin dicts ni listas."""
    lineas = tuple(map(linea_desde_item, estado.items))
    return ResultadoKit(
        cliente=estado.cliente,
        carrito=lineas,
        regalo=estado.regalo,
        resumen=Resumen(
            cantidad_items=len(lineas),
            subtotal=sumar_atributo(estado.items, "subtotal"),
            descuento_total=sumar_atributo(estado.items, "descuento"),
            total_final=sumar_atributo(estado.items, "total"),
        ),
        inventario=tuple((p.sku, p.stock) for p in estado.catalogo),
        avisos=estado.avisos,
    )


def cliente_a_mapping(cliente: Cliente) -> Mapping:
    """Proyecta el cliente a un mapeo de solo lectura para JSON."""
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
    """Proyecta una línea a un mapeo de solo lectura para JSON."""
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
    """Devuelve el SKU de una línea del resultado."""
    return linea.sku


def regalo_a_mapping(regalo: Regalo) -> Mapping:
    """Proyecta el regalo a un mapeo de solo lectura para JSON."""
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
    """Proyecta el resumen a un mapeo de solo lectura para JSON."""
    return MapeoInmutable(
        tuple((
            ("cantidad_items", resumen.cantidad_items),
            ("subtotal", resumen.subtotal),
            ("descuento_total", resumen.descuento_total),
            ("total_final", resumen.total_final),
        ))
    )


def resultado_a_mapping(resultado: ResultadoKit) -> Mapping:
    """Proyecta el resultado completo a mapeos inmutables para JSON."""
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


procesar = compose(resultado_a_mapping, estado_a_resultado, resolver)


# ---------------------------------------------------------------------------
# Frontera de E/S: aquí sí se materializan contenedores mutables para JSON
# ---------------------------------------------------------------------------


def desbloquear(valor: object) -> object:
    """Convierte mapeos y tuplas inmutables en dicts y listas para ``json``."""
    if isinstance(valor, Mapping):
        return {clave: desbloquear(item) for clave, item in valor.items()}
    if isinstance(valor, tuple):
        return [desbloquear(item) for item in valor]
    return valor


def cargar_catalogo(ruta: Path = RUTA_CATALOGO) -> tuple[Producto, ...]:
    """Lee el JSON y devuelve una tupla de productos inmutables."""
    with Path(ruta).open("r", encoding="utf-8") as archivo:
        datos = MappingProxyType(json.load(archivo))
    return catalogo_desde_dict(datos)


def exportar_resultado(resultado: Mapping, ruta: Path = RUTA_RESULTADO) -> Path:
    """Escribe el resultado de forma determinista y devuelve la ruta."""
    destino = Path(ruta)
    with destino.open("w", encoding="utf-8", newline="\n") as archivo:
        json.dump(desbloquear(resultado), archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")
    return destino


def imprimir_desglose(resultado: Mapping) -> None:
    """Muestra el desglose legible leyendo solo mapeos de solo lectura."""
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


def main() -> Mapping:
    """Ejecuta el pipeline funcional completo y exporta el resultado."""
    catalogo = cargar_catalogo()
    resultado = procesar(inicializar(catalogo))
    imprimir_desglose(resultado)
    exportar_resultado(resultado)
    return resultado


if __name__ == "__main__":
    main()
