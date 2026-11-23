"""Recomendaciones personalizadas por similitud de categoría y festividad.

Es una regla transversal: la usan los tres paradigmas para garantizar que la
misma entrada produzca exactamente las mismas sugerencias. La lógica es pura,
no modifica el catálogo ni el carrito y solo devuelve diccionarios nuevos.
"""

from carrito.datos import indice_productos


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


def sugerir(items, catalogo, evento):
    """Sugiere hasta `maximo` productos similares con descuento en festividades."""
    config = catalogo["recomendaciones"]  # Regla configurable desde el JSON.
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
        # "Similar" = precio más cercano al promedio de esa categoría en el carrito.
        opciones.sort(key=lambda p: (abs(p["precio"] - promedio), p["sku"]))

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
            })
            usados.add(producto["sku"])  # No repetir sugerencias.

    return seleccionados
