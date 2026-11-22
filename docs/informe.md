# Informe final — Tarea 1: Desarrollo Multiparadigma en Python de un Componente de E-commerce

**Tienda:** TechStore — `https://techstore-d8vn3rhk.myshopify.com`
**Grupo:** (completar con los integrantes)
**Fecha:** 22 de noviembre de 2026

---

## 1. Etapa 1 — Montaje de la tienda

La tienda se montó sobre **Shopify**, plataforma validada por el enunciado.

### Configuración realizada / prevista

| Elemento | Exigencia | Estado |
|---|---|---|
| Catálogo y navegación | Mínimo | Catálogo de **productos tecnológicos** definido en `datos/catalogo.json` (22 SKU, 8 categorías: Audio, Accesorios, Energía, Periféricos, Almacenamiento, Pantallas, Computadores y Redes). Carga a Shopify mediante `scripts/poblar_catalogo.py`. |
| Carrito y checkout | Mínimo | Provisto por Shopify en modo de prueba. |
| Pasarela de pagos | Mínimo | Configurar en **Configuración → Pagos → Proveedores de pago de prueba** (Shopify Payments test mode / Bogus Gateway). |
| Identidad visual (tema) | Mínimo | Configurar un tema coherente con TechStore en **Online Store → Themes**. |
| Gestión de usuarios | Recomendado | Habilitar cuentas de cliente en **Configuración → Clientes**. |
| Reseñas y prueba social | Recomendado | Instalar una app de reseñas; no exigible. |
| Catálogo e inventario (backend) | Recomendado | Los productos se crean con `inventoryManagement: SHOPIFY` y stock inicial desde el JSON. |
| Pedidos y envíos | Recomendado | Configurar tarifas de envío acordes al umbral de envío gratis ($50.000). |
| Marketing y promociones | Recomendado | Reglas 2x1 y cupones modeladas en el carrito; pueden replicarse como descuentos de Shopify. |
| Analítica, roles, integraciones | Referencial | No exigidas. |

### Integración desde Python

Se creó `shopify_client.py`, que usa el flujo **client credentials**:

1. `get_shopify_token()` intercambia `SHOPIFY_CLIENT_ID` + `SHOPIFY_CLIENT_SECRET` por un token de 24 h mediante `POST /admin/oauth/access_token`.
2. `graphql_query(query, variables)` envía el token en `X-Shopify-Access-Token` a la Admin GraphQL API `2026-01`.

Prueba ejecutada:

```
$ python shopify_client.py
Conectado a: TechStore (techstore-d8vn3rhk.myshopify.com)
```

---

## 2. Etapa 2 — Carrito Evento Especial

### Regla de negocio elegida

**Carrito por ocasión y cantidad de personas** (validable con el docente). El usuario elige uno de tres eventos:

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

### Resultados y paridad

`python -m carrito.demo` ejecuta cinco escenarios idénticos en las tres versiones:

| Escenario | Items | Faltantes | 2x1 | Cupón | Envío | Total |
|---|---:|---:|---:|---:|---:|---:|
| cumpleanos, 10 pers., FIESTA10 | 5 | 0 | 15.980 | 18.892 | 0 | 170.028 |
| trabajo_remoto, 12 pers., HOME10 | 5 | 0 | 77.940 | 295.752 | 0 | 2.661.768 |
| vuelta_a_clases, 12 pers., ESCUELA10 | 5 | 0 | 89.940 | 155.977 | 0 | 1.403.793 |
| cumpleanos, 200 pers., sin cupón | 5 | 1 | 319.600 | 0 | 0 | 4.018.600 |
| accesorios_basicos, 1 persona, sin cupón | 5 | 0 | 0 | 0 | 3.990 | 40.940 |

Las tres implementaciones devuelven diccionarios **exactamente iguales** en todos los casos; `tests/test_paridad.py` verifica esto automáticamente junto con validaciones, cupón inválido y envío.

### Errores y correcciones

Ver [`errores_corregidos.md`](errores_corregidos.md). Incluye 13 incidencias reales, desde credenciales y scopes de Shopify hasta ajustes en los casos de prueba.

### Explicación del código

- [`explicacion_lineas.md`](explicacion_lineas.md): tabla línea por línea de los módulos principales.
- `docs/prompts.md`: registro completo de los prompts usados con IA generativa.

---

## 3. Conclusión

Los tres paradigmas resuelven el mismo problema con resultados idénticos, pero expresan decisiones distintas. La versión imperativa es la más directa; la orientada a objetos facilita extender reglas y descuentos; la funcional ofrece trazabilidad y ausencia de efectos secundarios. La integración con la tienda real se realizó mediante la Admin GraphQL API, y todo el proceso quedó versionado en GitHub.
