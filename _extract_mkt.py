# Extrae imagenes de los PDFs y PPTX del material de Marketing UCES
import os, sys, zipfile, shutil

BASE = r"C:\Users\gerar\Downloads\Facultad Uces\1ER CUATR. _2026 - (892) MARKETING C29_2026068_0739"
OUT = r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\_img\marketing\_cand"
os.makedirs(OUT, exist_ok=True)

try:
    import fitz
except ImportError:
    print("NO_PYMUPDF"); sys.exit(1)

# 1. PDFs
n = 0
for root, dirs, files in os.walk(BASE):
    for fn in files:
        if not fn.lower().endswith(".pdf"):
            continue
        path = os.path.join(root, fn)
        tag = os.path.splitext(fn)[0][:40].replace(" ", "_")
        try:
            doc = fitz.open(path)
        except Exception as e:
            print("ERR", fn, e); continue
        seen = set()
        for pno in range(len(doc)):
            for img in doc.get_page_images(pno):
                xref = img[0]
                if xref in seen: continue
                seen.add(xref)
                try:
                    pix = fitz.Pixmap(doc, xref)
                    if pix.width < 200 or pix.height < 120:
                        continue
                    if pix.n - pix.alpha > 3:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    out = os.path.join(OUT, f"pdf_{tag}_p{pno+1:02d}_x{xref}.png")
                    pix.save(out)
                    n += 1
                except Exception as e:
                    print("imgerr", fn, xref, e)
        doc.close()
print("PDF images:", n)

# 2. PPTX (skip .ppt viejos)
m = 0
for root, dirs, files in os.walk(BASE):
    for fn in files:
        if not fn.lower().endswith(".pptx"):
            continue
        path = os.path.join(root, fn)
        tag = os.path.splitext(fn)[0][:40].replace(" ", "_")
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                if name.startswith("ppt/media/") and name.lower().endswith((".png",".jpg",".jpeg",".gif",".emf",".wmf")):
                    ext = os.path.splitext(name)[1]
                    if ext.lower() in (".emf",".wmf"):
                        continue
                    data = z.read(name)
                    if len(data) < 8000:
                        continue
                    out = os.path.join(OUT, f"pptx_{tag}_{os.path.basename(name)}")
                    with open(out, "wb") as f:
                        f.write(data)
                    m += 1
print("PPTX images:", m)

# 3. Imagenes sueltas
for rel in [r"Tema 1\Bibliografía obligatoria U1\las 4ps marketing mix.jpg",
            r"Tema 1\Bibliografía obligatoria U1\Mezcla de Comunicación.png"]:
    src = os.path.join(BASE, rel)
    if os.path.exists(src):
        shutil.copy(src, os.path.join(OUT, "suelta_" + os.path.basename(src).replace(" ", "_")))
        print("copiada:", rel)
    else:
        print("NO EXISTE:", rel)

# listado final con tamanos
for fn in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, fn)
    try:
        from PIL import Image
        with Image.open(p) as im:
            print(f"{os.path.getsize(p)//1024:5d}KB {im.width}x{im.height}  {fn}")
    except Exception as e:
        print(f"{os.path.getsize(p)//1024:5d}KB ???  {fn}  ({e})")
