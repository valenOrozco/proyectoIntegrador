import tkinter as tk
from tkinter import messagebox
import registro as reg

root = tk.Tk()
root.title("Sistema de Gestión de Datos")
root.iconbitmap("./src/img/star.ico")
root.geometry("500x500")
root.configure(bg="#000")

label = tk.Label(root, text="Aurora", font=("Vogue", 40, "bold"), bg="#000", fg="#fff")
label.pack(pady=20)


def registrar_usuario():
    ventana = tk.Toplevel(root)
    ventana.title("Registrar usuario")
    ventana.geometry("500x600")
    ventana.configure(bg="#000")
    try:
        ventana.iconbitmap("./src/img/star.ico")
    except Exception:
        pass

    label_args = {"bg": "#000", "fg": "#fff", "font": ("Utendo", 13,)}
    entry_args = {"font": ("Utendo", 13), "bg": "#fff", "fg": "#000", "insertbackground": "#000"}

    tk.Label(ventana, text="Nombre:", **label_args).pack(pady=5)
    entry_nombre = tk.Entry(ventana, **entry_args)
    entry_nombre.pack(pady=5)

    tk.Label(ventana, text="Apellidos:", **label_args).pack(pady=5)
    entry_apellidos = tk.Entry(ventana, **entry_args)
    entry_apellidos.pack(pady=5)

    tk.Label(ventana, text="Número de documento:", **label_args).pack(pady=5)
    entry_documento = tk.Entry(ventana, **entry_args)
    entry_documento.pack(pady=5)

    tk.Label(ventana, text="Edad:", **label_args).pack(pady=5)
    entry_edad = tk.Entry(ventana, **entry_args)
    entry_edad.pack(pady=5)

    tk.Label(ventana, text="Correo electrónico:", **label_args).pack(pady=5)
    entry_correo = tk.Entry(ventana, **entry_args)
    entry_correo.pack(pady=5)

    tk.Label(ventana, text="Teléfono:", **label_args).pack(pady=5)
    entry_telefono = tk.Entry(ventana, **entry_args)
    entry_telefono.pack(pady=5)

    def guardar_usuario():
        nombre = entry_nombre.get()
        apellidos = entry_apellidos.get()
        documento = entry_documento.get()
        edad = entry_edad.get()
        correo = entry_correo.get()
        telefono = entry_telefono.get()
        try:
            edad = int(edad)
            reg.registrar_usuaria(nombre, apellidos, documento, edad, correo, telefono)
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    btn_guardar = tk.Button(ventana, text="Guardar", command=guardar_usuario, font=("Utendo", 11), bg="#fff", fg="#000",
                            activebackground="#eee", activeforeground="#000", highlightbackground="#fff",
                            highlightcolor="#fff", highlightthickness=1)
    btn_guardar.pack(pady=20)


