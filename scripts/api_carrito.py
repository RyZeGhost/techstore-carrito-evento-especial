"""API HTTP mínima para integrar el Carrito Evento Especial.

Usa solo la librería estándar de Python, por lo que no añade dependencias.

Endpoints:
    GET  /health     -> estado del servicio
    GET  /eventos    -> eventos disponibles y sus reglas
    GET  /segmentos  -> tipos de usuario y sus beneficios
    POST /carrito    -> calcula el carrito en uno o los tres paradigmas

Uso:
    python -m scripts.api_carrito
    # en otra terminal:
    curl http://127.0.0.1:8000/health
    curl -X POST http://127.0.0.1:8000/carrito \
      -H "Content-Type: application/json" \
      -d '{"evento":"cumpleanos","personas":10,"cupon":"FIESTA10","paradigma":"todos"}'
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from carrito import (  # noqa: E402
    armar_funcional,
    armar_imperativo,
    armar_objetos,
    cargar_catalogo,
)

FUNCIONES = {
    "imperativo": armar_imperativo,
    "orientado_objetos": armar_objetos,
    "funcional": armar_funcional,
}

CATALOGO = cargar_catalogo()


class ManejadorCarrito(BaseHTTPRequestHandler):
    """Maneja las peticiones HTTP y devuelve respuestas JSON."""

    def responder(self, codigo, cargo):
        """Serializa un diccionario a JSON y lo envía con el código dado."""
        cuerpo = json.dumps(cargo, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        """Devuelve el estado del servicio o la lista de eventos."""
        if self.path == "/health":
            self.responder(200, {"estado": "ok", "productos": len(CATALOGO["productos"])})
        elif self.path == "/eventos":
            self.responder(200, CATALOGO["eventos"])
        elif self.path == "/segmentos":
            self.responder(200, CATALOGO["segmentos"])
        else:
            self.responder(404, {"error": "Ruta no encontrada"})

    def do_POST(self):
        """Calcula el carrito con el paradigma solicitado."""
        if self.path != "/carrito":
            self.responder(404, {"error": "Ruta no encontrada"})
            return

        try:
            longitud = int(self.headers.get("Content-Length", 0))
            datos = json.loads(self.rfile.read(longitud) or b"{}")
            paradigma = datos.pop("paradigma", "todos")
            evento = datos.get("evento")
            personas = datos.get("personas")
            cupon = datos.get("cupon")
            tipo_usuario = datos.get("tipo_usuario")

            if paradigma != "todos" and paradigma not in FUNCIONES:
                self.responder(400, {"error": f"Paradigma desconocido: {paradigma}"})
                return

            nombres = FUNCIONES if paradigma == "todos" else {paradigma: FUNCIONES[paradigma]}
            resultados = {
                nombre: funcion(evento, personas, CATALOGO, cupon, tipo_usuario)
                for nombre, funcion in nombres.items()
            }
            self.responder(200, resultados)
        except (ValueError, TypeError, KeyError) as error:
            self.responder(400, {"error": str(error)})
        except Exception as error:  # noqa: BLE001 - la API debe responder siempre
            self.responder(500, {"error": str(error)})

    def log_message(self, formato, *args):
        """Imprime cada petición en la consola del servidor."""
        print(f"[API] {self.address_string()} - {formato % args}")


def main():
    """Arranca el servidor HTTP en el puerto configurado."""
    puerto = int(os.getenv("PUERTO_API", "8000"))
    servidor = HTTPServer(("127.0.0.1", puerto), ManejadorCarrito)
    print(f"API del carrito escuchando en http://127.0.0.1:{puerto}")
    print("  GET /health | GET /eventos | GET /segmentos | POST /carrito")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nAPI detenida")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
