# Material de partida para el informe final

Este archivo reúne **todo lo verificado hasta hoy** para que solo tengas que redactar y rellenar los huecos marcados con `[COMPLETAR]`. No reemplaza a `informe.md` (que es el entregable), pero sí funciona como borrador y checklist.

> Estado: 24 de noviembre de 2026. Último commit: `3acdf8d` (segmentación de clientes).

---

## 0. Datos generales (portada)

| Campo | Valor |
|---|---|
| Tarea | Tarea 1: Desarrollo Multiparadigma en Python de un Componente de E-commerce con Asistencia de IA Generativa |
| Tienda | TechStore — `https://techstore-d8vn3rhk.myshopify.com` |
| Repositorio | https://github.com/RyZeGhost/techstore-carrito-evento-especial (público, rama `main`) |
| Moneda | CLP |
| Versión de API Shopify | `2026-01` |
| Grupo / integrantes | `[COMPLETAR con nombres y roles]` |
| Fecha de entrega | `[COMPLETAR]` |
| Docente / sección | `[COMPLETAR]` |

**Resumen ejecutivo sugerido (listo para usar):**

> Se implementó una tienda tecnológica en Shopify con 34 SKU en 8 categorías, paginación de 12 productos por página y un checkout en modo de prueba. Sobre esa tienda se construyó el *Carrito Evento Especial*, que arma automáticamente un pedido según la ocasión y la cantidad de personas, resuelve stock y sustituciones, aplica 2x1, cupón, envío, recomendaciones por festividad y beneficios por tipo de cliente (nuevo, frecuente o mayorista). La misma regla de negocio se implementó en tres paradigmas —imperativo, orientado a objetos y funcional— y se validó automáticamente: los tres producen resultados idénticos en todos los escenarios probados. Todo el código, la documentación y el historial de prompts y errores están versionados en GitHub; las credenciales nunca se subieron al repositorio.

---

## 1. Índice sugerido del informe

1. Portada y resumen ejecutivo
2. Etapa 1 — Montaje de la tienda (Shopify)
3. Etapa 2 — Carrito Evento Especial (regla de negocio)
4. Etapa 3 — Los tres paradigmas (marco teórico y análisis comparativo)
5. Integración con Shopify desde Python
6. API HTTP y terminaciones expuestas
7. Verificación, pruebas y resultados
8. Registro de errores y supervisión de IA
9. Conclusiones y trabajo futuro
10. Anexos (capturas, comandos, prompts, explicación línea por línea)

---

## 2. Etapa 1 — La tienda (datos verificados)

