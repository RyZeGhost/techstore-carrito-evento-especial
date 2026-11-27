# Informe final — Tarea 1: Desarrollo Multiparadigma en Python de un Componente de E-commerce

**Tienda:** SecureHome Seguridad — `https://games4you-k5xbi4h0.myshopify.com`
**Grupo:** (completar con los integrantes)
**Fecha:** 22–23 de noviembre de 2026

---

## 1. Etapa 1 — Montaje de la tienda

La tienda se montó sobre **Shopify**, plataforma validada por el enunciado.

### Configuración realizada

| Elemento | Exigencia | Estado |
|---|---|---|
| Catálogo y navegación | Mínimo | Catálogo de **productos tecnológicos** definido en `datos/catalogo.json` (**34 SKU**, 8 categorías: Audio, Accesorios, Energía, Periféricos, Almacenamiento, Pantallas, Computadores y Redes). Cada SKU incluye precio en **CLP** y una imagen real libre de marca de agua. Carga a Shopify mediante `scripts/poblar_catalogo.py`. El catálogo se **divide en páginas de 12 productos** para no mostrar todo de una vez. |
| Carrito y checkout | Mínimo | Provisto por Shopify en modo de prueba. |
| Pasarela de pagos | Mínimo | Configurada en **Configuración → Pagos → Proveedores de pago de prueba** (Shopify Payments test mode / Bogus Gateway). |
| Identidad visual (tema) | Mínimo | Tema coherente con SecureHome Seguridad configurado en **Online Store → Themes**. |
| Gestión de usuarios | Recomendado | Habilitar cuentas de cliente en **Configuración → Clientes**. |
| Reseñas y prueba social | Recomendado | Instalar una app de reseñas; no exigible. |
| Catálogo e inventario (backend) | Recomendado | Los productos se crean con `inventoryManagement: SHOPIFY` y stock inicial desde el JSON. |
| Pedidos y envíos | Recomendado | Tarifa plana de $3.990 y envío gratis sobre $50.000, coherentes con `datos/catalogo.json`. Los **16 productos ajenos** (snowboards y cera) se eliminaron para que no aparezcan artículos ajenos en el checkout; se conservó y reactivó la **Gift Card de crédito de la tienda** por pedido explícito. |
| Marketing y promociones | Recomendado | Reglas 2x1 y cupones modeladas en el carrito; pueden replicarse como descuentos de Shopify. |
| Analítica, roles, integraciones | Referencial | No exigidas. |

La evidencia visual de esta etapa (catálogo, navegación, carrito, checkout en modo prueba y repositorio de GitHub) tiene espacios reservados en el anexo de [`presentacion.md`](presentacion.md), pendientes de insertar las capturas por el grupo.

### Integración desde Python

Se creó `shopify_client.py`, que usa el flujo **client credentials**:

1. `get_shopify_token()` intercambia `SHOPIFY_CLIENT_ID` + `SHOPIFY_CLIENT_SECRET` por un token de 24 h mediante `POST /admin/oauth/access_token`.
2. `graphql_query(query, variables)` envía el token en `X-Shopify-Access-Token` a la Admin GraphQL API `2026-01`.

Se usa GraphQL directo (sin Bulk Operations) porque el catálogo tiene 34 SKU: una carga idempotente con backoff exponencial es suficiente y evita gestionar operaciones asíncronas. La **Admin REST API** se usa solo para los assets del tema, ya que GraphQL no permite leer/escribir archivos de Liquid; para eso se añadió `rest_request()` en `shopify_client.py`, que envía el mismo token en `X-Shopify-Access-Token`. Los errores de red, HTTP 429, fallos de token y errores GraphQL/REST se registran en `logs/shopify_errores.log`, carpeta excluida del repositorio. `peticion_con_reintento()` aplica espera exponencial y `carrito/datos.py` valida el esquema JSON antes de cualquier petición.

La interfaz se ajustó sobre el tema activo `test-data` con `scripts/actualizar_tema.py`: la sección `sections/main-collection-product-grid.liquid` pagina `collection.products` a **12 por página**, mantiene el control `{% render 'pagination', paginate: paginate, anchor: '' %}` y carga `assets/techstore-paginas.css` desde `layout/theme.liquid`. Los originales quedaron en `backups/` (ignorado por Git). La verificación se hizo por API: no se pudo comprobar visualmente porque la tienda está protegida con contraseña y no se compartió ese acceso.

