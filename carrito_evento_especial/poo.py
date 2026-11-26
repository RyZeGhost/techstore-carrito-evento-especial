"""Carrito Evento Especial - paradigma Orientado a Objetos.

Este módulo modela el agregado completo del carrito:

* ``Producto``: un SKU del catálogo, con sus datos privados y acceso controlado.
* ``ItemCarrito``: una línea del carrito, con cantidad, precio y descuento privados.
* ``CarritoEventoEspecial``: encapsula la colección de líneas, el estado del
  cliente y ejecuta polimórficamente las reglas de configuración del kit.
* ``RepositorioShopifyJSON``: carga el catálogo como ``Producto`` y persiste el
  estado final en ``resultado_poo.json``.

Paradigmas aplicados de forma explícita:

* Encapsulamiento: atributos privados y ``@property`` validados en ``Producto``,
  ``ItemCarrito``, ``CarritoEventoEspecial`` y ``RepositorioShopifyJSON``.
* Herencia: ``ReglaConfiguracionKit(ABC)`` define el contrato abstracto y sus
  cuatro subclases concretas lo implementan.
* Composición: ``ItemCarrito`` contiene un ``Producto``; el carrito contiene
  líneas, productos y reglas; el repositorio compone catálogo y resultado.
* Polimorfismo: ``ejecutar_reglas`` envía el mismo mensaje ``aplicar`` a cada
  objeto ``ReglaConfiguracionKit`` sin conocer su clase concreta.

Los métodos especiales ``__str__``, ``__repr__`` y ``__len__`` permiten imprimir
un desglose legible del kit: ``str`` muestra importes y cantidades, ``repr`` da
una forma inequívoca para depuración y ``len`` devuelve el stock de un
``Producto``, las unidades de un ``ItemCarrito`` y las líneas del carrito.

Las reglas convierten entradas inválidas o falta de stock en
``ParametroKitInvalidoError`` y ``StockInsuficienteError``, las capturan con
``try/except`` y las transforman en avisos, de modo que una regla fallida no
detiene la ejecución de las demás.

Regla de aislamiento: este archivo se escribió sin leer ni copiar los otros
paradigmas (``imperativo.py`` y ``funcional.py``). La información de precios,
stock y etiquetas sale de ``catalogo_shopify.json``."""

import json
from abc import ABC, abstractmethod
from pathlib import Path

RUTA_CATALOGO = Path(__file__).resolve().parent / "catalogo_shopify.json"


def _pesos(valor):
    """Encapsulamiento: función auxiliar privada del módulo; no expone estado.
    Composición: da formato a importes usados por las tres clases con ``__str__``.
    Polimorfismo: recibe cualquier número sin depender del tipo de objeto que lo entrega."""
    return "$" + format(valor, ",.0f").replace(",", ".")


class StockInsuficienteError(ValueError):
    """Error de dominio cuando faltan unidades para una reserva.

    Encapsulamiento: no añade estado mutable; solo transporta un mensaje.
    Herencia: deriva de ``ValueError`` para conservar compatibilidad con las
    validaciones previas.
    Composición: es lanzada por ``Producto.reservar`` y por las reglas del kit.
    Polimorfismo: las cuatro reglas la capturan de forma uniforme dentro de ``try/except``."""


class ParametroKitInvalidoError(ValueError):
    """Error de dominio para entradas del kit con tipo o rango inválido.

    Encapsulamiento: no expone atributos; comunica solo el parámetro afectado.
    Herencia: deriva de ``ValueError`` para integrarse con las validaciones existentes.
    Composición: la lanzan los helpers de reglas, ``reservar`` y ``porcentaje_descuento``.
    Polimorfismo: se maneja igual en todas las reglas mediante el mismo bloque ``except``."""


