"""Carrito Evento Especial - paradigma estrictamente imperativo.

Modelo de ejecución: todo el código vive a nivel de módulo, así que se ejecuta
de arriba hacia abajo una sola vez, sin definir funciones ni clases. El estado
son variables, listas y diccionarios ordinarios; cada bloque lee ese estado, lo
modifica en el mismo lugar (in-place) y se lo pasa al siguiente. No hay valores
de retorno ni ámbitos locales: el control de flujo es secuencial, con ``for``,
``if/elif/else``, ``break`` y ``raise`` para repetir, saltar o detener el proceso.

El catálogo se lee desde ``catalogo_shopify.json`` hacia variables y listas
mutables. No se usan ``map``/``filter``/``reduce``, ``lambda`` ni
comprensiones: cada recorrido es un ``for`` explícito con acumuladores.
"""

import json
import sys
from pathlib import Path

RUTA_CATALOGO = Path(__file__).resolve().parent / "catalogo_shopify.json"
RUTA_RESULTADO = Path(__file__).resolve().parent / "resultado_imperativo.json"

# ---------------------------------------------------------------------------
# 1. Lectura del catálogo hacia variables y listas mutables
# ---------------------------------------------------------------------------
# ``catalogo`` es el diccionario crudo devuelto por json.load: queda en memoria
# como referencia de solo lectura. A partir de él se construye ``productos``,
# una lista nueva: por cada producto se crea un dict y se vuelcan sus campos con
# asignaciones. Las listas anidadas (``etiquetas`` y ``variantes``) también se
# copian elemento por elemento con append, de modo que modificarlas después no
# altere el JSON original. ``categorias`` se llena igual. Al final se crea
# ``inventario``, un diccionario independiente con los sku y su stock: será la
# copia mutable que se descuenta al armar el carrito, sin tocar el stock leído.

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
# Estas cinco variables son el estado de entrada. Como no hay funciones, no hay
# parámetros formales: cambiar una asignación cambia los datos con los que
# trabajarán todos los bloques posteriores. ``tiene_mascotas`` es una bandera
# booleana; las cantidades se tratan como enteros y se validan antes de mutar
# cualquier estructura.

puertas = 2
ventanas = 4
tiene_mascotas = True
cantidad_camaras = 3

# Cantidad de sensores de movimiento confirmada como parámetro explícito en la
# definición anterior del kit. Se mantiene aparte de los cuatro parámetros
# solicitados para no perder esa regla.
cantidad_sensores_movimiento = 2

# ---------------------------------------------------------------------------
# 2b. Validaciones imperativas de casos borde y ajuste por stock
# ---------------------------------------------------------------------------
# ``avisos`` es una lista mutable que acumula mensajes: nace vacía y solo crece
# con append. Las validaciones usan ``raise``: si se cumple la condición
# inválida, el flujo se detiene ahí y ningún bloque posterior se ejecuta, por lo
# que no se descuenta stock ni se escribe el JSON. El acumulador de apertura
# empieza en 0 y crece con dos asignaciones ``+=`` (puertas y ventanas). Las
# banderas y etiquetas se fijan aquí porque el cálculo del stock máximo depende
# de ellas. Los dos ``stock_max_*`` se recalculan dentro de un for: cada producto
# puede elevar el valor guardado y al terminar queda el máximo de los elegibles.
# Si la cantidad pedida supera ese tope, se reasigna la cantidad al máximo y se
# deja constancia en ``avisos``; el flujo continúa con los valores ya ajustados.

avisos = []

if len(productos) == 0:
    raise ValueError("El catálogo está vacío: no hay productos para armar el carrito.")
else:
    pass

if puertas < 0:
    raise ValueError("puertas no puede ser negativo")
else:
    pass
if ventanas < 0:
    raise ValueError("ventanas no puede ser negativo")
else:
    pass
if cantidad_camaras < 0:
    raise ValueError("cantidad_camaras no puede ser negativo")
else:
    pass
if cantidad_sensores_movimiento < 0:
    raise ValueError("cantidad_sensores_movimiento no puede ser negativo")
else:
    pass

# Acumulador de apertura: se calcula aquí para poder ajustarlo al stock
# disponible antes de recorrer el catálogo en la sección siguiente.
cantidad_sensores_apertura = 0
cantidad_sensores_apertura += puertas
cantidad_sensores_apertura += ventanas

# La bandera de mascotas también se necesita para medir el stock elegible.
seleccionar_inmune = False
if tiene_mascotas:
    seleccionar_inmune = True
else:
    seleccionar_inmune = False

