"""Verificación de conexión con la Admin GraphQL API de Shopify.

Uso:
    python main.py            # comprueba la conexión (no modifica nada)
    python main.py --info     # muestra además la versión y el plan de la tienda

La carga del catálogo se realiza con:
    python -m scripts.poblar_catalogo
"""

import argparse

from shopify_client import API_VERSION, graphql_query


def verificar_conexion() -> dict:
    """Devuelve los datos básicos de la tienda o lanza un error con el motivo."""
    datos = graphql_query("{ shop { name myshopifyDomain } }")
    tienda = datos["shop"]
    print(f"Conectado exitosamente a: {tienda['name']} ({tienda['myshopifyDomain']})")
    return tienda


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--info", action="store_true", help="muestra versión y plan")
    parser.add_argument("--crear-ejemplo", action="store_true",
                        help="obsoleto: usa python -m scripts.poblar_catalogo")
    parser.add_argument("--dry-run", action="store_true",
                        help="obsoleto: usa python -m scripts.poblar_catalogo --dry-run")
    args = parser.parse_args()

    try:
        tienda = verificar_conexion()
    except Exception as error:
        print(f"Error: {error}")
        raise SystemExit(1) from None

    if args.info:
        print(f"  API version: {API_VERSION}")

    if args.crear_ejemplo or args.dry_run:
        print("  Nota: la creación de productos se hace con "
              "'python -m scripts.poblar_catalogo'")


if __name__ == "__main__":
    main()