class Producto:
    """Representa un SKU del catálogo con acceso controlado a sus datos.

    Encapsulamiento: ``_sku``, ``_titulo``, ``_categoria``, ``_precio``, ``_stock``,
    ``_etiquetas`` y ``_origen`` son privados y se exponen solo mediante ``@property``.
    Composición: lleva una colección interna de etiquetas defendida con copia en tupla.
    Herencia: no deriva de otra clase; es una entidad base del modelo.
    Polimorfismo: ``desde_dict`` es un ``classmethod`` que construye la misma clase
    desde el JSON sin acoplarse al repositorio."""

    def __init__(self, sku, titulo, categoria, precio, stock, etiquetas=None, origen=""):
        # Se crean todos los atributos privados antes de usar los setters, para
        # que las validaciones de las propiedades encuentren un estado coherente.
        """Encapsulamiento: crea primero los atributos privados y luego usa los setters
        para que cada validación encuentre un estado coherente.
        Composición: recibe la colección de etiquetas y delega su normalización en la
        propiedad ``etiquetas``.
        Herencia: no interviene; es el constructor de una entidad base.
        Polimorfismo: no interviene directamente, pero ``desde_dict`` reutiliza este constructor."""
        self._sku = ""
        self._titulo = ""
        self._categoria = ""
        self._precio = 0
        self._stock = 0
        self._etiquetas = []
        self._origen = ""

        self.sku = sku
        self.titulo = titulo
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.etiquetas = etiquetas
        self.origen = origen

    @property
    def sku(self):
        """Encapsulamiento: getter controlado de ``_sku``; devuelve el valor sin permitir
        escritura directa desde fuera de la clase.
        Composición: expone el identificador usado por ``ItemCarrito`` y el inventario."""
        return self._sku

    @sku.setter
    def sku(self, valor):
        """Encapsulamiento: valida cadena no vacía antes de asignar ``_sku``.
        Herencia: no interviene; la validación es propia de la entidad.
        Polimorfismo: no interviene; mantiene la interfaz común de propiedades del modelo."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("sku debe ser una cadena no vacía")
        self._sku = valor.strip()

    @property
    def titulo(self):
        """Encapsulamiento: getter de ``_titulo`` sin acceso directo al privado.
        Composición: el título se reutiliza en líneas, regalo y desglose en consola."""
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        """Encapsulamiento: exige cadena no vacía antes de guardar ``_titulo``.
        Polimorfismo: mantiene la misma convención de validación que las demás propiedades."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("titulo debe ser una cadena no vacía")
        self._titulo = valor.strip()

    @property
    def categoria(self):
        """Encapsulamiento: getter de ``_categoria`` controlado por la clase.
        Composición: la categoría se exporta en las líneas del carrito."""
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        """Encapsulamiento: valida cadena no vacía antes de asignar ``_categoria``.
        Polimorfismo: aplica el mismo patrón de setter validado que ``sku`` y ``titulo``."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("categoria debe ser una cadena no vacía")
        self._categoria = valor.strip()

    @property
    def precio(self):
        """Encapsulamiento: getter de ``_precio``; evita modificar el importe sin validar.
        Composición: las reglas leen este precio para calcular descuentos."""
        return self._precio

    @precio.setter
    def precio(self, valor):
        """Encapsulamiento: rechaza booleanos, no numéricos y negativos antes de fijar
        ``_precio``, garantizando el dominio del objeto.
        Polimorfismo: mismo patrón de validación que ``precio_unitario`` en ``ItemCarrito``."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("precio debe ser un número")
        if valor < 0:
            raise ValueError("precio no puede ser negativo")
        self._precio = valor

    @property
    def stock(self):
        """Encapsulamiento: getter de ``_stock`` sin exponer escritura libre.
        Composición: las reglas consultan el stock para decidir reservas."""
        return self._stock

    @stock.setter
    def stock(self, valor):
        """Encapsulamiento: acepta solo enteros no negativos antes de asignar ``_stock``.
        Polimorfismo: comparte la regla de dominio con otras cantidades del modelo."""
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("stock debe ser un entero")
        if valor < 0:
            raise ValueError("stock no puede ser negativo")
        self._stock = valor

    @property
    def etiquetas(self):
        """Encapsulamiento: devuelve una copia en tupla de ``_etiquetas``, de modo que el
        exterior no pueda modificar la lista interna.
        Composición: las reglas consultan etiquetas sin recibir la colección original."""
        return tuple(self._etiquetas)

    @etiquetas.setter
    def etiquetas(self, valores):
        """Encapsulamiento: descarta ``None``, rechaza cadenas y elementos no cadena,
        elimina duplicados y guarda la lista resultante en ``_etiquetas``.
        Polimorfismo: aplica la misma disciplina de validación que los otros setters."""
        if valores is None:
            self._etiquetas = []
            return
        if isinstance(valores, str):
            raise TypeError("etiquetas debe ser una colección de cadenas")
        lista = []
        for valor in valores:
            if not isinstance(valor, str):
                raise TypeError("cada etiqueta debe ser una cadena")
            if valor not in lista:
                lista.append(valor)
        self._etiquetas = lista

    @property
    def origen(self):
        """Encapsulamiento: getter de ``_origen`` controlado por la clase.
        Composición: el origen se conserva al exportar el producto con ``a_dict``."""
        return self._origen

    @origen.setter
    def origen(self, valor):
        """Encapsulamiento: valida que sea cadena antes de guardar ``_origen``.
        Polimorfismo: mantiene la interfaz de propiedades validadas del modelo."""
        if not isinstance(valor, str):
            raise TypeError("origen debe ser una cadena")
        self._origen = valor

    def tiene_etiqueta(self, etiqueta):
        """Encapsulamiento: consulta ``_etiquetas`` sin entregar la colección privada.
        Composición: es usada por ``_seleccionar`` para filtrar productos por regla.
        Polimorfismo: la misma consulta sirve para sensores, cámaras y cartel."""
        for propia in self._etiquetas:
            if propia == etiqueta:
                return True
        return False

    def hay_stock(self, cantidad):
        """Encapsulamiento: valida la cantidad y lee ``_stock`` sin modificar el estado.
        Composición: ``reservar`` la usa como paso previo al descuento de inventario.
        Polimorfismo: todas las reglas confían en el mismo contrato de disponibilidad."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise TypeError("cantidad debe ser un entero")
        if cantidad <= 0:
            raise ValueError("cantidad debe ser mayor a cero")
        return self._stock >= cantidad

    def reservar(self, cantidad):
        """Encapsulamiento: descuenta unidades usando el setter de ``stock``, nunca
        asignando ``_stock`` directamente.
        Composición: es invocada por las cuatro reglas para descontar inventario.
        Polimorfismo: lanza ``StockInsuficienteError`` o ``ParametroKitInvalidoError``,
        que las reglas capturan de forma uniforme."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ParametroKitInvalidoError("cantidad debe ser un entero mayor a cero")
        if not self.hay_stock(cantidad):
            raise StockInsuficienteError(
                "stock insuficiente para reservar la cantidad pedida"
            )
        self.stock = self._stock - cantidad
        return self._stock

    @classmethod
    def desde_dict(cls, datos):
        """Composición: construye un ``Producto`` a partir de un elemento del JSON.
        Polimorfismo: al ser ``classmethod`` respeta la clase concreta desde la que se llama.
        Encapsulamiento: usa los setters en lugar de tocar atributos privados directamente."""
        return cls(
            sku=datos["sku"],
            titulo=datos["titulo"],
            categoria=datos["categoria"],
            precio=datos["precio"],
            stock=datos["stock"],
            etiquetas=datos.get("tags_funcionales", []),
            origen=datos.get("origen", ""),
        )

    def a_dict(self):
        """Encapsulamiento: exporta una vista plana sin ceder referencias a atributos
        privados y devolviendo una copia de las etiquetas.
        Composición: el dict resultante alimenta ``ItemCarrito`` y el repositorio.
        Polimorfismo: misma interfaz de exportación que ``ItemCarrito`` y el carrito."""
        vista = {}
        vista["sku"] = self._sku
        vista["titulo"] = self._titulo
        vista["categoria"] = self._categoria
        vista["precio"] = self._precio
        vista["stock"] = self._stock
        vista["etiquetas"] = list(self.etiquetas)
        vista["origen"] = self._origen
        return vista

    def __str__(self):
        """Encapsulamiento: lee solo propiedades públicas controladas para formatear el SKU.
        Polimorfismo: todos los objetos del modelo pueden pasarse a ``str`` con salida legible.
        Composición: su salida se inserta en el desglose del carrito."""
        texto = self._sku + " | " + self._titulo + " | " + self._categoria
        return texto + " | " + _pesos(self._precio) + " | stock " + str(self._stock)

    def __repr__(self):
        """Encapsulamiento: reconstruye la firma pública desde los atributos privados.
        Polimorfismo: método especial estándar compartido con las otras clases del modelo.
        Composición: incluye etiquetas y origen para una representación unívoca."""
        return (
            "Producto(sku=" + repr(self._sku)
            + ", titulo=" + repr(self._titulo)
            + ", categoria=" + repr(self._categoria)
            + ", precio=" + repr(self._precio)
            + ", stock=" + repr(self._stock)
            + ", etiquetas=" + repr(list(self.etiquetas))
            + ", origen=" + repr(self._origen) + ")"
        )

    def __len__(self):
        """Encapsulamiento: expone ``_stock`` como longitud sin acceso directo al privado.
        Polimorfismo: cada clase define su propia longitud coherente con su dominio.
        Composición: el carrito usa ``len`` sobre sus propias líneas, no sobre productos."""
        return self._stock


