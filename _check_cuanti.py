"""Valida cuanti.html: emojis restantes, em dashes, paridad de tags y extrae el JS."""
import re, sys
from html.parser import HTMLParser
sys.stdout.reconfigure(encoding="utf-8")

txt = open(r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\cuanti.html", encoding="utf-8").read()

emo = re.compile(r'[\U0001F000-\U0001FAFF☀-➿️⃣]')
from collections import Counter
c = Counter(emo.findall(txt))
print("Emojis restantes:", {f"U+{ord(k):05X} {k}": v for k, v in c.items()})

print("Em dashes (—):", txt.count("—"))

VOID = {"meta", "br", "img", "input", "hr", "link", "polygon", "line", "circle", "path"}

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append((tag, self.getpos()))
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"cierre sin apertura: </{tag}> en {self.getpos()}")
            return
        t, pos = self.stack.pop()
        if t != tag:
            self.errors.append(f"esperaba </{t}> (abierto en {pos}) pero vino </{tag}> en {self.getpos()}")

p = P()
p.feed(txt)
p.close()
if p.stack:
    print("Tags sin cerrar:", [(t, pos) for t, pos in p.stack])
print("Errores de anidado:", p.errors if p.errors else "ninguno")

m = re.search(r"<script>(.*)</script>", txt, re.S)
open(r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\_js_check.js", "w", encoding="utf-8").write(m.group(1))
print("JS extraído:", len(m.group(1)), "chars")

# conteos
print("SVGs inline:", txt.count("<svg"))
print("Imgs data URI:", txt.count("src=\"data:image"))
print("Figures:", txt.count("<figure"))
