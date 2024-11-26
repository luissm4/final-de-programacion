import tkinter as tk
from tkinter import ttk, messagebox
#luis muñoz
class Transaccion:
    def __init__(self, tipo, categoria, monto, descripcion):
        self.tipo = tipo
        self.categoria = categoria
        self.monto = float(monto)
        self.descripcion = descripcion

class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.transacciones = []

    def agregar_transaccion(self, transaccion):
        self.transacciones.append(transaccion)

    def obtener_resumen(self):
        resumen = {"Ingresos": 0, "Gastos": 0}
        for t in self.transacciones:
            if t.tipo == "Ingreso":
                resumen["Ingresos"] += t.monto
            elif t.tipo == "Gasto":
                resumen["Gastos"] += t.monto
        return resumen

class Controlador:
    def __init__(self):
        self.usuario = None

    def establecer_usuario(self, nombre):
        self.usuario = Usuario(nombre)

    def registrar_transaccion(self, tipo, categoria, monto, descripcion):
        if not self.usuario:
            return False
        transaccion = Transaccion(tipo, categoria, monto, descripcion)
        self.usuario.agregar_transaccion(transaccion)
        return True

    def mostrar_resumen(self):
        return self.usuario.obtener_resumen() if self.usuario else None

class Vista:
    def __init__(self, controlador):
        self.controlador = controlador
        self.root = tk.Tk()
        self.root.title("Gestión de Presupuestos y Gastos")
        self.mensaje_label = None
        self.nombre_entry = None
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.root, text="Gestión de Presupuestos", font=("Arial", 16)).pack(pady=10)

        self.nombre_entry = tk.Entry(self.root, font=("Arial", 12))
        self.nombre_entry.insert(0, "Nombre")
        self.nombre_entry.pack(pady=5)

        ttk.Button(self.root, text="Registrar Transacción", command=self.mostrar_formulario).pack(pady=5)
        ttk.Button(self.root, text="Ver Resumen", command=self.mostrar_resumen).pack(pady=5)

        self.mensaje_label = tk.Label(self.root, text="", font=("Arial", 10), fg="green")
        self.mensaje_label.pack(pady=10)

    def mostrar_formulario(self):
        nombre_usuario = self.nombre_entry.get().strip()
        if not nombre_usuario:
            messagebox.showerror("Error", "Por favor, ingrese un nombre de usuario válido.")
            return

        if not self.controlador.usuario:
            self.controlador.establecer_usuario(nombre_usuario)

        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Transacción")

        tk.Label(ventana, text="Tipo:").grid(row=0, column=0, pady=5)
        tipo = ttk.Combobox(ventana, values=["Ingreso", "Gasto"])
        tipo.grid(row=0, column=1, pady=5)

        tk.Label(ventana, text="Categoría:").grid(row=1, column=0, pady=5)
        categoria = tk.Entry(ventana)
        categoria.grid(row=1, column=1, pady=5)

        tk.Label(ventana, text="Monto:").grid(row=2, column=0, pady=5)
        monto = tk.Entry(ventana)
        monto.grid(row=2, column=1, pady=5)

        tk.Label(ventana, text="Descripción:").grid(row=3, column=0, pady=5)
        descripcion = tk.Entry(ventana)
        descripcion.grid(row=3, column=1, pady=5)

        def guardar_transaccion():
            errores = []
            if tipo.get() not in ["Ingreso", "Gasto"]:
                errores.append("Debe seleccionar un tipo válido (Ingreso o Gasto).")
            if not categoria.get().strip():
                errores.append("La categoría no puede estar vacía.")
            try:
                monto_float = float(monto.get())
                if monto_float <= 0:
                    errores.append("El monto debe ser un número positivo.")
            except ValueError:
                errores.append("El monto debe ser un número válido.")
            if len(descripcion.get()) > 50:
                errores.append("La descripción no puede superar los 50 caracteres.")

            if errores:
                messagebox.showerror("Errores en el formulario", "\n".join(errores))
            else:
                if self.controlador.registrar_transaccion(
                        tipo.get(), categoria.get(), monto_float, descripcion.get()):
                    self.mensaje_label.config(text="¡Transacción registrada con éxito!")
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "Debe establecer un nombre de usuario antes de registrar transacciones.")

        ttk.Button(ventana, text="Registrar", command=guardar_transaccion).grid(row=4, column=0, columnspan=2, pady=10)

    def mostrar_resumen(self):
        nombre_usuario = self.nombre_entry.get().strip()
        if not nombre_usuario:
            messagebox.showerror("Error", "Por favor, ingrese un nombre de usuario válido.")
            return

        if not self.controlador.usuario:
            self.controlador.establecer_usuario(nombre_usuario)

        resumen = self.controlador.mostrar_resumen()
        if not resumen:
            messagebox.showerror("Error", "No se puede mostrar el resumen, no se ha registrado ninguna transacción.")
            return

        transacciones = self.controlador.usuario.transacciones

        ventana = tk.Toplevel(self.root)
        ventana.title("Resumen de Ingresos y Gastos")

        tk.Label(ventana, text=f"Usuario: {self.controlador.usuario.nombre}", font=("Arial", 12, "bold")).pack(pady=5)

        tk.Label(ventana, text=f"Ingresos Totales: ${resumen['Ingresos']:.2f}", font=("Arial", 12)).pack(pady=5)
        tk.Label(ventana, text=f"Gastos Totales: ${resumen['Gastos']:.2f}", font=("Arial", 12)).pack(pady=5)

        tk.Label(ventana, text="Historial de Transacciones:", font=("Arial", 10)).pack(pady=5)
        texto = tk.Text(ventana, width=60, height=15)
        texto.pack(pady=5)

        if transacciones:
            for t in transacciones:
                texto.insert(
                    tk.END,
                    f"{t.tipo}: ${t.monto:.2f} - {t.categoria} ({t.descripcion})\n"
                )
        else:
            texto.insert(tk.END, "No hay transacciones registradas.\n")

        texto.config(state="disabled")

    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    controlador = Controlador()
    vista = Vista(controlador)
    vista.iniciar()
