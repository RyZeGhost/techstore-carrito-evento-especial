# Presentación — TechStore: Carrito Evento Especial

**Tarea 1: Desarrollo Multiparadigma en Python de un Componente de E-commerce con Asistencia de IA Generativa**

Formato: diapositivas en Markdown. Cada `---` separa una diapositiva.

---

## 1. Título

**TechStore**
Tienda de productos tecnológicos + Carrito Evento Especial en tres paradigmas

- Shopify: `techstore-d8vn3rhk.myshopify.com`
- Repositorio: https://github.com/RyZeGhost/techstore-carrito-evento-especial
- Fecha: 22–23 de noviembre de 2026

> Nota: presentar en 8–10 minutos.

---

## 2. El problema

Una tienda tecnológica necesita un carrito que se arme automáticamente según:

- **la ocasión** (cumpleaños, vuelta a clases, trabajo remoto, accesorios básicos), y
- **la cantidad de personas**.

Debe resolver:

- cantidades por persona con redondeo hacia arriba y mínimos;
- stock insuficiente con sustitutos;
- promoción 2x1;
- cupón del 10 %;
- envío pagado o gratis según monto;
- **recomendaciones de objetos similares con descuento en festividades**.

**Restricción clave:** las tres implementaciones deben dar el mismo resultado.

---

## 3. Etapa 1 — La tienda

- Plataforma: **Shopify** (plan de desarrollo).
- **22 SKU** tecnológicos, **8 categorías**: Audio, Accesorios, Energía, Periféricos, Almacenamiento, Pantallas, Computadores y Redes.
- Productos con **precio en CLP**, stock, SKU, descripción e **imagen real sin marca de agua**.
- **8 colecciones** por categoría.
- Carrito y checkout provistos por Shopify; pasarela en modo prueba y tema configurados.
- Los 17 productos de ejemplo de Shopify se archivaron para que no aparezcan artículos ajenos en el checkout.

---

## 4. Etapa 2 — Regla de negocio

| Evento | Producto principal | 2x1 | Cupón |
|---|---|---|---|
| Cumpleaños | Parlante 1 c/10 pers. (mín. 1) | Cable HDMI | FIESTA10 |
| Vuelta a clases | Tablet 0,2/pers. (mín. 1) | Mouse | ESCUELA10 |
| Trabajo remoto | Monitor 1/pers. (mín. 1) | Soporte | HOME10 |
| Accesorios básicos | Cable USB-C 1/pers. | Cable USB-C | ACC10 |

**Reglas transversales**

- `ceil()` + mínimo por regla.
- Sustitutos: PARLANTE→PRO, AURICULARES→PRO, SSD→512, MONITOR→27.
- 2x1 sobre pares del producto promocionado (aunque sea sustituido).
- Cupón 10 % sobre la base ya descontada.
- Envío $3.990, gratis desde $50.000.
- Recomendaciones: hasta 2 similares por categoría; 15 % de descuento en `cumpleanos` y `vuelta_a_clases`.
- Aritmética entera en CLP con `// 100`.

---

## 5. Fuente única de datos

`datos/catalogo.json` es la única fuente para los tres paradigmas:

- `productos`: sku, nombre, precio, stock, categoría, descripción, imagen.
- `eventos`: reglas (`sku`, `por_persona`, `mínimo`), cupón y producto 2x1.
- `sustitutos`: mapeo de SKU alternativo.
- `envio`: costo y umbral de envío gratis.
- `recomendaciones`: máximo por categoría, tope global, porcentaje y eventos festivos.

`carrito/recomendaciones.py` aplica la regla de similitud; `carrito/datos.py` valida el esquema antes de usar o enviar los datos a Shopify.

---

## 6. Paradigma imperativo

- Una función `armar_carrito(...)`.
- Bucles `for`, acumuladores (`items`, `faltantes`, descuentos).
- Flujo lineal: validar → calcular cantidades → resolver stock → descontar → envío → total.
- Cada línea está comentada para su defensa en clase.

**Fortaleza:** lectura directa del flujo.
**Riesgo:** estado mutable compartido.

---

## 7. Paradigma orientado a objetos

- Clases inmutables (`dataclasses`): `Producto`, `Item`, `Regla`, `Evento`.
- `Carrito` orquesta la creación de ítems y totales.
- **Herencia y polimorfismo**: `Descuento` → `Descuento2x1` y `DescuentoPorcentaje`.
- `PoliticaEnvio` como clase separada, configurable desde el JSON.

