"""Recomendaciones personalizadas por similitud de categoría y festividad.

Es una regla transversal: la usan los tres paradigmas para garantizar que la
misma entrada produzca exactamente las mismas sugerencias. La lógica es pura,
no modifica el catálogo ni el carrito y solo devuelve diccionarios nuevos.
"""

from carrito.datos import indice_productos
from carrito.segmentos import config_para


def categorias_en_carrito(items, productos):
    """Devuelve las categorías presentes en el carrito, sin repetir y en orden."""
    categorias = []  # Acumulador local: no se comparte con el llamador.
    for item in items:  # Recorre las líneas ya armadas.
        categoria = productos[item["sku"]]["categoria"]  # Categoría del SKU vendido.
        if categoria not in categorias:  # Evita duplicados.
            categorias.append(categoria)  # Respeta el orden de aparición.
    return categorias  # Tupla/lista nueva; el original no se toca.


def precio_promedio(categoria, items, productos):
    """Promedio de precios de una categoría dentro del carrito."""
    precios = [
        productos[item["sku"]]["precio"]
        for item in items
        if productos[item["sku"]]["categoria"] == categoria
    ]
    return sum(precios) / len(precios) if precios else 0


def clave_orden(estilo, producto, promedio):
    """Clave de ordenación según el perfil del cliente."""
    if estilo == "economica":  # Nuevo: accesorios de entrada, los más baratos.
        return (producto["precio"], producto["sku"])
    if estilo == "premium":  # Frecuente: gama alta de la categoría.
        return (-producto["precio"], producto["sku"])
    if estilo == "alto_ticket":  # Mayorista: mayor valor disponible para volumen.
        return (-producto["precio"] * producto["stock"], producto["sku"])
    # Invitado: el similar clásico, más cercano al promedio del carrito.
    return (abs(producto["precio"] - promedio), producto["sku"])


def sugerir(items, catalogo, evento, tipo_usuario=None):
    """Sugiere hasta `maximo` productos según festividad y segmento."""
    config = catalogo["recomendaciones"]  # Regla configurable desde el JSON.
    clave, segmento = config_para(tipo_usuario, catalogo)  # Valida el tipo.
    estilo = segmento["recomendacion"] if segmento else "similar"
    perfil = clave or "invitado"
    productos = indice_productos(catalogo)  # {sku: producto}, acceso O(1).
    festivo = evento in config["eventos_festivos"]  # Solo ciertos eventos.
    porcentaje = config["descuento_porcentaje"] if festivo else 0

    usados = {item["sku"] for item in items}  # SKUs que ya están en el carrito.
    seleccionados = []  # Acumulador de sugerencias nuevas.

    for categoria in categorias_en_carrito(items, productos):
        if len(seleccionados) >= config["maximo"]:
            break  # Ya se completó el cupo de sugerencias.

        promedio = precio_promedio(categoria, items, productos)
        opciones = [
            producto
            for producto in catalogo["productos"]
            if producto["categoria"] == categoria
            and producto["sku"] not in usados
            and producto["stock"] > 0
        ]
        # El perfil cambia el criterio; invitado usa el precio más cercano al promedio.
        opciones.sort(key=lambda p: clave_orden(estilo, p, promedio))

        for producto in opciones[: config["por_categoria"]]:
            if len(seleccionados) >= config["maximo"]:
                break
            descuento = producto["precio"] * porcentaje // 100  # Enteros en CLP.
            seleccionados.append({
                "sku": producto["sku"],
                "nombre": producto["nombre"],
                "categoria": producto["categoria"],
                "precio": producto["precio"],
                "descuento": descuento,
                "precio_final": producto["precio"] - descuento,
                "motivo": "festividad" if festivo else "similar",
                "perfil": perfil,  # Segmento que originó la sugerencia.
            })
            usados.add(producto["sku"])  # No repetir sugerencias.

    return seleccionados
