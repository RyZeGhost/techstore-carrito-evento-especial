"""Versión ORIENTADA A OBJETOS del Carrito Evento Especial.

Características del paradigma usadas aquí:
- Clases e instancias que modelan Producto, Regla, Evento, Item y Carrito.
- Encapsulamiento: cada clase conoce solo su propia responsabilidad.
- Herencia y polimorfismo: `Descuento2x1` y `DescuentoPorcentaje` derivan de
  `Descuento` y se tratan de la misma forma desde el carrito.
"""

import math  # Para ceil().
from abc import ABC, abstractmethod  # ABC = clase abstracta.
from dataclasses import dataclass  # Reduce el código repetitivo de __init__.

from carrito.datos import indice_productos  # Índice compartido de productos.
from carrito.recomendaciones import sugerir  # Regla pura compartida.


# --- Modelo de datos ---

@dataclass(frozen=True)  # frozen=True => objetos inmutables.
class Producto:
    """Representa un producto del catálogo."""

    sku: str  # Identificador único.
    nombre: str  # Nombre visible.
    precio: int  # Precio en pesos enteros.
    stock: int  # Unidades disponibles.

    def crear_item(self, cantidad, sustituto_de=None):
        """Fábrica de líneas de carrito a partir del producto."""
        return Item(  # Devuelve un objeto Item.
            sku=self.sku,  # SKU del producto vendido.
            nombre=self.nombre,  # Nombre del producto vendido.
            cantidad=cantidad,  # Unidades calculadas.
            precio_unitario=self.precio,  # Precio unitario.
            subtotal=cantidad * self.precio,  # Precio total de la línea.
            sustituto_de=sustituto_de,  # SKU original si hubo sustitución.
        )


@dataclass(frozen=True)
class Item:
    """Una línea del carrito; también inmutable."""

    sku: str
    nombre: str
    cantidad: int
    precio_unitario: int
    subtotal: int
    sustituto_de: str | None  # None cuando no hubo sustitución.

    def como_dict(self):
        """Convierte el objeto en diccionario para igualar a los otros paradigmas."""
        return {
            "sku": self.sku,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal,
            "sustituto_de": self.sustituto_de,
        }


@dataclass(frozen=True)
class Regla:
    """Regla que define cuántas unidades se sugieren por persona."""

    sku: str  # Producto al que aplica.
    por_persona: float  # Unidades (o fracción) por persona.
    minimo: int  # Mínimo absoluto de unidades.

    def cantidad_para(self, personas):
        """Calcula la cantidad redondeada hacia arriba, con mínimo."""
        return max(self.minimo, math.ceil(personas * self.por_persona))


@dataclass(frozen=True)
class Evento:
    """Configuración de un evento: reglas, cupón y producto en 2x1."""

    nombre: str
    cupon: str
    producto_2x1: str
    reglas: tuple  # Tupla de Regla (inmutable).

    @classmethod
    def desde_dict(cls, datos):
        """Construye un Evento desde el diccionario del JSON."""
        reglas = tuple(  # Comprensión que crea objetos Regla.
            Regla(r["sku"], r["por_persona"], r["minimo"])
            for r in datos["reglas"]
        )
        return cls(datos["nombre"], datos["cupon"], datos["producto_2x1"], reglas)


# --- Estrategias de descuento (herencia y polimorfismo) ---

class Descuento(ABC):
    """Interfaz común: toda estrategia debe saber calcular un descuento."""

    @abstractmethod
    def calcular(self, items, evento, cupon):
        """Devuelve el monto de descuento (entero)."""
        raise NotImplementedError  # Obliga a las subclases a implementarlo.


