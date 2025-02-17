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
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("update.servers.HSB.fof")

# Dicionário de traduções
TRANSLATIONS = {
    "Português": {
        "game_running": "Feche o Fistful of Frags antes de continuar",
        "restore_success": "Atualização removida com sucesso!",
        "restore_button": "Remover atualização",
        "window_title": "Atualização - Fistful of Frags",
        "header": "Atualização da lista de servidores da comunidade (HSB)",
        "install_button": "Instalar atualização",
        "browse_button": "Selecionar jogo manualmente",
        "log_title": "Log de instalação:",
        "game_found_default": "Jogo detectado automaticamente com sucesso.\nClique em |Instalar atualização|",
        "game_not_found": "Não foi possível detectar o jogo automaticamente\nClique em |Selecionar jogo manualmente| e siga as instruções.",
        "new_location": "Jogo localizado: {}",
        "invalid_selection": "Seleção do jogo inválida ou cancelada. Tente novamente.",
        "file_not_found": "O arquivos a ser atualizado não foi encontrado.",
        "update_verified": "Atualizando... 0%",
        "original_not_found": "Atualizando... 25%",
        "original_found": "Atualizando... 50%",
        "backup_created": "Atualizando... 99%",
        "install_success": "Atualizando... 100%",
        "error_message": "Erro na atualização:\n\n"
                         "Certifique-se de que selecionou a instalação correta.\n"
                         "Se estiver correta, os arquivos do jogo podem estar corrompidos.\n\n"
                         "Para verificar, siga os passos abaixo:\n\n"
                         "1. Localize 'Fistful of Frags' na sua biblioteca Steam.\n\n"
                         "2. Clique com o botão direito sobre o jogo e selecione Propriedades.\n\n"
                         "3. Vá para Arquivos Instalados e clique em Verificar Integridade dos Arquivos.\n\n"
                         "Aguarde a conclusão e tente atualizar novamente.",
        "success_title": "concluído.",
        "success_message": "Atualização concluída com sucesso!",
        "error_title": "Atenção!",
        "select_folder": "Localize a pasta de instalação do Fistful of Frags.\n\n1. Navegue até:\nSteamLibrary\\steamapps\\common\\Fistful of Frags\\sdk.\n\n2. Selecione o arquivo \"hl2.exe\".",
        "select_exe": "Selecione o arquivo hl2.exe na pasta: SteamLibrary\\steamapps\\common\\Fistful of Frags\\sdk.",
        "update_already_installed": "A atualização já foi instalada!",
        "language_label": "Idioma",
    },
    "English": {
        "game_running": "Please close Fistful of Frags before continuing",
        "restore_success": "Update removed successfully!",
        "restore_button": "Remove update",
        "window_title": "Update - Fistful of Frags",
        "header": "Community Servers list Update (HSB)",
        "install_button": "Install update",
        "browse_button": "Select game manually",
        "log_title": "Installation log:",
        "game_found_default": "Game automatically detected successfully.",
        "game_not_found": "Game could not be automatically detected\nClick |Select game manually| and follow the instructions.",
        "new_location": "Game located: {}",
        "invalid_selection": "Invalid or cancelled game selection. Please try again.",
        "file_not_found": "The file to be updated was not found.",
        "update_verified": "Updating... 0%",
        "original_not_found": "Updating... 25%",
        "original_found": "Updating... 50%",
        "backup_created": "Updating... 99%",
        "install_success": "Updating... 100%",
        "error_message": "Update error:\n\n"
                         "Make sure you selected the correct installation.\n"
                         "If correct, the game files may be corrupted.\n\n"
                         "To verify, follow the steps below:\n\n"
                         "1. Locate 'Fistful of Frags' in your Steam library.\n\n"
                         "2. Right-click the game and select Properties.\n\n"
                         "3. Go to Installed Files and click Verify Integrity of Game Files.\n\n"
                         "Wait for it to complete and try updating again.",
        "success_title": "Completed.",
        "success_message": "Update completed successfully!",
        "error_title": "Warning!",
        "select_folder": "Locate the installation folder of Fistful of Frags.\n\n1. Navigate to:\nSteamLibrary\\steamapps\\common\\Fistful of Frags\\sdk.\n\n2. Select the file \"hl2.exe\".",
        "select_exe": "Select the hl2.exe file in the folder: SteamLibrary\\steamapps\\common\\Fistful of Frags\\sdk.",
        "update_already_installed": "The update has already been installed!",
        "language_label": "Language",
    },
    "Français": {
        "game_running": "Veuillez fermer Fistful of Frags avant de continuer",
        "restore_success": "Mise à jour supprimée avec succès !",
        "restore_button": "Supprimer la mise à jour",
        "window_title": "Mise à jour - Fistful of Frags",
        "header": "Mise à jour de la liste des serveurs communautaires (HSB)",
        "install_button": "Installer la mise à jour",
        "browse_button": "Sélectionner le jeu manuellement",
        "log_title": "Journal d'installation :",
        "game_found_default": "Jeu détecté automatiquement avec succès.",
        "game_not_found": "Le jeu n'a pas pu être détecté automatiquement\nCliquez sur |Sélectionner le jeu manuellement| et suivez les instructions.",
        "new_location": "Jeu localisé : {}",
        "invalid_selection": "Sélection du jeu invalide ou annulée. Veuillez réessayer.",
        "file_not_found": "Le fichier à mettre à jour n'a pas été trouvé.",
        "update_verified": "Mise à jour... 0%",
        "original_not_found": "Mise à jour... 25%",
        "original_found": "Mise à jour... 50%",
        "backup_created": "Mise à jour... 99%",
        "install_success": "Mise à jour... 100%",
        "error_message": "Erreur de mise à jour :\n\n"
                         "Assurez-vous que vous avez sélectionné la bonne installation.\n"
                         "Si elle est correcte, les fichiers du jeu peuvent être corrompus.\n\n"
                         "Pour vérifier, suivez les étapes ci-dessous :\n\n"
                         "1. Localisez 'Fistful of Frags' dans votre bibliothèque Steam.\n\n"
                         "2. Faites un clic droit sur le jeu et sélectionnez Propriétés.\n\n"
                         "3. Allez dans Fichiers installés et cliquez sur Vérifier l'intégrité des fichiers du jeu.\n\n"
                         "Attendez la fin et essayez de mettre à jour à nouveau.",
        "success_title": "Terminé.",
        "success_message": "Mise à jour terminée avec succès !",
        "error_title": "Attention !",
        "select_folder": "Localisez le dossier d'installation de Fistful of Frags.\n\n1. Allez dans :\nSteamLibrary\\steamapps\\common\\Fistful of Frags\\sdk.\n\n2. Sélectionnez le fichier \"hl2.exe\".",
        "select_exe": "Sélectionnez le fichier hl2.exe dans le dossier : SteamLibrary\\steamapps\\common\\Fistful of Frags\\sdk.",
        "update_already_installed": "La mise à jour est déjà installée !",
        "language_label": "Langue",
    },
    "Español": {
        "game_running": "Por favor, cierre Fistful of Frags antes de continuar",
        "restore_success": "Actualización eliminada con éxito!",
        "restore_button": "Eliminar actualización",
        "window_title": "Actualización - Fistful of Frags",
        "header": "Actualización de la lista de servidores de la comunidad (HSB)",
        "install_button": "Instalar actualización",
        "browse_button": "Seleccionar juego manualmente",
        "log_title": "Registro de instalación:",
        "game_found_default": "Juego detectado automáticamente con éxito.",
        "game_not_found": "No se pudo detectar el juego automáticamente\nHaga clic en |Seleccionar juego manualmente| y siga las instrucciones.",
        "new_location": "Juego localizado: {}",
        "invalid_selection": "Selección de juego inválida o cancelada. Intente nuevamente.",
        "file_not_found": "No se encontró el archivo a actualizar.",
        "update_verified": "Actualizando... 0%",
        "original_not_found": "Actualizando... 25%",
        "original_found": "Actualizando... 50%",
        "backup_created": "Actualizando... 99%",
        "install_success": "Actualizando... 100%",
        "error_message": "Error en la actualización:\n\n"
                         "Asegúrese de haber seleccionado la instalación correcta.\n"
                         "Si está correcta, los archivos del juego pueden estar corruptos.\n\n"
                         "Para verificar, siga los siguientes pasos:\n\n"
                         "1. Localice 'Fistful of Frags' en su biblioteca de Steam.\n\n"
                         "2. Haga clic derecho sobre el juego y seleccione Propiedades.\n\n"
                         "3. Vaya a Archivos instalados y haga clic en Verificar la integridad de los archivos del juego.\n\n"
                         "Espere a que termine y vuelva a intentar la actualización.",
        "success_title": "Completado.",
        "success_message": "¡Actualización completada con éxito!",
        "error_title": "¡Atención!",
        "select_folder": "Localiza la carpeta de instalación de Fistful of Frags.\n\n1. Navega a:\nSteamLibrary\\steamapps\\common\\Fistful of Frags\\sdk.\n\n2. Selecciona el archivo \"hl2.exe\".",
        "select_exe": "Выберите файл hl2.exe в папке: SteamLibrary\\steamapps\\common\\Fistful of Frags\\sdk.",
        "update_already_installed": "¡La actualización ya ha sido instalada!",
        "language_label": "Idioma",
    },
    "Русский": {
        "game_running": "Пожалуйста, закройте Fistful of Frags перед продолжением",
        "restore_success": "Обновление успешно удалено!",
        "restore_button": "Удалить обновление",
        "window_title": "Обновление - Fistful of Frags",
        "header": "Обновление списка серверов сообщества (HSB)",
        "install_button": "Установить обновление",
        "browse_button": "Выбрать игру вручную",
        "log_title": "Журнал установки:",
        "game_found_default": "Игра автоматически обнаружена успешно.",
        "game_not_found": "Не удалось автоматически обнаружить игру\nНажмите |Выбрать игру вручную| и следуйте инструкциям.",
        "new_location": "Игра найдена: {}",
        "invalid_selection": "Неверный или отмененный выбор игры. Попробуйте снова.",
        "file_not_found": "Файл для обновления не найден.",
        "update_verified": "Обновление... 0%",
        "original_not_found": "Обновление... 25%",
        "original_found": "Обновление... 50%",
        "backup_created": "Обновление... 99%",
        "install_success": "Обновление... 100%",
        "error_message": "Ошибка обновления:\n\n"
                         "Убедитесь, что вы выбрали правильную установку.\n"
                         "Если это так, файлы игры могут быть повреждены.\n\n"
                         "Чтобы проверить, выполните следующие шаги:\n\n"
                         "1. Найдите 'Fistful of Frags' в своей библиотеке Steam.\n\n"
                         "2. Щелкните правой кнопкой мыши на игре и выберите Свойства.\n\n"
                         "3. Перейдите в Установленные файлы и нажмите Проверить целостность файлов игры.\n\n"
                         "Подождите завершения и попробуйте обновить снова.",
        "success_title": "Завершено.",
        "success_message": "Обновление успешно завершено!",
        "error_title": "Внимание!",
        "select_folder": "Найдите папку установки Fistful of Frags.\n\n1. Перейдите в:\nSteamLibrary\\steamapps\\common\\Fistful of Frags\\sdk.\n\n2. Выберите файл \"hl2.exe\".",
        "select_exe": "Выберите файл hl2.exe в папке: SteamLibrary\\steamapps\\common\\Fistful of Frags\\sdk.",
        "update_already_installed": "Обновление уже установлено!",
        "language_label": "Язык",
    }
}

