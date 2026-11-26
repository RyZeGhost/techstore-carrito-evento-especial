"""Carrito Evento Especial - paradigma estrictamente imperativo.

El catálogo se lee desde ``catalogo_shopify.json`` hacia variables y listas
mutables. La lógica se resuelve con asignaciones, acumuladores, bucles ``for``
y condicionales ``if/else``: no hay clases, ni ``map``/``filter``/``reduce``,
ni funciones de orden superior.
"""

import json
from pathlib import Path

RUTA_CATALOGO = Path(__file__).resolve().parent / "catalogo_shopify.json"

# ---------------------------------------------------------------------------
# 1. Lectura del catálogo hacia variables y listas mutables
# ---------------------------------------------------------------------------

with RUTA_CATALOGO.open(encoding="utf-8") as archivo:
    catalogo = json.load(archivo)

productos = []
for producto_crudo in catalogo["productos"]:
    producto = {}
    producto["origen"] = producto_crudo["origen"]
    producto["id"] = producto_crudo["id"]
    producto["sku"] = producto_crudo["sku"]
    producto["titulo"] = producto_crudo["titulo"]
    producto["categoria"] = producto_crudo["categoria"]
    producto["precio"] = producto_crudo["precio"]
    producto["stock"] = producto_crudo["stock"]

    etiquetas = []
    for etiqueta in producto_crudo["tags_funcionales"]:
        etiquetas.append(etiqueta)
    producto["tags_funcionales"] = etiquetas

    variantes = []
    for variante_cruda in producto_crudo["variantes"]:
        variante = {}
        variante["id"] = variante_cruda["id"]
        variante["sku"] = variante_cruda["sku"]
        variante["precio"] = variante_cruda["precio"]
        variante["stock"] = variante_cruda["stock"]
        variantes.append(variante)
    producto["variantes"] = variantes

    productos.append(producto)

categorias = []
for categoria_cruda in catalogo["categorias"]:
    categoria = {}
    categoria["titulo"] = categoria_cruda["titulo"]
    categoria["handle"] = categoria_cruda["handle"]
    categoria["cantidad_productos"] = categoria_cruda["cantidad_productos"]
    categorias.append(categoria)

# Copia mutable del inventario: el catálogo queda como referencia y aquí se
# descuentan las unidades que entran al carrito.
inventario = {}
for producto in productos:
    inventario[producto["sku"]] = producto["stock"]

# ---------------------------------------------------------------------------
# 2. Parámetros de entrada del cliente
# ---------------------------------------------------------------------------

puertas = 2
ventanas = 4
tiene_mascotas = True
cantidad_camaras = 3

# Cantidad de sensores de movimiento confirmada como parámetro explícito en la
# definición anterior del kit. Se mantiene aparte de los cuatro parámetros
# solicitados para no perder esa regla.
cantidad_sensores_movimiento = 2

if puertas < 0:
    raise ValueError("puertas no puede ser negativo")
if ventanas < 0:
    raise ValueError("ventanas no puede ser negativo")
if cantidad_camaras < 0:
    raise ValueError("cantidad_camaras no puede ser negativo")
if cantidad_sensores_movimiento < 0:
    raise ValueError("cantidad_sensores_movimiento no puede ser negativo")

# ---------------------------------------------------------------------------
# 3. Sensores de apertura: acumulador puertas + ventanas
# ---------------------------------------------------------------------------

cantidad_sensores_apertura = 0
cantidad_sensores_apertura += puertas
cantidad_sensores_apertura += ventanas

carrito = []
subtotal_apertura = 0

if cantidad_sensores_apertura > 0:
    mejor_producto = None
    mejor_precio = None
    sin_stock = False
    sin_etiqueta = False

    for producto in productos:
        tiene_etiqueta = False
        for etiqueta in producto["tags_funcionales"]:
            if etiqueta == "sensor_apertura":
                tiene_etiqueta = True
            else:
                pass

        if tiene_etiqueta:
            if inventario[producto["sku"]] >= cantidad_sensores_apertura:
                if mejor_precio is None or producto["precio"] < mejor_precio:
                    mejor_producto = producto
                    mejor_precio = producto["precio"]
            else:
                sin_stock = True
        else:
            sin_etiqueta = True

    if mejor_producto is None:
        raise ValueError(
            "No hay sensores de apertura con stock suficiente "
            f"(sin_stock={sin_stock}, sin_etiqueta={sin_etiqueta})"
        )

    inventario[mejor_producto["sku"]] -= cantidad_sensores_apertura
    subtotal_apertura = mejor_producto["precio"] * cantidad_sensores_apertura

    linea = {}
    linea["sku"] = mejor_producto["sku"]
    linea["titulo"] = mejor_producto["titulo"]
    linea["categoria"] = mejor_producto["categoria"]
    linea["etiquetas"] = []
    for etiqueta in mejor_producto["tags_funcionales"]:
        linea["etiquetas"].append(etiqueta)
    linea["cantidad"] = cantidad_sensores_apertura
    linea["precio_unitario"] = mejor_producto["precio"]
    linea["subtotal"] = subtotal_apertura
    linea["descuento"] = 0
    linea["total"] = subtotal_apertura
    linea["stock_producto"] = inventario[mejor_producto["sku"]]
    linea["es_regalo"] = False
    carrito.append(linea)

