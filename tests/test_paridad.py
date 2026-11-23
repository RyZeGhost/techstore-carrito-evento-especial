"""Pruebas automáticas: las tres versiones deben producir el mismo resultado."""

import unittest  # Biblioteca estándar de testing.

from carrito import (
    armar_funcional,
    armar_imperativo,
    armar_objetos,
    cargar_catalogo,
)
from carrito.datos import indice_productos

FUNCIONES = (armar_imperativo, armar_objetos, armar_funcional)


class TestParidad(unittest.TestCase):
    """Verifica comportamiento común y reglas de negocio."""

    def setUp(self):
        self.catalogo = cargar_catalogo()  # Catálogo fresco para cada prueba.

    def test_paridad_casos(self):
        """Para las mismas entradas, los tres resultados son idénticos."""
        casos = [
            ("cumpleanos", 10, "FIESTA10"),
            ("trabajo_remoto", 12, "HOME10"),
            ("vuelta_a_clases", 12, "ESCUELA10"),
            ("cumpleanos", 200, None),
            ("accesorios_basicos", 1, None),
        ]
        for evento, personas, cupon in casos:  # Recorre los casos.
            resultados = [
                funcion(evento, personas, self.catalogo, cupon)
                for funcion in FUNCIONES
            ]
            self.assertEqual(resultados[0], resultados[1])  # Imperativo == OOP.
            self.assertEqual(resultados[1], resultados[2])  # OOP == Funcional.

    def test_cupon_incorrecto_no_descuenta(self):
        """Un cupón ajeno al evento no genera descuento."""
        for funcion in FUNCIONES:  # Las tres implementaciones.
            resultado = funcion("cumpleanos", 10, self.catalogo, "INCORRECTO")
            self.assertEqual(resultado["descuentos"]["cupon"], 0)

    def test_envio_gratis_por_monto(self):
        """Un monto alto debe dejar el envío en cero."""
        for funcion in FUNCIONES:
            resultado = funcion("cumpleanos", 40, self.catalogo, "FIESTA10")
            self.assertEqual(resultado["envio"], 0)

    def test_envio_pagado_por_monto_bajo(self):
        """Un monto bajo debe cobrar el envío configurado."""
        for funcion in FUNCIONES:
            resultado = funcion("accesorios_basicos", 1, self.catalogo)
            self.assertEqual(resultado["envio"], 3990)

    def test_recomendaciones_en_festividad(self):
        """En eventos festivos se sugieren similares con descuento."""
        config = self.catalogo["recomendaciones"]
        for funcion in FUNCIONES:
            resultado = funcion("cumpleanos", 10, self.catalogo, "FIESTA10")
            recomendaciones = resultado["recomendaciones"]
            self.assertTrue(recomendaciones)
            self.assertLessEqual(len(recomendaciones), config["maximo"])

            productos = indice_productos(self.catalogo)
            categorias_carrito = {
                productos[item["sku"]]["categoria"] for item in resultado["items"]
            }
            skus_carrito = {item["sku"] for item in resultado["items"]}

            for recom in recomendaciones:
                self.assertIn(recom["categoria"], categorias_carrito)
                self.assertNotIn(recom["sku"], skus_carrito)
                self.assertEqual(recom["motivo"], "festividad")
                esperado = recom["precio"] * config["descuento_porcentaje"] // 100
                self.assertEqual(recom["descuento"], esperado)
                self.assertEqual(recom["precio_final"], recom["precio"] - esperado)

            # Las sugerencias son ofertas: no modifican el total del carrito.
            self.assertEqual(resultado["total"], 143028)

    def test_recomendaciones_sin_festividad(self):
        """Fuera de festividades se muestran similares sin descuento."""
        for funcion in FUNCIONES:
            resultado = funcion("trabajo_remoto", 12, self.catalogo, "HOME10")
            recomendaciones = resultado["recomendaciones"]
            self.assertTrue(recomendaciones)
            for recom in recomendaciones:
                self.assertEqual(recom["motivo"], "similar")
                self.assertEqual(recom["descuento"], 0)
                self.assertEqual(recom["precio_final"], recom["precio"])

    def test_segmentos_paridad_y_descuento(self):
        """Los tres segmentos descuentan según su porcentaje configurado."""
        invitado = FUNCIONES[0]("cumpleanos", 10, self.catalogo, "FIESTA10")
        base = invitado["total"] - invitado["envio"]  # Base sin segmento.
        for tipo, porcentaje in (("nuevo", 10), ("frecuente", 5), ("mayorista", 15)):
            resultados = [
                funcion("cumpleanos", 10, self.catalogo, "FIESTA10", tipo)
                for funcion in FUNCIONES
            ]
            self.assertEqual(resultados[0], resultados[1])  # Paridad.
            self.assertEqual(resultados[1], resultados[2])
            resultado = resultados[0]
            self.assertEqual(resultado["tipo_usuario"], tipo)
            esperado = base * porcentaje // 100
            self.assertEqual(resultado["descuentos"]["segmento"], esperado)
            self.assertEqual(resultado["total"], base - esperado + resultado["envio"])

    def test_segmento_envio_gratis(self):
        """Nuevo y mayorista no pagan envío; frecuente conserva la tarifa."""
        for tipo in ("nuevo", "mayorista"):
            resultado = FUNCIONES[0]("accesorios_basicos", 1, self.catalogo, None, tipo)
            self.assertEqual(resultado["envio"], 0)
            self.assertTrue(resultado["beneficios"]["envio_gratis"])
        frecuente = FUNCIONES[0]("accesorios_basicos", 1, self.catalogo, None, "frecuente")
        self.assertEqual(frecuente["envio"], 3990)
        self.assertFalse(frecuente["beneficios"]["envio_gratis"])

    def test_recomendaciones_por_segmento(self):
        """El perfil cambia el estilo de las recomendaciones."""
        por_tipo = {
            tipo: FUNCIONES[0]("cumpleanos", 10, self.catalogo, "FIESTA10", tipo)
            for tipo in (None, "nuevo", "frecuente", "mayorista")
        }
        self.assertEqual(por_tipo[None]["recomendaciones"][0]["perfil"], "invitado")
        for tipo in ("nuevo", "frecuente", "mayorista"):
            for recom in por_tipo[tipo]["recomendaciones"]:
                self.assertEqual(recom["perfil"], tipo)
        # 'economica' prioriza precio bajo; 'premium', precio alto.
        self.assertLessEqual(
            por_tipo["nuevo"]["recomendaciones"][0]["precio"],
            por_tipo["frecuente"]["recomendaciones"][0]["precio"],
        )

    def test_tipo_usuario_invalido(self):
        """Un tipo de usuario no configurado lanza ValueError."""
        for funcion in FUNCIONES:
            with self.assertRaises(ValueError):
                funcion("cumpleanos", 10, self.catalogo, None, "vip")

    def test_validaciones(self):
        """Entradas inválidas lanzan ValueError en las tres versiones."""
        for funcion in FUNCIONES:
            with self.assertRaises(ValueError):
                funcion("cumpleanos", 0, self.catalogo)
            with self.assertRaises(ValueError):
                funcion("evento_inexistente", 10, self.catalogo)


if __name__ == "__main__":
    unittest.main(verbosity=2)
