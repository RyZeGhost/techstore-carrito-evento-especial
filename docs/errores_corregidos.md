# Errores encontrados y correcciones aplicadas

Este registro describe los fallos reales que aparecieron durante la construcción del proyecto y cómo se resolvieron. Se conserva porque el enunciado exige supervisión de código generado con IA.

| # | Error | Causa | Corrección |
|---|-------|-------|------------|
| 1 | `pip : El término 'pip' no se reconoce...` | El `python` del PATH apuntaba a MSYS2 sin `pip`. | Se usó `py -m venv .venv` (Python 3.14) y se instalaron las dependencias dentro del entorno virtual. |
| 2 | `No module named pip` al ejecutar `python -m pip` | Mismo intérprete MSYS2 sin módulo pip. | Se abandonó ese intérprete; todos los comandos usan `.venv\Scripts\python.exe`. |
| 3 | `ModuleNotFoundError: requests` | `requests` no estaba en `requirements.txt`. | Se añadió `requests>=2.31.0` al archivo y se instaló en el venv. |
| 4 | `Faltan credenciales en el archivo .env` | No existía el archivo `.env`. | Se creó `.env.example` como plantilla y el usuario creó `.env` con sus valores reales. |
| 5 | `HTTP 401: Invalid API key or access token` al conectar con `ShopifyAPI` | Se estaba usando un valor `shpss_...` (Client Secret de la app) como si fuera un Admin API access token (`shpat_...`). | Se cambió el enfoque: el `shpss_...` se usa como `SHOPIFY_CLIENT_SECRET` y se solicita un token mediante `grant_type=client_credentials`. |
| 6 | API version `2024-01` obsoleta | Era la versión del script original; Shopify ya la retiró. | Se actualizó `main.py` a `2026-10`. El cliente nuevo usa `2026-01` por indicación del enunciado (ambas versiones estaban soportadas en la fecha del taller). |
| 7 | `Faltan variables en .env: SHOPIFY_CLIENT_ID` | El flujo de client credentials necesita también el ID de la app. | Se añadió `SHOPIFY_CLIENT_ID` al `.env` con el valor entregado por el usuario. |
| 8 | `400 - Oauth error app_not_installed` | La app del Dev Dashboard existía pero no estaba instalada en la tienda. | Se instaló la app desde Dev Dashboard → **Installs → Install app**, seleccionando la tienda `techstore-d8vn3rhk`. Tras esto la prueba devolvió `Conectado a: TechStore (...)`. |
| 9 | Endpoint escrito como `https://techstore/admin/oauth/access_token` | `techstore` solo es el subdominio; Shopify exige el dominio completo. | Se implementó `normalizar_shop()` para aceptar `techstore`, `techstore.myshopify.com` o la URL con `/admin`, y construir `https://<shop>.myshopify.com/admin/...`. |
| 10 | Traceback extenso con HTML en errores HTTP | `raise_for_status()` no mostraba el cuerpo; la página de error de OAuth ensuciaba la salida. | Se añadió `resumen_error()` en `shopify_client.py`, que extrae el `<title>` del HTML o el JSON del error. |
| 11 | Error de tipeo `diccionarioPython` y carácter extraño en docstrings | Errores de redacción al generar los módulos. | Se corrigieron los docstrings de `carrito/datos.py` y `carrito/orientado_objetos.py`. |
| 12 | El caso de prueba de envío pagado dejó de ejercitar esa ruta | Al cambiar el catálogo a tecnología, el carrito mínimo subió por encima de `$50.000` y el envío quedaba gratis. | Se incorporó el evento `accesorios_basicos` (productos económicos) y el caso `accesorios_basicos, 1 persona`, con total `$40.940` y envío `$3.990`. |
| 13 | `Access denied for products field. (ACCESS_DENIED)` al poblar el catálogo | La app instalada solo tenía scopes de lectura básica; faltaban `read_products`, `write_products`, `read_locations` y `read_inventory/write_inventory`. | **Pendiente de corregir por el usuario:** agregar esos scopes a una nueva versión de la app en el Dev Dashboard, liberarla y aprobar el cambio en la tienda. El script `scripts/poblar_catalogo.py` ya está listo y es idempotente. |
| 14 | El catálogo inicial no representaba una tienda tecnológica | Los primeros productos eran de fiesta y útiles escolares, pero el docente indicó que TechStore debía vender tecnología. | Se reemplazó `datos/catalogo.json` por 22 SKU tecnológicos (audio, periféricos, almacenamiento, pantallas, computadores, redes y accesorios), se renombró el evento `asado` a `trabajo_remoto`, se agregó `accesorios_basicos` y se actualizaron reglas, sustitutos, pruebas y documentación. |

## Estado final verificado

- `python -m carrito.demo` → los cinco casos producen resultados idénticos en los tres paradigmas.
- `python -m unittest discover -s tests -v` → 4 pruebas, todas OK.
- `python shopify_client.py` → `Conectado a: TechStore (techstore-d8vn3rhk.myshopify.com)`.
- Poblado de catálogo → bloqueado únicamente por los scopes indicados en el punto 13.
