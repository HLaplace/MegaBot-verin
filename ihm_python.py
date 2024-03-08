import tkinter as tk
import serial.tools.list_ports
import serial
from colorama import Fore, Style, init

# Initialisation de colorama
init(autoreset=True)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Création des boutons LED
        self.buttons = []
        for i in range(4):
            col = []
            for j in range(3):
                button = tk.Button(self, text=f"LED {i +1},{j+1}", command=lambda row=i, col=j: self.button_click(row +1, col +1))
                button.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                col.append(button)
            self.buttons.append(col)

        # Bouton pour afficher les ports série
        self.serial_button = tk.Button(self, text="Afficher les ports série", command=self.list_serial_ports)
        self.serial_button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

        # Menu déroulant pour afficher les ports série
        self.serial_var = tk.StringVar(self)
        self.serial_dropdown = tk.OptionMenu(self, self.serial_var, "Sélectionnez un port")
        self.serial_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

        # Bouton pour uploader le code dans la carte sélectionnée
        self.upload_button = tk.Button(self, text="Uploader le code", command=self.upload_code)
        self.upload_button.grid(row=4, column=2, padx=5, pady=5, sticky="nsew")

        # Configurer le système de gestion de la grille pour rendre l'interface responsive
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for j in range(3):
            self.grid_columnconfigure(j, weight=1)

    def button_click(self, row, col):
        message = f"L{row}{col}"
        print(message)  # Écrit dans le terminal de l'ordinateur
        selected_port = self.serial_var.get()
        if selected_port == "Sélectionnez un port":
            print(Fore.RED + "Veuillez sélectionner un port série." + Style.RESET_ALL)
            return
        try:
            with serial.Serial(selected_port, 115200, timeout=0.5) as ser:
                ser.write(message.encode())  # Envoie le message à la carte sur le port série
            print(Fore.GREEN + f"Message envoyé avec succès à {selected_port}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Erreur lors de l'envoi du message sur le port série : {e}" + Style.RESET_ALL)

    def list_serial_ports(self):
        """Liste les ports série disponibles sur le système."""
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        self.serial_var.set("Sélectionnez un port")
        self.serial_dropdown['menu'].delete(0, 'end')
        for port in port_list:
            self.serial_dropdown['menu'].add_command(label=port, command=tk._setit(self.serial_var, port))
        print(Fore.GREEN + "Ports série listés avec succès." + Style.RESET_ALL)

    def upload_code(self):
        """Uploader le code dans la carte sélectionnée."""
        selected_port = self.serial_var.get()
        if selected_port == "Sélectionnez un port":
            print(Fore.RED + "Veuillez sélectionner un port série." + Style.RESET_ALL)
            return
        try:
            with serial.Serial(selected_port, 115200, timeout=30) as ser:
                with open("ihm_test_led.ino", "r") as file:
                    code = file.read()
                ser.write(code.encode())
            print(Fore.GREEN + "Code uploaded successfully." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error uploading code: {e}" + Style.RESET_ALL)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Test Contrôle LED & Ports Série")
root.geometry("450x550")

# Création de l'application
app = Application(master=root)
app.pack(fill="both", expand=True)

# Démarrage de la boucle principale
root.mainloop()