class ItemCarrito:
    """Representa una línea del carrito con importes calculados y validados.

    Encapsulamiento: ``_producto``, ``_cantidad``, ``_precio_unitario``,
    ``_precio_unitario_original``, ``_descuento`` y ``_es_regalo`` son privados.
    Composición: contiene un ``Producto`` y delega en él SKU, título, etiquetas y stock.
    Herencia: no hereda; colabora con la jerarquía de reglas como destino de ``aplicar``.
    Polimorfismo: ``a_dict``, ``__str__`` y ``__repr__`` tratan igual una línea normal
    y una línea promocional de regalo."""

    def __init__(self, producto, cantidad, precio_unitario=None, descuento=0,
                 es_regalo=False, precio_unitario_original=None):
        """Encapsulamiento: inicializa privados y pasa por los setters antes de usarlos.
        Composición: valida que el argumento sea un ``Producto`` y lo guarda como colaborador.
        Polimorfismo: el mismo constructor atiende líneas normales y de regalo mediante
        ``es_regalo`` y ``precio_unitario_original``."""
        self._producto = None
        self._cantidad = 0
        self._precio_unitario = 0
        self._precio_unitario_original = 0
        self._descuento = 0
        self._es_regalo = False

        if not isinstance(producto, Producto):
            raise TypeError("producto debe ser una instancia de Producto")
        self._producto = producto

        if precio_unitario is None:
            precio_unitario = producto.precio
        if precio_unitario_original is None:
            precio_unitario_original = precio_unitario
        # El orden importa: descuento se valida contra subtotal, que depende del
        # precio original y la cantidad, así que esos dos se asignan primero.
        self.precio_unitario_original = precio_unitario_original
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
        self.descuento = descuento
        self._es_regalo = bool(es_regalo)

    @property
    def producto(self):
        """Encapsulamiento: getter de ``_producto``; la referencia no se puede reasignar.
        Composición: expone el objeto contenido para que la línea delegue en él.
        Polimorfismo: todas las líneas comparten la misma forma de acceder a su producto."""
        return self._producto

    @property
    def sku(self):
        """Encapsulamiento: obtiene el SKU delegando en el ``Producto`` contenido.
        Composición: demuestra delegación entre ``ItemCarrito`` y ``Producto``.
        Polimorfismo: mismo acceso para líneas de sensores, cámaras y regalo."""
        return self._producto.sku

    @property
    def cantidad(self):
        """Encapsulamiento: getter de ``_cantidad`` sin exposición directa.
        Composición: interviene en ``subtotal`` y en ``len`` de la línea."""
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        """Encapsulamiento: exige entero positivo antes de asignar ``_cantidad``.
        Polimorfismo: replica la disciplina de validación de cantidades del modelo."""
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("cantidad debe ser un entero")
        if valor <= 0:
            raise ValueError("cantidad debe ser mayor a cero")
        self._cantidad = valor

    @property
    def precio_unitario(self):
        """Encapsulamiento: getter de ``_precio_unitario`` controlado por la clase.
        Composición: es el precio final que aparece en el desglose del kit."""
        return self._precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, valor):
        """Encapsulamiento: rechaza booleanos, no numéricos y negativos antes de fijar
        ``_precio_unitario``.
        Polimorfismo: misma validación que ``Producto.precio``."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("precio_unitario debe ser un número")
        if valor < 0:
            raise ValueError("precio_unitario no puede ser negativo")
        self._precio_unitario = valor

    @property
    def precio_unitario_original(self):
        """Encapsulamiento: getter del precio de lista previo al descuento.
        Composición: evita el doble descuento al calcular ``subtotal`` sobre este valor.
        Polimorfismo: las reglas de cámaras y la de regalo usan el mismo contrato."""
        return self._precio_unitario_original

    @precio_unitario_original.setter
    def precio_unitario_original(self, valor):
        """Encapsulamiento: valida número no negativo antes de guardar el precio original.
        Polimorfismo: comparte criterio con ``precio_unitario`` y ``Producto.precio``."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("precio_unitario_original debe ser un número")
        if valor < 0:
            raise ValueError("precio_unitario_original no puede ser negativo")
        self._precio_unitario_original = valor

    @property
    def descuento(self):
        """Encapsulamiento: getter de ``_descuento`` sin mutación externa.
        Composición: el carrito suma estos importes en ``descuento_total``."""
        return self._descuento

    @descuento.setter
    def descuento(self, valor):
        """Encapsulamiento: exige número no negativo y no mayor que el ``subtotal`` antes
        de asignar ``_descuento``.
        Polimorfismo: la regla de cámaras y la de regalo usan la misma propiedad."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("descuento debe ser un número")
        if valor < 0:
            raise ValueError("descuento no puede ser negativo")
        if valor > self.subtotal:
            raise ValueError("descuento no puede superar el subtotal de la línea")
        self._descuento = valor

    @property
    def subtotal(self):
        """Encapsulamiento: propiedad derivada de ``_precio_unitario_original`` y
        ``_cantidad``; no almacena estado duplicado.
        Composición: se calcula a partir de los privados de la propia línea.
        Polimorfismo: es la misma interfaz para todas las líneas del carrito."""
        return self._precio_unitario_original * self._cantidad

    @property
    def total(self):
        """Encapsulamiento: deriva el neto de ``subtotal`` y ``_descuento`` sin guardarlo.
        Composición: el desglose del carrito suma estos totales por línea.
        Polimorfismo: funciona igual para líneas con y sin descuento."""
        return self.subtotal - self._descuento

    @property
    def es_regalo(self):
        """Encapsulamiento: getter de ``_es_regalo``; nadie puede activar el regalo desde fuera.
        Composición: la bandera distingue la línea promocional dentro del carrito.
        Polimorfismo: ``a_dict`` y ``__str__`` cambian su salida según esta bandera."""
        return self._es_regalo

    def a_dict(self):
        """Encapsulamiento: exporta una vista plana sin ceder los atributos privados.
        Composición: delega en ``Producto`` para título, categoría y etiquetas.
        Polimorfismo: el repositorio serializa cualquier línea con la misma interfaz."""
        vista = {}
        vista["sku"] = self.sku
        vista["titulo"] = self._producto.titulo
        vista["categoria"] = self._producto.categoria
        vista["etiquetas"] = list(self._producto.etiquetas)
        vista["cantidad"] = self._cantidad
        vista["precio_unitario"] = self._precio_unitario
        vista["precio_unitario_original"] = self._precio_unitario_original
        vista["subtotal"] = self.subtotal
        vista["descuento"] = self._descuento
        vista["total"] = self.total
        vista["stock_producto"] = self._producto.stock
        vista["es_regalo"] = self._es_regalo
        return vista

    def __str__(self):
        """Encapsulamiento: lee propiedades validadas para mostrar cantidades e importes.
        Polimorfismo: añade la marca ``REGALO`` según el estado, reutilizando el mismo formato.
        Composición: cada línea se inserta numerada en el desglose del carrito."""
        texto = self.sku + " | " + self._producto.titulo
        texto += " | " + str(self._cantidad) + " x " + _pesos(self._precio_unitario)
        texto += " | subtotal " + _pesos(self.subtotal)
        texto += " | descuento -" + _pesos(self._descuento)
        texto += " | total " + _pesos(self.total)
        if self._es_regalo:
            texto += " | REGALO"
        return texto

    def __repr__(self):
        """Encapsulamiento: expresa los privados como una firma unívoca de constructor.
        Polimorfismo: método especial estándar, igual que en ``Producto`` y el carrito.
        Composición: incluye precio original y bandera de regalo para depurar sin ambigüedad."""
        return (
            "ItemCarrito(sku=" + repr(self.sku)
            + ", cantidad=" + repr(self._cantidad)
            + ", precio_unitario=" + repr(self._precio_unitario)
            + ", precio_unitario_original=" + repr(self._precio_unitario_original)
            + ", descuento=" + repr(self._descuento)
            + ", es_regalo=" + repr(self._es_regalo) + ")"
        )

    def __len__(self):
        """Encapsulamiento: devuelve ``_cantidad`` como longitud de la línea.
        Polimorfismo: define una longitud coherente con el dominio de la línea.
        Composición: el carrito suma longitudes propias, no las de sus líneas."""
        return self._cantidad


class ReglaConfiguracionKit(ABC):
    """Base abstracta que define la interfaz común de las reglas del kit.

    Herencia: declara ``aplicar`` como ``@abstractmethod``; las cuatro subclases
    concretas la implementan y la base no se puede instanciar.
    Polimorfismo: el motor envía el mismo mensaje ``aplicar`` sin conocer la clase.
    Encapsulamiento: centraliza validación, selección, avisos y manejo de errores en
    helpers privados reutilizables.
    Composición: recibe ya construidos el ``carrito``, el ``catalogo`` y los
    ``parametros`` sobre los que trabaja."""

    @abstractmethod
    def aplicar(self, carrito, catalogo, parametros):
        """Herencia: método abstracto que toda subclase concreta debe implementar.
        Polimorfismo: es el mensaje común que el carrito envía sin conocer la subclase.
        Encapsulamiento: define la interfaz pública; la lógica de ejecución queda en cada subclase.
        Composición: recibe carrito, catálogo y parámetros como colaboradores ya listos."""
        raise NotImplementedError

    @staticmethod
    def _entero_no_negativo(parametros, clave):
        """Encapsulamiento: valida tipo y rango dentro de la base antes de usar el valor.
        Polimorfismo: lanza ``ParametroKitInvalidoError``, manejado igual por todas las reglas.
        Composición: forma parte de los helpers compartidos por las cuatro subclases."""
        valor = parametros.get(clave, 0)
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ParametroKitInvalidoError(clave + " debe ser un entero")
        if valor < 0:
            raise ParametroKitInvalidoError(clave + " no puede ser negativo")
        return valor

    @staticmethod
    def _productos(catalogo):
        """Composición: acepta el dict del JSON o una lista de ``Producto`` y devuelve
        productos ya instanciados para que las reglas trabajen sobre objetos.
        Encapsulamiento: no modifica la estructura original cuando recibe el dict.
        Polimorfismo: las reglas concretas no necesitan saber de dónde salieron los productos."""
        productos = []
        if isinstance(catalogo, dict):
            for datos in catalogo["productos"]:
                productos.append(Producto.desde_dict(datos))
            return productos
        for producto in catalogo:
            if not isinstance(producto, Producto):
                raise TypeError("catalogo debe contener instancias de Producto")
            productos.append(producto)
        return productos

    @staticmethod
    def _registrar_aviso(parametros, mensaje):
        """Encapsulamiento: muta de forma controlada la lista de avisos compartida en
        ``parametros``, creándola si no existe.
        Composición: la lista de avisos pertenece al carrito y se comparte entre reglas.
        Polimorfismo: cualquier regla puede avisar con el mismo mecanismo."""
        if "avisos" not in parametros or not isinstance(parametros["avisos"], list):
            parametros["avisos"] = []
        parametros["avisos"].append(mensaje)

    def _registrar_error(self, parametros, nombre_regla, error):
        """Encapsulamiento: convierte una excepción controlada en mensaje de aviso sin
        exponer el error crudo al carrito.
        Composición: reutiliza ``_registrar_aviso`` en lugar de duplicar lógica.
        Polimorfismo: uniformiza el tratamiento de errores en las cuatro reglas."""
        mensaje = nombre_regla + " omitida: " + str(error)
        self._registrar_aviso(parametros, mensaje)

    def _seleccionar(self, catalogo, parametros, etiquetas, cantidad,
                     excluidas=None, mensaje_aviso=""):
        """Composición: filtra productos, ajusta a stock parcial y elige el SKU más barato.
        Encapsulamiento: lee etiquetas, precio y stock solo mediante propiedades de ``Producto``.
        Polimorfismo: la misma selección sirve a sensores, cámaras y cartel.
        Herencia: helper protegido por convención, disponible para todas las subclases."""
        if excluidas is None:
            excluidas = []

        elegibles = []
        for producto in self._productos(catalogo):
            cumple = True
            for etiqueta in etiquetas:
                if not producto.tiene_etiqueta(etiqueta):
                    cumple = False
            for etiqueta in excluidas:
                if producto.tiene_etiqueta(etiqueta):
                    cumple = False
            if cumple:
                elegibles.append(producto)

        stock_max = 0
        for producto in elegibles:
            if producto.stock > stock_max:
                stock_max = producto.stock

        # Stock parcial: si sobra demanda pero hay unidades, se ajusta la
        # cantidad y se avisa. Si no hay unidades, la regla lo maneja con
        # StockInsuficienteError dentro de su propio try/except.
        if cantidad > stock_max and stock_max > 0:
            if mensaje_aviso == "":
                mensaje_aviso = "Cantidad ajustada de"
            texto = mensaje_aviso + " " + str(cantidad) + " a " + str(stock_max)
            self._registrar_aviso(parametros, texto + " por stock disponible.")
            cantidad = stock_max

        if stock_max <= 0 or cantidad <= 0:
            return None, 0

        mejor = None
        for producto in elegibles:
            if producto.stock >= cantidad and (mejor is None or producto.precio < mejor.precio):
                mejor = producto
        return mejor, cantidad


class ReglaSensoresApertura(ReglaConfiguracionKit):
    """Regla concreta que agrega sensores por puertas y ventanas.

    Herencia: implementa el ``aplicar`` abstracto de ``ReglaConfiguracionKit``.
    Polimorfismo: se ejecuta con la misma firma que las demás reglas del kit.
    Encapsulamiento: usa helpers privados de la base y ``try/except`` controlado.
    Composición: convierte un ``Producto`` del catálogo en un ``ItemCarrito``."""

    def aplicar(self, carrito, catalogo, parametros):
        """Herencia: implementa el ``aplicar`` abstracto de la base.
        Polimorfismo: se ejecuta con la misma firma que las otras tres reglas.
        Encapsulamiento: su ``try/except`` convierte entradas inválidas o sin stock en avisos.
        Composición: suma ``puertas + ventanas`` y convierte el ``Producto`` elegido en
        un ``ItemCarrito`` dentro del carrito."""
        try:
            cantidad = self._entero_no_negativo(parametros, "puertas")
            cantidad += self._entero_no_negativo(parametros, "ventanas")
            if cantidad == 0:
                return None

            producto, cantidad = self._seleccionar(
                catalogo,
                parametros,
                ["sensor_apertura"],
                cantidad,
                mensaje_aviso="Sensores de apertura ajustados de",
            )
            if producto is None:
                raise StockInsuficienteError(
                    "No hay sensores de apertura con stock suficiente"
                )
            producto.reservar(cantidad)
        except (ParametroKitInvalidoError, StockInsuficienteError) as error:
            self._registrar_error(parametros, "ReglaSensoresApertura", error)
            return None

        item = ItemCarrito(producto, cantidad)
        carrito.append(item)
        return item


class ReglaSensorMovimientoMascotas(ReglaConfiguracionKit):
    """Regla concreta que elige sensores según la bandera de mascotas.

    Herencia: implementa el ``aplicar`` abstracto de ``ReglaConfiguracionKit``.
    Polimorfismo: comparte interfaz con las otras reglas pese a filtrar distinto.
    Encapsulamiento: valida la bandera y las etiquetas sin exponer estado propio.
    Composición: selecciona un ``Producto`` y lo inserta como ``ItemCarrito``."""

    def aplicar(self, carrito, catalogo, parametros):
        """Herencia: implementa el ``aplicar`` abstracto de la base.
        Polimorfismo: mantiene la interfaz común aunque cambia el filtro de etiquetas.
        Encapsulamiento: valida la bandera ``tiene_mascotas`` dentro del ``try`` y avisa si falla.
        Composición: usa ``_seleccionar`` y agrega un ``ItemCarrito`` al carrito."""
        try:
            cantidad = self._entero_no_negativo(parametros, "cantidad_sensores_movimiento")
            if cantidad == 0:
                return None

            tiene_mascotas = parametros.get("tiene_mascotas", False)
            if not isinstance(tiene_mascotas, bool):
                raise ParametroKitInvalidoError("tiene_mascotas debe ser booleano")

            etiquetas = ["sensor_movimiento"]
            excluidas = []
            if tiene_mascotas:
                etiquetas.append("inmune_mascotas")
            else:
                excluidas.append("inmune_mascotas")

            producto, cantidad = self._seleccionar(
                catalogo,
                parametros,
                etiquetas,
                cantidad,
                excluidas,
                "Sensores de movimiento ajustados de",
            )
            if producto is None:
                raise StockInsuficienteError(
                    "No hay sensores de movimiento con stock suficiente"
                )
            producto.reservar(cantidad)
        except (ParametroKitInvalidoError, StockInsuficienteError) as error:
            self._registrar_error(parametros, "ReglaSensorMovimientoMascotas", error)
            return None

        item = ItemCarrito(producto, cantidad)
        carrito.append(item)
        return item


class ReglaCamarasDescuentoProgresivo(ReglaConfiguracionKit):
    """Regla concreta con la escala de descuento por volumen de cámaras.

    Herencia: implementa el ``aplicar`` abstracto de ``ReglaConfiguracionKit``.
    Polimorfismo: recibe el mismo mensaje que las demás reglas y devuelve una línea.
    Encapsulamiento: ``porcentaje_descuento`` valida dominio con excepción propia.
    Composición: usa el precio del ``Producto`` para construir el ``ItemCarrito``."""

    @staticmethod
    def porcentaje_descuento(cantidad):
        """Encapsulamiento: valida dominio propio y lanza ``ParametroKitInvalidoError``.
        Polimorfismo: todas las reglas comparten el mismo tipo de error ante entradas inválidas.
        Composición: devuelve el porcentaje que ``aplicar`` usa sobre el precio del producto.
        Herencia: método estático propio de la subclase, no redefine el contrato base."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise ParametroKitInvalidoError("cantidad debe ser un entero")
        if cantidad < 0:
            raise ParametroKitInvalidoError("cantidad no puede ser negativa")
        if cantidad >= 4:
            return 0.20
        if cantidad >= 2:
            return 0.10
        return 0.0

    def aplicar(self, carrito, catalogo, parametros):
        """Herencia: implementa el ``aplicar`` abstracto de la base.
        Polimorfismo: recibe el mismo mensaje que las reglas de sensores y regalo.
        Encapsulamiento: maneja errores con ``try/except`` y conserva
        ``precio_unitario_original`` para evitar doble descuento.
        Composición: aplica la escala sobre el ``Producto`` y agrega el ``ItemCarrito``."""
        try:
            cantidad = self._entero_no_negativo(parametros, "cantidad_camaras")
            if cantidad == 0:
                return None

            # La escala se resuelve antes de elegir el SKU: el porcentaje depende
            # de la cantidad pedida, no del precio del producto seleccionado.
            porcentaje = self.porcentaje_descuento(cantidad)
            producto, cantidad = self._seleccionar(
                catalogo, parametros, ["camara"], cantidad
            )
            if producto is None:
                raise StockInsuficienteError("No hay cámaras con stock suficiente")

            # Descuento por unidad sobre el precio de lista. Se redondea a entero
            # porque el catálogo trabaja en pesos chilenos sin centavos.
            descuento_unitario = int(round(producto.precio * porcentaje))
            precio_unitario = producto.precio - descuento_unitario
            producto.reservar(cantidad)
        except (ParametroKitInvalidoError, StockInsuficienteError) as error:
            self._registrar_error(parametros, "ReglaCamarasDescuentoProgresivo", error)
            return None

        item = ItemCarrito(
            producto,
            cantidad,
            precio_unitario=precio_unitario,
            descuento=descuento_unitario * cantidad,
            precio_unitario_original=producto.precio,
        )
        carrito.append(item)
        return item


