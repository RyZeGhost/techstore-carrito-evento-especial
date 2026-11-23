# TechStore — Tienda de productos tecnológicos + Carrito Evento Especial (Python + Shopify)

Proyecto de la **Tarea 1: Desarrollo Multiparadigma en Python de un Componente de E-commerce con Asistencia de IA Generativa**.

TechStore es una tienda **de productos tecnológicos** con **34 SKU en 8 categorías** (audio, accesorios, energía, periféricos, almacenamiento, pantallas, computadores y redes). El catálogo completo está en `datos/catalogo.json`. El catálogo se muestra **paginado a 12 productos por página** y solo conserva la Gift Card de crédito como artículo no tecnológico.

Contiene:

1. Integración con una tienda Shopify real mediante la Admin GraphQL API.
2. Carrito Evento Especial implementado en **tres paradigmas**: imperativo, orientado a objetos y funcional, con **recomendaciones personalizadas** de productos similares y descuento en festividades.
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
SHOPIFY_SHOP=techstore-d8vn3rhk.myshopify.com
SHOPIFY_CLIENT_ID=tu-client-id
SHOPIFY_CLIENT_SECRET=shpss_...         # secreto de la app en el Dev Dashboard

# Heredados del primer enfoque (REST). Ya no son necesarios:
SHOPIFY_STORE_URL=techstore-d8vn3rhk.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_...
SHOPIFY_API_VERSION=2026-10

PUERTO_API=8000
```

> `shpss_...` es el **Client Secret** y se usa solo para pedir el token con `client_credentials`. Usarlo como `SHOPIFY_ACCESS_TOKEN` produce HTTP 401. `main.py` y los scripts ya no dependen de un token `shpat_`.

> `.env` está excluido por `.gitignore`. Nunca subas credenciales a GitHub.

La app de Shopify debe estar **instalada en la tienda** y tener los scopes de productos e inventario (`write_products` y `write_inventory`, que implican lectura). Para modificar el tema hace falta además `read_themes` y `write_themes`; sin ellos la API responde `ACCESS_DENIED`. `read_locations` no es obligatorio: el script solo consulta el ID de la ubicación, no su nombre.

---

## 2. Verificar la conexión

```powershell
.\.venv\Scripts\python.exe shopify_client.py
```

Salida esperada:

```
Conectado a: TechStore (techstore-d8vn3rhk.myshopify.com)
```

También puedes verificarlo con `main.py` (muestra la versión de la API):

```powershell
.\.venv\Scripts\python.exe main.py --info
```

```
Conectado exitosamente a: TechStore (techstore-d8vn3rhk.myshopify.com)
  API version: 2026-01
```

---

## 3. Ejecutar el carrito en los tres paradigmas

```powershell
.\.venv\Scripts\python.exe -m carrito.demo
```

Ejemplo de salida:

```
=== cumpleanos | 10 personas | cupón=FIESTA10 ===
  Imperativo           items=5, faltantes=0, 2x1=$13980, cupon=$15892, envio=$0, total=$143028, recs=2
  Orientado a objetos  items=5, faltantes=0, 2x1=$13980, cupon=$15892, envio=$0, total=$143028, recs=2
  Funcional            items=5, faltantes=0, 2x1=$13980, cupon=$15892, envio=$0, total=$143028, recs=2
  >>> Paridad: OK
    Recomendado: Auriculares deportivos in-ear (Audio) $19990 -> $16992 [festividad]
    Recomendado: Funda para notebook 14 pulgadas (Accesorios) $14990 -> $12742 [festividad]
```

Uso programático:

```python
from carrito import cargar_catalogo, armar_imperativo

