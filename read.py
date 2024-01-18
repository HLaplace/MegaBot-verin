nom_fichier = "C:/Archive/ENSEIRB/Controle moteur/data_ACQ/donnees_serie_acquisition_verrin_23_2024-01-10_11-48-11.txt"

variable1 = 0.0
variable2 = 0.0
variable3 = 0.0
variable4 = 0.0
variable5 = 0.0

with open(nom_fichier, 'r') as fichier:
    compteur_lignes = 0

    for ligne in fichier:
                # Ignorer les trois premières lignes
        if compteur_lignes < 3:
            compteur_lignes += 1
            continue

        ligne_sans_prefixe = ligne.strip().replace("L23#", "")
        valeurs = ligne_sans_prefixe.split('#')

        variable1 = float(valeurs[0])
        variable2 = float(valeurs[1])
        variable3 = float(valeurs[2])
        variable4 = float(valeurs[3])
        variable5 = float(valeurs[4])

        print("Variable 1 :", variable1)
        print("Variable 2 :", variable2)
        print("Variable 3 :", variable3)
        print("Variable 4 :", variable4)
        print("Variable 5 :", variable5)

