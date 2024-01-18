import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
import numpy as np
from scipy.ndimage import median_filter
import re
import os
import matplotlib.pyplot as plt
from scipy.stats import linregress

def extraire_poids(chaine):
    match = re.search(r'(\d+(\.\d+)?)kg', chaine)
    
    if match:
        poids_str = match.group(1)
        poids_entier = int(float(poids_str))
        return poids_entier
    else:
        print("Aucun poids trouvé dans la chaîne.")
        return None

def moyenne(tab):
    tab_sans_nan = [x for x in tab if not np.isnan(x)]
    somme = sum(tab_sans_nan)
    moyenne = somme / len(tab_sans_nan)
    return moyenne

def stat(nom_fichier):
    verify = False
    counter_values_pos_reel_1 = []
    counter_values_pwm_cible = []
    vit_positive = []
    vit_negative = []
    affichage = False
    base = "C:/Archive/ENSEIRB/Controle moteur/data_ACQ/"

    with open(base + nom_fichier, 'r', encoding="ISO-8859-1") as fichier:
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

            if verify == False:
                temp_0 = float(tab_valeurs[4])
                verify = True

            flt_pos_reel = float(tab_valeurs[0])
            flt_pwm_cible = float(tab_valeurs[3])
            flt_temp = float(tab_valeurs[4]) - temp_0

            counter_values_pos_reel_1.append((flt_temp, flt_pos_reel))
            counter_values_pwm_cible.append((flt_temp, flt_pwm_cible))

        data_array_values_pos_reel = np.array(counter_values_pos_reel_1)
        temps = data_array_values_pos_reel[:, 0]
        positions = data_array_values_pos_reel[:, 1]

        delta_positions = np.diff(positions)
        delta_temps = np.diff(temps)

        with np.errstate(divide='ignore', invalid='ignore'):
            vitesses = np.gradient(positions, temps)


        median_value = len(vitesses) * 0.01
        vitesses_filtre = median_filter(vitesses, size=int(median_value))
        #print("valeur du filtre :", str(int(median_value)))
        vit_positive = []
        vit_negative = []

        for i in range (0 ,len(vitesses_filtre)):
            if counter_values_pwm_cible[i][1] > 0:
                vit_positive.append(vitesses_filtre[i])
            else :
                vit_negative.append(vitesses_filtre[i])

        moyenn_vitesse_positive = moyenne(vit_positive)
        moyenne_vitesse_negative = moyenne(vit_negative)
        masse = extraire_poids(nom_fichier)

        if affichage == True:

            ### courbe ###
            app = QApplication(sys.argv)
            win = QMainWindow()
            central_widget = QWidget()
            layout = QVBoxLayout()
            graphique = pg.PlotWidget()
            
            courbe_vitesses_filtre = graphique.plot(temps, vitesses_filtre, pen='g')  # Ajout de la première courbe 
            courbe_pwm_cible = graphique.plot(temps, [item[1] for item in counter_values_pwm_cible], pen='r')  # Ajout de la deuxième courbe 

            layout.addWidget(graphique)
            central_widget.setLayout(layout)
            win.setCentralWidget(central_widget)
            win.show()
            sys.exit(app.exec_())
        return masse, moyenn_vitesse_positive, moyenne_vitesse_negative

### executions sur un fichier ##
#b = "donnees_serie_23_121kg_12.36V_22.8A_24.3A_acq3_2024-01-12_15-29-07.txt"
#t = stat(b)
#print("Pour une masse de ", t[0], "on a une vitesse positive moyenne de :", t[1],
  #  "m/s et une vitesse moyenne negative de ", t[2], "m/s.")

### executions sur plusieurs fichiers ##


# Chemin du répertoire
repertoire_specifie = "C:/Archive/ENSEIRB/Controle moteur/data_ACQ/"
tab_donnees = []
if os.path.exists(repertoire_specifie) and os.path.isdir(repertoire_specifie):
    for nom_fichier in os.listdir(repertoire_specifie):
        chemin_fichier = os.path.join(repertoire_specifie, nom_fichier)
        print(nom_fichier)
        t = stat(nom_fichier)
        tab_donnees.append(t)
        print("Pour une masse de ", t[0], "on a une vitesse positive moyenne de :", t[1],
             "m/s et une vitesse moyenne negative de ", t[2], "m/s.")
else:
    print("Le répertoire spécifié n'existe pas ou n'est pas un répertoire.")

x, y1, y2 = zip(*tab_donnees)

plt.scatter(x, y1, label='vitesse moyenne positive')
plt.scatter(x, y2, label='vitesse moyenne negative')

coefficients_y1 = np.polyfit(x, y1, 2)
polynome_deg2_y1 = np.poly1d(coefficients_y1)
y1_predites = polynome_deg2_y1(x)
plt.plot(x, y1_predites, label='Régression quadratique (y1)')

coefficients_y2 = np.polyfit(x, y2, 2)
polynome_deg2_y2 = np.poly1d(coefficients_y2)
y2_predites = polynome_deg2_y2(x)
plt.plot(x, y2_predites, label='Régression quadratique (y2)')

plt.legend()
plt.title('Tracé des vitesses moyennes avec régression quadratique')
plt.show()