class Descuento2x1(Descuento):
    """Descuento 2x1 sobre el producto configurado en el evento."""

    def calcular(self, items, evento, cupon):
        total = 0  # Acumulador local.
        for item in items:  # Polimorfismo: Item expone los mismos atributos.
            es_promo = item.sku == evento.producto_2x1
            es_sustituto = item.sustituto_de == evento.producto_2x1
            if es_promo or es_sustituto:  # Aplica también al sustituto.
                total += (item.cantidad // 2) * item.precio_unitario
        return total  # Cumple el contrato de Descuento.


class DescuentoPorcentaje(Descuento):
    """Descuento por cupón: porcentaje sobre la base ya descontada."""

    def __init__(self, porcentaje):
        self.porcentaje = porcentaje  # Estado interno encapsulado.

    def calcular(self, items, evento, cupon, base=0):
        # Firma extendida con `base`; se usa desde el carrito de forma explícita.
        if cupon != evento.cupon:  # Cupón incorrecto o ausente.
            return 0  # Sin descuento.
        return base * self.porcentaje // 100  # Entero, redondeo hacia abajo.


class Recomendador:
    """Encapsula la regla de sugerencias por similitud y festividad."""

    def __init__(self, catalogo):
        self.catalogo = catalogo  # Configuración de recomendaciones y productos.

    def sugerir_para(self, items, evento):
        """Devuelve sugerencias para las líneas ya armadas del carrito."""
        return sugerir(items, self.catalogo, evento)  # Delega en la función pura.


class PoliticaEnvio:
    """Define cuándo el envío es gratis."""

    def __init__(self, costo, gratis_desde):
        self.costo = costo  # Costo normal.
        self.gratis_desde = gratis_desde  # Umbral para envío gratis.

    def calcular(self, monto):
        """Devuelve el costo de envío según el monto después de descuentos."""
        return 0 if monto >= self.gratis_desde else self.costo


# --- Orquestación ---

class Carrito:
    """Coordina productos, reglas y descuentos para armar el carrito."""

    def __init__(self, evento, personas, catalogo, cupon=None):
        if personas <= 0:  # Validación de entrada.
            raise ValueError("personas debe ser mayor que cero")
        if evento not in catalogo["eventos"]:  # Validación de evento.
            raise ValueError(f"Evento desconocido: {evento}")

        self.evento = Evento.desde_dict(catalogo["eventos"][evento])  # Config.
        self.clave_evento = evento  # Clave exacta del JSON, para las sugerencias.
        self.personas = personas  # Cantidad de personas.
        self.productos = {  # Dict de objetos Producto.
            sku: Producto(p["sku"], p["nombre"], p["precio"], p["stock"])
            for sku, p in indice_productos(catalogo).items()
        }
        self.sustitutos = catalogo["sustitutos"]  # Mapa de reemplazos.
        self.cupon = cupon  # Cupón ingresado por el usuario.
        self.envio = PoliticaEnvio(  # Política de envío del catálogo.
            catalogo["envio"]["costo"], catalogo["envio"]["gratis_desde"]
        )
        self.descuentos = [Descuento2x1()]  # Estrategias polimórficas.
        self.recomendador = Recomendador(catalogo)  # Sugerencias personalizadas.

    def _resolver_regla(self, regla):
        """Aplica una regla; devuelve (item o None, faltante o None)."""
        producto = self.productos[regla.sku]  # Producto sugerido.
        cantidad = regla.cantidad_para(self.personas)  # Cantidad calculada.

        if cantidad <= producto.stock:  # Caso simple: hay stock.
            return producto.crear_item(cantidad), None

        # Sin stock suficiente: intenta sustituto.
        sku_alt = self.sustitutos.get(regla.sku)  # SKU alternativo.
        alternativo = self.productos.get(sku_alt)  # Objeto alternativo.
        if alternativo and alternativo.stock >= cantidad:  # El sustituto alcanza.
            return alternativo.crear_item(cantidad, regla.sku), None

        # No hay sustituto válido: se vende lo disponible y se reporta el falta.
        disponible = producto.stock
        item = producto.crear_item(disponible) if disponible > 0 else None
        faltante = {"sku": regla.sku, "cantidad": cantidad - disponible}
        return item, faltante

    def armar(self):
        """Ejecuta el algoritmo completo y devuelve el diccionario resultado."""
        items = []  # Lista mutable de objetos Item.
        faltantes = []  # Lista mutable de reportes de stock.

        for regla in self.evento.reglas:  # Iteración sobre reglas del evento.
            item, faltante = self._resolver_regla(regla)  # Delegación.
            if item is not None:  # Puede no haber item si stock = 0.
                items.append(item)  # Acumula el objeto.
            if faltante is not None:  # Puede no haber faltante.
                faltantes.append(faltante)  # Acumula el reporte.

        subtotal = sum(item.subtotal for item in items)  # Suma de líneas.

        # Polimorfismo: ambas estrategias responden a `calcular`.
        desc_2x1 = self.descuentos[0].calcular(items, self.evento, self.cupon)
        desc_cupon = DescuentoPorcentaje(10).calcular(
            items, self.evento, self.cupon, base=subtotal - desc_2x1
        )

        base = subtotal - desc_2x1 - desc_cupon  # Monto para evaluar envío.
        costo_envio = self.envio.calcular(base)  # Política de envío.
        total = base + costo_envio  # Total final.

        # El recomendador es un colaborador más del carrito, como la política de envío.
        items_dict = [item.como_dict() for item in items]
        recomendaciones = self.recomendador.sugerir_para(items_dict, self.clave_evento)

        return {  # Misma estructura que en el paradigma imperativo.
            "evento": self.evento.nombre.lower().replace(" ", "_"),
            "personas": self.personas,
            "items": items_dict,
            "faltantes": faltantes,
            "descuentos": {"2x1": desc_2x1, "cupon": desc_cupon},
            "envio": costo_envio,
            "total": total,
            "recomendaciones": recomendaciones,
        }


def armar_carrito(evento, personas, catalogo, cupon=None):
    """API pública equivalente a la de los otros dos módulos."""
    # El evento devuelto por la clase se normaliza al nombre de la clave JSON.
    carrito = Carrito(evento, personas, catalogo, cupon)
    resultado = carrito.armar()
    resultado["evento"] = evento  # Garantiza igualdad exacta entre versiones.
    return resultado
