# Arquitectura de sesión: banner de Shopify vs. motor determinista de Python

## Problema

Un carrito de compras **no es un dato global**: pertenece a la sesión del navegador. En Shopify Online Store ese carrito se identifica con un token que el tema envía en cada petición (cookie `cart`) y las APIs `/cart/add.js`, `/cart/update.js` y los *cart permalinks* actúan sobre ese carrito.

Por lo tanto, un programa Python que se ejecuta fuera del navegador **no puede decidir por sí solo** a qué carrito debe agregar un combo. Necesitaría recibir el `cart_token`/`session_id` desde la request, y entonces su resultado dejaría de depender únicamente de sus entradas.

## Decisión

Separar claramente dos responsabilidades:

| Capa | Responsabilidad | Estado |
|---|---|---|
| Motor Python (`imperativo.py`, `poo.py`, `funcional.py`) | Calcular **qué** lleva el combo: SKU, cantidades, descuentos y regalo a partir de entradas fijas | Puro y determinista; sin sesión, sin I/O de red |
| Tema de Shopify (banner en la portada) | Aplicar ese combo **al carrito de la sesión activa** porque el navegador ya posee el token | La sesión nunca sale del browser |

El usuario elige la oferta desde un banner visible en la página principal. El clic dispara la adición al carrito de **su propia sesión**; no hay un backend adivinando ni compartiendo carritos.

## Alternativas descartadas

1. **Python con `session_id` como parámetro.** Técnicamente sería puro si el identificador viniera como argumento, pero acoplaría el motor a la plataforma y haría que el JSON cambiara según la sesión. Rompería la igualdad byte-exacta entre los tres paradigmas que se usa como evidencia del trabajo.
2. **Combo solo para usuarios registrados.** Permite usar `customer_id`/metafields y segmentar, pero excluye al comprador invitado y obliga a autenticarse para una promoción que debería ser visible públicamente.

La opción elegida conserva el motor como una función de reglas reutilizable y respeta el modelo de sesión de Shopify: el banner es el único punto que toca el carrito.

## Flujo de datos

```
CLIENTE_PRUEBA + catálogo  ->  motor Python (puro)  ->  JSON del combo (SKU, cantidades)
                                                            |
                                                            v
                                   banner del tema (IDs de variante reales)
                                                            |
                                                            v
                              /cart/add.js o /cart/{variant}:{qty}  ->  carrito de la sesión
```

## Productos del combo en la tienda

El motor produce cuatro líneas para la demo (`resultado_funcional.json`):

| SKU | Cantidad | Origen | ¿Se agrega al carrito de Shopify? |
|---|---:|---|---|
| `SEN-APERT2` | 6 | Prueba local | No: no existe en Shopify (ID `prueba-SEN-APERT2-1`) |
| `ALM-SMARTLIFE` | 2 | Shopify | Sí: variante `68329720250732` |
| `CAM-EZVIZH6C` | 3 | Shopify | Sí: variante `68329691709804` |
| `PROM-CARTEL1` | 1 | Prueba local, regalo | No: no existe en Shopify (ID `prueba-PROM-CARTEL1-1`) |

Los dos SKU `prueba` son fixtures necesarios para evaluar las reglas del ejercicio; no son productos comprables en la tienda. Por eso el banner agrega únicamente las variantes reales con sus cantidades calculadas. El descuento del 10 % y el regalo siguen siendo resultados del motor en el informe; para cobrarlos en Shopify haría falta además un código de descuento o una Shopify Function de carrito, que no forma parte de este cambio.

## Implementación en el tema

- Sección nueva: `sections/combo_oferta.liquid`, visible solo en `templates/index.json`.
- Texto: **「Oferta Especial: Kit de Seguridad Residencial」**.
- Botón: enlace de *cart permalink* `/cart/68329720250732:2,68329691709804:3` como respaldo, mejorado con `POST /cart/add.js` para agregar los ítems a la sesión activa y abrir el carrito. Si `fetch` falla, se usa el permalink.
- Los IDs de variante se obtuvieron de `catalogo_shopify.json`, que es la entrada real de los tres motores.

## Verificación

Los archivos `imperativo.py`, `poo.py` y `funcional.py` **no se modificaron**. Los tres JSON siguen siendo byte-idénticos (SHA-256 `0B99768E…26093`), de modo que la igualdad de los paradigmas queda intacta. El estado anterior del catálogo, los resultados y el tema se respaldó en `versiones/v22_banner_sesion_<timestamp>/`.
