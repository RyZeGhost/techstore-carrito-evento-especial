"""Aplica la identidad visual TechStore (tech oscuro/azul) al tema activo.

El tema es Dawn y define sus colores con variables CSS en `layout/theme.liquid`.
Esta hoja se carga al final del `<head>` para sobrescribirlas sin editar el
archivo original. La paginación aplicada por `actualizar_tema.py` se conserva.

Uso:
    python -m scripts.estilizar_tema --dry-run
    python -m scripts.estilizar_tema
"""

import argparse
from pathlib import Path

from shopify_client import rest_request

RESPALDO = Path(__file__).resolve().parent.parent / "backups"
ASSET = "assets/techstore-estilo.css"
NOMBRE_CSS = ASSET.removeprefix("assets/")
ETIQUETA_CSS = "{{ '" + NOMBRE_CSS + "' | asset_url | stylesheet_tag }}"
LAYOUT = "layout/theme.liquid"

CSS = """\
/* TechStore — identidad visual tech oscuro/azul */
:root {
  color-scheme: dark;
  --color-base-background-1: 12 18 32;
  --color-base-background-2: 23 33 54;
  --color-base-text: 233 240 249;
  --color-base-accent-1: 14 165 233;
  --color-base-accent-2: 37 99 235;
  --color-base-solid-button-labels: 255 255 255;
  --color-base-outline-button-labels: 203 213 225;
  --color-shadow: 0 10px 30px rgba(2, 6, 23, 0.45);
  --borde-tech: rgba(148, 163, 184, 0.28);
  --radio-tech: 12px;
}

html { scroll-behavior: smooth; }
/* El tema Dawn fija el fondo en base.css; se fuerza el azul oscuro para que
   la identidad visual se vea también en el catálogo publicado. */
html, body {
  background-color: #0c1220 !important;
  color: rgb(var(--color-base-text)) !important;
}
a:hover { color: rgb(var(--color-base-accent-1)); }

.header {
  background: rgba(12, 18, 32, 0.94) !important;
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--borde-tech);
}
.header__logo { font-weight: 800; letter-spacing: 0.02em; }

.button {
  border-radius: 999px !important;
  font-weight: 600;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(14, 165, 233, 0.25);
}
.button--primary {
  background: linear-gradient(
    90deg,
    rgb(var(--color-base-accent-1)),
    rgb(var(--color-base-accent-2))
  ) !important;
  color: #fff !important;
  border: 0 !important;
}

.card,
.card--standard {
  border: 1px solid var(--borde-tech) !important;
  border-radius: var(--radio-tech) !important;
  box-shadow: var(--color-shadow);
  overflow: hidden;
  transition: transform 0.2s ease, border-color 0.2s ease;
}
.card:hover {
  transform: translateY(-4px);
  border-color: rgb(var(--color-base-accent-1)) !important;
}
.card__media img { border-radius: var(--radio-tech) var(--radio-tech) 0 0; }
.card__information { padding: 1rem; }
.price { font-weight: 700; }

/* Paginación acorde con el tema oscuro (refuerza techstore-paginas.css). */
.pagination { display: flex; gap: 0.5rem; justify-content: center; margin: 2rem 0; flex-wrap: wrap; }
.pagination a,
.pagination .current {
  padding: 0.5rem 0.9rem;
  border: 1px solid var(--borde-tech);
  border-radius: 8px;
  text-decoration: none;
  color: rgb(var(--color-base-text));
}
.pagination .current {
  background: linear-gradient(90deg, rgb(var(--color-base-accent-1)), rgb(var(--color-base-accent-2)));
  color: #fff;
  border-color: transparent;
}

.section { padding-block: 3rem; }
.footer {
  background: rgb(var(--color-base-background-2)) !important;
  border-top: 1px solid var(--borde-tech);
}
input, select, textarea {
  background: rgba(255, 255, 255, 0.06);
  color: inherit;
  border: 1px solid var(--borde-tech);
  border-radius: 8px;
}
"""


def tema_activo():
    """Devuelve el tema publicado."""
    temas = rest_request("GET", "themes.json")["themes"]
    activo = next((t for t in temas if t.get("role") == "main"), None)
    if not activo:
        raise RuntimeError("No hay un tema publicado (role=main)")
    return activo


def leer_asset(tema_id, clave):
    """Lee un asset del tema."""
    return rest_request("GET", f"themes/{tema_id}/assets.json?asset[key]={clave}")["asset"]["value"]


def escribir_asset(tema_id, clave, contenido, dry_run=False):
    """Escribe un asset o solo lo simula."""
    if dry_run:
        print(f"  [DRY RUN] Escribir {clave} ({len(contenido)} caracteres)")
        return
    rest_request(
        "PUT",
        f"themes/{tema_id}/assets.json",
        {"asset": {"key": clave, "value": contenido}},
    )
    print(f"  Escrito {clave}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="no escribe en Shopify")
    args = parser.parse_args()

    tema = tema_activo()
    print(f"Tema activo: {tema['name']} (id={tema['id']})")
    escribir_asset(tema["id"], ASSET, CSS, args.dry_run)

    original = leer_asset(tema["id"], LAYOUT)
    # Se eliminan enlaces duplicados y se garantiza uno solo antes de </head>.
    lineas = [
        linea for linea in original.splitlines() if linea.strip() != ETIQUETA_CSS
    ]
    limpio = "\n".join(lineas)
    if limpio == original:
        print("  La hoja de estilo ya estaba vinculada una sola vez")
        return 0

    nuevo = limpio.replace("</head>", ETIQUETA_CSS + "\n</head>", 1)
    if not args.dry_run:
        RESPALDO.mkdir(exist_ok=True)
        (RESPALDO / "layout_theme_estilo.liquid").write_text(original, encoding="utf-8")
        print("  Respaldo guardado en backups/layout_theme_estilo.liquid")
    escribir_asset(tema["id"], LAYOUT, nuevo, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
