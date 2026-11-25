"""Genera imágenes de catálogo limpias: solo el producto sobre fondo blanco.

Las ilustraciones se dibujan con Pillow en 800x800 y se guardan en
`datos/imagenes/<SKU>.png`. Son consistentes entre sí, no muestran personas,
manos, mesas ni objetos usados, y pueden republicarse en Shopify con
`scripts/actualizar_imagenes.py`.

Uso:
    python -m scripts.generar_imagenes_producto
    python -m scripts.generar_imagenes_producto --sku AURICULARES
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
CATALOGO = RAIZ / "datos" / "catalogo.json"
SALIDA = RAIZ / "datos" / "imagenes"

LADO = 800
K = 3
SZ = LADO * K

OSCURO = "#1f2937"
MEDIO = "#64748b"
CLARO = "#e2e8f0"
AZUL = "#0ea5e9"
AZUL_OSCURO = "#2563eb"
BLANCO = "#ffffff"
DORADO = "#d4a853"
VERDE = "#22c55e"


def e(valor):
    """Escala una coordenada del espacio 800x800 al lienzo de alta resolución."""
    return int(round(valor * K))


def xy(*valores):
    return tuple(e(v) for v in valores)


def caja(d, box, radio=0, relleno=None, borde=None, ancho=1):
    args = {"fill": relleno}
    if borde:
        args.update(outline=borde, width=e(ancho))
    if radio:
        d.rounded_rectangle(xy(*box), radius=e(radio), **args)
    else:
        d.rectangle(xy(*box), **args)


def ovalo(d, box, relleno=None, borde=None, ancho=1):
    args = {"fill": relleno}
    if borde:
        args.update(outline=borde, width=e(ancho))
    d.ellipse(xy(*box), **args)


def linea(d, puntos, relleno, ancho=6):
    d.line([xy(*p) for p in puntos], fill=relleno, width=e(ancho), joint="curve")


def poligono(d, puntos, relleno):
    d.polygon([xy(*p) for p in puntos], fill=relleno)


def arco(d, box, inicio, fin, relleno, ancho=10):
    d.arc(xy(*box), inicio, fin, fill=relleno, width=e(ancho))


def sombra(img, box=(190, 650, 610, 710), opacidad=45):
    capa = Image.new("RGBA", (SZ, SZ), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.ellipse(xy(*box), fill=(15, 23, 42, opacidad))
    capa = capa.filter(ImageFilter.GaussianBlur(e(18)))
    img.alpha_composite(capa)


def nuevo_lienzo():
    img = Image.new("RGBA", (SZ, SZ), BLANCO)
    sombra(img)
    return img, ImageDraw.Draw(img)


def rejilla(d, x0, y0, columnas, filas, paso=32, tam=20, color=MEDIO):
    for fila in range(filas):
        for col in range(columnas):
            x = x0 + col * paso
            y = y0 + fila * paso
            caja(d, (x, y, x + tam, y + tam), 4, color)


def auriculares(d, pro=False):
    tono = AZUL_OSCURO if pro else OSCURO
    arco(d, (190, 180, 610, 620), 180, 360, tono, 34)
    arco(d, (230, 220, 570, 580), 180, 360, CLARO, 8)
    for x in (140, 520):
        caja(d, (x, 370, x + 140, 570), 48, tono)
        ovalo(d, (x + 28, 400, x + 112, 540), CLARO)
        ovalo(d, (x + 45, 417, x + 95, 523), tono)
        caja(d, (x + 52, 440, x + 88, 500), 12, AZUL)
    if pro:
        arco(d, (300, 250, 500, 450), 200, 340, AZUL, 8)


def parlante(d, pro=False):
    tono = OSCURO if not pro else "#334155"
    caja(d, (160, 300, 640, 530), 46, tono)
    for x in range(210, 600, 34):
        for y in range(345, 495, 32):
            ovalo(d, (x, y, x + 9, y + 9), "#475569")
    ovalo(d, (540, 390, 570, 420), AZUL if not pro else VERDE)
    if pro:
        for x in (185, 600):
            caja(d, (x, 310, x + 22, 520), 10, MEDIO)
        poligono(d, ((430, 250), (450, 220), (470, 250), (450, 280)), AZUL)


def cable(d, tipo="hdmi"):
    color = OSCURO if tipo == "hdmi" else MEDIO
    linea(d, [(520, 560), (430, 520), (300, 540), (210, 470)], color, 16)
    if tipo == "hdmi":
        poligono(d, ((170, 430), (260, 450), (235, 505), (145, 485)), color)
        poligono(d, ((160, 438), (235, 455), (225, 480), (150, 463)), CLARO)
    else:
        caja(d, (140, 420, 250, 485), 18, color)
        caja(d, (155, 435, 235, 470), 8, CLARO)


def cargador(d, inalámbrico=False):
    if inalámbrico:
        ovalo(d, (190, 360, 610, 590), CLARO, OSCURO, 10)
        ovalo(d, (250, 410, 550, 550), BLANCO, AZUL, 8)
        caja(d, (290, 210, 510, 430), 28, "#0f172a")
        caja(d, (320, 240, 480, 390), 12, AZUL_OSCURO)
        return
    caja(d, (270, 300, 530, 540), 34, OSCURO)
    caja(d, (330, 380, 470, 450), 12, CLARO)
    caja(d, (355, 398, 445, 432), 6, AZUL)
    for x in (330, 440):
        caja(d, (x, 250, x + 30, 310), 5, MEDIO)


def soporte(d):
    poligono(d, ((160, 520), (640, 520), (580, 590), (220, 590)), MEDIO)
    poligono(d, ((220, 250), (610, 250), (580, 500), (250, 500)), "#0f172a")
    caja(d, (250, 280, 580, 470), 8, AZUL_OSCURO)
    linea(d, [(160, 600), (640, 600)], OSCURO, 10)


def powerbank(d):
    caja(d, (230, 260, 570, 570), 36, OSCURO)
    caja(d, (270, 300, 530, 520), 20, "#334155")
    for x in (310, 375, 440, 505):
        ovalo(d, (x, 470, x + 30, 500), VERDE)
    caja(d, (300, 340, 500, 385), 10, CLARO)
    caja(d, (330, 350, 470, 375), 5, AZUL)


def mouse(d):
    ovalo(d, (285, 230, 515, 580), OSCURO)
    linea(d, [(400, 240), (400, 360)], "#475569", 6)
    caja(d, (385, 285, 415, 350), 14, AZUL)
    ovalo(d, (330, 300, 390, 390), "#334155")
    ovalo(d, (410, 300, 470, 390), "#334155")


def teclado(d):
    caja(d, (110, 300, 690, 530), 24, "#334155")
    rejilla(d, 145, 335, 16, 5, paso=32, tam=23, color="#0f172a")
    caja(d, (280, 500, 520, 520), 6, AZUL)


def webcam(d):
    caja(d, (250, 270, 550, 470), 44, OSCURO)
    ovalo(d, (330, 310, 470, 450), CLARO)
    ovalo(d, (360, 340, 440, 420), AZUL_OSCURO)
    caja(d, (370, 470, 430, 540), 8, MEDIO)
    caja(d, (300, 540, 500, 575), 12, OSCURO)


def trackpad(d):
    caja(d, (170, 320, 630, 520), 24, "#e2e8f0", OSCURO, 8)
    caja(d, (210, 350, 590, 490), 14, BLANCO, MEDIO, 4)
    linea(d, [(400, 350), (400, 490)], CLARO, 4)


def ssd(d, pequeno=False):
    ancho = 420 if pequeno else 500
    x0 = (800 - ancho) // 2
    caja(d, (x0, 340, x0 + ancho, 460), 10, "#0f172a")
    for dx in (60, 170, 280):
        caja(d, (x0 + dx, 365, x0 + dx + 80, 435), 5, MEDIO)
    for x in range(x0 + 20, x0 + ancho - 20, 22):
        caja(d, (x, 455, x + 12, 475), 2, DORADO)


def disco_externo(d):
    caja(d, (210, 320, 590, 510), 22, MEDIO)
    caja(d, (240, 350, 560, 480), 10, CLARO)
    ovalo(d, (500, 390, 540, 430), AZUL)
    caja(d, (280, 520, 520, 545), 8, OSCURO)


def tarjeta_memoria(d):
    poligono(d, ((260, 250), (520, 250), (560, 290), (560, 550), (260, 550)), AZUL_OSCURO)
    poligono(d, ((260, 250), (520, 250), (560, 290), (300, 290)), AZUL)
    for x in (310, 360, 410, 460):
        caja(d, (x, 190, x + 26, 250), 4, DORADO)
    caja(d, (300, 360, 500, 400), 6, CLARO)


def monitor(d, grande=False):
    ancho = 560 if grande else 500
    x0 = (800 - ancho) // 2
    caja(d, (x0, 190, x0 + ancho, 520), 18, OSCURO)
    caja(d, (x0 + 25, 215, x0 + ancho - 25, 490), 8, AZUL_OSCURO)
    caja(d, (385, 520, 415, 610), 5, MEDIO)
    caja(d, (300, 610, 500, 640), 12, OSCURO)


def proyector(d):
    caja(d, (200, 330, 560, 520), 28, OSCURO)
    ovalo(d, (480, 370, 550, 440), CLARO)
    ovalo(d, (505, 395, 535, 425), AZUL)
    poligono(d, ((555, 390), (700, 330), (700, 470), (555, 420)), "#bae6fd")
    caja(d, (250, 530, 320, 560), 6, MEDIO)
    caja(d, (440, 530, 510, 560), 6, MEDIO)


def notebook(d):
    caja(d, (180, 210, 620, 520), 18, OSCURO)
    caja(d, (205, 235, 595, 495), 8, AZUL_OSCURO)
    ovalo(d, (392, 240, 408, 256), VERDE)
    poligono(d, ((130, 535), (670, 535), (620, 590), (180, 590)), MEDIO)
    caja(d, (330, 550, 470, 568), 6, CLARO)


def tablet(d):
    caja(d, (250, 160, 550, 600), 30, OSCURO)
    caja(d, (275, 190, 525, 570), 14, AZUL_OSCURO)
    ovalo(d, (385, 170, 415, 200), MEDIO)
    linea(d, [(600, 240), (650, 520)], MEDIO, 14)
    ovalo(d, (585, 210, 615, 250), CLARO)


def minipc(d):
    caja(d, (240, 320, 560, 530), 18, OSCURO)
    caja(d, (270, 350, 530, 500), 8, "#334155")
    ovalo(d, (500, 400, 520, 420), VERDE)
    for x in (300, 340, 380):
        caja(d, (x, 455, x + 22, 475), 3, MEDIO)
    caja(d, (330, 540, 470, 560), 6, MEDIO)


def router(d, repetidor=False):
    caja(d, (180, 430, 620, 560), 22, OSCURO)
    for x in (230, 570):
        linea(d, [(x, 430), (x - 25, 260)], MEDIO, 10)
    for x in (300, 360, 420):
        ovalo(d, (x, 480, x + 22, 502), VERDE if x == 300 else AZUL)
    if repetidor:
        arco(d, (320, 280, 480, 440), 200, 340, AZUL, 10)
        arco(d, (290, 250, 510, 470), 200, 340, AZUL_OSCURO, 8)


def microfono(d):
    ovalo(d, (320, 180, 480, 420), OSCURO)
    for y in range(220, 400, 28):
        linea(d, [(340, y), (460, y)], "#475569", 5)
    caja(d, (385, 410, 415, 570), 8, MEDIO)
    ovalo(d, (300, 570, 500, 610), OSCURO)


def auriculares_deportivos(d):
    for x in (240, 480):
        ovalo(d, (x, 280, x + 80, 380), OSCURO)
        ovalo(d, (x + 18, 298, x + 62, 342), AZUL)
        caja(d, (x + 30, 370, x + 50, 470), 8, OSCURO)
    linea(d, [(260, 465), (340, 560), (440, 560), (520, 465)], MEDIO, 10)


def funda_notebook(d):
    caja(d, (190, 240, 610, 560), 28, "#334155")
    caja(d, (225, 275, 575, 520), 18, OSCURO)
    linea(d, [(225, 300), (575, 300)], DORADO, 6)
    caja(d, (350, 390, 450, 420), 8, AZUL)


def mochila(d):
    caja(d, (260, 220, 540, 580), 60, OSCURO)
    arco(d, (310, 160, 490, 320), 180, 360, MEDIO, 18)
    caja(d, (300, 400, 500, 500), 20, "#334155")
    caja(d, (350, 420, 450, 455), 8, AZUL)
    linea(d, [(280, 260), (230, 520)], MEDIO, 12)
    linea(d, [(520, 260), (570, 520)], MEDIO, 12)


def hub_usb(d):
    caja(d, (200, 350, 600, 490), 24, OSCURO)
    for x in (250, 330, 410):
        caja(d, (x, 385, x + 55, 425), 6, CLARO)
    caja(d, (500, 380, 570, 430), 8, AZUL)
    linea(d, [(600, 420), (690, 420)], MEDIO, 12)


def adaptador(d):
    caja(d, (250, 340, 500, 470), 22, OSCURO)
    caja(d, (280, 370, 380, 440), 8, CLARO)
    caja(d, (500, 375, 600, 435), 8, MEDIO)
    caja(d, (610, 385, 680, 425), 5, DORADO)


def protector(d):
    caja(d, (280, 180, 520, 610), 40, OSCURO)
    caja(d, (295, 205, 505, 580), 30, "#bae6fd")
    caja(d, (310, 220, 490, 565), 24, BLANCO)
    ovalo(d, (380, 195, 420, 235), MEDIO)


def lapiz_tactil(d):
    linea(d, [(250, 600), (550, 220)], OSCURO, 30)
    poligono(d, ((540, 230), (580, 190), (600, 215), (560, 255)), MEDIO)
    caja(d, (245, 570, 285, 620), 10, AZUL)


DIBUJOS = {
    "AURICULARES": auriculares,
    "AURICULARES-PRO": lambda d: auriculares(d, pro=True),
    "PARLANTE": parlante,
    "PARLANTE-PRO": lambda d: parlante(d, pro=True),
    "MICROFONO-USB": microfono,
    "AURICULARES-DEPORTIVOS": auriculares_deportivos,
    "CABLE-HDMI": lambda d: cable(d, "hdmi"),
    "CABLE-USB": lambda d: cable(d, "usb"),
    "CARGADOR": cargador,
    "SOPORTE": soporte,
    "ADAPTADOR": adaptador,
    "PROTECTOR": protector,
    "LAPIZ-TACTIL": lapiz_tactil,
    "FUNDANOTEBOOK": funda_notebook,
    "MOCHILA-TECH": mochila,
    "HUB-USB": hub_usb,
    "POWERBANK": powerbank,
    "CARGADOR-WIRELESS": lambda d: cargador(d, inalámbrico=True),
    "MOUSE": mouse,
    "TECLADO": teclado,
    "WEBCAM": webcam,
    "TRACKPAD": trackpad,
    "SSD": ssd,
    "SSD-512": lambda d: ssd(d, pequeno=True),
    "DISCO-EXTERNO": disco_externo,
    "TARJETA-MEMORIA": tarjeta_memoria,
    "MONITOR": monitor,
    "MONITOR-27": lambda d: monitor(d, grande=True),
    "PROYECTOR": proyector,
    "NOTEBOOK": notebook,
    "TABLET": tablet,
    "MINIPC": minipc,
    "ROUTER": router,
    "REPETIDOR-WIFI": lambda d: router(d, repetidor=True),
}


def generar(sku):
    """Genera un PNG para un SKU y devuelve la ruta."""
    if sku not in DIBUJOS:
        raise ValueError(f"No hay dibujo definido para {sku}")
    img, d = nuevo_lienzo()
    DIBUJOS[sku](d)
    SALIDA.mkdir(parents=True, exist_ok=True)
    ruta = SALIDA / f"{sku}.png"
    img.convert("RGB").resize((LADO, LADO), Image.Resampling.LANCZOS).save(ruta)
    return ruta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sku", help="genera solo un SKU")
    args = parser.parse_args()

    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))
    skus = [args.sku] if args.sku else [p["sku"] for p in catalogo["productos"]]
    faltantes = [sku for sku in skus if sku not in DIBUJOS]
    if faltantes:
        raise SystemExit(f"Faltan dibujos para: {faltantes}")

    for sku in skus:
        ruta = generar(sku)
        print(f"  Generada {ruta.relative_to(RAIZ)}")
    print(f"Imágenes generadas: {len(skus)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
