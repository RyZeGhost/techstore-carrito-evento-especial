"""Regla transversal de segmentación de clientes: nuevo, frecuente y mayorista.

Es una función pura compartida por los tres paradigmas. El tipo se recibe como
parámetro (no se consulta Shopify): `None` representa a un invitado sin
beneficios, de modo que los resultados anteriores no cambian.

Los beneficios se configuran en `datos/catalogo.json` bajo `segmentos`:
descuento sobre la base ya descontada, envío gratis y estilo de recomendación.
"""

ESTILOS = ("economica", "premium", "alto_ticket")


def config_para(tipo_usuario, catalogo):
    """Devuelve `(clave, config)`; `clave` es None para un invitado."""
    if tipo_usuario is None:  # Sin segmento: mantiene el comportamiento original.
        return None, None
    if tipo_usuario not in catalogo["segmentos"]:
        raise ValueError(f"Tipo de usuario desconocido: {tipo_usuario}")
    return tipo_usuario, catalogo["segmentos"][tipo_usuario]


def descuento_para(base, tipo_usuario, catalogo):
    """Descuento del segmento sobre la base (ya sin 2x1 ni cupón)."""
    _, config = config_para(tipo_usuario, catalogo)
    if config is None:
        return 0
    return base * config["descuento_porcentaje"] // 100  # Enteros en CLP.


def envio_para(costo_envio, tipo_usuario, catalogo):
    """Anula el costo de envío cuando el segmento tiene ese beneficio."""
    _, config = config_para(tipo_usuario, catalogo)
    if config is not None and config["envio_gratis"]:
        return 0
    return costo_envio


def beneficios_para(tipo_usuario, catalogo):
    """Resumen de beneficios que se incluye en el resultado del carrito."""
    clave, config = config_para(tipo_usuario, catalogo)
    return {
        "envio_gratis": bool(config and config["envio_gratis"]),
        "estilo_recomendacion": config["recomendacion"] if config else "similar",
        "descripcion": config["descripcion"] if config else "Invitado",
        "segmento": clave or "invitado",
    }
