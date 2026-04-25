import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import threading
import subprocess
import os
import sys
import requests
import json
import time
import ctypes
import wmi
import psutil
import winreg
import struct
import re
import concurrent.futures
from bs4 import BeautifulSoup
from PIL import Image

# UI Theme Setup / Настройка темы интерфейса
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Localization Dictionary / Словарь локализации
TEXTS = {
    "ru": {
        "hw_cpu": "Процессор",
        "hw_ram": "Оперативная память",
        "hw_gpu": "Видеокарта",
        "step_1": "1. Выбор модели ИИ:",
        "other_model": "Выбрать другую модель:",
        "btn_catalog": "🌐 Онлайн-каталог",
        "selected": "✓ Выбрана модель:",
        "turbo": "TurboQuant (Аппаратное ускорение)",
        "turbo_no": "- не поддерживается на вашем ПК",
        "dns": "Вшить xbox-dns",
        "step_2": "2. Папка установки:",
        "btn_browse": "Обзор",
        "btn_install": "РАЗВЕРНУТЬ СРЕДУ",
        "btn_cancel": "ОТМЕНИТЬ УСТАНОВКУ",
        "btn_uninstall": "УДАЛИТЬ",
        "rec": "[РЕКОМЕНДОВАНО]",
        "err_admin": "Вы запустили программу без прав администратора. Продолжить?",
        "err_model": "Пожалуйста, выберите модель ИИ для установки.",
        "err_api": "Ollama API не отвечает. Возможно, программа не установлена или порт заблокирован.",
        "err_pull": "Ошибка скачивания модели: {}",
        "msg_success": "УСПЕХ! AutoJunior готов к работе (Модель: {}).",
        "msg_done": "Развертывание завершено успешно!",
        "log_check": "Проверка {}...",
        "log_install": "Установка {}...",
        "log_ready": "{} уже готов.",
        "log_path": "Обновление системных переменных (PATH)...",
        "log_env": "Настройка переменных...",
        "log_venv": "Создание venv...",
        "log_aider": "Обновление Aider...",
        "log_api": "Ожидание запуска службы Ollama...",
        "log_pull": "Загрузка модели {}...",
        "log_abort": "ОПЕРАЦИЯ ПРЕРВАНА",
        "log_dns_start": "Маршрутизация Ollama через Xbox-DNS...",
        "log_dns_success": "Xbox-DNS успешно применен (hosts обновлен).",
        "log_dns_remove": "Удаление маршрутов Xbox-DNS...",
        "log_dns_removed": "Маршруты Xbox-DNS очищены.",
        "cat_title": "Доступные модели Ollama",
        "cat_load": "Загрузка каталога моделей...",
        "cat_init": "Инициализация...",
        "cat_btn_abort": "Прервать парсинг",
        "cat_search": "Поиск по семейству...",
        "cat_hide": "Скрыть неподдерживаемые",
        "col_fam": "Семейство",
        "col_tag": "Версия (Тег)",
        "col_size": "Размер",
        "col_vram": "Требуется VRAM",
        "col_desc": "Описание",
        "cat_btn_select": "Выбрать модель",
        "cat_found": "Найдено семейств: {}. Сбор версий (многопоточный режим)...",
        "cat_proc": "Обработано {} из {}...",
        "cat_abort": "Прерывание процесса... Сохранение собранных данных.",
        "cat_total": "Всего доступно версий: {} | Доступно VRAM: {} ГБ",
        "un_title": "Деинсталляция",
        "un_desc": "Выберите компоненты для удаления:",
        "un_venv": "Aider (виртуальное окружение)",
        "un_models": "Все модели ИИ (20GB+)",
        "un_env": "Системные переменные",
        "un_path": "Удалить из переменной PATH",
        "un_git": "Git (полное удаление)",
        "un_ollama": "Ollama (полное удаление)",
        "un_btn_all": "Выбрать всё",
        "un_btn_none": "Снять всё",
        "un_btn_del": "УДАЛИТЬ ВЫБРАННОЕ",
        "un_log_start": "Начало деинсталляции...",
        "un_log_done": "Деинсталляция завершена.",
        "un_msg_done": "Компоненты удалены."
    },
    "en": {
        "hw_cpu": "Processor",
        "hw_ram": "RAM",
        "hw_gpu": "Graphics Card",
        "step_1": "1. AI Model Selection:",
        "other_model": "Choose another model:",
        "btn_catalog": "🌐 Online Catalog",
        "selected": "✓ Selected model:",
        "turbo": "TurboQuant (Hardware Acceleration)",
        "turbo_no": "- not supported on your PC",
        "dns": "Embed xbox-dns",
        "step_2": "2. Installation Path:",
        "btn_browse": "Browse",
        "btn_install": "DEPLOY ENVIRONMENT",
        "btn_cancel": "CANCEL INSTALLATION",
        "btn_uninstall": "UNINSTALL",
        "rec": "[RECOMMENDED]",
        "err_admin": "You are running without administrator privileges. Continue?",
        "err_model": "Please select an AI model to install.",
        "err_api": "Ollama API is not responding. It might not be installed correctly or the port is blocked.",
        "err_pull": "Model download error: {}",
        "msg_success": "SUCCESS! AutoJunior is ready (Model: {}).",
        "msg_done": "Deployment completed successfully!",
        "log_check": "Checking {}...",
        "log_install": "Installing {}...",
        "log_ready": "{} is already prepared.",
        "log_path": "Refreshing system variables (PATH)...",
        "log_env": "Configuring variables...",
        "log_venv": "Creating venv...",
        "log_aider": "Updating Aider...",
        "log_api": "Waiting for Ollama service to start...",
        "log_pull": "Downloading model {}...",
        "log_abort": "OPERATION ABORTED",
        "log_dns_start": "Routing Ollama through Xbox-DNS...",
        "log_dns_success": "Xbox-DNS applied successfully (hosts updated).",
        "log_dns_remove": "Removing Xbox-DNS routes...",
        "log_dns_removed": "Xbox-DNS routes cleared.",
        "cat_title": "Available Ollama Models",
        "cat_load": "Loading models catalog...",
        "cat_init": "Initializing...",
        "cat_btn_abort": "Abort Parsing",
        "cat_search": "Search by family...",
        "cat_hide": "Hide unsupported",
        "col_fam": "Family",
        "col_tag": "Version (Tag)",
        "col_size": "Size",
        "col_vram": "Required VRAM",
        "col_desc": "Description",
        "cat_btn_select": "Select Model",
        "cat_found": "Families found: {}. Collecting versions (multi-threaded)...",
        "cat_proc": "Processed {} of {}...",
        "cat_abort": "Interrupting... Saving collected data.",
        "cat_total": "Total versions available: {} | VRAM Available: {} GB",
        "un_title": "Uninstallation",
        "un_desc": "Select components to remove:",
        "un_venv": "Aider (Virtual Environment)",
        "un_models": "All AI Models (20GB+)",
        "un_env": "System Variables",
        "un_path": "Remove from PATH variable",
        "un_git": "Git (Full removal)",
        "un_ollama": "Ollama (Full removal)",
        "un_btn_all": "Select All",
        "un_btn_none": "Clear All",
        "un_btn_del": "DELETE SELECTED",
        "un_log_start": "Starting uninstallation...",
        "un_log_done": "Uninstallation completed.",
        "un_msg_done": "Components removed."
    }
}

