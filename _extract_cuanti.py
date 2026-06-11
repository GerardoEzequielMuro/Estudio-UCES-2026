"""Extrae imagenes de los PDFs teoricos de Instrumentos Cuantitativos."""
import fitz, os, pathlib, sys
sys.stdout.reconfigure(encoding="utf-8")

base = r"C:\Users\gerar\Downloads\Facultad Uces\1ER CUATR. _2026 - (1399) INSTRUMENTOS CUANTITATIVOS C15, C16, C36, C49, C51_2026068_0739"
out = pathlib.Path(r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\_img\cuanti")
out.mkdir(parents=True, exist_ok=True)

pdfs = {
    "u1": os.path.join(base, "Unidad 1 Expresiones algebraicas", "Teoría Ecuaciones e Inecuaciones.pdf"),
    "u2": os.path.join(base, "Unidad 2 Funciones y sistemas de ecuaciones", "Material teórico U2 - Funciones y Sistemas.pdf"),
    "u3": os.path.join(base, "Unidad 3 Ecuaciones de segundo grado en una variable", "Material Teórico U3 - Ecuacione___undo Grado en una variable.pdf"),
    "u4": os.path.join(base, "Unidad 4 Función Cuadrática", "Función Cuadrática.pdf"),
    "u5a": os.path.join(base, "Unidad 5", "Apunte teórico Unidad 5.pdf"),
    "u5b": os.path.join(base, "Unidad 5", "Material Teórico Func. Logarítmica y Exponencial", "FuncExpLog.pdf"),
}

for tag, path in pdfs.items():
    if not os.path.exists(path):
        print("MISSING", tag, path)
        continue
    doc = fitz.open(path)
    seen = set()
    n = 0
    for pno in range(len(doc)):
        for img in doc.get_page_images(pno):
            xref = img[0]
            if xref in seen:
                continue
            seen.add(xref)
            try:
                d = doc.extract_image(xref)
            except Exception as e:
                print("ERR", tag, xref, e)
                continue
            w, h = d["width"], d["height"]
            if w < 120 or h < 80:
                continue
            fn = out / f"{tag}_p{pno+1:02d}_x{xref}_{w}x{h}.{d['ext']}"
            fn.write_bytes(d["image"])
            n += 1
    print(tag, f"pages={len(doc)}", f"saved={n}")
    doc.close()
