import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from scipy.integrate import solve_ivp

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
        x2 = float(entry_x2.get())
        y2 = float(entry_y2.get())
        vx2 = float(entry_vx2.get())
        vy2 = float(entry_vy2.get())

        # Sistema de ecuaciones diferenciales
        def dos_cuerpos(t, y):
            x1, vx1, y1, vy1, x2, vx2, y2, vy2 = y
            dx = x2 - x1
            dy = y2 - y1
            r = np.sqrt(dx**2 + dy**2)
            ax1 = G * m2 * dx / r**3
            ay1 = G * m2 * dy / r**3
            ax2 = -G * m1 * dx / r**3
            ay2 = -G * m1 * dy / r**3
            return [vx1, ax1, vy1, ay1, vx2, ax2, vy2, ay2]

        # Condiciones iniciales
        y_init = [x1, vx1, y1, vy1, x2, vx2, y2, vy2]

        # Tiempo de simulación
        t_span = (0, 3.154e7)  # 1 año en segundos
        t_eval = np.linspace(0, 1e6, 2000)

        # Resolver
        sol = solve_ivp(dos_cuerpos, t_span, y_init, t_eval=t_eval)

        # Graficar trayectorias
        plt.plot(sol.y[0], sol.y[2], label="Cuerpo 1")
        plt.plot(sol.y[4], sol.y[6], label="Cuerpo 2")
        plt.scatter([sol.y[0][0], sol.y[4][0]], [sol.y[2][0], sol.y[6][0]], c=["blue","red"], marker="o")
        plt.title("Simulación de dos cuerpos")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.legend()
        plt.axis("equal")
        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Simulación de Dos Cuerpos")

# Campos de entrada
labels = ["Masa cuerpo 1 (kg)", "Masa cuerpo 2 (kg)",
          "x1", "y1", "vx1", "vy1",
          "x2", "y2", "vx2", "vy2"]

entries = []
for i, text in enumerate(labels):
    tk.Label(ventana, text=text).grid(row=i, column=0, padx=5, pady=5)
    e = tk.Entry(ventana)
    e.grid(row=i, column=1, padx=5, pady=5)
    entries.append(e)

entry_m1, entry_m2, entry_x1, entry_y1, entry_vx1, entry_vy1, entry_x2, entry_y2, entry_vx2, entry_vy2 = entries

# Botón de simulación
btn = tk.Button(ventana, text="Simular", command=simular)
btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

ventana.mainloop()
