import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Constante de gravitación universal
G = 6.67430e-11

def simular():
    try:
        # Obtener valores de la interfaz
        m1 = float(entry_m1.get())
        m2 = float(entry_m2.get())
        x1 = float(entry_x1.get())
        y1 = float(entry_y1.get())
        vx1 = float(entry_vx1.get())
        vy1 = float(entry_vy1.get())

        # Movimiento relativo: masa reducida
        mu = (m1*m2)/(m1+m2)

        # Condiciones iniciales
        r0 = np.sqrt(x1**2 + y1**2)
        v0 = np.sqrt(vx1**2 + vy1**2)

        # Momento angular aproximado
        L = mu * r0 * v0

        # Energía mecánica total
        E = 0.5*mu*v0**2 - G*m1*m2/r0

        # Parámetros orbitales
        a = -G*m1*m2/(2*E)   # semieje mayor
        e = np.sqrt(1 + (2*E*L**2)/(mu*(G*m1*m2)**2))  # excentricidad
        p = L**2/(mu*G*(m1+m2))

        # Generar órbita analítica
        theta = np.linspace(0, 2*np.pi, 1000)
        r = p/(1 + e*np.cos(theta))
        x = r*np.cos(theta)
        y = r*np.sin(theta)

        # Graficar
        plt.plot(x, y, label="Órbita analítica")
        plt.scatter([0], [0], c="yellow", marker="o", label="Centro de masas")
        plt.title("Órbita de dos cuerpos (solución analítica)")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.legend()
        plt.axis("equal")
        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Órbita Analítica de Dos Cuerpos")

# Campos de entrada
labels = ["Masa cuerpo 1 (kg)", "Masa cuerpo 2 (kg)",
          "x1 (m)", "y1 (m)", "vx1 (m/s)", "vy1 (m/s)"]

entries = []
for i, text in enumerate(labels):
    tk.Label(ventana, text=text).grid(row=i, column=0, padx=5, pady=5)
    e = tk.Entry(ventana)
    e.grid(row=i, column=1, padx=5, pady=5)
    entries.append(e)

entry_m1, entry_m2, entry_x1, entry_y1, entry_vx1, entry_vy1 = entries

# Botón de simulación
btn = tk.Button(ventana, text="Simular órbita", command=simular)
btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

ventana.mainloop()
