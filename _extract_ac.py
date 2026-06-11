# -*- coding: utf-8 -*-
import fitz, os

BASE = r"C:\Users\gerar\Downloads\Facultad Uces\1ER CUATR. _2026 - (390) ANÁLISIS CONCEPTUAL C13_2026068_0739"
OUT = r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES\_extract"
files = {
    "ac_u1_lenguaje_humaniza": r"Tema 1\Bibliografía obligatoria U1\Artículo Periodístico - El lenguaje nos humaniza .pdf",
    "ac_u1_bajtin_problema": r"Tema 1\Bibliografía obligatoria U1\Bajtín, Mijaíl. El problema de los géneros discursivos.pdf",
    "ac_u1_bajtin_generos": r"Tema 1\Bibliografía obligatoria U1\Batjín, Mijaíl. Géneros discursivos .pdf",
    "ac_u1_funciones_actividad": r"Tema 1\Bibliografía obligatoria U1\Funciones del lenguaje. Actividad.pdf",
    "ac_u1_saussure": r"Tema 1\Bibliografía obligatoria U1\Saussure, F. Objetivo de la Lingúistica.pdf",
    "ac_u1_quino_wolton": r"Tema 1\Bibliografía obligatoria U1\Viñetas de Quino - Texto de Dominique Wolton .pdf",
    "ac_u1_pres_funciones": r"Tema 1\Presentaciones U1\Funciones del lenguaje - Análisis Conceptual.pdf",
    "ac_u2_actividad_textos": r"Tema 2\Bibliografía obligatoria U2\Actividad para trabajar textos, soporte, portador y formato .pdf",
    "ac_u2_bonorino_cap7": r"Tema 2\Bibliografía obligatoria U2\Bonorino y Cuñarro - Capítulo 7 - Lengua, léxico y gramática.pdf",
    "ac_u2_vandendorpe": r"Tema 2\Bibliografía obligatoria U2\C. Vandendorpe - Del papiro al hipertexto.pdf",
    "ac_u2_cassany": r"Tema 2\Bibliografía obligatoria U2\D. Cassany - Tras las líneas.pdf",
    "ac_u2_pagani_cap5": r"Tema 2\Bibliografía obligatoria U2\G. Pagani - Capítulo 5 - Lengua, léxico y gramática.pdf",
    "ac_u2_marin_cap4": r"Tema 2\Bibliografía obligatoria U2\Marín, Marta. - Capítulo 4 - Li___ y enseñanza de la lengua-.pdf",
    "ac_u2_pres_textos": r"Tema 2\Presentaciones U2\Análisis Conceptual - Textos.pdf",
    "ac_u2_pres_macro": r"Tema 2\Presentaciones U2\Macroestructura y macrorreglas - Análisis Conceptual.pdf",
    "ac_u3_actividad_coherencia": r"Tema 3\Bibliografía obligatoria U3\Actividad coherencia y cohesión .pdf",
    "ac_u3_cap5": r"Tema 3\Bibliografía obligatoria U3\Capítulo 5. Lengua, léxico, gramática y texto.pdf",
    "ac_u3_cap7": r"Tema 3\Bibliografía obligatoria U3\Capítulo 7. Lengua, léxico, gramática y texto.pdf",
    "ac_u3_enunciacion_textos": r"Tema 3\Bibliografía obligatoria U3\La enunciación-textos-1.pdf",
    "ac_u3_secuencias_teoria": r"Tema 3\Bibliografía obligatoria U3\Secuencias Textuales - Teoría.pdf",
    "ac_u3_teoria_enunciacion": r"Tema 3\Bibliografía obligatoria U3\Teoría de la Enunciación.pdf",
    "ac_u3_textos_actividad_sec": r"Tema 3\Bibliografía obligatoria U3\Textos Actividad Secuencias Textuales .pdf",
    "ac_u3_pres_coherencia": r"Tema 3\Presentaciones U3\Coherencia textual - Análisis Conceptual.pdf",
    "ac_u3_pres_secuencias": r"Tema 3\Presentaciones U3\Secuencias textuales - Análisis Conceptual.pdf",
}

# glob fix for the truncated marin cap4 filename
import glob as g
marin4 = g.glob(os.path.join(BASE, "Tema 2", "Bibliografía obligatoria U2", "Marín, Marta.*.pdf"))
if marin4:
    files["ac_u2_marin_cap4"] = os.path.relpath(marin4[0], BASE)

os.makedirs(OUT, exist_ok=True)
for k, v in files.items():
    path = os.path.join(BASE, v)
    try:
        doc = fitz.open(path)
        txt = "\n".join("--- PAGE %d ---\n" % (i + 1) + p.get_text() for i, p in enumerate(doc))
        clean = "".join(c for c in txt if not c.isspace())
        outp = os.path.join(OUT, k + ".txt")
        with open(outp, "w", encoding="utf-8") as f:
            f.write(txt)
        print("%s\t%d pages\t%d chars\t%s" % (k, len(doc), len(clean), "SCAN?" if len(clean) < 200 * len(doc) else "ok"))
    except Exception as e:
        print(k, "ERROR", e)
