import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from scipy.integrate import solve_ivp

G = 6.67430e-11

class Simulador(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulación de Dos Cuerpos")
        self.setGeometry(100, 100, 400, 650)

        self.layout = QVBoxLayout()

        # Campos comunes (masas)
        self.lbl_m1 = QLabel("Masa cuerpo 1 (kg)")
        self.entry_m1 = QLineEdit()
        self.layout.addWidget(self.lbl_m1)
        self.layout.addWidget(self.entry_m1)

        self.lbl_m2 = QLabel("Masa cuerpo 2 (kg)")
        self.entry_m2 = QLineEdit()
        self.layout.addWidget(self.lbl_m2)
        self.layout.addWidget(self.entry_m2)

        # Frame para campos numéricos
        self.frame_numerico = QFrame()
        self.layout_numerico = QVBoxLayout(self.frame_numerico)

        labels_numerico = ["x1","y1","vx1","vy1","x2","y2","vx2","vy2","Tiempo de simulación (s)"]
        self.entries_numerico = []
        for text in labels_numerico:
            lbl = QLabel(text)
            e = QLineEdit()
            self.layout_numerico.addWidget(lbl)
            self.layout_numerico.addWidget(e)
            self.entries_numerico.append(e)

        (self.entry_x1, self.entry_y1, self.entry_vx1, self.entry_vy1,
         self.entry_x2, self.entry_y2, self.entry_vx2, self.entry_vy2,
         self.entry_tiempo) = self.entries_numerico

        self.layout.addWidget(self.frame_numerico)

        # Frame para campos analíticos
        self.frame_analitico = QFrame()
        self.layout_analitico = QVBoxLayout(self.frame_analitico)

        labels_analitico = ["xa1","ya1","vax1","vay1"]
        self.entries_analitico = []
        for text in labels_analitico:
            lbl = QLabel(text)
            e = QLineEdit()
            self.layout_analitico.addWidget(lbl)
            self.layout_analitico.addWidget(e)
            self.entries_analitico.append(e)

        (self.entry_xa1, self.entry_ya1, self.entry_vax1, self.entry_vay1) = self.entries_analitico

        self.layout.addWidget(self.frame_analitico)

        # Selector de sistema predefinido
        self.lbl_sistema = QLabel("Selecciona sistema predefinido")
        self.layout.addWidget(self.lbl_sistema)
        self.sistema_var = QComboBox()
        self.sistema_var.addItems(["Ninguno", "Sol-Tierra", "Tierra-Luna", "Sol-Júpiter"])
        self.sistema_var.currentTextChanged.connect(self.rellenar_predefinidos)
        self.layout.addWidget(self.sistema_var)

        # Selector de método
        self.lbl_metodo = QLabel("Método de simulación")
        self.layout.addWidget(self.lbl_metodo)
        self.metodo_var = QComboBox()
        self.metodo_var.addItems(["Numerico", "Analitica"])
        self.metodo_var.currentTextChanged.connect(self.actualizar_formulario)
        self.layout.addWidget(self.metodo_var)

        # Botón de simulación
        self.btn = QPushButton("Simular")
        self.btn.clicked.connect(self.simular)
        self.layout.addWidget(self.btn)

        # Resultado analítico
        self.lbl_resultado = QLabel("")
        self.lbl_resultado.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.lbl_resultado)

        self.setLayout(self.layout)
        self.actualizar_formulario("Numerico")

    def rellenar_predefinidos(self, sistema):
        if sistema == "Sol-Tierra":
            self.entry_m1.setText(str(1.989e30))
            self.entry_m2.setText(str(5.972e24))
            self.entry_x1.setText("0"); self.entry_y1.setText("0")
            self.entry_vx1.setText("0"); self.entry_vy1.setText("0")
            self.entry_x2.setText(str(1.496e11)); self.entry_y2.setText("0")
            self.entry_vx2.setText("0"); self.entry_vy2.setText(str(29780))
            self.entry_tiempo.setText(str(3.154e7))
            self.entry_xa1.setText(str(1.496e11)); self.entry_ya1.setText("0")
            self.entry_vax1.setText("0"); self.entry_vay1.setText(str(29780))

        elif sistema == "Tierra-Luna":
            self.entry_m1.setText(str(5.972e24))
            self.entry_m2.setText(str(7.348e22))
            self.entry_x1.setText("0"); self.entry_y1.setText("0")
            self.entry_vx1.setText("0"); self.entry_vy1.setText("0")
            self.entry_x2.setText(str(3.844e8)); self.entry_y2.setText("0")
            self.entry_vx2.setText("0"); self.entry_vy2.setText(str(1022))
            self.entry_tiempo.setText(str(2.36e6))
            self.entry_xa1.setText(str(3.844e8)); self.entry_ya1.setText("0")
            self.entry_vax1.setText("0"); self.entry_vay1.setText(str(1022))

        elif sistema == "Sol-Júpiter":
            self.entry_m1.setText(str(1.989e30))
            self.entry_m2.setText(str(1.898e27))
            self.entry_x1.setText("0"); self.entry_y1.setText("0")
            self.entry_vx1.setText("0"); self.entry_vy1.setText("0")
            self.entry_x2.setText(str(7.78e11)); self.entry_y2.setText("0")
            self.entry_vx2.setText("0"); self.entry_vy2.setText(str(13070))
            self.entry_tiempo.setText(str(3.74e8))
            self.entry_xa1.setText(str(7.78e11)); self.entry_ya1.setText("0")
            self.entry_vax1.setText("0"); self.entry_vay1.setText(str(13070))

    def actualizar_formulario(self, metodo):
        if metodo == "Numerico":
            self.frame_numerico.show()
            self.frame_analitico.hide()
            self.lbl_resultado.hide()
        elif metodo == "Analitica":
            self.frame_numerico.hide()
            self.frame_analitico.show()
            self.lbl_resultado.show()

    def simular(self):
        metodo = self.metodo_var.currentText()
        try:
            m1 = float(self.entry_m1.text())
            m2 = float(self.entry_m2.text())

            if metodo == "Numerico":
                x1 = float(self.entry_x1.text())
                y1 = float(self.entry_y1.text())
                vx1 = float(self.entry_vx1.text())
                vy1 = float(self.entry_vy1.text())
                x2 = float(self.entry_x2.text())
                y2 = float(self.entry_y2.text())
                vx2 = float(self.entry_vx2.text())
                vy2 = float(self.entry_vy2.text())
                tmax = float(self.entry_tiempo.text())

                def deriv(t, y):
                    x1, y1, vx1, vy1, x2, y2, vx2, vy2 = y
                    dx = x2 - x1
                    dy = y2 - y1
                    r = np.sqrt(dx**2 + dy**2)
                    f = G * m1 * m2 / r**3
                    ax1 = f * dx / m1
                    ay1 = f * dy / m1
                    ax2 = -f * dx / m2
                    ay2 = -f * dy / m2
                    return [vx1, vy1, ax1, ay1, vx2, vy2, ax2, ay2]

                y0 = [x1, y1, vx1, vy1, x2, y2, vx2, vy2]
                sol = solve_ivp(deriv, [0, tmax], y0, t_eval=np.linspace(0, tmax, 1000))

                plt.figure()
                plt.plot(sol.y[0], sol.y[1], marker="o", markersize=2, label="Cuerpo 1" )
                plt.plot(sol.y[4], sol.y[5], label="Cuerpo 2")
                plt.legend()
                plt.xlabel("x (m)")
                plt.ylabel("y (m)")
                plt.legend()
                plt.axis("equal")
                plt.show()

            elif metodo == "Analitica":
                xa1 = float(self.entry_xa1.text())
                ya1 = float(self.entry_ya1.text())
                vax1 = float(self.entry_vax1.text())
                vay1 = float(self.entry_vay1.text())
                mu = (m1 * m2) / (m1 + m2)
                r0 = np.sqrt(xa1**2 + ya1**2)
                v0 = np.sqrt(vax1**2 + vay1**2)
                L = mu * r0 * v0
                E = 0.5 * mu * v0**2 - G * m1 * m2 / r0
                a = -G * m1 * m2 / (2 * E)
                e = np.sqrt(1 + (2 * E * L**2) / (mu * (G * m1 * m2)**2))
                p = L**2 / (mu * G * (m1 + m2))

                theta = np.linspace(0, 2 * np.pi, 1000)
                r = p / (1 + e * np.cos(theta))
                x = r * np.cos(theta)
                y = r * np.sin(theta)

                plt.figure()
                plt.plot(x, y, label="Órbita analítica")
                plt.scatter([0], [0], c="yellow", marker="o", label="Centro de masas")
                plt.title("Órbita de dos cuerpos (solución analítica)")
                plt.xlabel("x (m)")
                plt.ylabel("y (m)")
                plt.legend()
                plt.axis("equal")
                plt.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Simulador()
    ventana.show()
    sys.exit(app.exec())
