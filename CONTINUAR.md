# CONTINUAR.md — Estado para retomar el proyecto desde otro dispositivo

Este archivo es el **punto de partida** si el proyecto se abre desde GitHub en otro equipo. Todo lo que estaba avanzado al 24 de noviembre de 2026 quedó versionado en el commit que incluye este archivo. Las credenciales y la contraseña de la tienda **no están aquí ni en el repositorio**.

---

## 1. Preparación en el otro dispositivo

```powershell
git clone https://github.com/RyZeGhost/techstore-carrito-evento-especial.git
cd techstore-carrito-evento-especial
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env
```

Después edita `.env` con las credenciales reales (pedírselas al usuario). Nunca hacer commit de `.env`.

Verificación inicial:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m carrito.demo
.\.venv\Scripts\python.exe shopify_client.py
.\.venv\Scripts\python.exe main.py --info
```

Resultado esperado: **11/11 tests OK**, `Resultado global: TODOS LOS CASOS COINCIDEN`, conexión a `TechStore` y API `2026-01`.

---

## 2. Datos fijos del proyecto

| Dato | Valor |
|---|---|
| Tienda | `techstore-d8vn3rhk.myshopify.com` |
| Repositorio | `https://github.com/RyZeGhost/techstore-carrito-evento-especial` |
| API Shopify | Admin GraphQL `2026-01` |
| Tema activo | `test-data`, id `189417029881` |
| Moneda | CLP |
| Catálogo | 34 SKU tecnológicos + 1 Gift Card |
| Colecciones | audio, accesorios, energía, periféricos, almacenamiento, pantallas, computadores, redes |
| Paginación | 12 productos por página (3 páginas en `/collections/all`) |
| Estilo | Tech oscuro/azul aplicado por `scripts/estilizar_tema.py` |

Autenticación correcta: flujo `client_credentials` con `SHOPIFY_CLIENT_ID` + `SHOPIFY_CLIENT_SECRET` (`shpss_...`) → token de 24 h → header `X-Shopify-Access-Token`. **No usar el `shpss_...` como token `shpat_`.**

Scopes disponibles: `write_products`, `write_inventory`, `read_themes`, `write_themes`. No hay `read_locations` ni `read_discounts`.

---

## 3. Estado real en Shopify al pausar

- Los 34 SKU technician tienen `publishedAt` no nulo; antes estaban `ACTIVE` pero invisibles en Online Store.
- `/collections/all` muestra 35 productos (34 tecnológicos + Gift Card), 12 por página, con controles `1 2 3`.
- `sections/main-collection-product-grid.liquid` contiene `{%- paginate collection.products by 12 -%}` y `{% render 'pagination', paginate: paginate, anchor: '' %}`.
- `templates/collection.json` tiene `"products_per_page": 12`.
- `layout/theme.liquid` vincula una sola vez cada hoja:
  - `techstore-paginas.css`
  - `techstore-estilo.css`
- Fondo verificado en navegador: `rgb(12, 18, 32)`; texto `rgb(233, 240, 249)`.
- Respaldo de temas en `backups/` (carpeta ignorada por Git).

Comandos que aplican el estado del tema si hiciera falta repetirlo:

```powershell
.\.venv\Scripts\python.exe -m scripts.poblar_catalogo
.\.venv\Scripts\python.exe -m scripts.actualizar_tema
.\.venv\Scripts\python.exe -m scripts.estilizar_tema
```

---

## 4. Pending crítico #1 — imágenes reales (lo último que pidió el usuario)

**Las imágenes actuales son provisionales.** Se generaron ilustraciones limpias con `scripts/generar_imagenes_producto.py` y se subieron a Shopify con `scripts/actualizar_imagenes.py`. El usuario aclaró que necesita **fotos reales de producto**, con fondo blanco, sin personas ni objetos usados.

Estado actual:
- `datos/imagenes/<SKU>.png`: ilustraciones generadas con Pillow (provisionales).
- `datos/catalogo.json`: campo `imagen` apunta a URLs `cdn.shopify.com/.../productos_<SKU>.png` de esas ilustraciones.
- Shopify tiene esas imágenes como media de cada producto.

**Próximo paso:** reemplazar esas URL por fotos reales de cada producto sobre fondo blanco.

Flujo sugerido:
1. Buscar fotos reales con licencia comercial (Openverse/Flickr, Wikimedia u otra fuente verificable).
2. Descargarlas a `datos/imagenes/<SKU>.<ext>` o guardar las URL definitivas.
3. Si se descargan localmente, ejecutar:
   ```powershell
   .\.venv\Scripts\python.exe -m scripts.actualizar_imagenes
   ```
   Ese script sube cada archivo como asset del tema, borra la media anterior y actualiza `datos/catalogo.json`.
4. Verificar en navegador `/collections/all` que se vean productos reales, no dibujos.
5. Borrar `scripts/generar_imagenes_producto.py` si ya no se usará, o dejarlo documentado como generador provisional.

> No volver a usar el generador de imágenes de OpenCode: falló por saldo insuficiente. Las ilustraciones actuales se hicieron con Pillow, no con IA.

Resultado de la primera búsqueda en Openverse: las consultas con la frase completa `isolated on white background` devuelven 0 resultados, pero las consultas simples sí funcionan. Por ejemplo, `q=computer mouse` devolvió **"Computer Mouse Isolated on White Background"** (`https://live.staticflickr.com/7242/6848810640_95f2076266_b.jpg`), que ya estaba en el catálogo. Conviene buscar por nombre simple y filtrar títulos que contengan `isolated`, `white` o `product`.

