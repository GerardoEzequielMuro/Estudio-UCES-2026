import shutil, os
ROOT = r"C:\Users\gerar\Downloads\Sistema-Estudio-UCES"
shutil.rmtree(os.path.join(ROOT, "_img", "marketing", "_cand"), ignore_errors=True)
for f in ("_check_mkt.py", "_check_mkt.js"):
    p = os.path.join(ROOT, f)
    if os.path.exists(p): os.remove(p)
print("ok")
for fn in sorted(os.listdir(os.path.join(ROOT, "_img", "marketing"))):
    print(fn)
print("marketing.html:", os.path.getsize(os.path.join(ROOT, "marketing.html")), "bytes")