| Elemento | Estado real |
|---|---|
| Plataforma | Shopify, plan de desarrollo |
| Catálogo | **34 SKU** tecnológicos, **8 categorías**: Audio, Accesorios, Energía, Periféricos, Almacenamiento, Pantallas, Computadores y Redes |
| Colecciones | 8 (una por categoría), con todos los productos asignados |
| Imágenes | URL reales de Openverse/Flickr, sin marca de agua, verificadas con HTTP 200 `image/jpeg` |
| Precios | Enteros en CLP, ajustados a mercado chileno (ej.: notebook $599.990, monitor 24" $139.990) |
| Paginación | **12 productos por página** en las colecciones, con control de navegación y CSS propio |
| Limpieza | **16 productos ajenos eliminados** (snowboards y cera de esquí) |
| Gift Card | **Conservada y reactivada** por pedido explícito (`productType: giftcard`) |
| Carrito / checkout | Provistos por Shopify; pasarela en modo prueba `[CONFIRMAR VISUALMENTE]` |
| Identidad visual | Tema activo `test-data` (id `189417029881`), modificado por API |
| Cuentas de cliente | `[COMPLETAR — pendiente de activar/documentar]` |
| Reseñas / prueba social | `[COMPLETAR — pendiente de implementar/documentar]` |
| Marketing y promociones | `[COMPLETAR — pendiente de implementar/documentar]` |
| Integraciones | API HTTP propia + GitHub + app de Shopify `[COMPLETAR detalle]` |

**Texto ya redactado que puedes copiar:**

> La tienda se montó sobre Shopify. El catálogo se definió en `datos/catalogo.json` como única fuente de datos y se cargó de forma idempotente con `scripts/poblar_catalogo.py`. Para evitar que el catálogo se mostrara completo en una sola pantalla, se modificó el tema activo con `scripts/actualizar_tema.py`: la sección de colecciones pagina a 12 productos, conserva el control `{% render 'pagination', paginate: paginate, anchor: '' %}` y vincula `assets/techstore-paginas.css`. Los archivos originales se respaldaron en `backups/` (excluido de Git). Como la tienda está protegida con contraseña, la comprobación fue por API y queda pendiente la captura visual.

**Evidencia pendiente en el anexo:** capturas de catálogo paginado, página de producto, carrito y checkout en modo prueba.

---

## 3. Etapa 2 — Regla de negocio del carrito

### 3.1 Eventos (fuente: `datos/catalogo.json`)

| Evento | Reglas por persona | 2x1 | Cupón |
|---|---|---|---|
| `cumpleanos` | PARLANTE 0,1 (mín. 1), AURICULARES 0,2, CABLE-HDMI 0,5, POWERBANK 0,1, CARGADOR 0,1 | CABLE-HDMI | FIESTA10 |
| `vuelta_a_clases` | TABLET 0,2 (mín. 1), MOUSE 1, TECLADO 0,5, AURICULARES 0,5, SSD 0,1 | MOUSE | ESCUELA10 |
| `trabajo_remoto` | MONITOR 1 (mín. 1), TECLADO 1, MOUSE 1, WEBCAM 0,5, SOPORTE 1 | SOPORTE | HOME10 |
| `accesorios_basicos` | CABLE-USB 1, PROTECTOR 0,5, ADAPTADOR 0,2, LAPIZ-TACTIL 0,1, SOPORTE 0,1 | CABLE-USB | ACC10 |

### 3.2 Reglas transversales

- **Cantidades:** `ceil()` y mínimo por regla; no se venden fracciones.
- **Stock:** si no alcanza, se prueba el sustituto (PARLANTE → PARLANTE-PRO, AURICULARES → AURICULARES-PRO, SSD → SSD-512, MONITOR → MONITOR-27). Si tampoco alcanza, se vende lo disponible y se reporta el faltante.
- **2x1:** por cada par de unidades del producto promocionado se descuenta una; aplica también al sustituto.
- **Cupón:** 10 % sobre la base ya descontada, solo si coincide con el cupón del evento.
- **Envío:** $3.990, gratis si la base supera $50.000.
- **Aritmética:** enteros en CLP con `// 100`; garantiza paridad exacta entre paradigmas.
- **Recomendaciones por festividad:** hasta 2 similares por categoría del carrito; 15 % de descuento en `cumpleanos` y `vuelta_a_clases`. No se suman a `items` ni cambian el total.

### 3.3 Segmentación de clientes (novedad más reciente)

Parámetro opcional `tipo_usuario`. Si se omite, se atiende como **invitado** y los totales no cambian.

| Tipo | Descuento | Envío | Estilo de recomendación | Configuración |
|---|---:|---|---|---|
| `nuevo` | 10 % | Gratis | `economica` (accesorios de entrada, precio bajo) | `datos/catalogo.json → segmentos.nuevo` |
| `frecuente` | 5 % | Tarifa normal | `premium` (gama alta de la categoría) | `segmentos.frecuente` |
| `mayorista` | 15 % | Gratis | `alto_ticket` (mayor valor disponible para volumen) | `segmentos.mayorista` |

Orden de cálculo: `subtotal → 2x1 → cupón → descuento por segmento → envío → total`.

### 3.4 Resultados verificados (`python -m carrito.demo`)

Escenarios base (invitado):

| Escenario | Ítems | Faltantes | 2x1 | Cupón | Envío | Total | Recs |
|---|---:|---:|---:|---:|---:|---:|---:|
| cumpleanos, 10 pers., FIESTA10 | 5 | 0 | 13.980 | 15.892 | 0 | 143.028 | 2 (15 %) |
| trabajo_remoto, 12 pers., HOME10 | 5 | 0 | 89.940 | 258.552 | 0 | 2.326.968 | 2 (sin dto.) |
| vuelta_a_clases, 12 pers., ESCUELA10 | 5 | 0 | 77.940 | 136.777 | 0 | 1.230.993 | 2 (15 %) |
| cumpleanos, 200 pers., sin cupón | 5 | 1 | 279.600 | 0 | 0 | 3.438.600 | 2 (15 %) |
| accesorios_basicos, 1 pers., sin cupón | 5 | 0 | 0 | 0 | 3.990 | 40.940 | 1 (sin dto.) |

Segmentación sobre `cumpleanos, 10 pers., FIESTA10` (base = $143.028):

| Perfil | Dto. segmento | Envío | Total | Recomendaciones |
|---|---:|---:|---:|---|
| invitado | 0 | 0 | 143.028 | Auriculares deportivos in-ear; Funda para notebook 14" |
| nuevo | 14.302 | 0 | **128.726** | Auriculares deportivos in-ear; Cable USB-C 1 m |
| frecuente | 7.151 | 0 | **135.877** | Auriculares con cancelación de ruido; Mochila técnica |
| mayorista | 21.454 | 0 | **121.574** | Parlante resistente al agua; Mochila técnica |

Prueba adicional: en `accesorios_basicos, 1 pers.` el envío de $3.990 se anula para `nuevo` y `mayorista`, pero no para `frecuente`.

---

## 4. Etapa 3 — Los tres paradigmas

| Aspecto | Imperativo | Orientado a objetos | Funcional |
|---|---|---|---|
| Unidad | Función con bucles | Clases e instancias | Funciones puras |
| Estado | Variables mutables | Atributos encapsulados | Sin estado, tuplas nuevas |
| Stock | `if/else` inline | `Carrito._resolver_regla` | `resolver()` + `map/filter` |
| Descuentos | Acumuladores | Estrategias `Descuento` polimórficas | `reduce` sobre `filter` |
| Segmento | Llamadas a `carrito/segmentos.py` | Colaborador `Segmento` | Funciones puras compuestas |
| Recomendaciones | `sugerir()` al final | Colaborador `Recomendador` | Función compuesta |

Archivos: `carrito/imperativo.py`, `carrito/orientado_objetos.py`, `carrito/funcional.py`.
Reglas compartidas: `carrito/datos.py`, `carrito/recomendaciones.py`, `carrito/segmentos.py`.

**Idea para conclusiones:** la paridad se garantiza porque los tres consumen la misma fuente de datos y las mismas reglas puras; la diferencia está solo en la organización del código, no en el resultado.

---

## 5. Integración con Shopify y API HTTP

**Autenticación:** flujo `client_credentials`; `SHOPIFY_CLIENT_ID` + `SHOPIFY_CLIENT_SECRET` (`shpss_...`) → token de 24 h → header `X-Shopify-Access-Token`. Usar el secret como `shpat_` da HTTP 401.

**Scopes:** `write_products`, `write_inventory`, `read_themes`, `write_themes` (estos últimos para la paginación). Sin `read_locations` ni `read_discounts` actualmente.

**Scripts:**
- `shopify_client.py`: `graphql_query()`, `rest_request()` (solo para assets del tema), reintentos con backoff y logs en `logs/shopify_errores.log`.
- `scripts/poblar_catalogo.py`: crea/actualiza productos, precios, imágenes y colecciones. La imagen va en `productCreateMedia`, **no** dentro de `ProductInput`.
- `scripts/actualizar_tema.py`: paginación, CSS y respaldos.
- `main.py --info`: comprueba conexión y versión.

**API HTTP (`scripts/api_carrito.py`, librería estándar):**

| Método | Ruta | Respuesta |
|---|---|---|
| GET | `/health` | `{"estado":"ok","productos":34}` |
| GET | `/eventos` | Configuración de los 4 eventos |
| GET | `/segmentos` | Configuración de los 3 tipos de usuario |
| POST | `/carrito` | Resultado por paradigma; acepta `evento`, `personas`, `cupon`, `tipo_usuario`, `paradigma` |

Ejemplo de cuerpo: `{"evento":"cumpleanos","personas":10,"cupon":"FIESTA10","tipo_usuario":"mayorista","paradigma":"todos"}`.

---

## 6. Verificación (comandos y resultados reales)

| Comando | Resultado |
|---|---|
| `python -m unittest discover -s tests -v` | **11/11 OK** |
| `python -m carrito.demo` | `Resultado global: TODOS LOS CASOS COINCIDEN` (incluye los 4 perfiles) |
| `python shopify_client.py` | `Conectado a: TechStore (techstore-d8vn3rhk.myshopify.com)` |
| `python main.py --info` | API version `2026-01` |
| `python -m scripts.poblar_catalogo --dry-run` | 34 SKUs existentes, 0 por crear |
| `python -m scripts.actualizar_tema` | `paginate collection.products by 12`, control de páginas y CSS vinculado |
| `POST /carrito` | Totales `143028 / 143028 / 143028`, 2 recomendaciones por paradigma |
| Verificación GraphQL en tienda | 34 SKU activos, 34 con imagen, precios correctos, Gift Card activa, 0 snowboards |

---

## 7. Errores y prompts

- `docs/errores_corregidos.md`: **28 incidencias documentadas** (hasta la #28: productos no publicados). Las incidencias #29 y #30 previstas en `CONTINUAR.md` se retiraron porque el catálogo de 34 SKU fue reemplazado por productos reales de Shopify.
- `docs/prompts.md`: 27 prompts de los tres paradigmas + prompts de revisión (tienda tecnológica, imágenes/precios, recomendaciones, paginación/interfaz, catálogo extendido, segmentación). `[VERificar el conteo final]`.
- `docs/explicacion_lineas.md`: generado automáticamente; **hay que regenerarlo** con `python -m scripts.generar_documentacion` después de la segmentación.

---

## 8. Lista de pendientes antes de entregar

- [ ] Documentar la segmentación en `README.md`, `informe.md`, `presentacion.md`, `errores_corregidos.md` (#27) y `prompts.md`.
- [ ] Regenerar `docs/explicacion_lineas.md`.
- [ ] **Marketing y promociones** en Shopify ( descuentos/códigos o replicar 2x1 y cupones como descuentos nativos ).
- [ ] **Reseñas y prueba social** (sección de testimonios en el tema o app de reseñas).
- [ ] **Gestión de usuarios y cuentas** (activar cuentas de cliente en Shopify).
- [ ] **Integraciones** (detallar API HTTP, GitHub y app de Shopify; evaluar webhooks si hay scopes).
- [ ] Completar integrantes y fecha en `informe.md` y `presentacion.md`.
- [ ] Insertar capturas en el anexo de `presentacion.md`.
- [ ] Validar el carrito por ocasión/personas con el docente.
- [ ] Confirmar visualmente la pasarela de prueba (la tienda tiene contraseña).
- [ ] Commit y push finales.

---

## 9. Anexo — enlaces internos

- Informe vigente: [`informe.md`](informe.md)
- Diapositivas: [`presentacion.md`](presentacion.md)
- Errores: [`errores_corregidos.md`](errores_corregidos.md)
- Prompts: [`prompts.md`](prompts.md)
- Explicación línea por línea: [`explicacion_lineas.md`](explicacion_lineas.md)
- Catálogo: [`../datos/catalogo.json`](../datos/catalogo.json)
- README: [`../README.md`](../README.md)
