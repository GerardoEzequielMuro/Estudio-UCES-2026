# Comprime las imagenes elegidas del material de Marketing y las embebe
# como data URI en marketing.html (reemplaza los placeholders <!--IMG:xxx-->)
import os, base64
from PIL import Image

ROOT = r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES"
CAND = os.path.join(ROOT, "_img", "marketing", "_cand")
OUT = os.path.join(ROOT, "_img", "marketing")
HTML = os.path.join(ROOT, "marketing.html")

# (placeholder, archivo candidato, nombre final, caption)
SEL = [
    ("holistico", "pdf_Bibliografía_Complementaria_-_Marketing__p07_x210.png", "u1_marketing_holistico.jpg",
     "El marketing holístico de Kotler y Keller: interno, integrado, de relaciones y rendimiento. Fuente: Bibliografía complementaria, Marketing 1.0 al 5.0 (U1)."),
    ("doscaras", "pdf_UNIDAD_2_-_Marketing_Estratégico_y_Opera_p01_x94.png", "u2_dos_caras_lambin.jpg",
     "Figura 1.1, las dos caras del marketing: estratégico (análisis) y operativo (acción). Fuente: Lambin, cap. 1, bibliografía obligatoria U2."),
    ("decision", "pptx_UNIDAD_5_-_Motivaciones_y_Compo___Consum_image20.png", "u5_proceso_decision.jpg",
     "Las cinco etapas del proceso de decisión del comprador. Fuente: presentación de cátedra, Motivaciones y Comportamiento del Consumidor (U5)."),
    ("maslow", "pdf_Unidad_5_-_Apunte_de_cátedra_p06_x49.png", "u5_piramide_maslow.jpg",
     "La pirámide de necesidades de Maslow, de las más urgentes (base) a las menos urgentes (cima). Fuente: apunte de cátedra, Unidad 5."),
    ("niveles", "pdf_Unidad_8_-_Apunte_de_Cátedra_-_Marketing_p02_x28.png", "u8_niveles_producto.jpg",
     "Los tres niveles del producto: valor esencial para el cliente, producto real y producto aumentado. Fuente: apunte de cátedra, Unidad 8."),
    ("mezcla", "suelta_Mezcla_de_Comunicación.png", "u8_mezcla_comunicacion.jpg",
     "La mezcla de comunicaciones de marketing: publicidad, ventas personales, promoción de ventas, relaciones públicas y marketing directo. Fuente: material de cátedra, Unidad 1."),
]

with open(HTML, encoding="utf-8") as f:
    html = f.read()

total = 0
for key, cand, final, caption in SEL:
    src = os.path.join(CAND, cand)
    im = Image.open(src)
    if im.mode in ("RGBA", "P", "LA"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        im2 = im.convert("RGBA")
        bg.paste(im2, mask=im2.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    if im.width > 900:
        h = round(im.height * 900 / im.width)
        im = im.resize((900, h), Image.LANCZOS)
    dst = os.path.join(OUT, final)
    im.save(dst, "JPEG", quality=80, optimize=True)
    size = os.path.getsize(dst)
    total += size
    with open(dst, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    fig = ('<figure class="fig"><img src="data:image/jpeg;base64,' + b64 +
           '" alt="' + caption.split(". Fuente")[0] + '" loading="lazy">' +
           '<figcaption>' + caption + '</figcaption></figure>')
    ph = "<!--IMG:" + key + "-->"
    if ph not in html:
        print("PLACEHOLDER FALTANTE:", ph)
        continue
    html = html.replace(ph, fig)
    print(f"{final}: {size//1024}KB ({im.width}x{im.height})")

with open(HTML, "w", encoding="utf-8") as f:
    f.write(html)

print("Total imagenes:", total // 1024, "KB")
print("HTML final:", os.path.getsize(HTML) // 1024, "KB")