def cargar_encuesta():
    import encuestas
    ventana = tk.Toplevel(root)
    ventana.title("Cargar encuesta")
    ventana.geometry("500x600")
    ventana.configure(bg="#000")
    try:
        ventana.iconbitmap("./src/img/star.ico")
    except Exception:
        pass

    label_args = {"bg": "#000", "fg": "#fff", "font": ("Utendo", 12,)}
    entry_args = {"font": ("Utendo", 11), "bg": "#fff", "fg": "#000", "insertbackground": "#000"}

    tk.Label(ventana, text="Número de documento:", **label_args).pack(pady=5)
    entry_documento = tk.Entry(ventana, **entry_args)
    entry_documento.pack(pady=5)

    respuestas = []
    widgets = []

    for idx, (pregunta, tipo) in enumerate(encuestas.preguntas):
        tk.Label(ventana, text=pregunta, **label_args).pack(pady=5)
        if tipo == "sn":
            var = tk.StringVar(value="S")
            frame = tk.Frame(ventana, bg="#000")
            tk.Radiobutton(frame, text="Sí", variable=var, value="S", bg="#000", fg="#fff", selectcolor="#222",
                           font=("Arial Rounded MT Bold", 11)).pack(side=tk.LEFT, padx=10)
            tk.Radiobutton(frame, text="No", variable=var, value="N", bg="#000", fg="#fff", selectcolor="#222",
                           font=("Arial Rounded MT Bold", 11)).pack(side=tk.LEFT, padx=10)
            frame.pack(pady=2)
            widgets.append(var)
        else:
            var = tk.IntVar(value=3)
            scale = tk.Scale(ventana, from_=1, to=5, orient=tk.HORIZONTAL, variable=var, bg="#000", fg="#fff",
                             troughcolor="#222", font=("Arial Rounded MT Bold", 10), highlightbackground="#000")
            scale.pack(pady=2)
            widgets.append(var)

    def guardar_encuesta():
        documento = entry_documento.get().strip()
        if not documento:
            messagebox.showerror("Error", "Debes ingresar el número de documento.")
            return
        respuestas_usuario = []
        for idx, (pregunta, tipo) in enumerate(encuestas.preguntas):
            val = widgets[idx].get()
            if tipo == "sn" and val not in ["S", "N"]:
                messagebox.showerror("Error", f"Responde correctamente la pregunta: {pregunta}")
                return
            if tipo == "num" and (not isinstance(val, int) or not (1 <= val <= 5)):
                messagebox.showerror("Error", f"Selecciona un valor entre 1 y 5 para: {pregunta}")
                return
            respuestas_usuario.append(val)
        try:
            encuestas._asegurar_archivo()
            from datetime import datetime
            import csv
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fila = [documento, fecha_actual] + respuestas_usuario
            with open(encuestas.archivo, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(fila)
            messagebox.showinfo("Éxito", "Encuesta registrada correctamente")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la encuesta: {e}")

    btn_guardar = tk.Button(ventana, text="Guardar encuesta", command=guardar_encuesta, font=("Utendo", 11), bg="#fff",
                            fg="#000", activebackground="#eee", activeforeground="#000", highlightbackground="#fff",
                            highlightcolor="#fff", highlightthickness=1)
    btn_guardar.pack(pady=20)


def ver_estadisticas():
    import subprocess
    import os
    from PIL import Image, ImageTk
    ventana = tk.Toplevel(root)
    ventana.title("Estadísticas - Histogramas")
    ventana.geometry("1270x550")
    ventana.configure(bg="#000")
    try:
        ventana.iconbitmap("./src/img/star.ico")
    except Exception:
        pass
    try:
        subprocess.run(["python", os.path.join("src", "visualizaciones.py")], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron generar los histogramas: {e}")
        ventana.destroy()
        return
    rutas = [
        "data/histograma_edad.png",
        "data/histograma_edad_malos_pensamientos.png",
        "data/histograma_edad_problemas_ambiente.png",
        "data/histograma_edad_comida_regular.png",
        "data/histograma_ansiedad_estrés.png",
        "data/histograma_estado_animo.png"
    ]
    imagenes = []
    frame = tk.Frame(ventana, bg="#000")
    frame.pack(expand=True, fill=tk.BOTH)

    def mostrar_zoom(ruta):
        zoom_win = tk.Toplevel(ventana)
        zoom_win.title("Zoom - Visualización")
        zoom_win.configure(bg="#000")
        try:
            zoom_win.iconbitmap("./src/img/star.ico")
        except Exception:
            pass
        img = Image.open(ruta)
        img_tk = ImageTk.PhotoImage(img)
        lbl_img = tk.Label(zoom_win, image=img_tk, bg="#000")
        lbl_img.image = img_tk
        lbl_img.pack(padx=10, pady=10)

    for idx, ruta in enumerate(rutas):
        try:
            img = Image.open(ruta)
            img = img.resize((400, 250))
            img_tk = ImageTk.PhotoImage(img)
            imagenes.append(img_tk)
            lbl = tk.Label(frame, image=img_tk, bg="#000", cursor="hand2")
            lbl.bind("<Button-1>", lambda e, r=ruta: mostrar_zoom(r))
            row, col = divmod(idx, 3)
            lbl.grid(row=row, column=col, padx=10, pady=10)
        except Exception as e:
            row, col = divmod(idx, 3)
            tk.Label(frame, text=f"No se pudo cargar {ruta}", fg="#fff", bg="#000").grid(row=row, column=col, padx=10,
                                                                                         pady=10)
    ventana.mainloop()


def ver_usuarias():
    import json
    import os
    ventana = tk.Toplevel(root)
    ventana.title("Usuarias registradas")
    ventana.geometry("980x600")
    ventana.configure(bg="#000")
    try:
        ventana.iconbitmap("./src/img/star.ico")
    except Exception:
        pass
    archivo = "data/usuarios.json"
    usuarias = []
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            usuarias = json.load(f)
    if not usuarias:
        tk.Label(ventana, text="No hay usuarias registradas.", fg="#fff", bg="#000", font=("Utendo", 13)).pack(pady=20)
        return
    frame = tk.Frame(ventana, bg="#000")
    frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    encabezados = ["Documento", "Nombre", "Apellidos", "Edad", "Correo", "Teléfono"]
    for col, enc in enumerate(encabezados):
        tk.Label(frame, text=enc, fg="#fff", bg="#222", font=("Utendo", 11, "bold"), borderwidth=1, relief="solid",
                 width=15).grid(row=0, column=col, sticky="nsew")
    for row, usuaria in enumerate(usuarias, start=1):
        tk.Label(frame, text=usuaria.get("documento", ""), fg="#fff", bg="#000", font=("Utendo", 11), borderwidth=1,
                 relief="solid").grid(row=row, column=0, sticky="nsew")
        tk.Label(frame, text=usuaria.get("nombre", ""), fg="#fff", bg="#000", font=("Utendo", 11), borderwidth=1,
                 relief="solid").grid(row=row, column=1, sticky="nsew")
        tk.Label(frame, text=usuaria.get("apellidos", ""), fg="#fff", bg="#000", font=("Utendo", 11), borderwidth=1,
                 relief="solid").grid(row=row, column=2, sticky="nsew")
        tk.Label(frame, text=usuaria.get("edad", ""), fg="#fff", bg="#000", font=("Utendo", 11), borderwidth=1,
                 relief="solid").grid(row=row, column=3, sticky="nsew")
        tk.Label(frame, text=usuaria.get("correo", ""), fg="#fff", bg="#000", font=("Utendo", 11), borderwidth=1,
                 relief="solid").grid(row=row, column=4, sticky="nsew")
        tk.Label(frame, text=usuaria.get("telefono", ""), fg="#fff", bg="#000", font=("Utendo", 11), borderwidth=1,
                 relief="solid").grid(row=row, column=5, sticky="nsew")


btn_registrar = tk.Button(root, text="Registrar usuario", width=30, command=registrar_usuario, font=("Utendo", 11),
                          bg="#fff", fg="#000", activebackground="#eee", activeforeground="#000",
                          highlightbackground="#fff", highlightcolor="#fff", highlightthickness=1)
btn_registrar.pack(pady=5)

btn_encuesta = tk.Button(root, text="Cargar encuesta", width=30, command=cargar_encuesta, font=("Utendo", 11),
                         bg="#fff", fg="#000", activebackground="#eee", activeforeground="#000",
                         highlightbackground="#fff", highlightcolor="#fff", highlightthickness=1)
btn_encuesta.pack(pady=5)

btn_estadisticas = tk.Button(root, text="Ver estadísticas", width=30, command=ver_estadisticas, font=("Utendo", 11),
                             bg="#fff", fg="#000", activebackground="#eee", activeforeground="#000",
                             highlightbackground="#fff", highlightcolor="#fff", highlightthickness=1)
btn_estadisticas.pack(pady=5)

btn_usuarias = tk.Button(root, text="Ver usuarias registradas", width=30, command=ver_usuarias, font=("Utendo", 11),
                         bg="#fff", fg="#000", activebackground="#eee", activeforeground="#000",
                         highlightbackground="#fff", highlightcolor="#fff", highlightthickness=1)
btn_usuarias.pack(pady=5)

btn_salir = tk.Button(root, text="Salir", width=30, command=root.quit, font=("Utendo", 11), bg="#fff", fg="#000",
                      activebackground="#eee", activeforeground="#000", highlightbackground="#fff",
                      highlightcolor="#fff", highlightthickness=1)
btn_salir.pack(pady=20)

root.mainloop()
