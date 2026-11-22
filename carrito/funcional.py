"""Versión FUNCIONAL del Carrito Evento Especial.

Características del paradigma usadas aquí:
- Funciones puras: misma entrada => misma salida, sin efectos secundarios.
- Inmutabilidad: se usan tuplas y diccionarios nuevos, nunca se mutan los de entrada.
- Funciones de orden superior: `map`, `filter` y `functools.reduce`.
- Composición: `armar_carrito` encadena funciones pequeñas.
"""

import math  # ceil().
from functools import reduce  # reduce() acumula una secuencia en un solo valor.

from carrito.datos import indice_productos  # Índice de productos compartido.


def validar(evento, personas, catalogo):
    """Función pura de validación: devuelve la configuración del evento."""
    if personas <= 0:  # Condición de error.
        raise ValueError("personas debe ser mayor que cero")
    if evento not in catalogo["eventos"]:  # El evento debe existir.
        raise ValueError(f"Evento desconocido: {evento}")
    return catalogo["eventos"][evento]  # Devuelve un dict existente (no lo muta).


def cantidad_para(personas, regla):
    """Calcula unidades de una regla: techo y mínimo."""
    return max(regla["minimo"], math.ceil(personas * regla["por_persona"]))


def crear_item(producto, cantidad, sustituto_de=None):
    """Construye un diccionario nuevo para una línea del carrito."""
    return {
        "sku": producto["sku"],  # SKU vendido.
        "nombre": producto["nombre"],  # Nombre del producto.
        "cantidad": cantidad,  # Unidades.
        "precio_unitario": producto["precio"],  # Precio unitario.
        "subtotal": cantidad * producto["precio"],  # Total de la línea.
        "sustituto_de": sustituto_de,  # SKU original si se sustituyó.
    }


def resolver(regla, personas, catalogo, productos):
    """Devuelve el par (item, faltante); uno de los dos puede ser None."""
    producto = productos[regla["sku"]]  # Producto de la regla.
    cantidad = cantidad_para(personas, regla)  # Cantidad calculada.

    if cantidad <= producto["stock"]:  # Hay stock.
        return crear_item(producto, cantidad), None  # Par sin faltante.

    # Sin stock: buscar sustituto con stock suficiente.
    sku_alternativo = catalogo["sustitutos"].get(regla["sku"])  # Puede no existir.
    alternativo = productos.get(sku_alternativo)  # Puede no existir.

    if alternativo and alternativo["stock"] >= cantidad:  # Sustituto válido.
        return crear_item(alternativo, cantidad, regla["sku"]), None

    # Sin sustituto válido: vender lo disponible y reportar la diferencia.
    disponible = producto["stock"]  # Stock disponible.
    item = crear_item(producto, disponible) if disponible > 0 else None  # Item opcional.
    faltante = {"sku": regla["sku"], "cantidad": cantidad - disponible}  # Reporte.
    return item, faltante


def construir_lineas(config, personas, catalogo, productos):
    """Aplica `resolver` a todas las reglas con map y separa resultados."""
    pares = tuple(  # Tupla inmutable de resultados.
        map(  # map aplica resolver a cada regla.
            lambda regla: resolver(regla, personas, catalogo, productos),
            config["reglas"],
        )
    )
    items = tuple(filter(None, map(lambda par: par[0], pares)))  # Solo items.
    faltantes = tuple(filter(None, map(lambda par: par[1], pares)))  # Solo faltantes.
    return items, faltantes


def sumar_subtotal(items):
    """Reduce los subtotales de las líneas en un entero."""
    return reduce(lambda total, item: total + item["subtotal"], items, 0)


def descuento_2x1(items, sku_promo):
    """Descuento 2x1 usando reduce sobre las líneas promocionadas."""
    promocionados = filter(  # filter conserva solo las líneas que cumplen.
        lambda item: item["sku"] == sku_promo or item["sustituto_de"] == sku_promo,
        items,
    )
    return reduce(  # Acumula pares * precio.
        lambda total, item: total + (item["cantidad"] // 2) * item["precio_unitario"],
        promocionados,
        0,  # Valor inicial del acumulador.
    )


def descuento_cupon(cupon, config, base):
    """Descuento de 10% solo si el cupón coincide con el del evento."""
    return base * 10 // 100 if cupon == config["cupon"] else 0


def costo_envio(catalogo, monto):
    """Costo de envío según el umbral configurado."""
    envio = catalogo["envio"]  # Configuración de envío.
    return 0 if monto >= envio["gratis_desde"] else envio["costo"]


def armar_carrito(evento, personas, catalogo, cupon=None):
    """Compone todas las funciones puras y devuelve el resultado final."""
    config = validar(evento, personas, catalogo)  # 1) Validar entradas.
    productos = indice_productos(catalogo)  # 2) Indexar productos.

    items, faltantes = construir_lineas(config, personas, catalogo, productos)  # 3)

    subtotal = sumar_subtotal(items)  # 4) Suma funcional de líneas.
    desc_2x1 = descuento_2x1(items, config["producto_2x1"])  # 5) Promoción.
    desc_cupon = descuento_cupon(cupon, config, subtotal - desc_2x1)  # 6) Cupón.

    base = subtotal - desc_2x1 - desc_cupon  # 7) Base para envío.
    envio = costo_envio(catalogo, base)  # 8) Envío.
    total = base + envio  # 9) Total.

    return {  # 10) Diccionario nuevo; equivalente a los otros paradigmas.
        "evento": evento,
        "personas": personas,
        "items": list(items),
        "faltantes": list(faltantes),
        "descuentos": {"2x1": desc_2x1, "cupon": desc_cupon},
        "envio": envio,
        "total": total,
    }
