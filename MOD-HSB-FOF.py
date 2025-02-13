import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import threading
import psutil

# Dicionário de traduções
TRANSLATIONS = {
    "Português": {
        "game_running": "Feche o Fistful of Frags antes de continuar",
        "select_backup": "Selecione o backup para restaurar",
        "restore_success": "Arquivo original restaurado com sucesso!",
        "no_backups": "Nenhum backup encontrado para restaurar",
        "restore_button": "Restaurar Original",
        "window_title": "Instalador do Mod - Fistful of Frags",
        "header": "Instalador do Mod - Fistful of Frags",
        "checking_install": "Verificando instalação...",
        "game_found": "Jogo encontrado. Pronto para instalar.",
        "select_location": "Selecione a localização do jogo",
        "install_button": "Instalar Mod",
        "browse_button": "Selecionar Local",
        "log_title": "Log de instalação:",
        "game_found_default": "Jogo encontrado no local padrão",
        "game_not_found": "Jogo não encontrado no local padrão",
        "new_location": "Novo local do jogo: {}",
        "invalid_selection": "Seleção inválida ou cancelada",
        "checking_files": "Verificando arquivos...",
        "mod_not_found": "Arquivo do mod não encontrado",
        "mod_verified": "Arquivo do mod verificado",
        "original_not_found": "client.dll original não encontrado",
        "original_found": "client.dll original encontrado",
        "backup_created": "Backup criado: {}",
        "install_success": "Mod instalado com sucesso!",
        "install_complete": "Instalação concluída com sucesso!",
        "success_title": "Sucesso",
        "success_message": "Mod instalado com sucesso!",
        "error_title": "Erro",
        "error_message": "Erro durante a instalação:\n{}",
        "select_exe": "1. Abra a pasta do Steam.\n2. Navegue até: steamapps\\common\\Fistful of Frags\\sdk.\n3. Selecione o arquivo \"hl2.exe\".",
        "language_label": "Idioma",
    },
    "English": {
        "game_running": "Please close Fistful of Frags before continuing",
        "select_backup": "Select backup to restore",
        "restore_success": "Original file restored successfully!",
        "no_backups": "No backups found to restore",
        "restore_button": "Restore Original",
        "window_title": "Mod Installer - Fistful of Frags",
        "header": "Mod Installer - Fistful of Frags",
        "checking_install": "Checking installation...",
        "game_found": "Game found. Ready to install.",
        "select_location": "Select game location",
        "install_button": "Install Mod",
        "browse_button": "Browse Location",
        "log_title": "Installation log:",
        "game_found_default": "Game found in default location",
        "game_not_found": "Game not found in default location",
        "new_location": "New game location: {}",
        "invalid_selection": "Invalid or canceled selection",
        "checking_files": "Checking files...",
        "mod_not_found": "Mod file not found",
        "mod_verified": "Mod file verified",
        "original_not_found": "Original client.dll not found",
        "original_found": "Original client.dll found",
        "backup_created": "Backup created: {}",
        "install_success": "Mod installed successfully!",
        "install_complete": "Installation completed successfully!",
        "success_title": "Success",
        "success_message": "Mod installed successfully!",
        "error_title": "Error",
        "error_message": "Error during installation:\n{}",
        "select_exe": "Select hl2.exe file",
        "language_label": "Language",
    },
    "Français": {
        "game_running": "Veuillez fermer Fistful of Frags avant de continuer",
        "select_backup": "Sélectionnez la sauvegarde",
        "restore_success": "Fichier original restauré avec succès!",
        "no_backups": "Aucune sauvegarde trouvée à restaurer",
        "restore_button": "Restaurer Original",
        "window_title": "Installateur de Mod - Fistful of Frags",
        "header": "Installateur de Mod - Fistful of Frags",
        "checking_install": "Vérification de l'installation...",
        "game_found": "Jeu trouvé. Prêt à installer.",
        "select_location": "Sélectionnez l'emplacement du jeu",
        "install_button": "Installer le Mod",
        "browse_button": "Parcourir",
        "log_title": "Journal d'installation:",
        "game_found_default": "Jeu trouvé dans l'emplacement par défaut",
        "game_not_found": "Jeu non trouvé dans l'emplacement par défaut",
        "new_location": "Nouvel emplacement du jeu: {}",
        "invalid_selection": "Sélection invalide ou annulée",
        "checking_files": "Vérification des fichiers...",
        "mod_not_found": "Fichier mod non trouvé",
        "mod_verified": "Fichier mod vérifié",
        "original_not_found": "client.dll original non trouvé",
        "original_found": "client.dll original trouvé",
        "backup_created": "Sauvegarde créée: {}",
        "install_success": "Mod installé avec succès!",
        "install_complete": "Installation terminée avec succès!",
        "success_title": "Succès",
        "success_message": "Mod installé avec succès!",
        "error_title": "Erreur",
        "error_message": "Erreur lors de l'installation:\n{}",
        "select_exe": "Sélectionnez le fichier hl2.exe",
        "language_label": "Langue",
    },
    "Español": {
        "game_running": "Por favor, cierre Fistful of Frags antes de continuar",
        "select_backup": "Seleccione la copia de seguridad",
        "restore_success": "¡Archivo original restaurado con éxito!",
        "no_backups": "No se encontraron copias de seguridad",
        "restore_button": "Restaurar Original",
        "window_title": "Instalador de Mod - Fistful of Frags",
        "header": "Instalador de Mod - Fistful of Frags",
        "checking_install": "Verificando instalación...",
        "game_found": "Juego encontrado. Listo para instalar.",
        "select_location": "Seleccione la ubicación del juego",
        "install_button": "Instalar Mod",
        "browse_button": "Seleccionar Ubicación",
        "log_title": "Registro de instalación:",
        "game_found_default": "Juego encontrado en la ubicación predeterminada",
        "game_not_found": "Juego no encontrado en la ubicación predeterminada",
        "new_location": "Nueva ubicación del juego: {}",
        "invalid_selection": "Selección inválida o cancelada",
        "checking_files": "Verificando archivos...",
        "mod_not_found": "Archivo mod no encontrado",
        "mod_verified": "Archivo mod verificado",
        "original_not_found": "client.dll original no encontrado",
        "original_found": "client.dll original encontrado",
        "backup_created": "Copia de seguridad creada: {}",
        "install_success": "¡Mod instalado con éxito!",
        "install_complete": "¡Instalación completada con éxito!",
        "success_title": "Éxito",
        "success_message": "¡Mod instalado con éxito!",
        "error_title": "Error",
        "error_message": "Error durante la instalación:\n{}",
        "select_exe": "Seleccione el archivo hl2.exe",
        "language_label": "Idioma",
    }
}