class ReglaCartelRegalo(ReglaConfiguracionKit):
    """Regla concreta que regala un cartel disuasivo a costo cero.

    Herencia: implementa el ``aplicar`` abstracto de ``ReglaConfiguracionKit``.
    Polimorfismo: se ejecuta igual que las reglas de sensores y cámaras.
    Encapsulamiento: ``_item_promocional`` fija precio, descuento y bandera de regalo.
    Composición: transforma el ``Producto`` cartel en un ``ItemCarrito`` promocional."""

    @staticmethod
    def _item_promocional(cartel):
        """Composición: construye un ``ItemCarrito`` a partir del ``Producto`` cartel.
        Encapsulamiento: fija precio cero, descuento cero y ``es_regalo`` en True sin
        exponer los privados de la línea.
        Polimorfismo: el carrito trata esta línea igual que las demás al serializarla.
        Herencia: helper estático propio de la subclase."""
        # ``precio_unitario_original`` queda en 0 a propósito: si guardara el
        # precio de lista, el subtotal del carrito incluiría el regalo y habría
        # que descontarlo para que el total volviera a ser 0.
        return ItemCarrito(cartel, 1, precio_unitario=0, descuento=0, es_regalo=True)

    def aplicar(self, carrito, catalogo, parametros):
        """Herencia: implementa el ``aplicar`` abstracto de la base.
        Polimorfismo: se ejecuta igual que las otras reglas dentro del bucle del carrito.
        Encapsulamiento: captura ``StockInsuficienteError`` y deja ``regalo`` en ``False``
        sin interrumpir la ejecución.
        Composición: exige carrito no vacío, reserva stock del cartel y agrega la línea promocional."""
        if len(carrito) == 0:
            parametros["regalo"] = {"incluido": False}
            return None

        try:
            cartel = None
            for producto in self._productos(catalogo):
                if producto.tiene_etiqueta("cartel_disuasivo") and producto.stock > 0:
                    cartel = producto
                    break
            if cartel is None:
                raise StockInsuficienteError("no hay stock del cartel disuasivo")

            precio_original = cartel.precio
            cartel.reservar(1)
        except (ParametroKitInvalidoError, StockInsuficienteError) as error:
            parametros["regalo"] = {"incluido": False}
            self._registrar_error(parametros, "ReglaCartelRegalo", error)
            return None

        item = self._item_promocional(cartel)
        carrito.append(item)

        parametros["regalo"] = {
            "incluido": True,
            "sku": cartel.sku,
            "titulo": cartel.titulo,
            "cantidad": 1,
            "precio_original": precio_original,
            "precio_final": 0,
            "subtotal": 0,
        }
        return item


