import json
import os
import time

archivo_usuarias = "data/usuarios.json"

def registrar_usuaria(nombre, apellidos, documento, edad, correo, telefono, archivo=archivo_usuarias):
    if not nombre or not apellidos or not documento or not str(edad).isdigit() or not correo or not telefono:
        raise ValueError("Datos incompletos o inválidos")
    usuarias = []
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            usuarias = json.load(f)
    for u in usuarias:
        if u["documento"] == documento:
            raise ValueError("El documento ya está registrado")
    nueva_usuaria = {
        "nombre": nombre,
        "apellidos": apellidos,
        "documento": documento,
        "edad": int(edad),
        "correo": correo,
        "telefono": telefono
    }
    usuarias.append(nueva_usuaria)
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(usuarias, f, ensure_ascii=False, indent=2)
    return True

def usuaria_registrada(documento, archivo=archivo_usuarias):
    if not os.path.exists(archivo):
        return False
    with open(archivo, "r", encoding="utf-8") as f:
        usuarias = json.load(f)
    for u in usuarias:
        if u["documento"] == documento:
            return True
    return False

def buscar_usuaria(documento, archivo=archivo_usuarias):
    if not os.path.exists(archivo):
        return None
    with open(archivo, "r", encoding="utf-8") as f:
        usuarias = json.load(f)
    for u in usuarias:
        if u["documento"] == documento:
            return u
    return None

def registrar_usuarias(archivo=archivo_usuarias):
    usuarias = []
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            usuarias = json.load(f)

    print("\n✨ Aurora - Salud mental sin costo ❤️‍🩹\n")
    print("Llena los siguientes datos:")

    while True:
        documento = input("Documento: ").strip()
        if usuaria_registrada(documento, archivo):
            print("⚠️ Este documento ya está registrado. Intenta con otro.\n")
        elif documento == "":
            print("⚠️ Debes ingresar un documento válido.\n")
        else:
            break

    nombre = input("Primer nombre: ").strip()
    apellidos = input("Apellidos: ").strip()
    telefono = input("Teléfono: ").strip()

    while True:
        try:
            edad = int(input("Edad: ").strip())
            break
        except ValueError:
            print("⚠️ Ingresa un número válido.\n")

    while True:
        correo = input("Correo electrónico: ").strip()
        if "@" in correo and "." in correo:
            break
        print("⚠️ Ingresa un correo válido.\n")

    usuaria = {
        "documento": documento,
        "nombre": nombre,
        "apellidos": apellidos,
        "edad": edad,
        "correo": correo,
        "telefono": telefono
    }

    usuarias.append(usuaria)

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(usuarias, f, indent=4, ensure_ascii=False)

    print("\nEspere...")
    time.sleep(2)
    print("\n✅ Registro exitoso! Ya puedes tomar la encuesta de salud mental.")


def ver_usuarias(archivo=archivo_usuarias):
    if not os.path.exists(archivo):
        print("\n⚠️ No hay usuarias registradas aún.")
        return

    with open(archivo, "r", encoding="utf-8") as f:
        usuarias = json.load(f)

    print("\n📋 Lista de usuarias registradas:\n")
    for u in usuarias:
        print(f"   📌 Documento: {u.get('documento', '')}")
        print(f"   👤 Nombre: {u.get('nombre', '')} {u.get('apellidos', '')}")
        print(f"   🎂 Edad: {u.get('edad', '')} años")
        print(f"   📞 Teléfono: {u.get('telefono', '')}")
        print(f"   📧 Correo: {u.get('correo', '')}\n")
