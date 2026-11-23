"""Versión IMPERATIVA del Carrito Evento Especial.

Características del paradigma usadas aquí:
- Variables mutables (`items`, `faltantes`, `total`).
- Estructuras de control explícitas (`for`, `if`).
- Estado construido paso a paso con asignaciones.
"""

import math  # ceil() redondea siempre hacia arriba.

from carrito.datos import indice_productos  # Convierte la lista de productos en un dict.
from carrito.recomendaciones import sugerir  # Regla transversal de sugerencias.
from carrito.segmentos import (  # Reglas compartidas de segmentación.
    beneficios_para,
    config_para,
    descuento_para,
    envio_para,
)


def armar_carrito(evento, personas, catalogo, cupon=None, tipo_usuario=None):
    """Devuelve el carrito armado como diccionario (misma forma en los 3 paradigmas)."""

    # Validación temprana: evita trabajar con entradas sin sentido.
    if personas <= 0:  # Una persona o menos no define un evento.
        raise ValueError("personas debe ser mayor que cero")  # Error explícito.

    if evento not in catalogo["eventos"]:  # El evento debe existir en el JSON.
        raise ValueError(f"Evento desconocido: {evento}")  # Mensaje útil.

    config_para(tipo_usuario, catalogo)  # Valida 'nuevo', 'frecuente', 'mayorista'.

    productos = indice_productos(catalogo)  # {sku: producto}, acceso O(1).
    config = catalogo["eventos"][evento]  # Reglas propias del evento elegido.
    items = []  # Acumulador mutable de líneas del carrito.
    faltantes = []  # Acumulador mutable de productos sin stock suficiente.

    # --- Paso 1: calcular cantidades y resolver stock ---
    for regla in config["reglas"]:  # Recorre las reglas en orden estable.
        sku = regla["sku"]  # SKU del producto sugerido por la regla.
        producto = productos[sku]  # Datos del producto (precio, stock, nombre).

        # ceil() porque no se pueden vender fracciones; max() aplica el mínimo.
        cantidad = max(regla["minimo"], math.ceil(personas * regla["por_persona"]))

        if cantidad > producto["stock"]:  # No hay stock suficiente.
            sku_sustituto = catalogo["sustitutos"].get(sku)  # Busca alternativa.
            sustituto = productos.get(sku_sustituto)  # Puede no existir.

            if sustituto and sustituto["stock"] >= cantidad:  # El sustituto alcanza.
                # Se agrega el sustituto, dejando registro del producto original.
                items.append({
                    "sku": sustituto["sku"],  # SKU que finalmente se vende.
                    "nombre": sustituto["nombre"],  # Nombre del sustituto.
                    "cantidad": cantidad,  # Cantidad calculada originalmente.
                    "precio_unitario": sustituto["precio"],  # Precio del sustituto.
                    "subtotal": cantidad * sustituto["precio"],  # Línea * precio.
                    "sustituto_de": sku,  # Trazabilidad del cambio.
                })
                continue  # Ya resolvimos esta regla; pasamos a la siguiente.

            disponible = producto["stock"]  # Stock real que sí se puede vender.
            if disponible > 0:  # Solo agregamos la línea si hay algo disponible.
                items.append({
                    "sku": sku,  # SKU original.
                    "nombre": producto["nombre"],  # Nombre original.
                    "cantidad": disponible,  # Se limita al stock disponible.
                    "precio_unitario": producto["precio"],  # Precio original.
                    "subtotal": disponible * producto["precio"],  # Subtotal de la línea.
                    "sustituto_de": None,  # No hubo sustitución.
                })

            falta = cantidad - disponible  # Diferencia no cubierta.
            if falta > 0:  # Solo se registra si realmente falta stock.
                faltantes.append({"sku": sku, "cantidad": falta})  # Reporte.
        else:  # Hay stock suficiente.
            items.append({
                "sku": sku,  # SKU original.
                "nombre": producto["nombre"],  # Nombre original.
                "cantidad": cantidad,  # Cantidad calculada.
                "precio_unitario": producto["precio"],  # Precio original.
                "subtotal": cantidad * producto["precio"],  # Subtotal de la línea.
                "sustituto_de": None,  # Sin sustitución.
            })

    # --- Paso 2: aplicar promoción 2x1 ---
    descuento_2x1 = 0  # Acumulador del descuento.
    sku_promo = config["producto_2x1"]  # Producto con 2x1 en este evento.
    for item in items:  # Revisa cada línea ya construida.
        # Se considera también el sustituto para no perder la promoción.
        if item["sku"] == sku_promo or item["sustituto_de"] == sku_promo:
            pares = item["cantidad"] // 2  # Cada par equivale a una unidad gratis.
            descuento_2x1 += pares * item["precio_unitario"]  # Acumula el descuento.

    # --- Paso 3: subtotal, cupón y envío ---
    subtotal = 0  # Acumulador del subtotal sin descuentos.
    for item in items:  # Recorre las líneas.
        subtotal += item["subtotal"]  # Suma el subtotal de cada línea.

    base = subtotal - descuento_2x1  # Subtotal después del 2x1.
    descuento_cupon = 0  # Valor por defecto: sin cupón.
    if cupon == config["cupon"]:  # Solo si el cupón coincide con el del evento.
        descuento_cupon = base * 10 // 100  # 10% redondeado hacia abajo (enteros).

    # --- Paso 4: beneficios del segmento (después del 2x1 y del cupón) ---
    base_final = base - descuento_cupon  # Monto sobre el que aplica el segmento.
    descuento_segmento = descuento_para(base_final, tipo_usuario, catalogo)
    monto = base_final - descuento_segmento  # Base para evaluar el envío.

    envio = catalogo["envio"]  # Configuración de envío del JSON.
    if monto >= envio["gratis_desde"]:  # Supera el umbral.
        costo_envio = 0  # Envío gratis.
    else:  # No supera el umbral.
        costo_envio = envio["costo"]  # Se cobra el envío.
    costo_envio = envio_para(costo_envio, tipo_usuario, catalogo)  # Beneficio.

    total = monto + costo_envio  # Resultado final.

    # --- Paso 5: sugerencias según carrito, festividad y segmento ---
    # Se calculan al final porque dependen de las líneas ya resueltas.
    recomendaciones = sugerir(items, catalogo, evento, tipo_usuario)

    # --- Paso 6: devolver estructura común a los tres paradigmas ---
    return {
        "evento": evento,  # Evento solicitado.
        "personas": personas,  # Cantidad de personas solicitada.
        "tipo_usuario": tipo_usuario or "invitado",  # Segmento atendido.
        "items": items,  # Líneas del carrito.
        "faltantes": faltantes,  # Productos sin stock.
        "descuentos": {
            "2x1": descuento_2x1,
            "cupon": descuento_cupon,
            "segmento": descuento_segmento,
        },
        "envio": costo_envio,  # Costo de envío aplicado.
        "beneficios": beneficios_para(tipo_usuario, catalogo),
        "total": total,  # Total a pagar.
        "recomendaciones": recomendaciones,  # Ofertas; no cambian el total.
    }
