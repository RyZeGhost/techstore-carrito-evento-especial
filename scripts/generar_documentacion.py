"""Genera docs/explicacion_lineas.md a partir de los comentarios del código.

Cada línea del código fuente queda documentada en una tabla con su número
de línea, el contenido y la explicación tomada de sus comentarios.
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "docs" / "explicacion_lineas.md"

ARCHIVOS = [
    "shopify_client.py",
    "carrito/datos.py",
    "carrito/imperativo.py",
    "carrito/orientado_objetos.py",
    "carrito/funcional.py",
    "carrito/demo.py",
    "scripts/poblar_catalogo.py",
]


def explicar_linea(linea, comentario_pendiente):
    """Devuelve (código, explicación, nuevo_comentario_pendiente)."""
    texto = linea.strip()

    if texto.startswith("#"):  # Línea equivalente a un comentario suelto.
        comentario = texto.lstrip("#").strip()
        return texto, comentario, comentario

    if texto.startswith(('"""', "'''")):  # Docstring de módulo o función.
        return texto, "Docstring: describe el propósito del bloque.", comentario_pendiente

    # Comentario al final de la línea (fuera de cadenas en este proyecto).
    partes = re.split(r"\s#\s(?![^{]*\})", texto, maxsplit=1)
    if len(partes) == 2 and not partes[0].startswith("#"):
        codigo, comentario = partes
        return codigo.strip(), comentario.strip(), comentario_pendiente

    if not texto:  # Línea en blanco: separación visual.
        return "", "Línea en blanco: separa bloques lógicos.", comentario_pendiente

    # Código sin comentario propio: se explica con el comentario vigente,
    # que se consume aquí para no repetirlo en todo el resto del archivo.
    explicacion = comentario_pendiente or "Declaración o expresión del algoritmo; ver el bloque comentado anterior."
    return texto, explicacion, ""


def main():
    """Recorre los archivos y escribe el documento Markdown."""
    lineas = [
        "# Explicación línea por línea del código",
        "",
        "Documento generado automáticamente desde los comentarios del código fuente.",
        "La columna **Explicación** corresponde al comentario de la línea o al",
        "comentario del bloque que le precede inmediatamente.",
        "",
    ]

    for ruta_relativa in ARCHIVOS:  # Recorre cada archivo configurado.
        ruta = RAIZ / ruta_relativa  # Ruta absoluta al archivo.
        contenido = ruta.read_text(encoding="utf-8").splitlines()  # Líneas.
        lineas += [f"## `{ruta_relativa}`", "", "| Línea | Código | Explicación |", "|---:|---|---|"]

        pendiente = ""  # Comentario heredado del bloque anterior.
        for numero, linea in enumerate(contenido, start=1):  # Numeración real.
            codigo, explicacion, pendiente = explicar_linea(linea, pendiente)
            codigo = codigo.replace("|", "\\|")  # Escapa para Markdown.
            explicacion = explicacion.replace("|", "\\|")
            codigo = codigo.replace("\n", " ")
            lineas.append(f"| {numero} | `{codigo}` | {explicacion} |")

        lineas.append("")  # Separador entre archivos.

    SALIDA.parent.mkdir(parents=True, exist_ok=True)  # Crea docs/ si falta.
    SALIDA.write_text("\n".join(lineas) + "\n", encoding="utf-8")  # Escribe.
    print(f"Generado: {SALIDA}")


if __name__ == "__main__":
    main()
