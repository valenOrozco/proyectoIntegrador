import csv
import random
from datetime import datetime
from pathlib import Path

preguntas = [
    ("¿Has tenido malos pensamientos frecuentemente?", "sn"),
    ("¿Has tenido problemas dentro de tu ambiente familiar, escolar, social o laboral?", "sn"),
    ("¿Has comido bien regularmente?", "sn"),
    ("¿Qué tan ansiosa o estresada te sientes? (1=Muy estresada, 5=Tranquila)", "num"),
    ("¿Cómo describirías tu estado de ánimo en general? (1=Muy bajo, 5=Excelente)", "num")
]

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
archivo = DATA_DIR / "encuestas.csv"


def _asegurar_archivo():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not archivo.exists():
        with archivo.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            encabezados = ["documento", "fecha"] + [p[0] for p in preguntas]
            writer.writerow(encabezados)


def registrar_encuesta(documento, modo="manual"):
    _asegurar_archivo()
    respuestas = []

    if modo == "manual":
        print("\nResponde las siguientes preguntas:")
        for p, tipo in preguntas:
            while True:
                if tipo == "sn":
                    r = input(p + " (S/N) → ").strip().upper()
                    if r in ["S", "N"]:
                        respuestas.append(r)
                        break
                    else:
                        print("⚠️ Responde con S o N.")
                else:
                    try:
                        r = int(input(p + " (1-5) → "))
                        if 1 <= r <= 5:
                            respuestas.append(r)
                            break
                        else:
                            print("⚠️ Ingresa un número entre 1 y 5.")
                    except ValueError:
                        print("⚠️ Ingresa un número válido.")
    else:
        for _, tipo in preguntas:
            if tipo == "sn":
                respuestas.append(random.choice(["S", "N"]))
            else:
                respuestas.append(random.randint(1, 5))

    with archivo.open("r", encoding="utf-8") as f:
        filas = list(csv.reader(f))

    encabezado = filas[0]
    datos = filas[1:]

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fila = [documento, fecha_actual] + respuestas

    datos.append(fila)

    with archivo.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(encabezado)
        writer.writerows(datos)

    print(f"\n✅ Encuesta registrada correctamente")


def ver_respuestas(documento=None):
    with archivo.open("r", encoding="utf-8") as f:
        filas = list(csv.reader(f))

    if len(filas) <= 1:
        print("\n⚠️ No hay encuestas registradas aún.")
        return

    encabezado = filas[0]
    datos = filas[1:]

    if documento:
        datos = [row for row in datos if row[0] == documento]
        if not datos:
            print(f"\n⚠️ No hay encuestas para el documento {documento}.")
            return
        print(f"\n📊 Historial de encuestas de {documento}:\n")
    else:
        print("\n📊 Encuestas registradas:\n")

    for row in datos:
        documento_id = row[0]
        fecha = row[1]
        respuestas = row[2:]
        print(f"📍 Documento: {documento_id}")
        print(f"📍 Fecha: {fecha}")
        for i, resp in enumerate(respuestas):
            print(f"     - {preguntas[i][0]} → {resp}")
        print("-" * 50)
