# -*- coding: utf-8 -*-
"""Extrae imagenes de los PDFs de teoria de Administracion UCES."""
import os, io, sys
import fitz
from PIL import Image

SRC = r"C:\Users\gerar\Downloads\Facultad Uces\1ER CUATR. _2026 - (886) ADMINISTRACIÓN C21, C45_2026068_0739"
OUT = r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\_img\administracion"
os.makedirs(OUT, exist_ok=True)

PDFS = [
    (r"Unidad 1 Introducción a la Administración\Teoría Unidad 1\concepto de administración.pdf", "u1concepto"),
    (r"Unidad 1 Introducción a la Administración\Teoría Unidad 1\continuación clases de planes.pdf", "u1planes"),
    (r"Unidad 1 Introducción a la Administración\Teoría Unidad 1\evolucion de las escuelas de administración.pdf", "u1escuelas"),
    (r"Unidad 1 Introducción a la Administración\Teoría Unidad 1\EXPERIMENTOS DE HAWTHORNE.pdf", "u1hawthorne"),
    (r"Unidad 1 Introducción a la Administración\Teoría Unidad 1\resumen escuelas de la administracion.pdf", "u1resumenesc"),
    (r"Unidad 1 Introducción a la Administración\Teoría Unidad 1\Unidad 1 - La Administración.pdf", "u1admin"),
    (r"Unidad 1 Introducción a la Administración\clase 2 (2024).pdf", "u1clase2"),
    (r"Unidad 2\Teoría Unidad 2\Unidad 2 - Las Organizaciones.pdf", "u2org"),
    (r"Unidad 2\clase 3 (2024).pdf", "u2clase3"),
    (r"Tema 3\Teoría Unidad 3 Las estructuras Orgánicas\principios de estructuras orgánicas.pdf", "u3principios"),
    (r"Tema 3\Teoría Unidad 3 Las estructuras Orgánicas\Teoría Centralización-descentralización.pdf", "u3central"),
    (r"Tema 3\Teoría Unidad 3 Las estructuras Orgánicas\Unidad 3 - Estructura Organizacional.pdf", "u3estructura"),
    (r"Tema 3\clase 4 (2023) Las Estructuras Orgánicas.pdf", "u3clase4"),
    (r"Tema 4\Teoría Unidad 4\Teoría Punto de Equilibrio.pdf", "u4pe"),
    (r"Tema 4\Teoría Unidad 4\Tipos de Puntos de equilibrios.pdf", "u4tipos"),
    (r"Tema 4\Teoría Unidad 4\Unidades 4 y 5 - Producción y Abastecimiento.pdf", "u45prod"),
    (r"Tema 4\clase 6 (2023) Funcion Producción y Punto de Equilibrio.pdf", "u4clase6"),
    (r"Tema 5\Unidad 5 funcion produccion teoria.pdf", "u5prod"),
    (r"Tema 5\Unidad 6 función personal teoria (1).pdf", "u6personal"),
]

MIN_W, MIN_H = 220, 160  # descartar iconitos y logos
count = 0
for rel, tag in PDFS:
    path = os.path.join(SRC, rel)
    if not os.path.exists(path):
        print("NO EXISTE:", rel); continue
    try:
        doc = fitz.open(path)
    except Exception as e:
        print("ERROR abriendo", rel, e); continue
    seen = set()
    for pno in range(len(doc)):
        for img in doc.get_page_images(pno, full=True):
            xref = img[0]
            if xref in seen: continue
            seen.add(xref)
            try:
                d = doc.extract_image(xref)
            except Exception:
                continue
            w, h = d.get("width", 0), d.get("height", 0)
            if w < MIN_W or h < MIN_H:
                continue
            try:
                im = Image.open(io.BytesIO(d["image"]))
                if im.mode in ("P", "RGBA", "LA", "CMYK"):
                    im = im.convert("RGB")
            except Exception:
                continue
            # descartar imagenes casi monocromas (fondos, banners lisos)
            small = im.resize((24, 24))
            px = list(small.convert("L").getdata())
            if max(px) - min(px) < 25:
                continue
            if im.width > 900:
                im = im.resize((900, int(im.height * 900 / im.width)), Image.LANCZOS)
            name = f"{tag}_p{pno+1:02d}_x{xref}.jpg"
            im.save(os.path.join(OUT, name), "JPEG", quality=78, optimize=True)
            kb = os.path.getsize(os.path.join(OUT, name)) // 1024
            print(f"{name}  {im.width}x{im.height}  {kb}KB")
            count += 1
    doc.close()
print("TOTAL:", count)
