"""Aplica paginación al catálogo de la tienda y estilos mínimos.

Requiere que la app tenga los scopes `read_themes` y `write_themes`
instalados en la tienda. Si no están, la API responde ACCESS_DENIED.

Uso:
    python -m scripts.actualizar_tema --dry-run   # muestra los cambios
    python -m scripts.actualizar_tema             # escribe en el tema activo
"""

import argparse
import re
from pathlib import Path

from shopify_client import rest_request

POR_PAGINA = 12
RESPALDO = Path(__file__).resolve().parent.parent / "backups"

SECCIONES = (
    "sections/main-collection-product-grid.liquid",
    "sections/collection-template.liquid",
    "templates/collection.liquid",
)

CSS = """\
/* TechStore: paginación legible y tarjetas uniformes */
.pagination { display: flex; gap: .5rem; justify-content: center; margin: 2rem 0; flex-wrap: wrap; }
.pagination a, .pagination .current { padding: .5rem .9rem; border: 1px solid #d9d9d9; border-radius: 6px; text-decoration: none; }
.pagination .current { background: #1f2937; color: #fff; border-color: #1f2937; }
.product-grid > li { display: flex; }
.product-grid .card { width: 100%; }
"""


def tema_activo():
    """Devuelve el tema publicado (role=main)."""
    temas = rest_request("GET", "themes.json")["themes"]
    activo = next((t for t in temas if t.get("role") == "main"), None)
    if not activo:
        raise RuntimeError("No hay un tema publicado (role=main)")
    return activo


def leer_asset(tema_id, clave):
    """Lee un archivo del tema; devuelve None si no existe."""
    try:
        respuesta = rest_request(
            "GET", f"themes/{tema_id}/assets.json?asset[key]={clave}"
        )
        return respuesta["asset"]["value"]
    except RuntimeError as error:
        if "404" in str(error) or "Not Found" in str(error):
            return None
        raise


def escribir_asset(tema_id, clave, contenido, dry_run=False):
    """Guarda un archivo del tema (o solo lo simula en dry-run)."""
    if dry_run:
        print(f"  [DRY RUN] Escribir {clave} ({len(contenido)} caracteres)")
        return
    rest_request(
        "PUT",
        f"themes/{tema_id}/assets.json",
        {"asset": {"key": clave, "value": contenido}},
    )
    print(f"  Escrito {clave}")


def aplicar_paginacion(contenido):
    """Fuerza 12 productos por página y asegura que exista el control de paginación."""
    if "paginate collection.products" in contenido:
        # El tema ya pagina: solo cambiamos el tamaño de página.
        modificado = re.sub(
            r"(\{%-?\s*paginate\s+collection\.products\s+by\s+)([^\n%]+?)(\s*-?%\})",
            rf"\g<1>{POR_PAGINA}\g<3>",
            contenido,
            count=1,
        )
        # Respaldo por si el tema usa otra forma de escribir la etiqueta.
        if f"by {POR_PAGINA}" not in modificado:
            modificado = contenido.replace(
                "section.settings.products_per_page", str(POR_PAGINA), 1
            )
        print(f"  Paginación existente ajustada a {POR_PAGINA} productos")
    else:
        inicio = re.search(
            r"\{%-?\s*for\s+product\s+in\s+collection\.products[^\n]*?%\}", contenido
        )
        if not inicio:
            return contenido, False
        fin = re.search(r"\{%-?\s*endfor\s*-?%\}", contenido[inicio.end():])
        if not fin:
            return contenido, False
        fin_abs = inicio.end() + fin.end()
        modificado = (
            contenido[: inicio.start()]
            + "{% paginate collection.products by "
            + str(POR_PAGINA)
            + " %}\n"
            + contenido[inicio.start():fin_abs]
            + "\n{% endpaginate %}"
            + contenido[fin_abs:]
        )
        print(f"  Paginación agregada ({POR_PAGINA} productos por página)")

    if "default_pagination" not in modificado and "render 'pagination'" not in modificado:
        modificado = modificado.replace(
            "{% endpaginate %}",
            "{{ paginate | default_pagination }}\n{% endpaginate %}",
            1,
        )
        print("  Control de páginas agregado")
    return modificado, True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="no escribe en Shopify")
    args = parser.parse_args()

    tema = tema_activo()
    print(f"Tema activo: {tema['name']} (id={tema['id']})")

    clave = None
    original = None
    for candidata in SECCIONES:
        contenido = leer_asset(tema["id"], candidata)
        if contenido:
            clave, original = candidata, contenido
            break
    if not clave:
        raise RuntimeError("No se encontró la plantilla de colección del tema")

    modificado, cambio = aplicar_paginacion(original)
    if not cambio:
        print("No se encontró el bucle de productos; no se modificó la plantilla")
        return 0

    if not args.dry_run:
        RESPALDO.mkdir(exist_ok=True)
        (RESPALDO / clave.replace("/", "_")).write_text(original, encoding="utf-8")
        print(f"  Respaldo guardado en backups/{clave.replace('/', '_')}")

    escribir_asset(tema["id"], clave, modificado, args.dry_run)

    # Alineamos también el JSON que guarda el ajuste "products_per_page".
    # Según la versión de Dawn puede vivir con la sección o en el template.
    for clave_settings in (clave.replace(".liquid", ".json"), "templates/collection.json"):
        settings = leer_asset(tema["id"], clave_settings)
        if not settings or "products_per_page" not in settings:
            continue
        nuevo_settings = re.sub(
            r'("products_per_page"\s*:\s*)\d+', rf"\g<1>{POR_PAGINA}", settings, count=1
        )
        if not args.dry_run:
            RESPALDO.mkdir(exist_ok=True)
            (RESPALDO / clave_settings.replace("/", "_")).write_text(
                settings, encoding="utf-8"
            )
        escribir_asset(tema["id"], clave_settings, nuevo_settings, args.dry_run)

    escribir_asset(tema["id"], "assets/techstore-paginas.css", CSS, args.dry_run)

    # Vinculamos la hoja de estilos en el layout sin duplicarla.
    layout = leer_asset(tema["id"], "layout/theme.liquid")
    if layout and "techstore-paginas.css" not in layout:
        nuevo_layout = layout.replace(
            "</head>",
            "{{ 'techstore-paginas.css' | asset_url | stylesheet_tag }}\n</head>",
            1,
        )
        if not args.dry_run:
            RESPALDO.mkdir(exist_ok=True)
            (RESPALDO / "layout_theme.liquid").write_text(layout, encoding="utf-8")
        escribir_asset(tema["id"], "layout/theme.liquid", nuevo_layout, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
