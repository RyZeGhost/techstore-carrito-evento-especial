# Registro de prompts utilizados con IA generativa

El desarrollo se realizó con asistencia de IA. A continuación se registran los prompts **en el orden en que fueron formulados**. Se agrupan en tres bloques por paradigma: tres prompts iniciales, tres para completar el código y tres finales para la versión definitiva.

---

## A. Paradigma imperativo

### Prompts iniciales

1. *"Define el problema del Carrito Evento Especial por ocasión y número de personas para una tienda de productos tecnológicos. Propón eventos con reglas de cantidades por persona, mínimos y redondeo hacia arriba. No escribas código todavía."*
2. *"Diseña la estructura de datos en JSON para productos (sku, nombre, precio, stock, categoría), eventos (reglas, cupón, producto 2x1), sustitutos y política de envío. Debe ser la misma fuente para los tres paradigmas."*
3. *"Escribe una función imperativa `armar_carrito(evento, personas, catalogo, cupon=None)` que use bucles y acumuladores para calcular cantidades, resolver stock con sustitutos y devolver un diccionario con items, faltantes, descuentos, envío y total."*

### Prompts para completar el código

4. *"Agrega validación de entradas: personas debe ser mayor que cero y el evento debe existir. Lanza ValueError con mensajes claros."*
5. *"Añade la promoción 2x1 sobre el producto configurado en el evento, considerando que el producto puede haber sido reemplazado por un sustituto."*
6. *"Aplica el cupón del 10 % sobre la base descontada y calcula envío gratis desde $50.000; usa enteros y división entera para evitar errores de punto flotante."*

### Prompts para la versión final

7. *"Comenta cada línea de la función imperativa explicando qué hace, para poder defenderla en clase."*
8. *"Revisa el orden de las claves del diccionario de salida y garantiza que sea idéntico al de las otras implementaciones."*
9. *"Verifica que la función no modifique el catálogo recibido como parámetro y que sea determinista para las mismas entradas."*

---

## B. Paradigma orientado a objetos

### Prompts iniciales

10. *"Modela el mismo carrito con clases. Propón clases para Producto, Item, Regla, Evento y Carrito, indicando responsabilidades y qué datos guarda cada una."*
11. *"Usa dataclasses inmutables para Producto, Item, Regla y Evento. El Carrito debe orquestar la creación de items y el cálculo de totales."*
12. *"Escribe `Producto.crear_item()` y `Regla.cantidad_para(personas)` con ceil() y mínimo, manteniendo la misma lógica que la versión imperativa."*

### Prompts para completar el código

13. *"Implementa herencia y polimorfismo: una clase abstracta Descuento con `calcular()` y dos subclases, Descuento2x1 y DescuentoPorcentaje."*
14. *"Encapsula la resolución de stock y sustitutos en `Carrito._resolver_regla()`, devolviendo una tupla (item, faltante)."*
15. *"Agrega `PoliticaEnvio` como clase separada con umbral de envío gratis y costo configurables desde el JSON."*

### Prompts para la versión final

16. *"Expón una función `armar_carrito(...)` equivalente a la del paradigma imperativo que oculte la creación de objetos al llamador."*
17. *"Normaliza el nombre del evento en el resultado para que el diccionario sea exactamente igual al de las otras versiones."*
18. *"Comenta cada línea de las clases y del método `armar()`, explicando encapsulamiento, herencia y polimorfismo."*

---

## C. Paradigma funcional

### Prompts iniciales

19. *"Reescribe el carrito usando solo funciones puras, sin mutar listas ni diccionarios. Usa tuplas y devuelve estructuras nuevas."*
20. *"Divide el problema en funciones pequeñas: validar, cantidad_para, crear_item, resolver, construir_lineas, sumar_subtotal, descuento_2x1, descuento_cupon y costo_envio."*
21. *"Usa map para aplicar las reglas, filter para separar items y faltantes, y reduce para sumar subtotales y calcular el 2x1."*

### Prompts para completar el código

22. *"Compón las funciones en `armar_carrito(...)` de forma que cada paso sea una llamada encadenada y el resultado sea el mismo diccionario de los otros paradigmas."*
23. *"Asegura que `resolver()` devuelva una tupla con un item o None y un faltante o None, y que `filter(None, ...)` elimine los None."*
24. *"Mantén la aritmética en enteros y el orden de las claves del resultado idéntico al de las versiones imperativa y orientada a objetos."*

### Prompts para la versión final

25. *"Comenta cada línea explicando qué función pura interviene y por qué no hay efectos secundarios."*
26. *"Escribe pruebas automáticas que comparen los tres resultados para cinco escenarios, incluyendo sustitución por stock y envío pagado."*
27. *"Genera un documento que explique línea por línea el código y otro que registre los errores encontrados y cómo se corrigieron."*

---

## Observaciones sobre el uso de IA

- Los prompts fueron evolucionando desde la definición del modelo de datos hasta la validación final.
- Cada respuesta generada fue **supervisada**: se ejecutó, se comparó contra los otros paradigmas y se corrigió cuando fue necesario.
- Prompt adicional recibido durante la revisión: *"La tienda debe ser de productos tecnológicos; ajusta el catálogo, los eventos y la documentación"*. A partir de él se generó el catálogo actual de 22 SKU y se renombró el evento `asado` a `trabajo_remoto`.
- Otro prompt de revisión: *"Agrega imágenes sin marca de agua y precios realistas de Chile a los productos de tecnología"*. Dio lugar a las imágenes de Openverse/Flickr, los precios en CLP y la sincronización de productos existentes.
- Prompt final: *"Continúa con lo solicitado"*. Se usó para cerrar la integración: backoff exponencial, validación del catálogo, `main.py` sobre GraphQL, API HTTP de los tres paradigmas y presentación en diapositivas.
- Las correcciones reales se detallan en [`errores_corregidos.md`](errores_corregidos.md).