# ---------------------------------------------------------------------------
# 4. Sensores de movimiento: filtro de mascotas
# ---------------------------------------------------------------------------

etiquetas_movimiento = []
etiquetas_movimiento.append("sensor_movimiento")
etiquetas_excluidas = []

# Bandera booleana que gobierna la selección del sensor de movimiento.
seleccionar_inmune = False
if tiene_mascotas:
    seleccionar_inmune = True
else:
    seleccionar_inmune = False

if seleccionar_inmune:
    etiquetas_movimiento.append("inmune_mascotas")
else:
    etiquetas_excluidas.append("inmune_mascotas")

subtotal_movimiento = 0

if cantidad_sensores_movimiento > 0:
    mejor_producto = None
    mejor_precio = None
    sin_stock = False
    sin_etiqueta = False

    for producto in productos:
        es_movimiento = False
        es_inmune = False
        for etiqueta in producto["tags_funcionales"]:
            if etiqueta == "sensor_movimiento":
                es_movimiento = True
            else:
                pass
            if etiqueta == "inmune_mascotas":
                es_inmune = True
            else:
                pass

        elegible = False
        if seleccionar_inmune:
            if es_movimiento and es_inmune:
                elegible = True
            else:
                elegible = False
        else:
            if es_movimiento and not es_inmune:
                elegible = True
            else:
                elegible = False

        if elegible:
            if inventario[producto["sku"]] >= cantidad_sensores_movimiento:
                if mejor_precio is None or producto["precio"] < mejor_precio:
                    mejor_producto = producto
                    mejor_precio = producto["precio"]
            else:
                sin_stock = True
        else:
            sin_etiqueta = True

    if mejor_producto is None:
        raise ValueError(
            "No hay sensores de movimiento con stock suficiente "
            f"(sin_stock={sin_stock}, sin_etiqueta={sin_etiqueta})"
        )

    if inventario[mejor_producto["sku"]] >= cantidad_sensores_movimiento:
        inventario[mejor_producto["sku"]] -= cantidad_sensores_movimiento
        subtotal_movimiento = mejor_producto["precio"] * cantidad_sensores_movimiento

        linea = {}
        linea["sku"] = mejor_producto["sku"]
        linea["titulo"] = mejor_producto["titulo"]
        linea["categoria"] = mejor_producto["categoria"]
        linea["etiquetas"] = []
        for etiqueta in mejor_producto["tags_funcionales"]:
            linea["etiquetas"].append(etiqueta)
        linea["cantidad"] = cantidad_sensores_movimiento
        linea["precio_unitario"] = mejor_producto["precio"]
        linea["subtotal"] = subtotal_movimiento
        linea["descuento"] = 0
        linea["total"] = subtotal_movimiento
        linea["stock_producto"] = inventario[mejor_producto["sku"]]
        linea["es_regalo"] = False
        carrito.append(linea)
    else:
        raise ValueError("Stock insuficiente antes de agregar el sensor de movimiento al carrito")

# ---------------------------------------------------------------------------
# 5. Cámaras: descuento progresivo sobre el subtotal de cámaras
# ---------------------------------------------------------------------------

# Tramos definidos con if / elif / else según cantidad_camaras:
# 2-3 unidades = 10% de descuento; 4 o más = 20%; 0 o 1 = sin descuento.
porcentaje_camaras = 0.0
if cantidad_camaras >= 4:
    porcentaje_camaras = 0.20
elif cantidad_camaras >= 2:
    porcentaje_camaras = 0.10
else:
    porcentaje_camaras = 0.0

subtotal_camaras = 0
descuento_total = 0

if cantidad_camaras > 0:
    mejor_producto = None
    mejor_precio = None
    sin_stock = False
    sin_etiqueta = False

    for producto in productos:
        tiene_etiqueta = False
        for etiqueta in producto["tags_funcionales"]:
            if etiqueta == "camara":
                tiene_etiqueta = True
            else:
                pass

        if tiene_etiqueta:
            if inventario[producto["sku"]] >= cantidad_camaras:
                if mejor_precio is None or producto["precio"] < mejor_precio:
                    mejor_producto = producto
                    mejor_precio = producto["precio"]
            else:
                sin_stock = True
        else:
            sin_etiqueta = True

    if mejor_producto is None:
        raise ValueError(
            "No hay cámaras con stock suficiente "
            f"(sin_stock={sin_stock}, sin_etiqueta={sin_etiqueta})"
        )

    if inventario[mejor_producto["sku"]] < cantidad_camaras:
        raise ValueError("Stock insuficiente antes de agregar las cámaras al carrito")

    inventario[mejor_producto["sku"]] -= cantidad_camaras

    # El precio unitario es mutable: se reduce con el descuento del tramo.
    precio_unitario_original = mejor_producto["precio"]
    precio_unitario = precio_unitario_original

    monto_descuento_unitario = 0
    if porcentaje_camaras > 0:
        monto_descuento_unitario = int(round(precio_unitario * porcentaje_camaras))
    else:
        monto_descuento_unitario = 0
    precio_unitario -= monto_descuento_unitario

    subtotal_camaras = precio_unitario_original * cantidad_camaras
    monto_descuento = monto_descuento_unitario * cantidad_camaras
    descuento_total += monto_descuento

    linea = {}
    linea["sku"] = mejor_producto["sku"]
    linea["titulo"] = mejor_producto["titulo"]
    linea["categoria"] = mejor_producto["categoria"]
    linea["etiquetas"] = []
    for etiqueta in mejor_producto["tags_funcionales"]:
        linea["etiquetas"].append(etiqueta)
    linea["cantidad"] = cantidad_camaras
    linea["precio_unitario"] = precio_unitario
    linea["precio_unitario_original"] = precio_unitario_original
    linea["subtotal"] = subtotal_camaras
    linea["descuento"] = descuento_total
    linea["total"] = subtotal_camaras - descuento_total
    linea["stock_producto"] = inventario[mejor_producto["sku"]]
    linea["es_regalo"] = False
    carrito.append(linea)

