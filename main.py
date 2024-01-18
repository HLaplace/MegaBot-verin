import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import numpy as np

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.nom_fichier = "C:/Archive/ENSEIRB/Controle moteur/data_ACQ/donnees_serie_acquisition_verrin_23_2024-01-10_11-48-11.txt"

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.plot_widget_vitesse = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget_vitesse)
        self.plot_widget_vitesse.plotItem.layout.setContentsMargins(0, 0, 0, 0)
        self.curve_vitesse = self.plot_widget_vitesse.plot(pen='g', name='reel')
        self.plot_widget_vitesse.plotItem.showGrid(True, True, alpha=0.5)

        self.plot_widget_1 = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget_1)
        self.plot_widget_1.plotItem.layout.setContentsMargins(0, 0, 0, 0)
        self.curve_1_pos_reel = self.plot_widget_1.plot(pen='g', name='reel')
        self.curve_1_pos_cible = self.plot_widget_1.plot(pen='r', name='target')
        self.plot_widget_1.plotItem.showGrid(True, True, alpha=0.5)

        self.plot_widget_2 = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget_2)
        self.plot_widget_2.plotItem.layout.setContentsMargins(0, 0, 0, 0)
        self.curve_2_pwm_reel = self.plot_widget_2.plot(pen='g', name='reel')
        self.curve_2_pwm_cible = self.plot_widget_2.plot(pen='r', name='target')
        self.plot_widget_2.plotItem.showGrid(True, True, alpha=0.5)

        self.counter_values_pos_reel_1 = []
        self.counter_values_pos_cible_1 = []
        self.counter_values_pwm_reel_2 = []
        self.counter_values_pwm_cible_2 = []
        self.verify = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plots)

    def update_plots(self):
        with open(self.nom_fichier, 'r') as fichier:
            ligne = fichier.readline()
            if not ligne:
                # Fin du fichier
                self.timer.stop()
                return

            if self.verify == False:
                tab_valeurs = ligne.strip().replace("L23#", "").split('#')
                temp_0 = float(tab_valeurs[4])
                print("Temps_0 : ", temp_0)
                self.verify = True

            tab_valeurs = ligne.strip().replace("L23#", "").split('#')
            flt_pos_reel = float(tab_valeurs[0])
            flt_pos_cible = float(tab_valeurs[1])
            flt_pwm_reel = float(tab_valeurs[2])
            flt_pwm_cible = float(tab_valeurs[3])
            flt_temp = float(tab_valeurs[4]) - temp_0

            self.counter_values_pos_reel_1.append((flt_temp, flt_pos_reel))
            self.counter_values_pos_cible_1.append((flt_temp, flt_pos_cible))
            self.counter_values_pwm_reel_2.append((flt_temp, flt_pwm_reel))
            self.counter_values_pwm_cible_2.append((flt_temp, flt_pwm_cible))

            data_array_values_pos_reel = np.array(self.counter_values_pos_reel_1)
            temps = data_array_values_pos_reel[:, 0]
            positions = data_array_values_pos_reel[:, 1]

            with np.errstate(divide='ignore', invalid='ignore'):
                vitesses = np.gradient(positions, temps)

            self.curve_vitesse.setData(temps, vitesses)
            self.curve_1_pos_reel.setData(*zip(*self.counter_values_pos_reel_1))
            self.curve_1_pos_cible.setData(*zip(*self.counter_values_pos_cible_1))
            self.curve_2_pwm_reel.setData(*zip(*self.counter_values_pwm_reel_2))
            self.curve_2_pwm_cible.setData(*zip(*self.counter_values_pwm_cible_2))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