def is_game_running():
    """Check if hl2.exe is currently running"""
    for process in psutil.process_iter(['name']):
        try:
            if process.info['name'].lower() == 'hl2.exe':
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False


class InstallerGUI:
    def __init__(self):
        self.backup_path = None
        self.log_text = None
        self.log_label = None
        self.restore_button = None
        self.browse_button = None
        self.install_button = None
        self.progress = None
        self.header_label = None
        self.language_var = None
        self.root = tk.Tk()
        self.current_language = "English"
        self.setup_window()

        # Configurações do instalador
        self.default_game_path = r"D:\Program Files (x86)\Steam\steamapps\common\Fistful of Frags"
        self.hl2_exe_path = os.path.join(self.default_game_path, "sdk", "hl2.exe")
        self.client_dll_path = os.path.join(self.default_game_path, "fof", "bin", "client.dll")
        self.mod_dll_path = "mod_client.dll"

        self.setup_gui()

    def setup_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 600
        window_height = 400
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        self.root.title(TRANSLATIONS[self.current_language]["window_title"])
        self.root.resizable(False, False)
        self.root.iconbitmap("fof.ico")

    def setup_gui(self):
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f0f0")
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), padding=10)
        style.configure("Info.TLabel", font=("Helvetica", 10), padding=5)

        # Container principal
        main_frame = ttk.Frame(self.root, style="Custom.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Seletor de idioma
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill=tk.X, pady=(0, 10))

        self.language_label = ttk.Label(lang_frame, text=TRANSLATIONS[self.current_language]["language_label"])
        self.language_label.pack(side=tk.LEFT)

        self.language_var = tk.StringVar(value=self.current_language)
        language_menu = ttk.Combobox(lang_frame, textvariable=self.language_var, width=10)
        language_menu['values'] = ['English', 'Português', 'Français', 'Español']
        language_menu.pack(side=tk.LEFT, padx=5)
        language_menu.bind('<<ComboboxSelected>>', self.change_language)

        # Cabeçalho
        self.header_label = ttk.Label(
            main_frame,
            text=TRANSLATIONS[self.current_language]["header"],
            style="Header.TLabel"
        )
        self.header_label.pack(pady=(0, 20))

        # Barra de progresso
        self.progress = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            length=500,
            mode="determinate"
        )
        self.progress.pack(pady=20)

        # Frame para botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        # Botões
        self.install_button = ttk.Button(
            button_frame,
            text=TRANSLATIONS[self.current_language]["install_button"],
            command=self.start_installation,
            width=20
        )
        self.install_button.pack(side=tk.LEFT, padx=5)

        self.browse_button = ttk.Button(
            button_frame,
            text=TRANSLATIONS[self.current_language]["browse_button"],
            command=self.browse_location,
            width=20
        )
        self.browse_button.pack(side=tk.LEFT, padx=5)

        self.restore_button = ttk.Button(
            button_frame,
            text=TRANSLATIONS[self.current_language]["restore_button"],
            command=self.restore_backup,
            width=20
        )
        self.restore_button.pack(side=tk.LEFT, padx=5)

        # Log de instalação
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        self.log_label = ttk.Label(log_frame, text=TRANSLATIONS[self.current_language]["log_title"])
        self.log_label.pack(anchor=tk.W)

        # log font size
        self.log_text = tk.Text(log_frame, height=8, width=100, font=("Helvetica", 10))
        self.log_text.pack(pady=5)

        # Verificação inicial
        self.verify_initial_installation()

    def change_language(self, _event=None):
        self.current_language = self.language_var.get()
        self.update_texts()

    def update_texts(self):
        # Atualiza os textos da interface
        self.root.title(TRANSLATIONS[self.current_language]["window_title"])
        self.header_label.config(text=TRANSLATIONS[self.current_language]["header"])
        self.install_button.config(text=TRANSLATIONS[self.current_language]["install_button"])
        self.browse_button.config(text=TRANSLATIONS[self.current_language]["browse_button"])
        self.restore_button.config(text=TRANSLATIONS[self.current_language]["restore_button"])
        self.log_label.config(text=TRANSLATIONS[self.current_language]["log_title"])
        self.language_label.config(text=TRANSLATIONS[self.current_language]["language_label"])

        # Limpa o log atual
        self.log_text.delete(1.0, tk.END)

        # Re-verifica a instalação para atualizar o log com o novo idioma
        self.verify_initial_installation()

    def verify_initial_installation(self):
        if os.path.exists(self.hl2_exe_path):
            self.log(TRANSLATIONS[self.current_language]["game_found_default"])
            self.install_button.config(state=tk.NORMAL)
        else:
            self.log(TRANSLATIONS[self.current_language]["game_not_found"])
            self.install_button.config(state=tk.DISABLED)

    # Rest of the methods remain the same...
    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

    def browse_location(self):
        if is_game_running():
            messagebox.showwarning("", TRANSLATIONS[self.current_language]["game_running"])
            return

        messagebox.showinfo("", TRANSLATIONS[self.current_language]["select_exe"])
        filepath = filedialog.askopenfilename(
            title=TRANSLATIONS[self.current_language]["select_exe"],
            filetypes=[("Executável", "*.exe")]
        )

        if filepath and os.path.basename(filepath) == "hl2.exe":
            self.default_game_path = os.path.dirname(os.path.dirname(filepath))
            self.client_dll_path = os.path.join(self.default_game_path, "fof", "bin", "client.dll")
            self.log(TRANSLATIONS[self.current_language]["new_location"].format(self.default_game_path))
            self.install_button.config(state=tk.NORMAL)
        else:
            self.log(TRANSLATIONS[self.current_language]["invalid_selection"])

    def start_installation(self):
        if is_game_running():
            messagebox.showwarning("Warning", TRANSLATIONS[self.current_language]["game_running"])
            return

        self.install_button.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.install_mod)
        thread.start()

    def install_mod(self):
        try:
            self.progress["value"] = 0

            if not os.path.exists(self.mod_dll_path):
                raise Exception(TRANSLATIONS[self.current_language]["mod_not_found"])

            self.progress["value"] = 25
            self.log(TRANSLATIONS[self.current_language]["mod_verified"])

            if not os.path.exists(self.client_dll_path):
                raise Exception(TRANSLATIONS[self.current_language]["original_not_found"])

            self.progress["value"] = 50
            self.log(TRANSLATIONS[self.current_language]["original_found"])

            backup_dir = os.path.dirname(self.client_dll_path)
            self.backup_path = os.path.join(backup_dir, "client.dll.backup")
            if os.path.exists(self.backup_path):
                os.remove(self.backup_path)

            shutil.copy2(self.client_dll_path, self.backup_path)

            self.progress["value"] = 75
            self.log(TRANSLATIONS[self.current_language]["backup_created"].format("client.dll.backup"))

            shutil.copy2(self.mod_dll_path, self.client_dll_path)

            self.progress["value"] = 100
            self.log(TRANSLATIONS[self.current_language]["install_success"])

            messagebox.showinfo(
                TRANSLATIONS[self.current_language]["success_title"],
                TRANSLATIONS[self.current_language]["success_message"]
            )

        except Exception as e:
            self.log(f"{str(e)}")
            messagebox.showerror(
                TRANSLATIONS[self.current_language]["error_title"],
                TRANSLATIONS[self.current_language]["error_message"].format(str(e))
            )

        finally:
            self.install_button.config(state=tk.NORMAL)
            self.browse_button.config(state=tk.NORMAL)

    def find_backups(self):
        backup_dir = os.path.dirname(self.client_dll_path)
        if not os.path.exists(backup_dir):
            return []

        backups = []
        for file in os.listdir(backup_dir):
            if file.startswith("client.dll.backup_"):
                backups.append(file)

        return sorted(backups, reverse=True)

    def restore_backup(self):
        if is_game_running():
            messagebox.showwarning("Warning", TRANSLATIONS[self.current_language]["game_running"])
            return

        backup_dir = os.path.dirname(self.client_dll_path)
        backup_path = os.path.join(backup_dir, "client.dll.backup")

        if not os.path.exists(backup_path):
            messagebox.showinfo(
                TRANSLATIONS[self.current_language]["error_title"],
                TRANSLATIONS[self.current_language]["no_backups"]
            )
            return

        try:
            shutil.copy2(backup_path, self.client_dll_path)
            self.log(TRANSLATIONS[self.current_language]["restore_success"])
            messagebox.showinfo(
                "",
                TRANSLATIONS[self.current_language]["restore_success"]
            )
            self.progress["value"] = 0

        except Exception as e:
            messagebox.showerror(
                TRANSLATIONS[self.current_language]["error_title"],
                TRANSLATIONS[self.current_language]["error_message"].format(str(e))
            )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = InstallerGUI()
    app.run()
