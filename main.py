import time

from src.encuestas import registrar_encuesta, ver_respuestas
from src.registro import registrar_usuarias, ver_usuarias, usuaria_registrada, buscar_usuaria


def menu_principal():
    print("\n✨ Bienvenida a Aurora ✨\n")
    print(
        "Aquí en Aurora te ayudamos sin ningún costo a mantenerte sana mentalmente. \n¡Inicia tu proceso ahora mismo!"
    )

    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Soy nueva y quisiera registrarme")
        print("2. Usuarias registradas")
        print("3. Encuesta de estado emocional")
        print("4. Ver todas las encuestas registradas")
        print("5. Salir\n")

        opcion = input("Elige una opción → ").strip()

        if opcion == "1":
            registrar_usuarias()

        elif opcion == "2":
            while True:
                print("\n📋 Elige una opción")
                print("1. Ver todas las usuarias")
                print("2. Buscar usuaria por documento")
                print("3. Volver al menú principal")

                sub_op = input("Elige una opción → ").strip()

                if sub_op == "1":
                    ver_usuarias()

                elif sub_op == "2":
                    documento = input("Ingresa el número de documento que deseas buscar: ").strip()
                    usuaria = buscar_usuaria(documento)
                    if usuaria:
                        print(f"   📌 Documento: {usuaria['documento']}")
                        print(f"   👤 Nombre: {usuaria['nombre']} {usuaria['apellidos']}")
                        print(f"   🎂 Edad: {usuaria['edad']} años")
                        print(f"   📞 Teléfono: {usuaria['telefono']}")
                        print(f"   📧 Correo: {usuaria['correo']}\n")
                    else:
                        print("⚠️ No se encontró ninguna usuaria con ese documento.")

                elif sub_op == "3":
                    break

                else:
                    print("⚠️ Opción inválida. Intenta de nuevo.")

        elif opcion == "3":
            documento = input("Ingresa tu número de documento: ").strip()
            if usuaria_registrada(documento):
                while True:
                    print("\n¿Qué deseas hacer?")
                    print("1. Hacer nueva encuesta")
                    print("2. Ver historial de encuestas")
                    print("3. Volver al menú principal")
                    sub_op = input("Elige una opción → ").strip()

                    if sub_op == "1":
                        registrar_encuesta(documento, modo="manual")
                        break
                    elif sub_op == "2":
                        ver_respuestas(documento=documento)
                        break
                    elif sub_op == "3":
                        break
                    else:
                        print("⚠️ Opción inválida. Intenta de nuevo.")
            else:
                print("⚠️ No estás registrada en el sistema. Regístrate primero.")

        elif opcion == "4":
            ver_respuestas()

        elif opcion == "5":
            print("Saliendo...")
            time.sleep(2)
            print("👋 ¡Gracias por usar Aurora!")
            break

        else:
            print("⚠️ Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    menu_principal()
