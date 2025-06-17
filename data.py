import json
import os

# Archivos
ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_ELEMENTOS = "elementos.json"
ARCHIVO_VENTAS = "ventas.json"
ARCHIVO_COMPRAS = "compras.json"
ARCHIVO_FACTURAS = "facturas.json"

# Funciones generales
def cargar_datos(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return []

def guardar_datos(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

# Funciones específicas
def cargar_usuarios():
    return cargar_datos(ARCHIVO_USUARIOS)

def guardar_usuarios(lista):
    guardar_datos(ARCHIVO_USUARIOS, lista)

def cargar_elementos():
    return cargar_datos(ARCHIVO_ELEMENTOS)

def guardar_elementos(lista):
    guardar_datos(ARCHIVO_ELEMENTOS, lista)

def cargar_ventas():
    return cargar_datos(ARCHIVO_VENTAS)

def guardar_ventas(lista):
    guardar_datos(ARCHIVO_VENTAS, lista)

def cargar_compras():
    return cargar_datos(ARCHIVO_COMPRAS)

def guardar_compras(lista):
    guardar_datos(ARCHIVO_COMPRAS, lista)

def cargar_facturas():
    return cargar_datos(ARCHIVO_FACTURAS)

def guardar_facturas(lista):
    guardar_datos(ARCHIVO_FACTURAS, lista)