class CarritoEventoEspecial:
    """Agregado que encapsula el carrito, el cliente y las reglas.

    Encapsulamiento: ``_items``, ``_catalogo``, el estado del cliente, ``_avisos`` y
    ``_regalo`` son privados con ``@property`` validados.
    Composición: contiene ``ItemCarrito``, ``Producto`` y objetos regla.
    Herencia: no deriva de otra clase; coordina la jerarquía ``ReglaConfiguracionKit``.
    Polimorfismo: ``ejecutar_reglas`` invoca ``aplicar`` en cada regla concreta sin
    conocer su tipo."""

    def __init__(self, catalogo, puertas=0, ventanas=0, tiene_mascotas=False,
                 cantidad_camaras=0, cantidad_sensores_movimiento=0):
        """Encapsulamiento: crea primero todos los privados y luego usa los setters.
        Composición: recibe el catálogo y lo clona en ``_catalogo`` para no mutar objetos externos.
        Herencia: no hereda; es el agregado que coordina la jerarquía de reglas.
        Polimorfismo: prepara el estado que luego se enviará a cualquier regla concreta."""
        self._items = []
        self._catalogo = []
        self._puertas = 0
        self._ventanas = 0
        self._tiene_mascotas = False
        self._cantidad_camaras = 0
        self._cantidad_sensores_movimiento = 0
        self._avisos = []
        self._regalo = {"incluido": False}

        self.catalogo = catalogo
        self.puertas = puertas
        self.ventanas = ventanas
        self.tiene_mascotas = tiene_mascotas
        self.cantidad_camaras = cantidad_camaras
        self.cantidad_sensores_movimiento = cantidad_sensores_movimiento

    @staticmethod
    def _validar_entero(nombre, valor):
        """Encapsulamiento: centraliza la validación de dominio de los enteros del cliente.
        Polimorfismo: el mismo validador sirve para puertas, ventanas, cámaras y movimiento.
        Composición: helper interno reutilizado por varios setters del agregado."""
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError(nombre + " debe ser un entero")
        if valor < 0:
            raise ValueError(nombre + " no puede ser negativo")
        return valor

    @property
    def items(self):
        """Encapsulamiento: devuelve una tupla copia, impidiendo agregar o quitar líneas
        desde fuera del agregado.
        Composición: expone las líneas contenido para el desglose y las pruebas.
        Polimorfismo: la colección contiene ``ItemCarrito`` sin importar su clase de regla de origen."""
        return tuple(self._items)

    @property
    def cantidad_items(self):
        """Encapsulamiento: deriva el conteo de ``_items`` sin exponer la lista.
        Composición: se usa en ``resumen``, ``__len__`` y ``__repr__``.
        Polimorfismo: cuenta igual líneas normales y de regalo."""
        return len(self._items)

    @property
    def catalogo(self):
        """Encapsulamiento: devuelve una tupla copia de los ``Producto`` internos.
        Composición: expone el inventario ya reservado para el desglose y las pruebas.
        Polimorfismo: el repositorio y las reglas trabajan sobre la misma interfaz de catálogo."""
        return tuple(self._catalogo)

    @catalogo.setter
    def catalogo(self, valor):
        """Encapsulamiento: clona cada ``Producto`` antes de guardarlo en ``_catalogo``,
        aislando las reservas de stock de objetos externos.
        Composición: acepta el dict del JSON o una colección de ``Producto``.
        Polimorfismo: el mismo agregado admite catálogo crudo o ya instanciado."""
        productos = []
        if isinstance(valor, dict):
            datos_productos = valor.get("productos")
            if not isinstance(datos_productos, list):
                raise TypeError("catalogo debe tener una lista 'productos'")
            for datos in datos_productos:
                productos.append(Producto.desde_dict(datos))
        else:
            if isinstance(valor, (str, bytes)):
                raise TypeError("catalogo debe ser un dict o una colección de Producto")
            for producto in valor:
                if not isinstance(producto, Producto):
                    raise TypeError("catalogo debe contener instancias de Producto")
                productos.append(Producto(
                    sku=producto.sku,
                    titulo=producto.titulo,
                    categoria=producto.categoria,
                    precio=producto.precio,
                    stock=producto.stock,
                    etiquetas=producto.etiquetas,
                    origen=producto.origen,
                ))
        self._catalogo = productos

    @property
    def puertas(self):
        """Encapsulamiento: getter de ``_puertas`` controlado por el agregado.
        Composición: forma parte del estado enviado a las reglas como parámetro."""
        return self._puertas

    @puertas.setter
    def puertas(self, valor):
        """Encapsulamiento: usa ``_validar_entero`` antes de asignar ``_puertas``.
        Polimorfismo: mismo patrón que los demás atributos del cliente."""
        self._puertas = self._validar_entero("puertas", valor)

    @property
    def ventanas(self):
        """Encapsulamiento: getter de ``_ventanas`` sin acceso directo al privado.
        Composición: junto con ``puertas`` alimenta la regla de apertura."""
        return self._ventanas

    @ventanas.setter
    def ventanas(self, valor):
        """Encapsulamiento: valida entero no negativo antes de guardar ``_ventanas``.
        Polimorfismo: comparte validador con el resto del estado del cliente."""
        self._ventanas = self._validar_entero("ventanas", valor)

    @property
    def tiene_mascotas(self):
        """Encapsulamiento: getter de ``_tiene_mascotas`` controlado por la clase.
        Composición: la regla de movimiento consulta esta bandera vía parámetros."""
        return self._tiene_mascotas

    @tiene_mascotas.setter
    def tiene_mascotas(self, valor):
        """Encapsulamiento: exige booleano antes de asignar ``_tiene_mascotas``.
        Polimorfismo: mantiene la interfaz validada del estado del cliente."""
        if not isinstance(valor, bool):
            raise TypeError("tiene_mascotas debe ser booleano")
        self._tiene_mascotas = valor

    @property
    def cantidad_camaras(self):
        """Encapsulamiento: getter de ``_cantidad_camaras`` controlado.
        Composición: alimenta la regla de descuento progresivo."""
        return self._cantidad_camaras

    @cantidad_camaras.setter
    def cantidad_camaras(self, valor):
        """Encapsulamiento: valida entero no negativo antes de guardar la cantidad.
        Polimorfismo: usa el mismo validador que puertas y ventanas."""
        self._cantidad_camaras = self._validar_entero("cantidad_camaras", valor)

    @property
    def cantidad_sensores_movimiento(self):
        """Encapsulamiento: getter de ``_cantidad_sensores_movimiento`` controlado.
        Composición: se envía a la regla de sensores con mascotas."""
        return self._cantidad_sensores_movimiento

    @cantidad_sensores_movimiento.setter
    def cantidad_sensores_movimiento(self, valor):
        """Encapsulamiento: valida dominio con ``_validar_entero`` antes de asignar.
        Polimorfismo: mismo contrato que el resto de cantidades del cliente."""
        self._cantidad_sensores_movimiento = self._validar_entero(
            "cantidad_sensores_movimiento", valor
        )

    @property
    def avisos(self):
        """Encapsulamiento: devuelve copia de ``_avisos`` para impedir mutación externa.
        Composición: las reglas escriben en la lista real compartida en ``_parametros``.
        Polimorfismo: cualquier regla puede aportar avisos con el mismo formato."""
        return list(self._avisos)

    @property
    def regalo(self):
        """Encapsulamiento: devuelve copia de ``_regalo`` sin ceder el dict interno.
        Composición: la regla del cartel actualiza este estado vía ``parametros``.
        Polimorfismo: el repositorio serializa el regalo sin conocer la regla que lo creó."""
        return dict(self._regalo)

    @property
    def subtotal(self):
        """Encapsulamiento: suma importes derivados sin almacenar un estado redundante.
        Composición: recorre los ``ItemCarrito`` contenidos y usa su propiedad ``subtotal``.
        Polimorfismo: trata igual líneas de sensores, cámaras y regalo."""
        total = 0
        for item in self._items:
            total += item.subtotal
        return total

    @property
    def descuento_total(self):
        """Encapsulamiento: acumula los descuentos de las líneas sin exponer privados.
        Composición: delega en ``ItemCarrito.descuento``.
        Polimorfismo: funciona con reglas que descuentan y con reglas que no."""
        total = 0
        for item in self._items:
            total += item.descuento
        return total

    @property
    def total_final(self):
        """Encapsulamiento: deriva el neto de ``subtotal`` y ``descuento_total``.
        Composición: concentra el resultado de todas las líneas y reglas ejecutadas.
        Polimorfismo: es el valor que consumen ``__repr__``, ``__str__`` y el repositorio."""
        return self.subtotal - self.descuento_total

    def agregar_item(self, item):
        """Encapsulamiento: valida el tipo antes de append en ``_items``.
        Composición: incorpora un ``ItemCarrito`` ya construido al agregado.
        Polimorfismo: acepta cualquier línea, sin importar la regla que la originó."""
        if not isinstance(item, ItemCarrito):
            raise TypeError("item debe ser una instancia de ItemCarrito")
        self._items.append(item)
        return item

    def _parametros(self):
        """Encapsulamiento: traduce el estado privado al dict que esperan las reglas
        y comparte la lista real de avisos y el dict de regalo.
        Composición: arma los colaboradores ``carrito``, ``catalogo`` y ``parametros``.
        Polimorfismo: el dict resultante es indistinto para cualquier regla concreta."""
        parametros = {}
        parametros["puertas"] = self._puertas
        parametros["ventanas"] = self._ventanas
        parametros["tiene_mascotas"] = self._tiene_mascotas
        parametros["cantidad_camaras"] = self._cantidad_camaras
        parametros["cantidad_sensores_movimiento"] = self._cantidad_sensores_movimiento
        # Se comparte la lista real para que los avisos de las reglas queden en
        # el estado del carrito; el dict de regalo se vuelve a leer tras cada regla.
        parametros["avisos"] = self._avisos
        parametros["regalo"] = self._regalo
        return parametros

    def ejecutar_reglas(self, reglas):
        """Polimorfismo: envía el mismo mensaje ``aplicar`` a cada regla sin conocer su
        clase concreta, en el orden dado.
        Encapsulamiento: pasa los objetos privados reales para que las reglas muten el
        estado del agregado y no copias desechables.
        Composición: coordina reglas, catálogo y líneas; vuelve a leer ``regalo`` tras cada regla.
        Herencia: exige que cada elemento sea instancia de ``ReglaConfiguracionKit``."""
        if isinstance(reglas, (str, bytes)):
            raise TypeError("reglas debe ser una colección de ReglaConfiguracionKit")

        aplicadas = []
        for regla in reglas:
            if not isinstance(regla, ReglaConfiguracionKit):
                raise TypeError(
                    "cada regla debe ser una instancia de ReglaConfiguracionKit"
                )
            parametros = self._parametros()
            regla.aplicar(self._items, self._catalogo, parametros)
            self._regalo = parametros.get("regalo", self._regalo)
            aplicadas.append(regla)
        return tuple(aplicadas)

    def a_dict(self):
        """Encapsulamiento: exporta una vista plana sin ceder referencias a privados.
        Composición: delega en ``ItemCarrito.a_dict`` y construye cliente, regalo, resumen,
        inventario y avisos.
        Polimorfismo: el repositorio serializa el carrito usando solo esta interfaz pública."""
        vista = {}

        cliente = {}
        cliente["puertas"] = self._puertas
        cliente["ventanas"] = self._ventanas
        cliente["tiene_mascotas"] = self._tiene_mascotas
        cliente["cantidad_camaras"] = self._cantidad_camaras
        cliente["cantidad_sensores_movimiento"] = self._cantidad_sensores_movimiento
        vista["cliente"] = cliente

        lineas = []
        for item in self._items:
            lineas.append(item.a_dict())
        vista["carrito"] = lineas
        vista["regalo"] = dict(self._regalo)

        resumen = {}
        resumen["cantidad_items"] = self.cantidad_items
        resumen["subtotal"] = self.subtotal
        resumen["descuento_total"] = self.descuento_total
        resumen["total_final"] = self.total_final
        vista["resumen"] = resumen

        inventario = {}
        for producto in self._catalogo:
            inventario[producto.sku] = producto.stock
        vista["inventario"] = inventario
        vista["avisos"] = list(self._avisos)
        return vista

    def __str__(self):
        """Encapsulamiento: lee propiedades controladas para formatear el desglose.
        Composición: muestra cliente, líneas contenido, regalo y avisos.
        Polimorfismo: cada línea aporta su propio ``str`` sin que el carrito conozca su origen."""
        lineas = []
        lineas.append("Kit de Seguridad Residencial")
        cliente = "Cliente: " + str(self._puertas) + " puertas, " + str(self._ventanas)
        cliente += " ventanas, mascotas: " + ("si" if self._tiene_mascotas else "no")
        cliente += ", camaras: " + str(self._cantidad_camaras)
        cliente += ", sensores movimiento: " + str(self._cantidad_sensores_movimiento)
        lineas.append(cliente)
        lineas.append("-" * 68)

        numero = 0
        for item in self._items:
            numero += 1
            lineas.append(str(numero) + ". " + str(item))

        lineas.append("-" * 68)
        lineas.append("Subtotal: " + _pesos(self.subtotal))
        lineas.append("Descuento: -" + _pesos(self.descuento_total))
        lineas.append("Total final: " + _pesos(self.total_final))
        if self._regalo.get("incluido"):
            precio = self._regalo.get("precio_original") or 0
            lineas.append("Regalo: " + str(self._regalo.get("sku"))
                          + " (normalmente " + _pesos(precio) + ")")
        else:
            lineas.append("Regalo: no incluido")

        if self._avisos:
            for aviso in self._avisos:
                lineas.append("Aviso: " + aviso)
        else:
            lineas.append("Avisos: ninguno")
        return "\n".join(lineas)

    def __repr__(self):
        """Encapsulamiento: resume el estado privado del cliente y el total en una firma.
        Polimorfismo: método especial estándar compartido con las otras clases.
        Composición: incluye el número de líneas contenido."""
        return (
            "CarritoEventoEspecial(puertas=" + repr(self._puertas)
            + ", ventanas=" + repr(self._ventanas)
            + ", tiene_mascotas=" + repr(self._tiene_mascotas)
            + ", cantidad_camaras=" + repr(self._cantidad_camaras)
            + ", cantidad_sensores_movimiento=" + repr(self._cantidad_sensores_movimiento)
            + ", items=" + repr(self.cantidad_items)
            + ", total_final=" + repr(self.total_final) + ")"
        )

    def __len__(self):
        """Encapsulamiento: devuelve ``cantidad_items`` sin exponer la lista privada.
        Polimorfismo: cada clase define una longitud acorde a su dominio.
        Composición: ``ReglaCartelRegalo`` usa ``len(carrito)`` para decidir si hay artículos."""
        return self.cantidad_items


