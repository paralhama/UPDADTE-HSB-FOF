import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import threading
import psutil
import locale
import ctypes

# Define um ID único para o programa, evitando o ícone genérico do Python
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("meu.programa.fof")

# Dicionário de traduções
TRANSLATIONS = {
    "Português": {
        "game_running": "Feche o Fistful of Frags antes de continuar",
        "restore_success": "Arquivo original restaurado com sucesso!",
        "restore_button": "Restaurar Original",
        "window_title": "Instalador do Mod - Fistful of Frags",
        "header": "Instalador do Mod - Fistful of Frags",
        "install_button": "Instalar Mod",
        "browse_button": "Selecionar Local",
        "log_title": "Log de instalação:",
        "game_found_default": "Jogo encontrado no local padrão",
        "game_not_found": "Jogo não encontrado no local padrão",
        "new_location": "Jogo localizado: {}",
        "invalid_selection": "Seleção inválida ou cancelada",
        "mod_not_found": "Arquivo do mod não encontrado",
        "mod_verified": "Arquivo do mod verificado",
        "original_not_found": "client.dll original não encontrado",
        "original_found": "client.dll original encontrado",
        "backup_created": "Backup criado: {}",
        "install_success": "Mod instalado com sucesso!",
        "success_title": "Sucesso",
        "success_message": "Mod instalado com sucesso!",
        "error_title": "Erro",
        "error_message": "Erro durante a instalação:\n{}",
        "select_folder": "Localize a pasta de instalação do Fistful of Frags.\n1. Navegue até: steamapps\\common\\Fistful of Frags\\sdk.\n2. Selecione o arquivo \"hl2.exe\".",
        "select_exe": "Selecione o arquivo hl2.exe na pasta: steamapps\\common\\Fistful of Frags\\sdk.",
        "language_label": "Idioma",
    },
    "English": {
        "game_running": "Please close Fistful of Frags before continuing",
        "restore_success": "Original file restored successfully!",
        "restore_button": "Restore Original",
        "window_title": "Mod Installer - Fistful of Frags",
        "header": "Mod Installer - Fistful of Frags",
        "install_button": "Install Mod",
        "browse_button": "Browse Location",
        "log_title": "Installation log:",
        "game_found_default": "Game found in default location",
        "game_not_found": "Game not found in default location",
        "new_location": "New game location: {}",
        "invalid_selection": "Invalid or canceled selection",
        "mod_not_found": "Mod file not found",
        "mod_verified": "Mod file verified",
        "original_not_found": "Original client.dll not found",
        "original_found": "Original client.dll found",
        "backup_created": "Backup created: {}",
        "install_success": "Mod installed successfully!",
        "success_title": "Success",
        "success_message": "Mod installed successfully!",
        "error_title": "Error",
        "error_message": "Error during installation:\n{}",
        "select_folder": "Select hl2.exe file",
        "select_exe": "Selecione o arquivo hl2.exe na pasta: steamapps\\common\\Fistful of Frags\\sdk.",
        "language_label": "Language",
    },
    "Français": {
        "game_running": "Veuillez fermer Fistful of Frags avant de continuer",
        "restore_success": "Fichier original restauré avec succès!",
        "restore_button": "Restaurer Original",
        "window_title": "Installateur de Mod - Fistful of Frags",
        "header": "Installateur de Mod - Fistful of Frags",
        "install_button": "Installer le Mod",
        "browse_button": "Parcourir",
        "log_title": "Journal d'installation:",
        "game_found_default": "Jeu trouvé dans l'emplacement par défaut",
        "game_not_found": "Jeu non trouvé dans l'emplacement par défaut",
        "new_location": "Nouvel emplacement du jeu: {}",
        "invalid_selection": "Sélection invalide ou annulée",
        "mod_not_found": "Fichier mod non trouvé",
        "mod_verified": "Fichier mod vérifié",
        "original_not_found": "client.dll original non trouvé",
        "original_found": "client.dll original trouvé",
        "backup_created": "Sauvegarde créée: {}",
        "install_success": "Mod installé avec succès!",
        "success_title": "Succès",
        "success_message": "Mod installé avec succès!",
        "error_title": "Erreur",
        "error_message": "Erreur lors de l'installation:\n{}",
        "select_folder": "Sélectionnez le fichier hl2.exe",
        "select_exe": "Selecione o arquivo hl2.exe na pasta: steamapps\\common\\Fistful of Frags\\sdk.",
        "language_label": "Langue",
    },
    "Español": {
        "game_running": "Por favor, cierre Fistful of Frags antes de continuar",
        "restore_success": "¡Archivo original restaurado con éxito!",
        "restore_button": "Restaurar Original",
        "window_title": "Instalador de Mod - Fistful of Frags",
        "header": "Instalador de Mod - Fistful of Frags",
        "install_button": "Instalar Mod",
        "browse_button": "Seleccionar Ubicación",
        "log_title": "Registro de instalación:",
        "game_found_default": "Juego encontrado en la ubicación predeterminada",
        "game_not_found": "Juego no encontrado en la ubicación predeterminada",
        "new_location": "Nueva ubicación del juego: {}",
        "invalid_selection": "Selección inválida o cancelada",
        "mod_not_found": "Archivo mod no encontrado",
        "mod_verified": "Archivo mod verificado",
        "original_not_found": "client.dll original no encontrado",
        "original_found": "client.dll original encontrado",
        "backup_created": "Copia de seguridad creada: {}",
        "install_success": "¡Mod instalado con éxito!",
        "success_title": "Éxito",
        "success_message": "¡Mod instalado con éxito!",
        "error_title": "Error",
        "error_message": "Error durante la instalación:\n{}",
        "select_folder": "Seleccione el archivo hl2.exe",
        "select_exe": "Selecione o arquivo hl2.exe na pasta: steamapps\\common\\Fistful of Frags\\sdk.",
        "language_label": "Idioma",
    }
}

