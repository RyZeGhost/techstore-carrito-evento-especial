import json

with open("resultado_imperativo.json", encoding="utf-8") as f1, \
     open("resultado_poo.json", encoding="utf-8") as f2, \
     open("resultado_funcional.json", encoding="utf-8") as f3:
    imp, poo, fun = json.load(f1), json.load(f2), json.load(f3)

assert imp == poo == fun, f"Discrepancia detectada:\nIMP: {imp}\nPOO: {poo}\nFUN: {fun}"
print("OK: Los 3 paradigmas producen exactamente la misma salida.")
