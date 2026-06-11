"""Genera planchas de contacto con nombres de archivo para revisar candidatas."""
import pathlib, math
from PIL import Image, ImageDraw

src = pathlib.Path(r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\_img\cuanti")
files = sorted(p for p in src.iterdir() if p.suffix.lower() in (".png", ".jpeg", ".jpg"))
COLS, TH = 4, 260
PER_SHEET = 12
for s in range(math.ceil(len(files) / PER_SHEET)):
    batch = files[s * PER_SHEET:(s + 1) * PER_SHEET]
    rows = math.ceil(len(batch) / COLS)
    cw, ch = 330, TH + 34
    sheet = Image.new("RGB", (COLS * cw, rows * ch), "white")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(batch):
        im = Image.open(f).convert("RGB")
        im.thumbnail((cw - 14, TH))
        x, y = (i % COLS) * cw, (i // COLS) * ch
        sheet.paste(im, (x + 7, y + 4))
        d.text((x + 7, y + TH + 8), f.name, fill="black")
        d.rectangle([x, y, x + cw - 1, y + ch - 1], outline="#bbb")
    out = src / f"_sheet{s+1}.png"
    sheet.save(out)
    print(out, len(batch))