catalogo = cargar_catalogo()
resultado = armar_imperativo("cumpleanos", 10, catalogo, "FIESTA10")
print(resultado["total"])
```

Las otras dos funciones son `armar_objetos` y `armar_funcional`, con la misma firma.

El resultado incluye `recomendaciones`: hasta 2 productos de las categorías presentes en el carrito, con el precio más cercano al promedio de su categoría. En los eventos marcados como festivos en `datos/catalogo.json` (`cumpleanos` y `vuelta_a_clases`) se aplica un 15 % de descuento (`motivo: "festividad"`); en el resto se muestran sin descuento (`motivo: "similar"`). Son ofertas informativas: **no se suman a `items` ni modifican `total`**.

---

## 4. Pruebas automáticas

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Verifican paridad entre paradigmas, cupón inválido, envío gratis, recomendaciones en festividad y sin festividad, y validaciones (7 pruebas).

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
- Crea productos con precio, SKU, stock, categoría e imagen.
- Sincroniza precio e imagen de los productos que ya existen.
- Crea colecciones por categoría y agrega los productos.
- Reintenta con backoff exponencial y registra los fallos en `logs/shopify_errores.log` (excluido de Git).

Ajustar la interfaz y la paginación del tema activo (requiere scopes de tema):

```powershell
.\.venv\Scripts\python.exe -m scripts.actualizar_tema --dry-run
.\.venv\Scripts\python.exe -m scripts.actualizar_tema
```

El script fuerza **12 productos por página**, asegura el control de navegación entre páginas, vincula `assets/techstore-paginas.css` en `layout/theme.liquid` y guarda respaldos de los archivos originales en `backups/` (excluido de Git).

Regenerar la documentación línea por línea:

```powershell
.\.venv\Scripts\python.exe -m scripts.generar_documentacion
```

---

## 6. API HTTP del carrito

Servicio mínimo que expone los tres paradigmas sin dependencias adicionales:

```powershell
.\.venv\Scripts\python.exe -m scripts.api_carrito
```

En otra terminal:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/eventos
$cuerpo = '{"evento":"cumpleanos","personas":10,"cupon":"FIESTA10","paradigma":"todos"}'
$r = Invoke-RestMethod http://127.0.0.1:8000/carrito -Method Post -ContentType "application/json" -Body $cuerpo
$r.imperativo.total                  # 143028
$r.imperativo.recomendaciones.Count  # 2
$r.orientado_objetos.total
$r.funcional.total
```

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado y cantidad de productos |
| GET | `/eventos` | Eventos y sus reglas |
| POST | `/carrito` | Resultado de uno o los tres paradigmas |

El campo `paradigma` acepta `imperativo`, `orientado_objetos`, `funcional` o `todos` (por defecto). Las entradas inválidas devuelven HTTP 400 con un mensaje describiendo el error. El puerto se puede cambiar con `PUERTO_API` en `.env`.

---

## 7. Estructura del proyecto

```
.
├── .env.example               Plantilla de credenciales
├── .gitignore                 Excluye .env y el entorno virtual
├── requirements.txt           Dependencias
├── main.py                    Verificación de conexión (GraphQL, client credentials)
├── shopify_client.py          Cliente GraphQL con backoff exponencial
├── datos/
│   └── catalogo.json          Fuente única de productos y reglas
├── carrito/
│   ├── datos.py               Carga y validación del catálogo
│   ├── recomendaciones.py     Sugerencias por similitud y festividad
│   ├── imperativo.py          Versión imperativa
│   ├── orientado_objetos.py   Versión orientada a objetos
│   ├── funcional.py           Versión funcional
│   ├── demo.py                Demostración y comparación
│   └── __init__.py
├── scripts/
│   ├── poblar_catalogo.py     Carga de productos y colecciones a Shopify
│   ├── api_carrito.py         API HTTP de los tres paradigmas
│   └── generar_documentacion.py
├── tests/
│   └── test_paridad.py        Pruebas automáticas
└── docs/
    ├── informe.md             Informe final
    ├── explicacion_lineas.md  Explicación línea por línea
    ├── errores_corregidos.md  Errores y correcciones
    ├── prompts.md             Registro de prompts
    └── presentacion.md        Diapositivas de la exposición
```

---

## 8. Documentación

- [Informe final](docs/informe.md)
- [Explicación línea por línea](docs/explicacion_lineas.md)
- [Errores encontrados y corregidos](docs/errores_corregidos.md)
- [Registro de prompts](docs/prompts.md)
- [Presentación final](docs/presentacion.md)
