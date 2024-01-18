import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
import numpy as np
from scipy.ndimage import median_filter
import pyqtgraph.exporters as pe
import re
class MainWindow(QMainWindow):

    def __init__(self, chemin):
        super(MainWindow, self).__init__()

        self.nom_fichier = chemin
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.plot_widget_vitesse = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget_vitesse)
        #self.plot_widget_vitesse.plotItem.layout.setContentsMargins(0, 0, 0, 0)  # Ajustement des marges
        self.curve_vitesse = self.plot_widget_vitesse.plot(pen='g', name='reel')
        self.plot_widget_vitesse.plotItem.showGrid(True, True, alpha=0.5)  

        self.plot_widget_t = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget_t)
        #self.plot_widget_t.plotItem.layout.setContentsMargins(0, 0, 0, 0)  # Ajustement des marges
        self.curve_t = self.plot_widget_t.plot(pen='g', name='reel')
        self.plot_widget_t.plotItem.showGrid(True, True, alpha=0.5)  

        self.plot_widget_1 = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget_1)
        #self.plot_widget_1.plotItem.layout.setContentsMargins(0, 0, 0, 0)  # Ajustement des marges
        self.curve_1_pos_reel = self.plot_widget_1.plot(pen='g', name='reel')  
        self.curve_1_pos_cible = self.plot_widget_1.plot(pen='r', name='target')  
        self.plot_widget_1.plotItem.showGrid(True, True, alpha=0.5) 

        self.plot_widget_2 = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget_2)
        #self.plot_widget_2.plotItem.layout.setContentsMargins(0, 0, 0, 0)  # Ajustement des marges
        self.curve_2_pwm_reel = self.plot_widget_2.plot(pen='g', name='reel')  
        self.curve_2_pwm_cible = self.plot_widget_2.plot(pen='r', name='target')  
        self.plot_widget_2.plotItem.showGrid(True, True, alpha=0.5) 

        self.counter_values_pos_reel_1 = []
        self.counter_values_pos_cible_1 = []
        self.counter_values_pwm_reel_2 = []
        self.counter_values_pwm_cible_2 = []

        self.verify = False
        self.median_value = 30
        self.update_plots()
        
    def update_plots(self):
        with open(self.nom_fichier, 'r', encoding="ISO-8859-1") as fichier:
            compteur_lignes = 0

            for ligne in fichier:
                if compteur_lignes < 3:
                    compteur_lignes += 1
                    continue
                if ligne.startswith("$SOPE"):
                        continue 
                ligne_sans_prefixe = ligne.strip().replace("L23#", "")
                tab_valeurs = ligne_sans_prefixe.split('#')

                if len(tab_valeurs) < 5:
                    continue

                if self.verify == False:
                    temp_0 = float(tab_valeurs[4])
                    print("Temps_0 : ", temp_0)
                    self.verify = True

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
            temps = data_array_values_pos_reel[:, 0] # s
            positions = data_array_values_pos_reel[:, 1] # m
            
            with np.errstate(divide='ignore', invalid='ignore'):# gere le 0 divide error
                vitesses = np.gradient(positions, temps)
            
            print("Nombres de valeurs echantilllone : ",len(data_array_values_pos_reel))
            vitesses_filtre = median_filter(vitesses, size=self.median_value)
            print("V max : ", max(vitesses_filtre))
            vitesses_filtre[np.isnan(vitesses_filtre)] = 0 # enleve les nan
            print("V moyenne : ", np.sum(np.absolute(vitesses_filtre)) / len(vitesses_filtre) )

            self.plot_widget_vitesse.setYRange(-0.5, 0.5)
            self.plot_widget_vitesse.setXRange(0, max(temps))
            self.plot_widget_1.setXRange(0, max(temps))
            self.plot_widget_2.setXRange(0, max(temps))

            self.curve_vitesse.setData(temps, vitesses_filtre) 

            donnees_croissantes = np.linspace(0, max(temps), len(temps))
            self.curve_t.setData(donnees_croissantes, temps) 

            self.curve_1_pos_reel.setData(*zip(*self.counter_values_pos_reel_1))
            self.curve_1_pos_cible.setData(*zip(*self.counter_values_pos_cible_1))

            self.curve_2_pwm_reel.setData(*zip(*self.counter_values_pwm_reel_2))
            self.curve_2_pwm_cible.setData(*zip(*self.counter_values_pwm_cible_2))
            print("Pourcentage de valeur filtre : ",round((self.median_value / len(vitesses_filtre)) * 100, 2))

if __name__ == "__main__":
    app = QApplication(sys.argv)

   # main_window = MainWindow("C:/Archive/ENSEIRB/Controle moteur/data_ACQ/donnees_serie_23_150kg_12.31V_22.8A_25.4A_acq3_2024-01-12_15-44-07.txt")
    a ="C:/Archive/ENSEIRB/Controle moteur/data_ACQ/"

    b = "donnees_serie_23_111kg_12.37V_24.9A_22.9A_acq4_2024-01-12_15-25-47.txt"

    c = a + b
    main_window = MainWindow(c)

    main_window.show()
    sys.exit(app.exec_())
