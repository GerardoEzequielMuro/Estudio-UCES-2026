# -*- coding: utf-8 -*-
"""Arma contact sheets de las imagenes extraidas para revisarlas rapido."""
import os, math
from PIL import Image, ImageDraw

IMG = r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\_img\administracion"
OUT = r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\_img\administracion\_sheets"
os.makedirs(OUT, exist_ok=True)

files = sorted(f for f in os.listdir(IMG) if f.endswith(".jpg"))
TH_W, TH_H, COLS = 230, 330, 6
PER = 24

for si in range(0, len(files), PER):
    chunk = files[si:si+PER]
    rows = math.ceil(len(chunk) / COLS)
    sheet = Image.new("RGB", (COLS*TH_W, rows*(TH_H+18)), "white")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(chunk):
        im = Image.open(os.path.join(IMG, f))
        im.thumbnail((TH_W-8, TH_H-8))
        x = (i % COLS)*TH_W; y = (i // COLS)*(TH_H+18)
        sheet.paste(im, (x+4, y+4))
        d.text((x+4, y+TH_H+2), f[:38], fill="black")
    name = os.path.join(OUT, f"sheet_{si//PER:02d}.jpg")
    sheet.save(name, "JPEG", quality=70)
    print(name, len(chunk))
