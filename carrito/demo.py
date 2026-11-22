"""Demostración: ejecuta las tres versiones con las mismas entradas y las compara.

Uso desde la raíz del proyecto:
    python -m carrito.demo
"""

from carrito import (
    armar_funcional,
    armar_imperativo,
    armar_objetos,
    cargar_catalogo,
)

# Casos de prueba definidos una sola vez para las tres implementaciones.
CASOS = [
    ("cumpleanos", 10, "FIESTA10"),
    ("trabajo_remoto", 12, "HOME10"),
    ("vuelta_a_clases", 12, "ESCUELA10"),
    ("cumpleanos", 200, None),  # Fuerza sustituciones y faltantes por stock.
    ("accesorios_basicos", 1, None),  # Monto bajo: debe cobrar envío.
]

# Las tres funciones se agrupan en una tupla para iterarlas por igual.
IMPLEMENTACIONES = (
    ("Imperativo", armar_imperativo),
    ("Orientado a objetos", armar_objetos),
    ("Funcional", armar_funcional),
)


def formatear(resultado):
    """Resume un resultado para mostrarlo en pantalla."""
    return (
        f"items={len(resultado['items'])}, "
        f"faltantes={len(resultado['faltantes'])}, "
        f"2x1=${resultado['descuentos']['2x1']}, "
        f"cupon=${resultado['descuentos']['cupon']}, "
        f"envio=${resultado['envio']}, total=${resultado['total']}"
    )


def main():
    """Ejecuta todos los casos y verifica que los tres resultados sean iguales."""
    catalogo = cargar_catalogo()  # Misma fuente de datos para todos.
    todos_iguales = True  # Bandera global del resultado de la comparación.

    for evento, personas, cupon in CASOS:  # Recorre los escenarios.
        print(f"\n=== {evento} | {personas} personas | cupón={cupon} ===")
        resultados = []  # Resultados de las tres implementaciones.

        for nombre, funcion in IMPLEMENTACIONES:  # Recorre los paradigmas.
            resultado = funcion(evento, personas, catalogo, cupon)  # Ejecuta.
            resultados.append(resultado)  # Guarda para comparar.
            print(f"  {nombre:<20} {formatear(resultado)}")

        # Comparación estricta: los tres dict deben ser exactamente iguales.
        iguales = resultados[0] == resultados[1] == resultados[2]
        todos_iguales = todos_iguales and iguales  # Actualiza la bandera.
        print(f"  >>> Paridad: {'OK' if iguales else 'FALLO'}")

        # Detalle del caso de stock agotado para hacer visible la sustitución.
        if personas == 200:
            for item in resultados[0]["items"]:
                if item["sustituto_de"]:
                    print(
                        f"    Sustituto: {item['sustituto_de']} -> "
                        f"{item['sku']} x{item['cantidad']}"
                    )
            for falta in resultados[0]["faltantes"]:
                print(f"    Faltante: {falta['sku']} x{falta['cantidad']}")

    print(f"\nResultado global: {'TODOS LOS CASOS COINCIDEN' if todos_iguales else 'HAY DIFERENCIAS'}")
    return 0 if todos_iguales else 1  # Código de salida para CI.


if __name__ == "__main__":
    raise SystemExit(main())  # Permite usar el demo en scripts y tests.