# Mapeamento de códigos de idioma do sistema para idiomas suportados
LANGUAGE_MAPPING = {
    'pt': 'Português',
    'pt_BR': 'Português',
    'pt_PT': 'Português',
    'en': 'English',
    'fr': 'Français',
    'es': 'Español'
}


def get_system_language():
    """
    Detecta o idioma do sistema e retorna o idioma correspondente suportado pelo aplicativo.
    Se o idioma do sistema não for suportado, retorna 'English' como padrão.
    """
    try:
        # Configura o locale para o padrão do sistema
        locale.setlocale(locale.LC_ALL, '')
        # Obtém o código do idioma atual
        system_locale = locale.getlocale()[0]

        if system_locale:
            # Tenta primeiro o código completo (ex: pt_BR)
            if system_locale in LANGUAGE_MAPPING:
                return LANGUAGE_MAPPING[system_locale]
            # Tenta o código base (ex: pt)
            base_locale = system_locale.split('_')[0]
            if base_locale in LANGUAGE_MAPPING:
                return LANGUAGE_MAPPING[base_locale]
    except:
        pass
    return 'English'  # Idioma padrão caso não encontre correspondência


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
        self.language_label = None
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
        self.current_language = get_system_language()
        self.setup_window()

        # Configurações do instalador
        self.default_game_path = r"C:\Program Files (x86)\Steam\steamapps\common\Fistful of Frags"
        self.hl2_exe_path = os.path.join(self.default_game_path, "sdk", "hl2.exe")
        self.client_dll_path = os.path.join(self.default_game_path, "fof", "bin", "client.dll")
        self.mod_dll_path = "mod_client.dll"

        self.setup_gui()
        self.check_backup_status()

    def check_backup_status(self):
        """Verifica se existe backup e atualiza o estado do botão restore"""
        backup_dir = os.path.dirname(self.client_dll_path)
        backup_path = os.path.join(backup_dir, "client.dll.backup")

        if os.path.exists(backup_path):
            self.restore_button.config(state=tk.NORMAL)
        else:
            self.restore_button.config(state=tk.DISABLED)

    def verify_initial_installation(self):
        if os.path.exists(self.hl2_exe_path):
            self.log(TRANSLATIONS[self.current_language]["game_found_default"])
            self.install_button.config(state=tk.NORMAL)
        else:
            self.log(TRANSLATIONS[self.current_language]["game_not_found"])
            self.install_button.config(state=tk.DISABLED)

        # Verifica o status do backup após verificar a instalação
        self.check_backup_status()

    def setup_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 700
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
        self.language_label.pack(side=tk.TOP)  # Changed from BOTTOM to TOP

        self.language_var = tk.StringVar(value=self.current_language)
        language_menu = ttk.Combobox(lang_frame,
                                   textvariable=self.language_var,
                                   width=10,
                                   state="readonly")  # Adicionado state="readonly"
        language_menu['values'] = ['English', 'Português', 'Français', 'Español']
        language_menu.pack(side=tk.TOP, padx=5)  # Changed from BOTTOM to TOP
        language_menu.bind('<<ComboboxSelected>>', self.change_language)

        # Cabeçalho
        self.header_label = ttk.Label(
            main_frame,
            text=TRANSLATIONS[self.current_language]["header"],
            style="Header.TLabel"
        )
        self.header_label.pack(pady=(0, 20))

        # Frame para botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        # Barra de progresso
        self.progress = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            length=550,
            mode="determinate",
        )
        self.progress.pack(pady=1)

        # Botões
        self.install_button = ttk.Button(
            button_frame,
            text=TRANSLATIONS[self.current_language]["install_button"],
            command=self.start_installation,
            width=30
        )
        self.install_button.pack(side=tk.LEFT, padx=5)

        self.browse_button = ttk.Button(
            button_frame,
            text=TRANSLATIONS[self.current_language]["browse_button"],
            command=self.browse_location,
            width=30
        )
        self.browse_button.pack(side=tk.LEFT, padx=5)

        self.restore_button = ttk.Button(
            button_frame,
            text=TRANSLATIONS[self.current_language]["restore_button"],
            command=self.restore_backup,
            width=30
        )
        self.restore_button.pack(side=tk.LEFT, padx=5)

        # Log de instalação
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        self.log_label = ttk.Label(log_frame, text=TRANSLATIONS[self.current_language]["log_title"])
        self.log_label.pack(anchor=tk.W)

        # log font size
        self.log_text = tk.Text(log_frame, height=12, width=100, font=("Helvetica", 11))
        self.log_text.pack(pady=5)

        self.log_text.tag_config("green", foreground="green")
        self.log_text.tag_config("red", foreground="red")
        self.log_text.tag_config("black", foreground="black")

        # Verificação inicial
        self.verify_initial_installation()

        # Verifica o status do backup após a criação do botão de restauração
        self.check_backup_status()

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
            self.log(TRANSLATIONS[self.current_language]["game_found_default"], "green")
            self.install_button.config(state=tk.NORMAL)
        else:
            self.log(TRANSLATIONS[self.current_language]["game_not_found"], "red")
            self.install_button.config(state=tk.DISABLED)

    # Rest of the methods remain the same...
    def log(self, message, tag="info"):
        # Habilita a edição temporariamente
        self.log_text.config(state="normal")
        # Insere a mensagem no log
        self.log_text.insert(tk.END, f"{message}\n", tag)
        # Desabilita a edição novamente
        self.log_text.config(state="disabled")
        # Rola para o final do log
        self.log_text.see(tk.END)

    def browse_location(self):
        if is_game_running():
            messagebox.showwarning("", TRANSLATIONS[self.current_language]["game_running"])
            return

        messagebox.showinfo("", TRANSLATIONS[self.current_language]["select_folder"])
        filepath = filedialog.askopenfilename(
            title=TRANSLATIONS[self.current_language]["select_exe"],
            filetypes=[("Executável", "*.exe")]
        )

        if filepath and os.path.basename(filepath) == "hl2.exe":
            self.default_game_path = os.path.dirname(os.path.dirname(filepath))
            self.client_dll_path = os.path.join(self.default_game_path, "fof", "bin", "client.dll")
            self.log(TRANSLATIONS[self.current_language]["new_location"].format(self.default_game_path), "green")
            self.install_button.config(state=tk.NORMAL)
            # Verifica o status do backup após a criação do botão de restauração
            self.check_backup_status()
        else:
            self.log(TRANSLATIONS[self.current_language]["invalid_selection"], "red")

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
            self.log(TRANSLATIONS[self.current_language]["mod_verified"], "black")

            if not os.path.exists(self.client_dll_path):
                raise Exception(TRANSLATIONS[self.current_language]["original_not_found"])

            self.progress["value"] = 50
            self.log(TRANSLATIONS[self.current_language]["original_found"], "black")

            backup_dir = os.path.dirname(self.client_dll_path)
            self.backup_path = os.path.join(backup_dir, "client.dll.backup")
            if os.path.exists(self.backup_path):
                os.remove(self.backup_path)

            shutil.copy2(self.client_dll_path, self.backup_path)

            self.progress["value"] = 75
            self.log(TRANSLATIONS[self.current_language]["backup_created"].format("client.dll.backup"))

            shutil.copy2(self.mod_dll_path, self.client_dll_path)

            self.progress["value"] = 100
            self.log(TRANSLATIONS[self.current_language]["install_success"], "green")

            # Atualiza o estado do botão restore após criar o backup
            self.check_backup_status()

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

        try:
            # Restaura o arquivo original
            shutil.copy2(backup_path, self.client_dll_path)

            # Remove o arquivo de backup
            os.remove(backup_path)

            # Atualiza o estado do botão restore
            self.check_backup_status()

            self.log(TRANSLATIONS[self.current_language]["restore_success"], "green")
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