**Fortaleza:** extensible; agregar un descuento nuevo no toca el algoritmo.
**Riesgo:** más clases de las necesarias para reglas simples.

---

## 8. Paradigma funcional

- Funciones puras, sin mutar listas ni diccionarios.
- Tuplas inmutables, `map` para reglas, `filter` para separar ítems/faltantes, `reduce` para totales.
- Composición encadenada en `armar_carrito(...)`.

**Fortaleza:** trazabilidad y ausencia de efectos secundarios.
**Riesgo:** curva de aprendizaje de `reduce`.

---

## 9. Resultados — paridad

| Escenario | Ítems | 2x1 | Cupón | Envío | Total | Recs |
|---|---:|---:|---:|---:|---:|---:|
| Cumpleaños, 10 pers., FIESTA10 | 5 | 13.980 | 15.892 | 0 | 143.028 | 2 (15 %) |
| Trabajo remoto, 12 pers., HOME10 | 5 | 89.940 | 258.552 | 0 | 2.326.968 | 2 (sin dto.) |
| Vuelta a clases, 12 pers., ESCUELA10 | 5 | 77.940 | 136.777 | 0 | 1.230.993 | 2 (15 %) |
| Cumpleaños, 200 pers., sin cupón | 5 | 279.600 | 0 | 0 | 3.438.600 | 2 (15 %) |
| Accesorios básicos, 1 pers. | 5 | 0 | 0 | 3.990 | 40.940 | 1 (sin dto.) |

Ejemplo: en cumpleaños se sugieren `PARLANTE-PRO` ($54.990 → $46.742) y `SOPORTE` ($14.990 → $12.742).

- `python -m carrito.demo` → **TODOS LOS CASOS COINCIDEN**.
- `python -m unittest discover -s tests -v` → **7/7 OK**.

---

## 10. Integración

**Shopify Admin GraphQL API 2026-01**

- Flujo `client_credentials`: `SHOPIFY_CLIENT_ID` + `SHOPIFY_CLIENT_SECRET`.
- Header `X-Shopify-Access-Token`.
- `python -m scripts.poblar_catalogo`: idempotente; crea y sincroniza precios, imágenes y colecciones.
- Backoff exponencial ante HTTP 429 / `THROTTLED`.
- Esquema JSON validado antes de enviar datos; fallos registrados en `logs/shopify_errores.log`.

**API HTTP del carrito**

- `python -m scripts.api_carrito` (solo librería estándar).
- `GET /health`, `GET /eventos`, `POST /carrito`.
- `POST /carrito` acepta `paradigma: "todos"` y devuelve los tres resultados.

---

## 11. Errores y supervisión de IA

Se registraron **25 incidencias reales** en `errores_corregidos.md`, entre ellas:

- confundir Client Secret (`shpss_`) con access token (`shpat_`);
- scopes insuficientes en la app;
- cambios de la API 2026 (`variants`, `collectionAddProducts`);
- productos de ejemplo en el checkout;
- imágenes y precios;
- recomendación personalizada omitida y luego integrada.

Cada respuesta generada con IA se **ejecutó, comparó y corrigió**. Los 27 prompts (9 por paradigma) están en `prompts.md`.

---

## 12. Conclusión

- Los tres paradigmas resuelven el mismo problema con **resultados idénticos**.
- Cada uno expresa decisiones distintas: flujo, encapsulamiento y composición.
- La tienda real quedó poblada, limpia y con precios/imágenes coherentes.
- El código, la documentación y el historial están en GitHub.

**Preguntas**

---

## Anexo — Comandos para la demostración

```powershell
.\.venv\Scripts\python.exe shopify_client.py
.\.venv\Scripts\python.exe main.py --info
.\.venv\Scripts\python.exe -m carrito.demo
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m scripts.poblar_catalogo --dry-run
.\.venv\Scripts\python.exe -m scripts.api_carrito
```

---

## Anexo — Evidencia visual (insertar capturas)

Espacios reservados para la entrega presencial:

1. **Catálogo TechStore:** `[captura: colecciones y productos con imagen y precio CLP]`
2. **Carrito y checkout en modo prueba:** `[captura: carrito armado y pasarela de prueba]`
3. **Repositorio GitHub:** `[captura: commits y rama main sincronizada]`
4. **Validación con el docente:** `[captura o firma: resultado de la validación del evento]`
