# serie.py
import os
import serial
from datetime import datetime
import keyboard  # Ajout de la bibliothèque keyboard
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

maintenant = datetime.now()
date_heure_formattees = maintenant.strftime("%Y-%m-%d_%H-%M-%S")
annexe = "170kg_12.23V_acq5"
# annexe = "testets1"

annexe = "22_" + annexe + "_"
titre_document = f"data_ACQ_2/donnees_serie_{annexe + date_heure_formattees}.txt"

dossier = os.path.dirname(titre_document)
if not os.path.exists(dossier):
    os.makedirs(dossier)

port_COM = 'COM5'
baudrate = 576000
ser = serial.Serial(port_COM, baudrate)
ser.write(b'T\n')

with open(titre_document, 'w') as fichier:
    fichier.write(f"Port COM: {port_COM}\n")
    fichier.write(f"Baudrate: {baudrate}\n")
    fichier.write("Données reçues :\n")


    while True:
        ligne = ser.readline()

        donnee_str = ligne.decode('utf-8').strip()

        fichier.write(donnee_str + '\n')

