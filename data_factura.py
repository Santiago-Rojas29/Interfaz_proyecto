import json
import os

RUTA_FACTURAS = "facturas.json"

def cargar_facturas():
    if not os.path.exists(RUTA_FACTURAS):
        return []
    with open(RUTA_FACTURAS, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_facturas(facturas):
    with open(RUTA_FACTURAS, 'w', encoding='utf-8') as f:
        json.dump(facturas, f, indent=4, ensure_ascii=False)
