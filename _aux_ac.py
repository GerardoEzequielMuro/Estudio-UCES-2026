# -*- coding: utf-8 -*-
import zipfile, re, glob, os, struct, html

BASE = r"C:\Users\gerar\Downloads\Facultad Uces\1ER CUATR. _2026 - (390) ANÁLISIS CONCEPTUAL C13_2026068_0739"
OUT = r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\_extract"

# 1) programa docx -> txt
f = glob.glob(os.path.join(BASE, 'Tema 0', '*.docx'))[0]
z = zipfile.ZipFile(f)
xml = z.read('word/document.xml').decode('utf8')
text = re.sub(r'<w:p[ >]', '\n<', xml)
text = re.sub(r'<[^>]+>', '', text)
text = html.unescape(text)
text = re.sub(r'\n{3,}', '\n\n', text)
with open(os.path.join(OUT, 'ac_programa.txt'), 'w', encoding='utf8') as fh:
    fh.write(text)
print('programa chars:', len(text))

# 2) png dims
for p in sorted(glob.glob(r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\_scans\*.png"))[:6]:
    with open(p, 'rb') as fh:
        d = fh.read(33)
    w, h = struct.unpack('>II', d[16:24])
    print(os.path.basename(p), w, h)