Prueba ejecutada:

```
$ python shopify_client.py
Conectado a: SecureHome Seguridad (games4you-k5xbi4h0.myshopify.com)
```

---

## 2. Etapa 2 — Carrito Evento Especial

### Regla de negocio elegida

**Carrito por ocasión y cantidad de personas** (validable con el docente). El usuario elige uno de cuatro eventos:

| Evento | Reglas principales | 2x1 | Cupón |
|---|---|---|---|
| `cumpleanos` | Kit de regalo tech: parlante 1 cada 10 personas (mín. 1), auriculares 0,2/persona, cable HDMI 0,5/persona, power bank 0,1/persona, cargador 0,1/persona | CABLE-HDMI | FIESTA10 |
| `vuelta_a_clases` | Tablet 0,2/persona (mín. 1), mouse 1/persona, teclado 0,5/persona, auriculares 0,5/persona, SSD 0,1/persona | MOUSE | ESCUELA10 |
| `trabajo_remoto` | Monitor 1/persona (mín. 1), teclado 1/persona, mouse 1/persona, webcam 0,5/persona, soporte 1/persona | SOPORTE | HOME10 |
| `accesorios_basicos` | Cable USB-C 1/persona, protector 0,5/persona, adaptador 0,2/persona, lápiz táctil 0,1/persona, soporte 0,1/persona | CABLE-USB | ACC10 |

Reglas transversales:

- **Redondeo:** `ceil()` porque no se venden fracciones; se aplica un mínimo por regla.
- **Stock:** si no alcanza, se busca un sustituto con stock suficiente (PARLANTE → PARLANTE-PRO, AURICULARES → AURICULARES-PRO, SSD → SSD-512, MONITOR → MONITOR-27). Si no hay sustituto, se vende lo disponible y se reporta el faltante.
- **Promoción 2x1:** por cada par de unidades del producto promocionado se descuenta una. Aplica también si el producto fue sustituido.
- **Cupón:** 10 % sobre la base ya descontada, solo si coincide con el cupón del evento.
- **Envío:** $3.990, gratis si la base supera $50.000.
- **Aritmética:** todos los montos son enteros en CLP; el porcentaje se calcula con `// 100` para evitar errores de coma flotante y garantizar paridad.
- **Recomendaciones personalizadas:** al cierre se sugieren hasta 2 productos de las categorías ya presentes en el carrito, priorizando el precio más cercano al promedio de esa categoría. En `cumpleanos` y `vuelta_a_clases` (eventos configurados como festivos) se aplica un 15 % de descuento sobre el precio sugerido; en los demás eventos se muestran como sugerencias sin descuento. Son ofertas informativas: **no se agregan a los ítems ni cambian el total**.

### Marco teórico de los paradigmas

- **Imperativo:** el programa es una secuencia de instrucciones que transforman variables mutables. El foco está en *cómo* se hace: bucles `for`, acumuladores `items`, `faltantes`, `descuento_2x1`.
- **Orientado a objetos:** se modela el dominio con clases (`Producto`, `Item`, `Regla`, `Evento`, `Carrito`). El estado se encapsula en objetos y el comportamiento se reparte entre ellos. La herencia y el polimorfismo aparecen en `Descuento` con `Descuento2x1` y `DescuentoPorcentaje`.
- **Funcional:** el cómputo se expresa como composición de funciones puras. No hay estado mutable: se usan tuplas, `map`, `filter` y `reduce`. Misma entrada garantiza misma salida sin efectos colaterales.

### Análisis por paradigma

| Aspecto | Imperativo | Orientado a objetos | Funcional |
|---|---|---|---|
| Unidad de organización | Función con bucles | Clases e instancias | Funciones puras |
| Estado | Variables mutables | Atributos encapsulados | Sin estado; tuplas nuevas |
| Stock y sustituciones | `if/else` inline | Delegado a `Carrito._resolver_regla` | `resolver()` + `map/filter` |
| Descuentos | Acumuladores | Estrategias polimórficas | `reduce` sobre `filter` |
| Facilidad de lectura | Alta para flujo lineal | Alta para dominio complejo | Alta para transformaciones |
| Extensibilidad | Media (hay que tocar la función) | Alta (nueva clase de descuento) | Alta (nueva función y composición) |
| Riesgo principal | Estado compartido accidental | Demasiadas clases para reglas simples | Curva de aprendizaje de `reduce` |
| Recomendaciones | Llamada a `sugerir()` al final del flujo | Colaborador `Recomendador` inyectado en `Carrito` | Función pura añadida a la composición |