# Mapeamento de códigos de idioma do sistema para idiomas suportados
LANGUAGE_MAPPING = {
    'pt': 'Português',
    'pt_BR': 'Português',
    'pt_PT': 'Português',
    'en': 'English',
    'fr': 'Français',
    'es': 'Español',
    'ru': 'Русский'
}


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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

    def log_with_custom_colors(self, message, default_color="red"):
        # Divide o texto em partes com base nas aspas simples
        parts = message.split("|")

        # Habilita a edição do widget de texto
        self.log_text.config(state=tk.NORMAL)

        # Itera sobre as partes do texto
        for i, part in enumerate(parts):
            if i % 2 == 1:  # Partes dentro de aspas simples
                self.log_text.insert(tk.END, f"'{part}'", "black")  # Aplica a tag "black"
            else:  # Partes fora das aspas simples
                self.log_text.insert(tk.END, part, default_color)  # Aplica a cor padrão (vermelho)

        # Adiciona uma quebra de linha no final
        self.log_text.insert(tk.END, "\n")

        # Desabilita a edição do widget de texto
        self.log_text.config(state=tk.DISABLED)

        # Rola para o final do texto
        self.log_text.see(tk.END)

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
        try:
            icon_path = resource_path("fof.ico")
            self.root.iconbitmap(icon_path)
        except:
            pass  # Silently fail if icon cannot be loaded


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
        language_menu['values'] = ['English', 'Português', 'Français', 'Español', 'Русский']
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
        # Verifica se já existe um backup
        backup_dir = os.path.dirname(self.client_dll_path)
        backup_path = os.path.join(backup_dir, "client.dll.backup")

        if os.path.exists(backup_path):
            self.log(TRANSLATIONS[self.current_language]["update_already_installed"], "green")
            messagebox.showinfo("", TRANSLATIONS[self.current_language]["update_already_installed"])
            return
        elif os.path.exists(self.hl2_exe_path):
            message = TRANSLATIONS[self.current_language]["game_found_default"]
            self.log_with_custom_colors(message, "green")
            self.install_button.config(state=tk.NORMAL)
        else:
            message = TRANSLATIONS[self.current_language]["game_not_found"]
            self.log_with_custom_colors(message, "red")
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

        # Verifica se já existe um backup
        backup_dir = os.path.dirname(self.client_dll_path)
        backup_path = os.path.join(backup_dir, "client.dll.backup")

        if os.path.exists(backup_path):
            messagebox.showinfo("", TRANSLATIONS[self.current_language]["update_already_installed"])
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

        # Verifica se já existe um backup
        backup_dir = os.path.dirname(self.client_dll_path)
        backup_path = os.path.join(backup_dir, "client.dll.backup")

        if os.path.exists(backup_path):
            messagebox.showinfo("", TRANSLATIONS[self.current_language]["update_already_installed"])
            return

        self.install_button.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.install_mod)
        thread.start()

    def install_mod(self):
        try:
            self.progress["value"] = 0

            if not os.path.exists(self.mod_dll_path):
                raise Exception(TRANSLATIONS[self.current_language]["file_not_found"])

            self.progress["value"] = 25
            self.log(TRANSLATIONS[self.current_language]["update_verified"], "black")

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