class RepositorioShopifyJSON:
    """Persistencia JSON del catálogo y del resultado del carrito.

    Encapsulamiento: ``_ruta_catalogo`` y ``_ruta_resultado`` son privados con
    ``@property`` validados.
    Composición: produce ``Producto`` y consume el estado de ``CarritoEventoEspecial``.
    Herencia: no hereda de otra clase; es un colaborador de infraestructura.
    Polimorfismo: depende solo de la interfaz pública ``a_dict`` del carrito, no de
    su estructura interna."""

    def __init__(self, ruta_catalogo=None, ruta_resultado=None):
        """Encapsulamiento: guarda rutas en privados y usa setters cuando se proporcionan.
        Composición: mantiene referencias a los archivos de catálogo y resultado.
        Herencia: no hereda; es un colaborador de infraestructura.
        Polimorfismo: admite rutas como ``str`` o ``pathlib.Path`` desde el mismo constructor."""
        self._ruta_catalogo = RUTA_CATALOGO
        self._ruta_resultado = RUTA_CATALOGO.parent / "resultado_poo.json"
        if ruta_catalogo is not None:
            self.ruta_catalogo = ruta_catalogo
        if ruta_resultado is not None:
            self.ruta_resultado = ruta_resultado

    @staticmethod
    def _validar_ruta(nombre, valor):
        """Encapsulamiento: valida tipo y extensión antes de devolver la ``Path``.
        Polimorfismo: acepta dos tipos de entrada distintos con la misma validación.
        Composición: helper reutilizado por ambos setters de rutas."""
        if isinstance(valor, Path):
            ruta = valor
        elif isinstance(valor, str) and valor.strip():
            ruta = Path(valor)
        else:
            raise TypeError(nombre + " debe ser una cadena o pathlib.Path")
        if ruta.suffix.lower() != ".json":
            raise ValueError(nombre + " debe terminar en .json")
        return ruta

    @property
    def ruta_catalogo(self):
        """Encapsulamiento: getter de ``_ruta_catalogo`` controlado.
        Composición: ``cargar_catalogo`` usa esta ruta para abrir el JSON."""
        return self._ruta_catalogo

    @ruta_catalogo.setter
    def ruta_catalogo(self, valor):
        """Encapsulamiento: valida cadena o ``Path`` con extensión ``.json`` antes de asignar.
        Polimorfismo: mismo contrato de validación que ``ruta_resultado``."""
        self._ruta_catalogo = self._validar_ruta("ruta_catalogo", valor)

    @property
    def ruta_resultado(self):
        """Encapsulamiento: getter de ``_ruta_resultado`` controlado.
        Composición: ``exportar_resultado`` usa esta ruta para escribir el archivo."""
        return self._ruta_resultado

    @ruta_resultado.setter
    def ruta_resultado(self, valor):
        """Encapsulamiento: valida la ruta antes de guardarla en el privado.
        Polimorfismo: comparte ``_validar_ruta`` con ``ruta_catalogo``."""
        self._ruta_resultado = self._validar_ruta("ruta_resultado", valor)

    def cargar_catalogo(self):
        """Composición: lee el JSON y construye objetos ``Producto`` con ``desde_dict``.
        Encapsulamiento: no expone el dict crudo ni modifica los objetos devueltos por el carrito.
        Polimorfismo: los productos devueltos sirven a cualquier regla y al agregado.
        Herencia: no interviene; usa la interfaz pública de ``Producto``."""
        with self._ruta_catalogo.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if not isinstance(datos, dict) or not isinstance(datos.get("productos"), list):
            raise ValueError("catalogo_shopify.json debe contener una lista 'productos'")

        productos = []
        for fila in datos["productos"]:
            productos.append(Producto.desde_dict(fila))
        return productos

    def exportar_resultado(self, carrito):
        """Encapsulamiento: valida el tipo del carrito y serializa solo su vista pública.
        Composición: consume ``CarritoEventoEspecial.a_dict`` y escribe ``resultado_poo.json``.
        Polimorfismo: depende de la interfaz ``a_dict`` y no de la estructura interna del carrito.
        Herencia: no interviene; colabora con la jerarquía de reglas de forma indirecta."""
        if not isinstance(carrito, CarritoEventoEspecial):
            raise TypeError("carrito debe ser una instancia de CarritoEventoEspecial")

        contenido = carrito.a_dict()
        # newline="\n" evita que Windows convierta los saltos en CRLF: el JSON
        # resultante es byte-idéntico en cualquier sistema operativo.
        with self._ruta_resultado.open("w", encoding="utf-8", newline="\n") as archivo:
            json.dump(contenido, archivo, ensure_ascii=False, indent=2)
            archivo.write("\n")
        return self._ruta_resultado


if __name__ == "__main__":
    # El repositorio entrega ``Producto`` instanciados; el agregado los clona
    # para que las reservas de stock no modifiquen los objetos cargados.
    repositorio = RepositorioShopifyJSON()
    productos = repositorio.cargar_catalogo()

    carrito = CarritoEventoEspecial(
        catalogo=productos,
        puertas=2,
        ventanas=4,
        tiene_mascotas=True,
        cantidad_camaras=3,
        cantidad_sensores_movimiento=2,
    )

    reglas = []
    reglas.append(ReglaSensoresApertura())
    reglas.append(ReglaSensorMovimientoMascotas())
    reglas.append(ReglaCamarasDescuentoProgresivo())
    reglas.append(ReglaCartelRegalo())

    carrito.ejecutar_reglas(reglas)
    repositorio.exportar_resultado(carrito)
    # str(carrito) imprime el desglose; el JSON ya quedó en resultado_poo.json.
    print(carrito)