# Admin Privileges Validator / Проверка прав администратора
def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

# Icon Path Resolver (PyInstaller _MEIPASS support) / Путь к вшитым ресурсам
def get_icon_path(filename):
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)

# Cache Path Resolver / Вычисление пути для JSON кэша (рядом с exe)
def get_cache_path():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "ollama_catalog.json")

# Hardware Telemetry Collector / Сбор телеметрии оборудования (CPU, RAM, GPU, VRAM)
def get_hw_info():
    info = {"cpu": "Unknown", "ram": 0, "gpu": "Unknown", "vram": 0, "turbo_support": False}
    try:
        w = wmi.WMI()
        
        cpus = w.Win32_Processor()
        if cpus: info["cpu"] = cpus[0].Name.strip()
        
        info["ram"] = round(psutil.virtual_memory().total / (1024**3))
        
        controllers = w.Win32_VideoController()
        if controllers:
            selected_gpu = controllers[0]
            for g in controllers:
                name = g.Caption.lower()
                if any(x in name for x in ["nvidia", "amd", "radeon", "geforce", "rtx", "gtx", "rx"]):
                    selected_gpu = g
                    break
            info["gpu"] = selected_gpu.Caption

            vram_bytes = 0
            reg_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as root_key:
                    for i in range(20):
                        try:
                            sub_key_name = winreg.EnumKey(root_key, i)
                            with winreg.OpenKey(root_key, sub_key_name) as sub_key:
                                try:
                                    driver_desc, _ = winreg.QueryValueEx(sub_key, "DriverDesc")
                                    if info["gpu"] in driver_desc or driver_desc in info["gpu"]:
                                        try:
                                            vram_bytes, _ = winreg.QueryValueEx(sub_key, "HardwareInformation.qwMemorySize")
                                            break
                                        except FileNotFoundError: pass
                                            
                                        try:
                                            raw_val, val_type = winreg.QueryValueEx(sub_key, "HardwareInformation.AdapterMemorySize")
                                            if val_type == winreg.REG_BINARY:
                                                if len(raw_val) == 8: vram_bytes = struct.unpack("<Q", raw_val)[0]
                                                else: vram_bytes = struct.unpack("<I", raw_val)[0]
                                            else:
                                                vram_bytes = int(raw_val)
                                            break
                                        except FileNotFoundError: pass
                                except: continue
                        except OSError: break
            except: pass

            if vram_bytes == 0 and hasattr(selected_gpu, 'AdapterRAM') and selected_gpu.AdapterRAM:
                vram_bytes = int(selected_gpu.AdapterRAM)
                if vram_bytes < 0: vram_bytes += 4294967296

            info["vram"] = round(vram_bytes / (1024**3))
            if info["vram"] <= 0: info["vram"] = 4

            gpu_lower = info["gpu"].lower()
            if "rtx" in gpu_lower and any(x in gpu_lower for x in ["40", "50"]):
                info["turbo_support"] = True
    except Exception as e:
        print(f"HW Detection Error: {e}")
    return info

# VRAM Estimator Engine / Эвристический анализатор требований VRAM
def estimate_vram_from_text(text):
    max_b = 0.0
    words = re.findall(r'\b\d+(?:\.\d+)?b\b', text.lower())
    for word in words:
        try:
            val = float(word.replace('b', ''))
            if val > max_b: max_b = val
        except: pass
        
    if max_b == 0: return 8    
    if max_b <= 3: return 4    
    if max_b <= 9: return 8    
    if max_b <= 15: return 16  
    if max_b <= 35: return 24  
    return 32                  

