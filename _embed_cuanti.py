"""Comprime con PIL y embebe las imagenes seleccionadas como data URI en cuanti.html."""
import base64, io, pathlib, sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")

src = pathlib.Path(r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\_img\cuanti")
html_path = pathlib.Path(r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\cuanti.html")

# tag -> (archivo, alt)
SEL = {
    "u2_p05": ("u2_p05_x65_357x221.jpeg", "Gráfico de función con un máximo en (b, f(b)) y un mínimo en (c, f(c)) para análisis completo"),
    "u2_p09": ("u2_p09_x106_313x294.png", "Haz de infinitas rectas que pasan por un punto P de coordenadas (x1, y1)"),
    "u2_p14": ("u2_p14_x157_406x460.png", "Dos rectas paralelas, y = menos 2x + 1 e y = menos 2x + 2: sistema incompatible"),
    "u2_p02": ("u2_p02_x48_331x348.jpeg", "Curva de demanda con pendiente negativa: precio 4 corresponde a cantidad 6, precio 2 a cantidad 10"),
    "u4_p02": ("u4_p02_x57_446x408.png", "Parábola con ordenada al origen c, su punto simétrico, eje de simetría y vértice V"),
    "u5a_p01": ("u5a_p01_x36_268x399.png", "Función exponencial creciente y = 2 a la x, pasa por el punto (0, 1)"),
    "u5a_p02": ("u5a_p02_x41_303x409.png", "Función exponencial decreciente y = un medio a la x, pasa por el punto (0, 1)"),
    "u5a_p05": ("u5a_p05_x58_369x403.png", "Función logarítmica y = logaritmo en base 2 de x, pasa por (1, 0) con asíntota vertical en x = 0"),
    "u5a_p07": ("u5a_p07_x65_447x464.png", "Funciones inversas: exponencial de base un medio y logaritmo de base un medio, simétricas respecto de la recta y = x"),
}

MAX_W = 900
total = 0
uris = {}
for tag, (fn, alt) in SEL.items():
    p = src / fn
    im = Image.open(p)
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    if p.suffix.lower() in (".jpg", ".jpeg"):
        im.convert("RGB").save(buf, "JPEG", quality=82, optimize=True)
        mime = "image/jpeg"
    else:
        # line-art: paleta de 64 colores + PNG optimizado
        im2 = im.convert("RGB").quantize(colors=64, method=Image.MEDIANCUT)
        buf2 = io.BytesIO()
        im2.save(buf2, "PNG", optimize=True)
        im.save(buf, "PNG", optimize=True)
        if buf2.tell() < buf.tell():
            buf = buf2
        mime = "image/png"
    raw = buf.getvalue()
    b64 = base64.b64encode(raw).decode()
    total += len(b64)
    uris[tag] = f'<img alt="{alt}" loading="lazy" src="data:{mime};base64,{b64}">'
    print(f"{tag}: {len(raw)/1024:.1f} KB raw, {len(b64)/1024:.1f} KB base64")

print(f"TOTAL base64: {total/1024:.1f} KB")
assert total < 2 * 1024 * 1024, "supera el tope de 2MB"

html = html_path.read_text(encoding="utf-8")
missing = []
for tag, img in uris.items():
    ph = f"<!--IMG:{tag}-->"
    if ph not in html:
        missing.append(tag)
        continue
    html = html.replace(ph, img)
if missing:
    print("PLACEHOLDERS FALTANTES:", missing)
    sys.exit(1)
if "<!--IMG:" in html:
    print("QUEDARON PLACEHOLDERS SIN REEMPLAZAR")
    sys.exit(1)
html_path.write_text(html, encoding="utf-8")
print("OK, archivo final:", f"{html_path.stat().st_size/1024:.1f} KB")
