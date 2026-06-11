# -*- coding: utf-8 -*-
"""Renderiza paginas de PDFs vectoriales como contact sheet."""
import os, math
import fitz
from PIL import Image, ImageDraw

SRC = r"C:\Users\gerar\Downloads\Facultad Uces\1ER CUATR. _2026 - (886) ADMINISTRACIÓN C21, C45_2026068_0739"
OUT = r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\_img\administracion\_sheets"
PDFS = [
    (r"Tema 3\clase 4 (2023) Las Estructuras Orgánicas.pdf", "r_u3clase4"),
    (r"Unidad 1 Introducción a la Administración\clase 2 (2024).pdf", "r_u1clase2"),
    (r"Tema 4\Teoría Unidad 4\Teoría Punto de Equilibrio.pdf", "r_u4pe"),
    (r"Tema 4\Teoría Unidad 4\Tipos de Puntos de equilibrios.pdf", "r_u4tipos"),
    (r"Tema 4\clase 6 (2023) Funcion Producción y Punto de Equilibrio.pdf", "r_u4clase6"),
    (r"Unidad 2\clase 3 (2024).pdf", "r_u2clase3"),
]
TH_W, TH_H, COLS = 240, 190, 5
thumbs = []
for rel, tag in PDFS:
    doc = fitz.open(os.path.join(SRC, rel))
    for pno in range(len(doc)):
        pix = doc[pno].get_pixmap(dpi=40)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        im.thumbnail((TH_W-6, TH_H-20))
        thumbs.append((f"{tag}_p{pno+1:02d}", im))
    doc.close()
rows = math.ceil(len(thumbs)/COLS)
sheet = Image.new("RGB", (COLS*TH_W, rows*TH_H), "white")
d = ImageDraw.Draw(sheet)
for i, (name, im) in enumerate(thumbs):
    x = (i % COLS)*TH_W; y = (i//COLS)*TH_H
    sheet.paste(im, (x+3, y+3))
    d.text((x+3, y+TH_H-14), name, fill="black")
sheet.save(os.path.join(OUT, "render_sheet.jpg"), "JPEG", quality=70)
print("OK", len(thumbs))