etiquetas_movimiento = []
etiquetas_movimiento.append("sensor_movimiento")
etiquetas_excluidas = []
if seleccionar_inmune:
    etiquetas_movimiento.append("inmune_mascotas")
else:
    etiquetas_excluidas.append("inmune_mascotas")

# Stock máximo por grupo, recorriendo el catálogo con for / if.
stock_max_apertura = 0
stock_max_movimiento = 0
for producto in productos:
    es_apertura = False
    es_movimiento = False
    es_inmune = False
    for etiqueta in producto["tags_funcionales"]:
        if etiqueta == "sensor_apertura":
            es_apertura = True
        else:
            pass
        if etiqueta == "sensor_movimiento":
            es_movimiento = True
        else:
            pass
        if etiqueta == "inmune_mascotas":
            es_inmune = True
        else:
            pass

    if es_apertura:
        if inventario[producto["sku"]] > stock_max_apertura:
            stock_max_apertura = inventario[producto["sku"]]
        else:
            pass
    else:
        pass

    elegible_movimiento = False
    if seleccionar_inmune:
        if es_movimiento and es_inmune:
            elegible_movimiento = True
        else:
            elegible_movimiento = False
    else:
        if es_movimiento and not es_inmune:
            elegible_movimiento = True
        else:
            elegible_movimiento = False

    if elegible_movimiento:
        if inventario[producto["sku"]] > stock_max_movimiento:
            stock_max_movimiento = inventario[producto["sku"]]
        else:
            pass
    else:
        pass

# Ajuste al máximo disponible, dejando el aviso en la lista mutable.
if cantidad_sensores_apertura > stock_max_apertura:
    avisos.append(
        "Sensores de apertura ajustados de "
        f"{cantidad_sensores_apertura} a {stock_max_apertura} por stock disponible."
    )
    cantidad_sensores_apertura = stock_max_apertura
else:
    pass

if cantidad_sensores_movimiento > stock_max_movimiento:
    avisos.append(
        "Sensores de movimiento ajustados de "
        f"{cantidad_sensores_movimiento} a {stock_max_movimiento} por stock disponible."
    )
    cantidad_sensores_movimiento = stock_max_movimiento
else:
    pass

# ---------------------------------------------------------------------------
# 3. Sensores de apertura: se usa el acumulador ya ajustado
# ---------------------------------------------------------------------------
# ``carrito`` nace como lista vacía y es el contenedor donde se insertarán todas
# las líneas. Dentro del if se recorre ``productos`` con un for: las variables
# ``mejor_producto`` y ``mejor_precio`` son estado del bucle, se inicializan en
# None y se reasignan cada vez que aparece un SKU más barato con stock suficiente.
# Los if/else solo deciden si se actualiza ese estado. Al salir del bucle, el
# stock se descuenta in-place del dict ``inventario`` restando en la clave del
# sku elegido. Después se construye ``linea`` campo por campo con asignaciones y
# se agrega al final de ``carrito`` con append; ``stock_producto`` ya guarda el
# valor posterior al descuento.

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
# La bandera ``seleccionar_inmune`` (definida arriba) decide la elegibilidad
# dentro del for: por cada producto se levantan banderas locales
# ``es_movimiento`` y ``es_inmune`` recorriendo sus etiquetas, y ``elegible`` se
# reasigna según la bandera global. El mismo patrón de estado de bucle del bloque
# anterior elige el SKU más barato con stock. La verificación de stock se repite
# justo antes del append: si pasa, se resta del ``inventario`` y se agrega la
# línea; si no, el else lanza ValueError y ``carrito`` queda sin esa línea.

# La bandera y las etiquetas ya se definieron en la sección de validaciones,
# donde se usaron para medir el stock máximo elegible.
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
# Primero una cadena if/elif/else asigna ``porcentaje_camaras`` una sola vez,
# antes de cualquier recorrido: 20% para 4 o más, 10% para 2-3 y 0 en caso
# contrario. Luego el for selecciona el SKU más barato con stock, con el mismo
# esquema de ``mejor_producto``/``mejor_precio``. A diferencia de los bloques
# anteriores, el precio unitario es mutable: ``precio_unitario`` arranca con el
# precio original y se reduce con ``-=``. El acumulador ``descuento_total`` crece
# con ``+=`` y se copia en ``descuento_camaras_monto`` para distinguirlo del
# descuento global que se calculará al final. La línea entra a ``carrito`` con
# el precio ya mutado y el total neto.

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
descuento_camaras_monto = 0

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
    descuento_camaras_monto = descuento_total

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
# Se recorre el catálogo con un for y la bandera ``es_cartel``; en cuanto se
# encuentra un cartel con stock mayor que cero se guarda en ``cartel`` y se
# ejecuta ``break`` para salir del bucle, sin evaluar los SKU restantes. El if
# exterior exige que ``carrito`` ya tenga elementos: usa ``len()`` sobre la lista
# mutable, no una bandera derivada de etiquetas. Dentro se descuenta 1 del
# inventario del cartel y se agrega una línea nueva con precio_unitario,
# subtotal, descuento y total en 0, más ``es_regalo`` en True. Esa línea también
# vive en ``carrito``, por lo que el bucle final del resumen la contabilizará con
# subtotal cero.

