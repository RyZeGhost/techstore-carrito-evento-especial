# TechStore — Tienda de productos tecnológicos + Carrito Evento Especial (Python + Shopify)

Proyecto de la **Tarea 1: Desarrollo Multiparadigma en Python de un Componente de E-commerce con Asistencia de IA Generativa**.

TechStore es una tienda **de productos tecnológicos** (audio, periféricos, almacenamiento, pantallas, computadores, redes y accesorios). El catálogo completo está en `datos/catalogo.json`.

Contiene:

1. Integración con una tienda Shopify real mediante la Admin GraphQL API.
2. Carrito Evento Especial implementado en **tres paradigmas**: imperativo, orientado a objetos y funcional.
3. Documentación, registro de prompts y registro de errores corregidos.
4. Control de versiones en GitHub.

---

## 1. Instalación

Requiere Python 3.10 o superior.

```powershell
# Desde la raíz del proyecto
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copia la plantilla de credenciales y complétala:

```powershell
Copy-Item .env.example .env
```

Contenido de `.env`:

```ini
SHOPIFY_STORE_URL=techstore-d8vn3rhk.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_...          # usado por main.py (ShopifyAPI)
SHOPIFY_API_VERSION=2026-10
SHOPIFY_SHOP=techstore-d8vn3rhk.myshopify.com
SHOPIFY_CLIENT_ID=e8d52a9b0224bae336b05c4cd79aaa0a
SHOPIFY_CLIENT_SECRET=shpss_...         # secreto de la app en el Dev Dashboard
```

> `.env` está excluido por `.gitignore`. Nunca subas credenciales a GitHub.

La app de Shopify debe estar **instalada en la tienda** y tener los scopes `read_products`, `write_products`, `read_locations`, `read_inventory` y `write_inventory`.

---

## 2. Verificar la conexión

```powershell
.\.venv\Scripts\python.exe shopify_client.py
```

Salida esperada:

```
Conectado a: TechStore (techstore-d8vn3rhk.myshopify.com)
```

---

## 3. Ejecutar el carrito en los tres paradigmas

```powershell
.\.venv\Scripts\python.exe -m carrito.demo
```

Ejemplo de salida:

```
=== cumpleanos | 10 personas | cupón=FIESTA10 ===
  Imperativo           items=5, faltantes=0, 2x1=$2990, cupon=$8630, envio=$0, total=$77670
  Orientado a objetos  items=5, faltantes=0, 2x1=$2990, cupon=$8630, envio=$0, total=$77670
  Funcional            items=5, faltantes=0, 2x1=$2990, cupon=$8630, envio=$0, total=$77670
  >>> Paridad: OK
```

Uso programático:

```python
from carrito import cargar_catalogo, armar_imperativo

catalogo = cargar_catalogo()
resultado = armar_imperativo("cumpleanos", 10, catalogo, "FIESTA10")
print(resultado["total"])
```

Las otras dos funciones son `armar_objetos` y `armar_funcional`, con la misma firma.

---

## 4. Pruebas automáticas

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Verifican paridad entre paradigmas, cupón inválido, envío gratis y validaciones.

---

## 5. Integración con Shopify

Poblar el catálogo desde `datos/catalogo.json`:

```powershell
.\.venv\Scripts\python.exe -m scripts.poblar_catalogo --dry-run
.\.venv\Scripts\python.exe -m scripts.poblar_catalogo
```

El script:

- Consulta los SKUs existentes para no duplicar productos (idempotente).
- Obtiene la ubicación de inventario principal.
- Crea productos con precio, SKU, stock y categoría.
- Crea colecciones por categoría y agrega los productos.

Regenerar la documentación línea por línea:

```powershell
.\.venv\Scripts\python.exe -m scripts.generar_documentacion
```

---

## 6. Estructura del proyecto

```
.
├── .env.example               Plantilla de credenciales
├── .gitignore                 Excluye .env y el entorno virtual
├── requirements.txt           Dependencias
├── main.py                    Verificación con ShopifyAPI (token shpat_)
├── shopify_client.py          Cliente GraphQL con client credentials
├── datos/
│   └── catalogo.json          Fuente única de productos y reglas
├── carrito/
│   ├── datos.py               Carga del catálogo
│   ├── imperativo.py          Versión imperativa
│   ├── orientado_objetos.py   Versión orientada a objetos
│   ├── funcional.py           Versión funcional
│   ├── demo.py                Demostración y comparación
│   └── __init__.py
├── scripts/
│   ├── poblar_catalogo.py     Carga de productos y colecciones a Shopify
│   └── generar_documentacion.py
├── tests/
│   └── test_paridad.py        Pruebas automáticas
└── docs/
    ├── informe.md             Informe final
    ├── explicacion_lineas.md  Explicación línea por línea
    ├── errores_corregidos.md  Errores y correcciones
    └── prompts.md             Registro de prompts
```

---

## 7. Documentación

- [Informe final](docs/informe.md)
- [Explicación línea por línea](docs/explicacion_lineas.md)
- [Errores encontrados y corregidos](docs/errores_corregidos.md)
- [Registro de prompts](docs/prompts.md)