### Resultados y paridad

`python -m carrito.demo` ejecuta cinco escenarios idénticos en las tres versiones:

| Escenario | Items | Faltantes | 2x1 | Cupón | Envío | Total | Recs |
|---|---:|---:|---:|---:|---:|---:|---:|
| cumpleanos, 10 pers., FIESTA10 | 5 | 0 | 13.980 | 15.892 | 0 | 143.028 | 2 (15 %) |
| trabajo_remoto, 12 pers., HOME10 | 5 | 0 | 89.940 | 258.552 | 0 | 2.326.968 | 2 (sin dto.) |
| vuelta_a_clases, 12 pers., ESCUELA10 | 5 | 0 | 77.940 | 136.777 | 0 | 1.230.993 | 2 (15 %) |
| cumpleanos, 200 pers., sin cupón | 5 | 1 | 279.600 | 0 | 0 | 3.438.600 | 2 (15 %) |
| accesorios_basicos, 1 persona, sin cupón | 5 | 0 | 0 | 0 | 3.990 | 40.940 | 1 (sin dto.) |

Las tres implementaciones devuelven diccionarios **exactamente iguales** en todos los casos; `tests/test_paridad.py` verifica esto automáticamente junto con validaciones, cupón inválido, envío y recomendaciones.

Detalle de la recomendación para el primer caso, ya con el catálogo ampliado: `AURICULARES-DEPORTIVOS` ($19.990 → $16.992) y `FUNDANOTEBOOK` ($14.990 → $12.742), ambos de categorías presentes en el carrito (Audio y Accesorios). Antes de ampliar el catálogo se sugerían `PARLANTE-PRO` y `SOPORTE`; la regla es la misma, pero al incorporar 12 SKU nuevos el precio más cercano al promedio cambió. El hecho de que el evento tenga cupón no es condición del descuento: basta con que el evento esté marcado como festivo en el JSON.

### Errores y correcciones

Ver [`errores_corregidos.md`](errores_corregidos.md). Incluye 30 incidencias reales, desde credenciales y scopes de Shopify hasta cambios de la API 2026, imágenes, precios, limpieza del checkout, validación del catálogo, límites de tasa, registro de errores, la recomendación personalizada omitida en la primera versión, la paginación del tema y el campo `media` rechazado por `productCreate`.

### Explicación del código

- [`explicacion_lineas.md`](explicacion_lineas.md): tabla línea por línea de los módulos principales.
- [`prompts.md`](prompts.md): registro completo de los 27 prompts usados con IA generativa (9 por paradigma).
- [`presentacion.md`](presentacion.md): diapositivas de la exposición final.

### Integración como servicio HTTP

Además de la carga a Shopify, `scripts/api_carrito.py` expone el componente sin añadir dependencias (solo librería estándar):

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado del servicio y cantidad de productos |
| GET | `/eventos` | Eventos disponibles con sus reglas |
| POST | `/carrito` | Calcula el carrito en `imperativo`, `orientado_objetos`, `funcional` o `todos` |

Ejemplo de petición y respuesta (paradigma `todos`):

```json
{"evento": "cumpleanos", "personas": 10, "cupon": "FIESTA10", "paradigma": "todos"}
```

```json
{
  "imperativo": {"total": 143028, "..." : "..."},
  "orientado_objetos": {"total": 143028, "..." : "..."},
  "funcional": {"total": 143028, "..." : "..."}
}
```

Las entradas inválidas devuelven HTTP 400 con un mensaje descriptivo. La verificación realizada confirmó los tres totales idénticos y el rechazo de `personas = -1`.

---

## 3. Conclusión

Los tres paradigmas resuelven el mismo problema con resultados idénticos, pero expresan decisiones distintas. La versión imperativa es la más directa; la orientada a objetos facilita extender reglas y descuentos; la funcional ofrece trazabilidad y ausencia de efectos secundarios. La integración con la tienda real se realizó mediante la Admin GraphQL API, y todo el proceso quedó versionado en GitHub.