# ---------------------------------------------------------------------------
# 6. Regalo automático: cartel disuasivo a $0
# ---------------------------------------------------------------------------

hay_sensor_o_camara = False
for linea in carrito:
    for etiqueta in linea["etiquetas"]:
        if etiqueta == "sensor_apertura":
            hay_sensor_o_camara = True
        elif etiqueta == "sensor_movimiento":
            hay_sensor_o_camara = True
        elif etiqueta == "camara":
            hay_sensor_o_camara = True
        else:
            pass

cartel = None
for producto in productos:
    es_cartel = False
    for etiqueta in producto["tags_funcionales"]:
        if etiqueta == "cartel_disuasivo":
            es_cartel = True
        else:
            pass

    if es_cartel:
        if inventario[producto["sku"]] >= 1:
            cartel = producto
        else:
            pass
    else:
        pass

regalo = {}
regalo["incluido"] = False
regalo["sku"] = None
regalo["titulo"] = None
regalo["cantidad"] = 0
regalo["precio_original"] = 0
regalo["precio_final"] = 0
regalo["subtotal"] = 0
regalo["motivo"] = "No hay sensores ni cámaras en el carrito."

if hay_sensor_o_camara and cartel is not None:
    inventario[cartel["sku"]] -= 1

    regalo["incluido"] = True
    regalo["sku"] = cartel["sku"]
    regalo["titulo"] = cartel["titulo"]
    regalo["cantidad"] = 1
    regalo["precio_original"] = cartel["precio"]
    regalo["precio_final"] = 0
    regalo["subtotal"] = 0
    regalo["motivo"] = "Regalo automático: hay sensor o cámara y stock del cartel."

    linea = {}
    linea["sku"] = cartel["sku"]
    linea["titulo"] = cartel["titulo"]
    linea["categoria"] = cartel["categoria"]
    linea["etiquetas"] = []
    for etiqueta in cartel["tags_funcionales"]:
        linea["etiquetas"].append(etiqueta)
    linea["cantidad"] = 1
    linea["precio_unitario"] = cartel["precio"]
    linea["subtotal"] = cartel["precio"]
    linea["descuento"] = cartel["precio"]
    linea["total"] = 0
    linea["stock_producto"] = inventario[cartel["sku"]]
    linea["es_regalo"] = True
    carrito.append(linea)

# ---------------------------------------------------------------------------
# 7. Resultado
# ---------------------------------------------------------------------------

total = 0
for linea in carrito:
    total += linea["total"]

cliente = {}
cliente["puertas"] = puertas
cliente["ventanas"] = ventanas
cliente["tiene_mascotas"] = tiene_mascotas
cliente["cantidad_camaras"] = cantidad_camaras
cliente["cantidad_sensores_movimiento"] = cantidad_sensores_movimiento

resumen = {}
resumen["cantidad_sensores_apertura"] = cantidad_sensores_apertura
resumen["cantidad_sensores_movimiento"] = cantidad_sensores_movimiento
resumen["cantidad_camaras"] = cantidad_camaras
resumen["etiquetas_movimiento_usadas"] = etiquetas_movimiento
resumen["etiquetas_movimiento_excluidas"] = etiquetas_excluidas
resumen["subtotal_sensores_apertura"] = subtotal_apertura
resumen["subtotal_sensores_movimiento"] = subtotal_movimiento
resumen["subtotal_camaras"] = subtotal_camaras
resumen["descuento_camaras_porcentaje"] = porcentaje_camaras
resumen["descuento_camaras_monto"] = descuento_total
resumen["descuento_total"] = descuento_total
resumen["subtotal_camaras_con_descuento"] = subtotal_camaras - descuento_total
resumen["total"] = total

resultado = {}
resultado["cliente"] = cliente
resultado["carrito"] = carrito
resultado["regalo"] = regalo
resultado["resumen"] = resumen
resultado["inventario"] = inventario

if __name__ == "__main__":
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