# El regalo se activa cuando el carrito ya tiene artículos (todos los que se
# insertan son sensores o cámaras). Se recorre el catálogo buscando el cartel
# disuasivo con stock disponible en la copia mutable del inventario.
cartel = None
for producto in productos:
    es_cartel = False
    for etiqueta in producto["tags_funcionales"]:
        if etiqueta == "cartel_disuasivo":
            es_cartel = True
        else:
            pass

    if es_cartel:
        if inventario[producto["sku"]] > 0:
            cartel = producto
            break
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
regalo["motivo"] = "El carrito está vacío o no hay stock del cartel disuasivo."

if len(carrito) > 0 and cartel is not None:
    inventario[cartel["sku"]] -= 1

    regalo["incluido"] = True
    regalo["sku"] = cartel["sku"]
    regalo["titulo"] = cartel["titulo"]
    regalo["cantidad"] = 1
    regalo["precio_original"] = cartel["precio"]
    regalo["precio_final"] = 0
    regalo["subtotal"] = 0
    regalo["motivo"] = "Regalo automático: carrito con artículos y stock del cartel."

    linea = {}
    linea["sku"] = cartel["sku"]
    linea["titulo"] = cartel["titulo"]
    linea["categoria"] = cartel["categoria"]
    linea["etiquetas"] = []
    for etiqueta in cartel["tags_funcionales"]:
        linea["etiquetas"].append(etiqueta)
    linea["cantidad"] = 1
    linea["precio_unitario"] = 0
    linea["precio_original"] = cartel["precio"]
    linea["subtotal"] = 0
    linea["descuento"] = 0
    linea["total"] = 0
    linea["stock_producto"] = inventario[cartel["sku"]]
    linea["es_regalo"] = True
    carrito.append(linea)

# ---------------------------------------------------------------------------
# 7. Cálculo secuencial y guardado del resultado
# ---------------------------------------------------------------------------
# Único recorrido final sobre ``carrito``: en cada iteración se mutan tres
# acumuladores con ``+=``. ``subtotal`` suma los importes antes de descuento,
# ``descuento_total`` suma el descuento de cada línea y, una vez cerrado el for,
# ``total_final`` se deriva con una resta. No se recalcula ningún precio: este
# bloque solo lee el estado que los anteriores dejaron en la lista. Luego se
# construyen ``cliente``, ``resumen`` y ``resultado`` con asignaciones campo por
# campo; el orden de inserción fija el orden de claves del JSON, por eso el
# archivo es determinista. ``avisos`` se comparte por referencia en dos lugares
# del resultado. El bloque ``with`` abre el archivo en modo escritura y lo cierra
# automáticamente al salir; json.dump vuelca el dict con indentación y caracteres
# UTF-8 reales, y se añade un salto de línea final.

subtotal = 0
descuento_total = 0
total_final = 0

for linea in carrito:
    subtotal += linea["subtotal"]
    descuento_total += linea["descuento"]

total_final = subtotal - descuento_total

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
resumen["descuento_camaras_monto"] = descuento_camaras_monto
resumen["subtotal_camaras_con_descuento"] = subtotal_camaras - descuento_camaras_monto
resumen["subtotal"] = subtotal
resumen["descuento_total"] = descuento_total
resumen["total_final"] = total_final
resumen["total"] = total_final
resumen["avisos"] = avisos

resultado = {}
resultado["cliente"] = cliente
resultado["carrito"] = carrito
resultado["regalo"] = regalo
resultado["resumen"] = resumen
resultado["inventario"] = inventario
resultado["avisos"] = avisos

with RUTA_RESULTADO.open("w", encoding="utf-8") as archivo:
    json.dump(resultado, archivo, ensure_ascii=False, indent=2)
    archivo.write("\n")

# Al ejecutar como script los avisos van a stderr para no mezclarse con el JSON
# de stdout. El guardián ``__name__`` evita esta impresión si el archivo se importa.
if __name__ == "__main__":
    for aviso in avisos:
        sys.stderr.write("AVISO: " + aviso + "\n")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