# Main Application Instance / Экземпляр основного приложения
class AutoJunior(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.lang = "ru"
        self.title("AutoJunior")
        self.center_window(self, 750, 780) 
        self.resizable(False, False)
        
        icon_path = get_icon_path("icon.ico")
        if os.path.exists(icon_path):
            try: self.iconbitmap(icon_path)
            except: pass

        self.hw = get_hw_info()
        
        self.models_data = {
            "VRAM 4GB+ (Model: qwen3.5:4b)": "qwen3.5:4b",
            "VRAM 8GB+ (Model: qwen3.5:9b)": "qwen3.5:9b",
            "VRAM 16GB+ (Model: qwen2.5-coder:14b)": "qwen2.5-coder:14b",
            "VRAM 24GB+ (Model: qwen3.6-35b-a3b)": "qwen3.6-35b-a3b" 
        }
        
        self.install_path = ctk.StringVar(value=r"C:\AutoJunior")
        self.selected_model_key = ctk.StringVar()
        self.custom_model_target = None
        
        self.parsed_catalog_data = [] 
        self.cancel_parsing = False
        
        self.is_cancelled = False
        self.current_process = None
        self.current_request = None

        self.setup_ui()
        self.auto_recommend()
        self.update_ui_texts() 

    # Text Translator Helper / Помощник перевода текста
    def t(self, key):
        return TEXTS.get(self.lang, TEXTS["ru"]).get(key, key)

    # Change Language Logic / Логика смены языка
    def toggle_language(self, choice):
        self.lang = choice.lower()
        self.update_ui_texts()

    # Dynamic Environment Variable Reloader / Динамическое обновление переменных среды текущего процесса
    def refresh_env_path(self):
        new_path = ""
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
                sys_path, _ = winreg.QueryValueEx(key, "Path")
                new_path += sys_path + ";"
        except: pass
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
                usr_path, _ = winreg.QueryValueEx(key, "Path")
                new_path += usr_path
        except: pass
        
        if new_path:
            os.environ["PATH"] = os.path.expandvars(new_path)

    # Window Coordinates Calculator / Расчет координат для центрирования окна
    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")

    # Core Interface Renderer / Отрисовка базового интерфейса
    def setup_ui(self):
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=30, pady=(20, 5))
        
        self.seg_lang = ctk.CTkSegmentedButton(self.top_bar, values=["RU", "EN"], command=self.toggle_language, width=80)
        self.seg_lang.pack(side="right")
        self.seg_lang.set("RU")

        title_wrapper = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        title_wrapper.pack(side="top", expand=True)

        icon_path = get_icon_path("icon.ico")
        if os.path.exists(icon_path):
            try:
                img = ctk.CTkImage(Image.open(icon_path), size=(32, 32))
                ctk.CTkLabel(title_wrapper, text="", image=img).pack(side="left", padx=(0, 10))
            except: pass

        self.lbl_title = ctk.CTkLabel(title_wrapper, text="AutoJunior", font=ctk.CTkFont(size=32, weight="bold"))
        self.lbl_title.pack(side="left")

        self.frame_hw = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=10)
        self.frame_hw.pack(pady=10, padx=30, fill="x")
        self.lbl_hw = ctk.CTkLabel(self.frame_hw, text="", justify="left", font=ctk.CTkFont(size=13))
        self.lbl_hw.pack(padx=20, pady=10)

        self.frame_vram = ctk.CTkFrame(self)
        self.frame_vram.pack(pady=5, padx=30, fill="x")
        
        self.lbl_step1 = ctk.CTkLabel(self.frame_vram, text="", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_step1.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.radio_buttons = {}
        for key in self.models_data.keys():
            rb = ctk.CTkRadioButton(self.frame_vram, text=key, variable=self.selected_model_key, value=key, command=self.clear_custom_model)
            rb.pack(anchor="w", padx=25, pady=4)
            self.radio_buttons[key] = rb
            
        catalog_panel = ctk.CTkFrame(self.frame_vram, fg_color="transparent")
        catalog_panel.pack(fill="x", padx=25, pady=(10, 2))
        
        self.lbl_other_model = ctk.CTkLabel(catalog_panel, text="", font=ctk.CTkFont(size=13))
        self.lbl_other_model.pack(side="left")
        
        self.btn_catalog = ctk.CTkButton(catalog_panel, text="", width=140, height=26, command=self.open_online_catalog)
        self.btn_catalog.pack(side="left", padx=15)
            
        self.lbl_custom_model = ctk.CTkLabel(self.frame_vram, text="", text_color="#5fb1ff", font=ctk.CTkFont(weight="bold"))
        self.lbl_custom_model.pack(anchor="w", padx=25, pady=(0, 10))

        self.frame_opts = ctk.CTkFrame(self)
        self.frame_opts.pack(pady=5, padx=30, fill="x")
        self.var_turbo = ctk.BooleanVar(value=self.hw['turbo_support'])
        
        self.cb_turbo = ctk.CTkCheckBox(self.frame_opts, text="", variable=self.var_turbo)
        if not self.hw['turbo_support']: self.cb_turbo.configure(state="disabled")
        self.cb_turbo.pack(anchor="w", padx=25, pady=10)

        # Custom DNS Bypass Toggle
        self.var_dns = ctk.BooleanVar(value=False)
        self.cb_dns = ctk.CTkCheckBox(self.frame_opts, text="", variable=self.var_dns, command=self.toggle_dns)
        self.cb_dns.pack(anchor="w", padx=25, pady=(0, 10))

        self.frame_path = ctk.CTkFrame(self)
        self.frame_path.pack(pady=5, padx=30, fill="x")
        self.lbl_step2 = ctk.CTkLabel(self.frame_path, text="", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_step2.pack(anchor="w", padx=15, pady=(10, 5))
        
        path_inner = ctk.CTkFrame(self.frame_path, fg_color="transparent")
        path_inner.pack(fill="x", padx=15, pady=(0, 10))
        self.entry_path = ctk.CTkEntry(path_inner, textvariable=self.install_path, height=35)
        self.entry_path.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.btn_browse = ctk.CTkButton(path_inner, text="", width=90, height=35, command=self.browse_folder)
        self.btn_browse.pack(side="left")

        self.textbox_log = ctk.CTkTextbox(self, height=100, state="disabled", font=("Consolas", 12), corner_radius=10)
        self.textbox_log.pack(pady=10, padx=30, fill="x")
        self.progress = ctk.CTkProgressBar(self, height=10)
        self.progress.pack(pady=(0, 5), padx=30, fill="x")
        self.progress.set(0)

        btn_container = ctk.CTkFrame(self, fg_color="transparent")
        btn_container.pack(pady=(15, 20)) 
        
        self.btn_install = ctk.CTkButton(btn_container, text="", font=ctk.CTkFont(size=15, weight="bold"), height=50, command=self.start_installation)
        self.btn_install.pack(side="left", padx=10)

        self.btn_uninstall = ctk.CTkButton(btn_container, text="", fg_color="#444444", hover_color="#333333", font=ctk.CTkFont(size=15), height=50, command=self.show_uninstall_dialog)
        self.btn_uninstall.pack(side="left", padx=10)

    # Dynamic UI Text Updater / Динамическое обновление текстов интерфейса
    def update_ui_texts(self):
        hw_text = f"{self.t('hw_cpu')}: {self.hw['cpu']}\n{self.t('hw_ram')}: {self.hw['ram']} GB\n{self.t('hw_gpu')}: {self.hw['gpu']} ({self.hw['vram']} GB VRAM)"
        self.lbl_hw.configure(text=hw_text)
        
        self.lbl_step1.configure(text=self.t("step_1"))
        self.lbl_other_model.configure(text=self.t("other_model"))
        self.btn_catalog.configure(text=self.t("btn_catalog"))
        
        if self.custom_model_target:
            self.lbl_custom_model.configure(text=f"{self.t('selected')} {self.custom_model_target}")
            
        turbo_text = self.t("turbo")
        if not self.hw['turbo_support']: turbo_text += f" {self.t('turbo_no')}"
        self.cb_turbo.configure(text=turbo_text)
        
        self.cb_dns.configure(text=self.t("dns"))
        
        self.lbl_step2.configure(text=self.t("step_2"))
        self.btn_browse.configure(text=self.t("btn_browse"))
        
        if not self.is_cancelled and not self.current_process:
            self.btn_install.configure(text=self.t("btn_install"))
        else:
            self.btn_install.configure(text=self.t("btn_cancel"))
            
        self.btn_uninstall.configure(text=self.t("btn_uninstall"))
        
        for k, rb in self.radio_buttons.items():
            if self.selected_model_key.get() == k:
                rb.configure(text=k + " " + self.t("rec"))
            else:
                rb.configure(text=k)

    # VRAM Dependency Resolver / Модуль автоматического выбора модели на основе VRAM
    def auto_recommend(self):
        v = self.hw['vram']
        rec_key = "VRAM 4GB+ (Model: qwen3.5:4b)"
        if v >= 24: rec_key = "VRAM 24GB+ (Model: qwen3.6-35b-a3b)"
        elif v >= 12: rec_key = "VRAM 16GB+ (Model: qwen2.5-coder:14b)"
        elif v >= 8: rec_key = "VRAM 8GB+ (Model: qwen3.5:9b)"
        
        self.selected_model_key.set(rec_key)

    # State Reset Handlers / Обработчики сброса состояния
    def clear_custom_model(self):
        self.custom_model_target = None
        self.lbl_custom_model.configure(text="")

    def set_custom_model(self, model_name):
        self.custom_model_target = model_name
        self.selected_model_key.set("") 
        self.lbl_custom_model.configure(text=f"{self.t('selected')} {model_name}")

    # DNS Patch Controller / Контроллер патча DNS
    def toggle_dns(self):
        self.cb_dns.configure(state="disabled")
        if self.var_dns.get():
            threading.Thread(target=self.apply_dns_patch, daemon=True).start()
        else:
            threading.Thread(target=self.remove_dns_patch, daemon=True).start()

    # Hosts File Modifier for Xbox-DNS / Модификатор файла hosts для Xbox-DNS
    def apply_dns_patch(self):
        self.log(self.t("log_dns_start"))
        domains = ["ollama.com", "registry.ollama.ai"]
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        
        try: os.chmod(hosts_path, 0o666)
        except: pass
        
        try:
            with open(hosts_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except: lines = []

        clean_lines = [l for l in lines if not any(d in l for d in domains)]
        new_entries = []
        
        for domain in domains:
            try:
                proc = subprocess.run(["nslookup", domain, "111.88.96.50"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', proc.stdout)
                ips = [ip for ip in ips if ip not in ["111.88.96.50", "111.88.96.51", "127.0.0.1"]]
                if ips:
                    target_ip = ips[-1]
                    new_entries.append(f"{target_ip}\t{domain} # AutoJunior Xbox-DNS\n")
            except: pass
            
        if new_entries:
            try:
                with open(hosts_path, "w", encoding="utf-8") as f:
                    f.writelines(clean_lines)
                    if clean_lines and not clean_lines[-1].endswith('\n'):
                        f.write('\n')
                    f.writelines(new_entries)
                subprocess.run(["ipconfig", "/flushdns"], creationflags=subprocess.CREATE_NO_WINDOW)
                self.log(self.t("log_dns_success"))
            except Exception as e:
                self.log(f"Xbox-DNS Error: {e}")
                
        try: self.cb_dns.configure(state="normal")
        except: pass

    # Hosts File Cleaner / Очистка файла hosts от патчей
    def remove_dns_patch(self):
        self.log(self.t("log_dns_remove"))
        domains = ["ollama.com", "registry.ollama.ai"]
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        
        try: os.chmod(hosts_path, 0o666)
        except: pass
        
        try:
            with open(hosts_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            clean_lines = [l for l in lines if not any(d in l for d in domains)]
            with open(hosts_path, "w", encoding="utf-8") as f:
                f.writelines(clean_lines)
            subprocess.run(["ipconfig", "/flushdns"], creationflags=subprocess.CREATE_NO_WINDOW)
            self.log(self.t("log_dns_removed"))
        except: pass
        
        try: self.cb_dns.configure(state="normal")
        except: pass

    # Catalog Lifecycle Manager / Управление жизненным циклом окна каталога
    def open_online_catalog(self):
        self.diag = ctk.CTkToplevel(self)
        self.diag.title(self.t("cat_title"))
        self.center_window(self.diag, 900, 650)
        self.diag.minsize(750, 500)
        self.diag.grab_set()

        self.top_frame = ctk.CTkFrame(self.diag, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        self.lbl_cat_title = ctk.CTkLabel(self.top_frame, text=self.t("cat_load"), font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_cat_title.pack()
        
        self.cat_progress = ctk.CTkProgressBar(self.top_frame, height=10)
        self.cat_progress.pack(fill="x", pady=(10, 5))
        self.cat_progress.set(0)
        
        status_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        status_frame.pack(fill="x")
        
        self.lbl_cat_status = ctk.CTkLabel(status_frame, text=self.t("cat_init"), text_color="gray")
        self.lbl_cat_status.pack(side="left", expand=True)
        
        self.btn_cancel_parse = ctk.CTkButton(status_frame, text=self.t("cat_btn_abort"), width=120, fg_color="#c93434", hover_color="#992424", command=self.stop_parsing)
        self.btn_cancel_parse.pack(side="right")

        self.filter_frame = ctk.CTkFrame(self.diag, fg_color="transparent")
        
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_treeview())
        self.entry_search = ctk.CTkEntry(self.filter_frame, textvariable=self.search_var, placeholder_text=self.t("cat_search"), width=250)
        self.entry_search.pack(side="left", padx=(0, 15))
        
        self.var_hide_unsupported = ctk.BooleanVar(value=True)
        self.cb_hide = ctk.CTkCheckBox(self.filter_frame, text=self.t("cat_hide"), variable=self.var_hide_unsupported, command=self.refresh_treeview)
        self.cb_hide.pack(side="left")

        self.tree_frame = ctk.CTkFrame(self.diag)
        
        style = ttk.Style(self.diag)
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=30, fieldbackground="#2b2b2b", borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#333333", foreground="white", relief="flat", font=('Segoe UI', 10, 'bold'))
        style.map("Treeview.Heading", background=[('active', '#444444')])

        self.tree = ttk.Treeview(self.tree_frame, columns=("name", "tag", "size", "vram", "desc"), show="headings")
        self.tree.heading("name", text=self.t("col_fam"), command=lambda: self.sort_tree("name", False))
        self.tree.heading("tag", text=self.t("col_tag"), command=lambda: self.sort_tree("tag", False))
        self.tree.heading("size", text=self.t("col_size"), command=lambda: self.sort_tree("size", False))
        self.tree.heading("vram", text=self.t("col_vram"), command=lambda: self.sort_tree("vram", False))
        self.tree.heading("desc", text=self.t("col_desc"), command=lambda: self.sort_tree("desc", False))
        
        self.tree.column("name", width=140, anchor="w")
        self.tree.column("tag", width=220, anchor="w")
        self.tree.column("size", width=80, anchor="center")
        self.tree.column("vram", width=120, anchor="center")
        self.tree.column("desc", width=300, anchor="w")
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.btn_select_model = ctk.CTkButton(self.diag, text=self.t("cat_btn_select"), height=40, font=ctk.CTkFont(weight="bold"), state="disabled", command=self.confirm_tree_selection)

        if self.parsed_catalog_data:
            self.finish_parsing_ui()
            return
            
        cache_file = get_cache_path()
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    self.parsed_catalog_data = json.load(f)
                if self.parsed_catalog_data:
                    self.finish_parsing_ui()
                    return
            except: pass

        self.cancel_parsing = False
        threading.Thread(target=self.fetch_all_models_logic, daemon=True).start()

    # Async Interrupt Signal / Асинхронный сигнал прерывания
    def stop_parsing(self):
        self.cancel_parsing = True
        self.lbl_cat_status.configure(text=self.t("cat_abort"), text_color="#c93434")
        self.btn_cancel_parse.configure(state="disabled")

    # Multi-threaded Web Scraper / Многопоточный веб-парсер
    def fetch_all_models_logic(self):
        try:
            with requests.Session() as session:
                session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                
                r = session.get("https://ollama.com/library", timeout=10)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, 'html.parser')
                
                families = []
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith('/library/') and href.count('/') == 2:
                        name = href.split('/')[-1]
                        if any(f['name'] == name for f in families): continue
                        
                        p_tag = a.find('p')
                        desc = p_tag.text.strip() if p_tag else ""
                        families.append({"name": name, "desc": desc})

                self.diag.after(0, lambda: self.lbl_cat_status.configure(text=self.t("cat_found").format(len(families))))
                
                self.parsed_catalog_data = []
                total = len(families)
                completed = 0

                def fetch_tags(fam):
                    if self.cancel_parsing: return []
                    fam_name = fam["name"]
                    desc = fam["desc"]
                    variants = []
                    try:
                        res = session.get(f"https://ollama.com/library/{fam_name}/tags", timeout=5) 
                        if res.status_code == 200:
                            s = BeautifulSoup(res.text, 'html.parser')
                            for a in s.find_all('a', href=True):
                                if a['href'].startswith(f"/library/{fam_name}:"):
                                    full_target = a['href'].split('/')[-1]
                                    tag = full_target.split(':')[-1]
                                    if not any(v['full'] == full_target for v in variants):
                                        req_vram = estimate_vram_from_text(tag)
                                        
                                        size_str = "-"
                                        parent = a.parent
                                        for _ in range(3):
                                            if parent:
                                                m = re.search(r'(\d+(?:\.\d+)?)\s*(GB|MB)', parent.text, re.IGNORECASE)
                                                if m:
                                                    size_str = f"{m.group(1)} {m.group(2).upper()}"
                                                    break
                                                parent = parent.parent

                                        variants.append({
                                            "name": fam_name, "tag": full_target, "size": size_str,
                                            "vram": req_vram, "desc": desc, "full": full_target
                                        })
                    except: pass
                    
                    if not variants: 
                        variants.append({"name": fam_name, "tag": f"{fam_name}:latest", "size": "-", "vram": 8, "desc": desc, "full": f"{fam_name}:latest"})
                    return variants

                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    futures = {executor.submit(fetch_tags, f): f for f in families}
                    for future in concurrent.futures.as_completed(futures):
                        if self.cancel_parsing: break
                        res = future.result()
                        if res: self.parsed_catalog_data.extend(res)
                        completed += 1
                        self.diag.after(0, lambda v=completed/total: self.cat_progress.set(v))
                        self.diag.after(0, lambda c=completed, t=total: self.lbl_cat_status.configure(text=self.t("cat_proc").format(c, t)))

                if not self.cancel_parsing and self.parsed_catalog_data:
                    try:
                        with open(get_cache_path(), "w", encoding="utf-8") as f:
                            json.dump(self.parsed_catalog_data, f, ensure_ascii=False, indent=2)
                    except Exception as e:
                        self.diag.after(0, lambda err=e: print(f"Cache Error: {err}"))

                self.diag.after(0, self.finish_parsing_ui)

        except Exception as e:
            self.diag.after(0, lambda err=e: self.lbl_cat_status.configure(text=f"Error: {err}", text_color="#c93434"))
            self.diag.after(0, self.btn_cancel_parse.pack_forget)

    # Post-Parsing UI Rebuilder / Перестроение UI после парсинга
    def finish_parsing_ui(self):
        self.lbl_cat_title.configure(text=self.t("cat_title"))
        
        status_text = self.t("cat_total").format(len(self.parsed_catalog_data), self.hw['vram'])
        if self.cancel_parsing: status_text += " (Aborted/Прервано)"
        self.lbl_cat_status.configure(text=status_text, text_color="white")
        
        self.cat_progress.pack_forget() 
        self.btn_cancel_parse.pack_forget()
        
        self.filter_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.btn_select_model.pack(pady=(5, 20))
        
        self.refresh_treeview()

    # Dynamic Filter Engine / Динамический движок фильтрации
    def refresh_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        search_q = self.search_var.get().lower()
        hide_unsup = self.var_hide_unsupported.get()
        my_vram = self.hw['vram']
        
        for item in self.parsed_catalog_data:
            if search_q and search_q not in item["name"].lower(): continue
            if hide_unsup and item["vram"] > my_vram: continue
                
            vram_text = f"~ {item['vram']} GB"
            self.tree.insert("", "end", values=(item["name"], item["tag"], item.get("size", "-"), vram_text, item["desc"]))

    # Relational Sorter / Сортировка отношений в таблице
    def sort_tree(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        try:
            if col == "vram" or col == "size":
                def extract_val(s):
                    m = re.search(r'([\d\.]+)', s.replace('~', ''))
                    if not m: return 0.0
                    val = float(m.group(1))
                    if 'MB' in s.upper() or 'МБ' in s.upper(): return val / 1024.0
                    return val
                l.sort(key=lambda t: extract_val(t[0]), reverse=reverse)
            else:
                l.sort(reverse=reverse)
        except Exception:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sort_tree(col, not reverse))

    # Row Interaction Observer / Наблюдатель взаимодействия со строками
    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected: self.btn_select_model.configure(state="normal")
        else: self.btn_select_model.configure(state="disabled")

    def on_tree_double_click(self, event):
        self.confirm_tree_selection()

    # Data Transfer Pipeline / Перенос выбранных данных
    def confirm_tree_selection(self):
        selected = self.tree.selection()
        if selected:
            item_values = self.tree.item(selected[0], "values")
            full_tag = item_values[1] 
            self.set_custom_model(full_tag)
            self.diag.grab_release()
            self.diag.destroy()

    # Directory Picker Dialog / Диалог выбора системной директории
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.install_path.get())
        if folder: self.install_path.set(os.path.normpath(folder))

    # Real-time Console Logger / Логгер консольного вывода в реальном времени
    def log(self, text):
        self.textbox_log.configure(state="normal")
        self.textbox_log.insert("end", f"> {text}\n")
        self.textbox_log.see("end")
        self.textbox_log.configure(state="disabled")
        self.update()

    # Subprocess Executor / Выполнение системных подпроцессов
    def run_command(self, cmd, silent=True, cwd=None):
        creationflags = subprocess.CREATE_NO_WINDOW if silent else 0
        try:
            self.current_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, encoding='utf-8', errors='replace', creationflags=creationflags, cwd=cwd)
            for line in self.current_process.stdout:
                if self.is_cancelled:
                    self.current_process.terminate()
                    break
            self.current_process.wait()
            return self.current_process.returncode
        except: return 1
        finally: self.current_process = None

    # Deployment Initializer / Инициализатор цикла развертывания
    def start_installation(self):
        if not is_admin():
            if not messagebox.askyesno("AutoJunior", self.t("err_admin")):
                return
                
        if not self.custom_model_target and not self.selected_model_key.get():
            messagebox.showwarning("AutoJunior", self.t("err_model"))
            return
        
        self.is_cancelled = False
        self.btn_install.configure(text=self.t("btn_cancel"), command=self.cancel_action, fg_color="#c93434", hover_color="#992424")
        self.btn_uninstall.configure(state="disabled")
        self.btn_catalog.configure(state="disabled")
        threading.Thread(target=self.installation_worker, daemon=True).start()

    # Core Deployment Worker / Основной поток развертывания компонентов
    def installation_worker(self):
        try:
            steps = [
                ("Git", "Git.Git", "git --version"),
                ("Python 3.11", "Python.Python.3.11", "python --version"),
                ("Ollama", "Ollama.Ollama", "ollama --version")
            ]
            
            for i, (name, pkg_id, check_cmd) in enumerate(steps):
                self.log(self.t("log_check").format(name))
                if self.run_command(check_cmd) != 0:
                    self.log(self.t("log_install").format(name))
                    self.run_command(f"winget install --id {pkg_id} -e --silent --accept-source-agreements --accept-package-agreements")
                else:
                    self.log(self.t("log_ready").format(name))
                self.progress.set((i+1)*0.1)

            self.log(self.t("log_path"))
            self.refresh_env_path()

            base = self.install_path.get()
            os.makedirs(base, exist_ok=True)
            m_folder = os.path.join(base, "OllamaModels")
            os.makedirs(m_folder, exist_ok=True)
            
            self.log(self.t("log_env"))
            ps_env = f'[Environment]::SetEnvironmentVariable("OLLAMA_MODELS", "{m_folder}", "User"); '
            if self.var_turbo.get(): ps_env += '[Environment]::SetEnvironmentVariable("OLLAMA_TURBO_QUANT", "1", "User")'
            subprocess.run(["powershell", "-Command", ps_env], creationflags=subprocess.CREATE_NO_WINDOW)
            
            self.run_command("taskkill /F /IM ollama.exe", silent=True)
            self.run_command("taskkill /F /IM \"ollama app.exe\"", silent=True)
            time.sleep(2)
            
            venv_path = os.path.join(base, "venv")
            if not os.path.exists(os.path.join(venv_path, "Scripts", "pip.exe")):
                self.log(self.t("log_venv"))
                self.run_command(f"python -m venv \"{venv_path}\"")
            
            self.log(self.t("log_aider"))
            pip_bin = os.path.join(venv_path, "Scripts", "pip.exe")
            self.run_command(f"\"{pip_bin}\" install aider-chat")
            self.progress.set(0.4)

            target = self.custom_model_target if self.custom_model_target else self.models_data[self.selected_model_key.get()]
            
            self.log(self.t("log_api"))
            subprocess.Popen(["ollama", "serve"], env={**os.environ, "OLLAMA_MODELS": m_folder}, creationflags=subprocess.CREATE_NO_WINDOW)
            
            api_ready = False
            for _ in range(30):
                try: 
                    requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
                    api_ready = True
                    break
                except: time.sleep(1)
                
            if not api_ready:
                raise Exception(self.t("err_api"))
            
            self.pull_model(target, 0.4, 0.95)

            bat = os.path.join(base, "aid.bat")
            with open(bat, "w", encoding="utf-8") as f:
                f.write(f"@echo off\nset OLLAMA_NUM_CTX=32768\ncd /d \"%~dp0\"\nif not exist \".git\" git init\n\"%~dp0\\venv\\Scripts\\aider\" --model ollama/{target} --edit-format architect\n")
            
            ps_path = f'$old = [Environment]::GetEnvironmentVariable("Path", "User"); if ($old -notlike "*{base}*") {{ [Environment]::SetEnvironmentVariable("Path", "$old;{base}", "User") }}'
            subprocess.run(["powershell", "-Command", ps_path], creationflags=subprocess.CREATE_NO_WINDOW)
            
            self.progress.set(1.0)
            self.log(self.t("msg_success").format(target))
            messagebox.showinfo("AutoJunior", self.t("msg_done"))

        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.reset_buttons()

    # Network Model Loader / Сетевой загрузчик модели
    def pull_model(self, name, start, end):
        self.log(self.t("log_pull").format(name))
        try:
            self.current_request = requests.post("http://127.0.0.1:11434/api/pull", json={"name": name}, stream=True, timeout=30)
            self.current_request.raise_for_status()
            r_range = end - start
            for line in self.current_request.iter_lines(decode_unicode=True):
                if self.is_cancelled: break
                if line:
                    data = json.loads(line)
                    if data.get("status") in ["downloading", "verifying"]:
                        comp, tot = data.get("completed", 0), data.get("total", 1)
                        if tot > 0:
                            self.progress.set(start + (comp / tot * r_range))
                    elif "error" in data:
                        raise Exception(data["error"])
        except Exception as e:
            raise Exception(self.t("err_pull").format(str(e)))

    # Modular Uninstaller Trigger / Триггер модульного деинсталлятора
    def show_uninstall_dialog(self):
        diag = ctk.CTkToplevel(self)
        diag.title(self.t("un_title"))
        self.center_window(diag, 450, 520)
        
        diag.transient(self)
        diag.grab_set()
        
        ctk.CTkLabel(diag, text=self.t("un_desc"), font=ctk.CTkFont(size=14, weight="bold")).pack(pady=20)
        
        comps = {
            "venv": ctk.BooleanVar(value=True, name=self.t("un_venv")),
            "models": ctk.BooleanVar(value=False, name=self.t("un_models")),
            "env": ctk.BooleanVar(value=True, name=self.t("un_env")),
            "path": ctk.BooleanVar(value=True, name=self.t("un_path")),
            "git": ctk.BooleanVar(value=False, name=self.t("un_git")),
            "ollama": ctk.BooleanVar(value=False, name=self.t("un_ollama"))
        }
        
        vars_list = []
        for key, var in comps.items():
            cb = ctk.CTkCheckBox(diag, text=var._name, variable=var)
            cb.pack(anchor="w", padx=50, pady=8)
            vars_list.append(var)

        btn_frame = ctk.CTkFrame(diag, fg_color="transparent")
        btn_frame.pack(pady=20)

        def toggle_all(val):
            for v in vars_list: v.set(val)

        ctk.CTkButton(btn_frame, text=self.t("un_btn_all"), width=110, command=lambda: toggle_all(True)).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.t("un_btn_none"), width=110, command=lambda: toggle_all(False)).pack(side="left", padx=5)

        def proceed():
            selected = {k: v.get() for k, v in comps.items()}
            diag.grab_release()
            diag.destroy()
            threading.Thread(target=self.uninstallation_worker, args=(selected,), daemon=True).start()

        ctk.CTkButton(diag, text=self.t("un_btn_del"), fg_color="#c93434", hover_color="#992424", height=45, width=250, command=proceed).pack(pady=10)

    # Core Deletion Worker / Базовый поток очистки
    def uninstallation_worker(self, targets):
        try:
            self.log(self.t("un_log_start"))
            base = os.path.normpath(self.install_path.get())
            
            self.run_command("taskkill /F /IM ollama.exe", silent=True)
            self.run_command("taskkill /F /IM \"ollama app.exe\"", silent=True)

            if targets["venv"]:
                self.run_command(f"rmdir /s /q \"{os.path.join(base, 'venv')}\"")
            if targets["models"]:
                self.run_command(f"rmdir /s /q \"{os.path.join(base, 'OllamaModels')}\"")
            if targets["env"]:
                self.remove_dns_patch()
                subprocess.run(["powershell", "-Command", '[Environment]::SetEnvironmentVariable("OLLAMA_MODELS", $null, "User"); [Environment]::SetEnvironmentVariable("OLLAMA_TURBO_QUANT", $null, "User")'], creationflags=subprocess.CREATE_NO_WINDOW)
            if targets["path"]:
                import winreg
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                        val, _ = winreg.QueryValueEx(key, "Path")
                        new_path = ";".join([p for p in val.split(";") if p.strip() and os.path.normpath(p) != base])
                        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                except: pass

            if targets["git"]: self.run_command("winget uninstall --id Git.Git -e --silent")
            if targets["ollama"]: self.run_command("winget uninstall --id Ollama.Ollama -e --silent")

            self.log(self.t("un_log_done"))
            messagebox.showinfo("AutoJunior", self.t("un_msg_done"))
        except Exception as e: self.log(f"Error: {e}")

    # Process Interruption Flag / Флаг прерывания процессов
    def cancel_action(self):
        self.is_cancelled = True
        self.log(self.t("log_abort"))
        if self.current_process: self.current_process.terminate()
        if self.current_request: self.current_request.close()

    # UI State Restorer / Восстановление состояния интерфейса
    def reset_buttons(self):
        self.btn_install.configure(text=self.t("btn_install"), command=self.start_installation, fg_color=["#3a7ebf", "#1f538d"])
        self.btn_uninstall.configure(state="normal")
        self.btn_catalog.configure(state="normal")

if __name__ == "__main__":
    AutoJunior().mainloop()