import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
import numpy as np
from scipy.ndimage import median_filter
import pyqtgraph.exporters as pe
import re

def moyenne_glissante_np(tableau, taille):
    if taille <= 0 or not isinstance(taille, int):
        raise ValueError("La taille de la moyenne glissante doit être un entier positif.")

    if not isinstance(tableau, np.ndarray):
        raise ValueError("Le tableau doit être de type numpy.ndarray.")

    if taille > len(tableau):
        raise ValueError("La taille de la fenêtre glissante ne peut pas être plus grande que la taille du tableau d'entrée.")

    resultats = np.zeros_like(tableau, dtype=float)
    
    # Remplir les premières positions avec les données du tableau d'entrée
    resultats[:taille-1] = tableau[:taille-1]

    for i in range(taille-1, len(tableau)):
        moyenne = np.mean(tableau[i - taille + 1:i + 1])
        resultats[i] = moyenne

    return resultats

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
        self.median_value = 3
        self.update_plots()
        
    def update_plots(self):
        print(self.nom_fichier)
        with open(self.nom_fichier, 'r', encoding="ISO-8859-1") as fichier:
            compteur_lignes = 0

            for ligne in fichier:
                print(ligne)
                if compteur_lignes < 3:
                    compteur_lignes += 1
                    continue
                if ligne.startswith("$SOPE"):
                        continue 
                ligne_sans_prefixe = ligne.strip().replace("L22#", "")
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
            
            vitesses_filtre = median_filter(vitesses, size=self.median_value)
            #vitesses_filtre = moyenne_glissante_np(vitesses_filtre_median, self.median_value)
            vitesses_filtre[np.isnan(vitesses_filtre)] = 0 # enleve les nan

            print("Temps_0 : ", temp_0)
            print("Nombres de valeurs echantilllone : ",len(data_array_values_pos_reel))
            print("V max : ", max(vitesses_filtre))
            print("V moyenne : ", np.sum(np.absolute(vitesses_filtre)) / len(vitesses_filtre) )
            print("Pourcentage de valeur filtre : ",round((self.median_value / len(vitesses_filtre)) * 100, 2))

            self.plot_widget_vitesse.setYRange(-0.5, 0.5)
            self.plot_widget_vitesse.setXRange(0, max(temps))
            self.plot_widget_1.setXRange(0, max(temps))
            self.plot_widget_2.setXRange(0, max(temps))

            self.curve_vitesse.setData(temps, vitesses_filtre) 

            # courbe dans la fenetre
            # donnees_croissantes = np.linspace(0, max(temps), len(temps))
            # self.curve_t.setData(donnees_croissantes, temps) 
            # self.curve_1_pos_reel.setData(*zip(*self.counter_values_pos_reel_1))
            # self.curve_1_pos_cible.setData(*zip(*self.counter_values_pos_cible_1))
            # self.curve_2_pwm_reel.setData(*zip(*self.counter_values_pwm_reel_2))
            # self.curve_2_pwm_cible.setData(*zip(*self.counter_values_pwm_cible_2))
            
            # points dans la fenetre
            donnees_croissantes = np.linspace(0, max(temps), len(temps))
            self.plot_widget_vitesse.plot(temps, vitesses_filtre, pen=None, symbol='o', symbolPen='g', symbolBrush='g', name='reel')
            self.plot_widget_t.plot(donnees_croissantes, temps, pen=None, symbol='o', symbolPen='g', symbolBrush='g', name='reel')
            self.plot_widget_1.plot(*zip(*self.counter_values_pos_reel_1), pen=None, symbol='o', symbolPen='g', symbolBrush='g', name='reel')
            self.plot_widget_1.plot(*zip(*self.counter_values_pos_cible_1), pen=None, symbol='o', symbolPen='r', symbolBrush='r', name='target')
            self.plot_widget_2.plot(*zip(*self.counter_values_pwm_reel_2), pen=None, symbol='o', symbolPen='g', symbolBrush='g', name='reel')
            self.plot_widget_2.plot(*zip(*self.counter_values_pwm_cible_2), pen=None, symbol='o', symbolPen='r', symbolBrush='r', name='target')

if __name__ == "__main__":
    app = QApplication(sys.argv)

   # main_window = MainWindow("C:/Archive/ENSEIRB/Controle moteur/data_ACQ/donnees_serie_23_150kg_12.31V_22.8A_25.4A_acq3_2024-01-12_15-44-07.txt")
    a ="C:/Archive/ENSEIRB/Controle moteur/data_ACQ_2/"
    b = "donnees_serie_22_1kg_12.31V_23.5A_acq3_2024-01-15_14-27-46.txt"


    c = a + b
    main_window = MainWindow(c)

    main_window.show()
    sys.exit(app.exec_())
