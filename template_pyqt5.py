import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont

class CSVViewer(QWidget):
    def __init__(self, file_path):
        super().__init__()

        self.file_path = file_path
        self.init_ui()

    def init_ui(self):
        # Charger les données CSV depuis le fichier
        data = self.load_csv()

        # Créer l'interface utilisateur avec une mise en page verticale
        layout = QVBoxLayout(self)

        # Ajouter une étiquette pour chaque ligne de données
        for row in data:
            label = QLabel(row[0], self)
            label.setFont(QFont('Arial', 12))
            layout.addWidget(label)

        self.setWindowTitle('CSV Viewer')
        self.show()

    def load_csv(self):
        data = []
        try:
            with open(self.file_path, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    data.append(row)
        except FileNotFoundError:
            print(f"Fichier {self.file_path} non trouvé.")
            sys.exit(1)
        except Exception as e:
            print(f"Une erreur s'est produite lors de la lecture du fichier CSV : {e}")
            sys.exit(1)
        return data

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Utilisation : python script.py chemin/vers/fichier.csv")
        sys.exit(1)

    app = QApplication(sys.argv)
    viewer = CSVViewer(sys.argv[1])
    sys.exit(app.exec_())