---

## 5. Pending crítico #2 — precios mostrados 5 % más bajos

Los precios de `datos/catalogo.json` ya son realistas y terminan en `990` (ej.: notebook `599990`, monitor `139990`, cable HDMI `6990`). Pero la tienda muestra un 5 % menos:

| SKU | `price` GraphQL | `presentmentPrices` | Tienda |
|---|---:|---:|---:|
| PROYECTOR | 129990 | 123491.0 | $123,491 |
| AURICULARES | 24990 | 23741.0 | $23,741 |

Diagnóstico: Shopify aplica un ajuste de mercado/lista de precios al calcular `presentmentPrices`. No es un error del tema ni del catálogo.

Consultas útiles ya probadas:

```graphql
{
  products(first: 1, query: "sku:PROYECTOR") {
    nodes {
      variants(first: 1) {
        nodes {
          sku
          price
          presentmentPrices(first: 10) {
            nodes { price { amount currencyCode } }
          }
        }
      }
    }
  }
}
```

Opciones para corregir:
- Investigar y eliminar el ajuste de precio del mercado en Shopify admin, **o**
- Ajustar los precios base para que el precio presentado termine en `990` (por ejemplo, base `136832` produce presentado `129990`).

Después de cualquier cambio, ejecutar:

```powershell
.\.venv\Scripts\python.exe -m scripts.poblar_catalogo
```

y verificar en navegador que los precios terminen en `990`.

---

## 6. Reglas de negocio que ya están listas (no cambiar)

- Eventos: `cumpleanos`, `vuelta_a_clases`, `trabajo_remoto`, `accesorios_basicos`.
- Cantidades con `ceil()` y mínimo por regla; sustitutos por stock.
- 2x1 → cupón → descuento por segmento → envío → total.
- Envío `$3.990`, gratis desde `$50.000` (y para `nuevo`/`mayorista`).
- Recomendaciones: hasta 2 similares por categoría; 15 % en festividades; no alteran el total.
- Segmentos: `nuevo` 10 %, `frecuente` 5 %, `mayorista` 15 %, `None` = invitado.
- La Gift Card se conserva por pedido explícito.
- Los tres paradigmas deben seguir dando resultados idénticos.

Totales verificados para `cumpleanos, 10 personas, FIESTA10`: invitado `$143.028`, nuevo `$128.726`, frecuente `$135.877`, mayorista `$121.574`.

---

## 7. API HTTP y scripts

`scripts/api_carrito.py` expone:

| Método | Ruta |
|---|---|
| GET | `/health` |
| GET | `/eventos` |
| GET | `/segmentos` |
| POST | `/carrito` |

Cuerpo de ejemplo:

```json
{"evento":"cumpleanos","personas":10,"cupon":"FIESTA10","tipo_usuario":"mayorista","paradigma":"todos"}
```

Scripts principales:

| Script | Función |
|---|---|
| `shopify_client.py` | Cliente GraphQL/REST con reintentos y logs |
| `main.py --info` | Comprobación de conexión |
| `scripts/poblar_catalogo.py` | Crea/actualiza productos, precios, imágenes, colecciones y publicación |
| `scripts/actualizar_tema.py` | Paginación a 12 y CSS de paginación |
| `scripts/estilizar_tema.py` | Identidad visual oscura/azul |
| `scripts/actualizar_imagenes.py` | Sube imágenes al tema y reemplaza media |
| `scripts/api_carrito.py` | API HTTP del carrito |
| `scripts/generar_documentacion.py` | Regenera `docs/explicacion_lineas.md` |

---

## 8. Documentación pendiente

- `docs/errores_corregidos.md`: ya tiene incidencias hasta la **#28** (productos no publicados). Faltan:
  - #29: imágenes con objetos usados/escenarios → reemplazo por fotos reales con fondo blanco.
  - #30: precios presentados 5 % más bajos por `presentmentPrices`.
- `docs/informe_borrador.md`: borrador listo con datos verificados y huecos `[COMPLETAR]`.
- Falta traspasar a `README.md`, `docs/informe.md` y `docs/presentacion.md` la segmentación y los cambios visuales.
- Regenerar `docs/explicacion_lineas.md`:
  ```powershell
  .\.venv\Scripts\python.exe -m scripts.generar_documentacion
  ```
- Requisitos aún pendientes del enunciado/usuario: marketing y promociones, reseñas/prueba social, gestión de usuarios y cuentas, integraciones.

---

## 9. No olvidar

- No subir `.env`, `backups/`, `logs/` ni la contraseña de la tienda.
- Si la tienda vuelve a pedir contraseña, pedírsela al usuario; no está guardada.
- El `client_credentials` devuelve token de 24 h; si falla autenticación, se renueva automáticamente.
- No consultar `locations.name` ni `discountNodes` con los scopes actuales.
- Verificar siempre con el navegador además de la API, porque `ACTIVE` no implica publicado en Online Store.

---

## 10. Checklist para cerrar la entrega

- [ ] Fotos reales de producto con fondo blanco en los 34 SKU.
- [ ] Precios visibles terminados en `990`.
- [ ] Incidencias #29 y #30 registradas.
- [ ] Documentación y prompts actualizados.
- [ ] `explicacion_lineas.md` regenerado.
- [ ] Marketing, reseñas, cuentas e integraciones documentados o implementados.
- [ ] Capturas insertadas en `docs/presentacion.md`.
- [ ] Validación del carrito con el docente.
- [ ] Commit y push finales.
