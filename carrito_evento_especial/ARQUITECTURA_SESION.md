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
                              /cart/add.js + /discount/KIT10  o  /cart/{variant}:{qty}?discount=KIT10  ->  carrito de la sesión
```

## Productos del combo en la tienda

El motor produce cuatro líneas para la demo (`resultado_funcional.json`):

| SKU | Cantidad | Origen | ¿Se agrega al carrito de Shopify? |
|---|---:|---|---|
| `SEN-APERT2` | 6 | Shopify | Sí: variante `68330993090924`, creada para completar la categoría |
| `ALM-SMARTLIFE` | 2 | Shopify | Sí: variante `68329720250732` |
| `CAM-EZVIZH6C` | 3 | Shopify | Sí: variante `68329691709804`, con 10 % vía `KIT10` |
| `PROM-CARTEL1` | 1 | Shopify (regalo) | Sí: variante `68330868113772`, publicada a $0 |

El descuento y el regalo ya se materializan en Shopify: el descuento `Kit Seguridad 10% camara` (creado con GraphQL `discountCodeBasicCreate`) expone el código `KIT10` con un **10 % restringido únicamente a la variante `68329691709804`** de la cámara, y el producto `Cartel disuasivo` está publicado a **$0** con SKU `PROM-CARTEL1`. Además, `SEN-APERT2` se creó como producto real con precio $9.990, stock 15 y etiqueta `sensor_apertura`, y se asoció a la colección `Sensores de apertura` (id `649894986092`). El catálogo conserva el precio de referencia de $4.990 para el cartel, pero su cobro real es $0.

Comprando por separado las cuatro líneas serían `6 × $9.990 + 2 × $49.990 + 3 × $20.990 + $4.990 = $227.880`. Con el combo son **$216.593**: se descuentan $6.297 en la cámara y el cartel sale gratis (-$4.990). El total coincide exactamente con el informe de los tres paradigmas.

## Implementación en el tema

- Sección nueva: `sections/combo_oferta.liquid`, visible solo en `templates/index.json`.
- Texto: **「Oferta Especial: Kit de Seguridad Residencial」**.
- Botón: `POST /cart/add.js` con las cuatro variantes reales (sensor ×6, alarma ×2, cámara ×3, regalo ×1). Al tener éxito navega a `/discount/KIT10?redirect=/cart` para aplicar el código a la sesión activa. Si `fetch` falla, se usa el *cart permalink* `/cart/68330993090924:6,68329720250732:2,68329691709804:3,68330868113772:1?discount=KIT10`.
- Los IDs de variante se obtuvieron de `catalogo_shopify.json`, que es la entrada real de los tres motores. `PROM-CARTEL1` y `SEN-APERT2` se sincronizaron con sus productos reales de Shopify conservando los campos que consumen los motores.
- La sesión sigue siendo propiedad del navegador: ni el código de descuento ni el regalo se calculan en Python con un `session_id`.

## Verificación

Los archivos `imperativo.py`, `poo.py` y `funcional.py` **no se modificaron**. Tras crear el sensor y sincronizarlo se volvieron a ejecutar los tres motores: los JSON siguen siendo byte-idénticos (SHA-256 `0B99768E…26093`), de modo que la igualdad de los paradigmas queda intacta. El estado anterior se respaldó en `versiones/v22_banner_sesion_<timestamp>/`, `versiones/v23_promo_real_<timestamp>/` y `versiones/v24_sensor_apertura_<timestamp>/`.
