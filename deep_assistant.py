"""
╔══════════════════════════════════════════════════════════════╗
║   D.E.E.P. - Digital Electronic Expert Processor             ║
║   Персональный ИИ-ассистент в ретро-терминале                ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import time
import random
import textwrap
import json
import string
import unicodedata
import hashlib
import threading
import speech_recognition as sr
import pyttsx3
import keyboard
import pystray
from PIL import Image, ImageDraw
from datetime import datetime
from datetime import datetime as dt
from pathlib import Path

# ====== ПРИНУДИТЕЛЬНАЯ КОДИРОВКА UTF-8 ДЛЯ WINDOWS ======
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except:
            pass
    if hasattr(sys.stderr, 'reconfigure'):
        try:
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except:
            pass

# ====== УСТАНОВКА ЗАВИСИМОСТЕЙ ======
def install_requirements():
    required = {
        'requests': 'requests',
        'duckduckgo_search': 'duckduckgo-search',
        'deep_translator': 'deep-translator'
    }
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    if missing:
        print("\n  [*] Устанавливаю библиотеки...")
        for package in missing:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package, "--quiet"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        print("  [OK] Библиотеки установлены.\n")

install_requirements()

import requests
from ddgs import DDGS 
from deep_translator import GoogleTranslator

# ====== НАСТРОЙКИ ======
AI_PROVIDER = "cloudflare"
CF_ACCOUNT_ID = ""
CF_API_TOKEN = ""
HF_API_KEY = ""
OPENROUTER_API_KEY = ""
GEMINI_API_KEY = ""
DEEPSEEK_API_KEY = ""
ASSISTANT_NAME = "D.E.E.P."
TYPO_SPEED = 0.01
BOX_WIDTH = 66

# ====== ИЗБРАННЫЕ ПРОГРАММЫ ======
FAVORITES = {
    '1': ('хром', 'Google Chrome'),
    '2': ('яндекс', 'Yandex Browser'),
    '3': ('стим', 'Steam'),
    '4': ('Happ', 'хап'),
    '5': ('калькулятор', 'Калькулятор'),
    '6': ('блокнот', 'Блокнот'),
    '7': ('проводник', 'Проводник'),
    '8': ('vs code', 'VS Code'),
    '9': ('телеграм', 'Telegram'),
    '10': ('дискорд', 'Discord'),
    '11': ('документы', 'Документы'),
    '12': ('загрузки', 'Загрузки'),
    
}

# ====== ИСТОРИЯ ЧАТОВ ======
HISTORY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history')
os.makedirs(HISTORY_DIR, exist_ok=True)
SESSION_FILE = os.path.join(HISTORY_DIR, f"session_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")

def init_session():
    """Создаёт файл новой сессии при запуске"""
    with open(SESSION_FILE, 'w', encoding='utf-8') as f:
        f.write(f"╔══════════════════════════════════════════════════════════════╗\n")
        f.write(f"║  D.E.E.P. Assistant - Сессия от {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        f.write(f"╚══════════════════════════════════════════════════════════════╝\n\n")

def save_to_history(user_msg, deep_response):
    """Дописывает запрос и ответ в файл текущей сессии"""
    with open(SESSION_FILE, 'a', encoding='utf-8') as f:
        f.write(f"┌─ ЗАПРОС [{datetime.now().strftime('%H:%M:%S')}]\n")
        for line in user_msg.split('\n'):
            f.write(f"│  {line}\n")
        f.write(f"├─ ОТВЕТ\n")
        for line in deep_response.split('\n'):
            f.write(f"│  {line}\n")
        f.write(f"└{'─'*60}\n\n")
        
# ====== БЕЗОПАСНАЯ КОДИРОВКА ======
def safe_encode(text):
    if not text:
        return ""
    result = []
    for char in text:
        code = ord(char)
        if code > 0xFFFF:
            continue
        elif 0x2500 <= code <= 0x257F:
            result.append(char)
        elif 0x0400 <= code <= 0x04FF:
            result.append(char)
        elif code == 0x2014:
            result.append('--')
        elif code == 0x00A0:
            result.append(' ')
        elif 0x0080 <= code <= 0x024F:
            try:
                n = unicodedata.normalize('NFKD', char).encode('ascii', 'ignore').decode('ascii')
                result.append(n if n else '?')
            except:
                result.append('?')
        else:
            result.append(char)
    return ''.join(result)

# ====== ТЕРМИНАЛ ======
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    if os.name == 'nt':
        os.system(f'title {ASSISTANT_NAME} v{VERSION}')

def type_text(text, speed=TYPO_SPEED, end='\n'):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if speed > 0:
            time.sleep(speed)
    sys.stdout.write(end)
    sys.stdout.flush()

def print_banner():
    banner = f"""
 ╔════════════════════════════════════════════════════════════════╗
 ║                                                                ║
 ║   ██████╗ ███████╗███████╗██████╗    ██████╗ ███████╗██████╗   ║
 ║   ██╔══██╗██╔════╝██╔════╝██╔══██╗  ██╔═══██╗██╔════╝██╔══██╗  ║
 ║   ██║  ██║█████╗  █████╗  ██████╔╝  ██║   ██║███████╗██████╔╝  ║
 ║   ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝   ██║   ██║╚════██║██╔═══╝   ║
 ║   ██████╔╝███████╗███████╗██║       ╚██████╔╝███████║██║       ║
 ║   ╚═════╝ ╚══════╝╚══════╝╚═╝        ╚═════╝ ╚══════╝╚═╝       ║
 ║                                                                ║
 ║            Digital Electronic Expert Processor                 ║
 ║                      v{VERSION}                                   ║
 ╚════════════════════════════════════════════════════════════════╝
"""
    for line in banner.split('\n'):
        print(line)
        time.sleep(0.02)

def show_boot_sequence():
    clear_screen()
    print_banner()
    print()
    for msg, delay in [("Инициализация ядра", 0.3), ("Загрузка модулей", 0.4),
                        ("Подключение нейросети", 0.5), ("Калибровка поиска", 0.3),
                        ("Загрузка команд", 0.3), ("Готов к работе", 0.2)]:
        type_text(f"  [>] {msg}... ", 0.02, end='')
        time.sleep(delay)
        type_text("OK", 0.01)
    print("\n  " + "=" * (BOX_WIDTH - 4))
    type_text(f"  Запуск: {datetime.now().strftime('%d.%m.%Y %H:%M')}", 0.02)
    type_text("  Введите HELP для списка команд.", 0.01)
    print("  " + "=" * (BOX_WIDTH - 4) + "\n")

def get_prompt():
    return f"{ASSISTANT_NAME} [{datetime.now().strftime('%H:%M:%S')}]> "

# ====== ОФОРМЛЕНИЕ ======
def wrap_text(text, width):
    text = safe_encode(text)
    lines = []
    for p in text.split('\n'):
        if not p.strip():
            lines.append('')
        else:
            lines.extend(textwrap.wrap(p, width=width) or [''])
    return lines

def print_box(text, sender, box_width=BOX_WIDTH):
    text = safe_encode(text)
    now = datetime.now().strftime('%H:%M:%S')
    header = f" {sender} [{now}] "
    inner = box_width - 4
    print("╔" + "═" * (box_width - 2) + "╗")
    print("║" + header.ljust(box_width - 2) + "║")
    print("╠" + "═" * (box_width - 2) + "╣")
    for line in wrap_text(text, inner):
        if line == '':
            print("║" + " " * (box_width - 2) + "║")
        else:
            print("║  " + line.ljust(inner) + " ║")
    print("╚" + "═" * (box_width - 2) + "╝")

# ====== ГОЛОС ======
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 0.9)
voices = engine.getProperty('voices')
for voice in voices:
    if 'russian' in voice.name.lower() or 'irina' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
speak_lock = threading.Lock()
def speak(text):
    if not speak_lock.acquire(blocking=False):
        return  # уже говорит — пропускаем
    
    try:
        clean = text.replace('╔', '').replace('╗', '').replace('║', '').replace('╚', '').replace('╝', '').replace('═', '').replace('╠', '').replace('╣', '')
        clean = clean.replace('[OK]', 'Открыто').replace('[ОШИБКА]', 'Ошибка').replace('[*]', '')
        engine.say(clean[:300])
        engine.runAndWait()
    except:
        pass
    finally:
        speak_lock.release()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n  🎤 Говорите...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            text = r.recognize_google(audio, language="ru-RU")
            print(f"  Вы: {text}")
            return text
        except sr.WaitTimeoutError:
            print("  [!] Время ожидания истекло.")
            return None
        except sr.UnknownValueError:
            print("  [!] Не разобрал речь.")
            return None
        except sr.RequestError:
            print("  [!] Проблема с сетью.")
            return None

def hotkey_listener():
    def on_ctrl_g():
        if hasattr(hotkey_listener, 'running') and hotkey_listener.running:
            return
        hotkey_listener.running = True
        print("\n  🎤 Ctrl+G — Говорите...")
        spoken = listen()
        if spoken:
            print()
            print_box(spoken, "ПОЛЬЗОВАТЕЛЬ (ГОЛОС)")
            result, sender = process_command(spoken)
            if result:
                print()
                if sender == "D.E.E.P.":
                    print_box(result, "D.E.E.P.")
                    threading.Thread(target=speak, args=(result[:300],), daemon=True).start()
                else:
                    print(result)
                print()
            print(get_prompt(), end='', flush=True)
        hotkey_listener.running = False
    keyboard.add_hotkey('ctrl+g', on_ctrl_g)

# ====== AI ======
def ask_cloudflare(prompt):
    """Запрос к Cloudflare с умной моделью и системным промптом"""
    try:
        system_prompt = """Ты — D.E.E.P., персональный ИИ-ассистент. Отвечай на русском языке.
Твои правила:
1. Если не знаешь точный ответ — скажи честно, но предложи где найти.
2. Для вопросов о времени/погоде — скажи, что не имеешь доступа к реальному времени, и предложи поиск через команду НАЙДИ.
3. Отвечай кратко, по делу.
4. Если просят код — дай рабочий код с комментариями.
5. Если просят ссылки — дай ссылки, если они есть в контексте."""
        
        r = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/meta/llama-3.1-8b-instruct",
            headers={"Authorization": f"Bearer {CF_API_TOKEN}"},
            json={
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            },
            timeout=60
        )
        r.encoding = 'utf-8'
        if r.status_code == 200:
            data = r.json()
            if data.get("success") and "result" in data:
                return safe_encode(data["result"]["response"])
            return f"[ОШИБКА] {safe_encode(str(data)[:200])}"
        return f"[ОШИБКА {r.status_code}] {safe_encode(r.text[:200])}"
    except Exception as e:
        return f"[ОШИБКА CF] {safe_encode(str(e))}"
def ask_ai(prompt):
    if AI_PROVIDER == "cloudflare":
        return ask_cloudflare(prompt)
    return "[ОШИБКА] Неизвестный AI_PROVIDER."
# ====== ПОИСК И ПЕРЕВОД ======
def search_web(query):
    try:
        type_text("  [*] Поиск...", TYPO_SPEED)
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return "Ничего не найдено."
        search_text = "\n\n".join([f"Источник {i+1}: {r['title']}\n{r['href']}\n{r['body']}" for i, r in enumerate(results)])
        type_text("  [*] Анализ...", TYPO_SPEED)
        
        ai_prompt = f"""Твоя задача — дать КОНКРЕТНЫЙ ответ на русском языке, используя ТОЛЬКО информацию из источников ниже.

Запрос пользователя: "{query}"

Источники:
{search_text}

Правила:
1. Если в источниках есть точный ответ (время, дата, число) — напиши его
2. Если точного ответа нет — напиши "В источниках нет точной информации" и предложи ссылки
3. ОТВЕЧАЙ КРАТКО, без воды
4. Ссылки указывай в конце"""
        
        return ask_ai(ai_prompt)
    except Exception as e:
        return f"[ОШИБКА ПОИСКА] {safe_encode(str(e))}"

def translate_text(text):
    try:
        return GoogleTranslator(source='auto', target='ru').translate(text)
    except Exception as e:
        return f"[ОШИБКА ПЕРЕВОДА] {str(e)}"

# ====== ОТКРЫТИЕ ПРОГРАММ ======
def find_file_deep(filename, search_paths, max_depth=4):
    search_name = filename.lower()
    search_name_no_ext = os.path.splitext(search_name)[0]
    executable_extensions = ['.exe', '.cmd', '.bat', '.com', '.lnk', '.msc']
    for root in search_paths:
        if not os.path.exists(root):
            continue
        try:
            for dirpath, dirnames, filenames in os.walk(root):
                if dirpath.replace(root, '').count(os.sep) > max_depth:
                    dirnames.clear()
                    continue
                for fname in filenames:
                    fname_lower = fname.lower()
                    if os.path.splitext(fname_lower)[1] not in executable_extensions:
                        continue
                    if fname_lower == search_name or os.path.splitext(fname_lower)[0] == search_name_no_ext:
                        return os.path.join(dirpath, fname)
        except (PermissionError, OSError):
            continue
    return None

def find_folder_deep(foldername, search_paths, max_depth=3):
    lower_name = foldername.lower().strip()
    for root in search_paths:
        if not os.path.exists(root):
            continue
        try:
            for dirpath, dirnames, _ in os.walk(root):
                if dirpath.replace(root, '').count(os.sep) > max_depth:
                    dirnames.clear()
                    continue
                for dname in dirnames:
                    if dname.lower() == lower_name:
                        return os.path.join(dirpath, dname)
        except (PermissionError, OSError):
            continue
    return None

def find_program(target):
    lower_target = target.lower().strip()
    home = str(Path.home())

    known_folders = {
        'документы': os.path.join(home, 'Documents'),
        'загрузки': os.path.join(home, 'Downloads'),
        'рабочий стол': os.path.join(home, 'Desktop'),
        'музыка': os.path.join(home, 'Music'),
        'видео': os.path.join(home, 'Videos'),
        'изображения': os.path.join(home, 'Pictures'),
        'корзина': '::{645FF040-5081-101B-9F08-00AA002F954E}',
        'мой компьютер': '::{20D04FE0-3AEA-1069-A2D8-08002B30309D}',
    }

    known_programs = {
        'хром': 'chrome.exe', 'google chrome': 'chrome.exe', 'chrome': 'chrome.exe',
        'Happ':'Happ.exe', 'хап': 'Happ.exe', 'хапп': 'Happ.exe',
        'яндекс': 'browser.exe', 'yandex': 'browser.exe',
        'firefox': 'firefox.exe', 'мозилла': 'firefox.exe',
        'edge': 'msedge.exe', 'microsoft edge': 'msedge.exe',
        'excel': 'EXCEL.EXE', 'word': 'WINWORD.EXE', 'ворд': 'WINWORD.EXE',
        'powerpoint': 'POWERPNT.EXE', 'пауэрпоинт': 'POWERPNT.EXE',
        'блокнот': 'notepad.exe', 'notepad': 'notepad.exe',
        'калькулятор': 'calc.exe', 'calc': 'calc.exe',
        'cmd': 'cmd.exe', 'командная строка': 'cmd.exe',
        'проводник': 'explorer.exe', 'explorer': 'explorer.exe',
        'диспетчер задач': 'Taskmgr.exe',
        'telegram': 'telegram.exe', 'телеграм': 'telegram.exe', 'тг': 'telegram.exe',
        'discord': 'discord.exe', 'дискорд': 'discord.exe',
        'steam': 'steam.exe', 'стим': 'steam.exe',
        'spotify': 'spotify.exe', 'спотифай': 'spotify.exe',
        'vs code': 'code.exe', 'vscode': 'code.exe', 'code': 'code.exe',
        'pycharm': 'pycharm64.exe', 'notepad++': 'notepad++.exe',
        'photoshop': 'photoshop.exe', 'фотошоп': 'photoshop.exe',
        'vlc': 'vlc.exe', 'obs': 'obs64.exe',
        '7zip': '7zFM.exe', 'winrar': 'winrar.exe',
    }

    if os.path.exists(target):
        return target

    if lower_target in known_folders:
        path = known_folders[lower_target]
        return path if path.startswith('::') or os.path.exists(path) else None

    exe_to_find = known_programs.get(lower_target, target if target.endswith('.exe') else target + '.exe')

    for path_dir in os.environ.get('PATH', '').split(os.pathsep):
        if not path_dir:
            continue
        full = os.path.join(path_dir, exe_to_find)
        if os.path.isfile(full):
            return full

    search_paths = []
    for env in ['ProgramFiles', 'ProgramFiles(x86)', 'ProgramW6432', 'LOCALAPPDATA', 'APPDATA']:
        p = os.environ.get(env)
        if p and os.path.exists(p):
            search_paths.append(p)
    for folder in [os.path.join(home, d) for d in ['Desktop', 'Downloads', 'Documents']]:
        if os.path.exists(folder):
            search_paths.append(folder)
    for drive in string.ascii_uppercase:
        dp = f"{drive}:\\"
        if os.path.exists(dp):
            search_paths.append(dp)
    search_paths = list(set(search_paths))

    result = find_file_deep(exe_to_find, search_paths) or find_file_deep(os.path.splitext(exe_to_find)[0], search_paths)
    return result or find_folder_deep(target, search_paths)

def open_item(target):
    target = target.strip('"').strip("'").strip()
    if not target:
        return "[ОШИБКА] Укажите, что открыть."
    result = find_program(target)
    if result:
        try:
            os.startfile(result)
            return f"[OK] Открыто: {result}"
        except Exception as e:
            return f"[ОШИБКА] {str(e)}"
    return f"[ОШИБКА] Не удалось найти: {target}"

# ====== ТРЕЙ ======
def create_tray_icon():
    image = Image.new('RGB', (64, 64), color='black')
    draw = ImageDraw.Draw(image)
    draw.rectangle([8, 8, 56, 56], fill='#00ff00', outline='#00cc00', width=2)
    draw.text((18, 12), "D", fill='black')
    
    def on_show(icon, item):
        show_console()
    
    def on_exit(icon, item):
        icon.stop()
        os._exit(0)
    
    menu = pystray.Menu(
        pystray.MenuItem("Показать", on_show, default=True),
        pystray.MenuItem("Выход", on_exit)
    )
    
    icon = pystray.Icon("DEEP", image, "D.E.E.P. Assistant", menu)
    return icon

def show_console():
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 9)

def hide_console():
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# ====== АВТОИНКРЕМЕНТ ВЕРСИИ ======
def get_file_hash(filepath):
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def update_version():
    script_path = os.path.abspath(__file__)
    version_file = os.path.join(os.path.dirname(script_path), 'version.txt')
    hash_file = os.path.join(os.path.dirname(script_path), '.codehash')
    
    current_hash = get_file_hash(script_path)
    
    try:
        with open(hash_file, 'r') as f:
            saved_hash = f.read().strip()
    except:
        saved_hash = None
    
    try:
        with open(version_file, 'r') as f:
            parts = f.read().strip().split('.')
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    except:
        major, minor, patch = 2, 0, 0
    
    if current_hash != saved_hash:
        patch += 1
        if patch > 999:
            patch = 0
            minor += 1
        if minor > 99:
            minor = 0
            major += 1
        new_version = f"{major}.{minor}.{patch}"
        with open(version_file, 'w') as f:
            f.write(new_version)
        with open(hash_file, 'w') as f:
            f.write(current_hash)
        return new_version
    else:
        return f"{major}.{minor}.{patch}"

VERSION = update_version()

# ====== СПРАВКА ======
def show_help():
    print("""
╔════════════════════════════════════════════════════════════╗
║                    ДОСТУПНЫЕ КОМАНДЫ                       ║
╠════════════════════════════════════════════════════════════╣
║  HELP, ?       - справка                                   ║
║  CLEAR, CLS    - очистить экран                            ║
║  EXIT, QUIT    - выход                                     ║
║  TIME, ВРЕМЯ   - дата и время                              ║
║  VER, ВЕРСИЯ   - версия системы                            ║
║  LIST, СПИСОК  - избранные программы                       ║
║  ГОЛОС, СЛУШАЙ - голосовая команда                         ║
║  СВЕРНИСЬ      - свернуть в трей                           ║
║  Ctrl+G        - быстрая голосовая команда                 ║
║                                                            ║
║  ОТКРОЙ [что]  - открыть файл/программу/папку              ║
║  НАЙДИ [запрос] - поиск в интернете                        ║
║  ПЕРЕВЕДИ [текст] - перевод                                ║
║                                                            ║
║  Примеры:                                                  ║
║    открой браузер                                          ║
║    найди погоду в Москве                                   ║
║    переведи Hello world                                    ║
║    напиши код калькулятора на Python                       ║
║    list                                                    ║
╚════════════════════════════════════════════════════════════╝
""")

def show_favorites():
    print("""
╔══════════════════════════════════════════════════════════════╗
║               БЫСТРЫЙ ДОСТУП (LIST)                          ║
╠══════════════════════════════════════════════════════════════╣""")
    for key, (cmd, name) in FAVORITES.items():
        print(f"║  [{key}]  {name:<52}║")
    print("""║                                                 ║
║  Введите номер или EXIT для выхода                           ║
╚══════════════════════════════════════════════════════════════╝
""")

# ====== ОБРАБОТКА КОМАНД ======
def process_command(cmd):
    cmd = cmd.strip()
    if not cmd:
        return None, None
    lower = cmd.lower()
    if len(cmd) == 1 and cmd.isalpha():
        return "Введите команду (HELP для справки).", "D.E.E.P."
    if lower in ['help', 'помощь', '?', 'команды']:
        show_help()
        return None, None
    if lower in ['clear', 'cls', 'очистить']:
        clear_screen()
        print_banner()
        return None, None
    if lower in ['exit', 'quit', 'выход', 'выключись']:
        type_text("\n  [*] До свидания!", TYPO_SPEED)
        time.sleep(0.5)
        sys.exit(0)
    if lower in ['свернись', 'в трей', 'спрячься', 'hide', 'tray']:
        print("\n  [*] Сворачиваюсь в трей...")
        hide_console()
        return None, None
    if lower in ['time', 'время', 'дата']:
        return f"Текущая дата и время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", "D.E.E.P."
    if lower in ['ver', 'version', 'версия']:
        return f"{ASSISTANT_NAME} v{VERSION} | Python {sys.version.split()[0]}", "D.E.E.P."
    
    if lower in ['голос', 'слушай', 'voice', 'микрофон']:
        spoken = listen()
        if spoken:
            print()
            print_box(spoken, "ПОЛЬЗОВАТЕЛЬ (ГОЛОС)")
            return process_command(spoken)
        return "Не удалось распознать речь.", "D.E.E.P."

    if lower in ['list', 'список', 'фавориты', 'favorites', 'избранное']:
        show_favorites()
        while True:
            choice = input("\n  Введите номер (или EXIT): ").strip().lower()
            if choice in ['exit', 'назад', 'выход']:
                print("  [OK] Выход из списка.")
                break
            if choice in FAVORITES:
                target, name = FAVORITES[choice]
                result = open_item(target)
                print(f"\n  [OK] Запущено: {name}")
                break
            else:
                print("  [!] Неверный номер. Попробуйте ещё раз или EXIT.")
        return None, None

    if lower.startswith(('открой ', 'запусти ', 'покажи ', 'выполни ')):
        parts = cmd.split(maxsplit=1)
        if len(parts) > 1:
            result = open_item(parts[1])
            print(f"\n  {result}\n")
            return None, None
        return "Укажите, что открыть.", "D.E.E.P."

    if lower.startswith(('найди ', 'поищи ', 'гугл ', 'поиск ')):
        query = cmd.split(maxsplit=1)[1]
        return search_web(query), "D.E.E.P."

    if lower.startswith('переведи '):
        text = cmd[9:].strip()
        if not text:
            return "Укажите текст для перевода.", "D.E.E.P."
        type_text("  [*] Перевод...", TYPO_SPEED)
        return translate_text(text), "D.E.E.P."

    type_text("  [*] Обрабатываю запрос...", TYPO_SPEED)
    return ask_ai(cmd), "D.E.E.P."


# ====== ВЕБ-СЕРВЕР ДЛЯ ДОСТУПА С ТЕЛЕФОНА ======
from flask import Flask, request, jsonify, render_template_string

web_app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>D.E.E.P. Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: #0a0a0a; 
            color: #00ff00; 
            font-family: 'Courier New', monospace;
            height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 10px;
        }
        #chat {
            flex: 1;
            overflow-y: auto;
            border: 2px solid #00ff00;
            padding: 10px;
            margin-bottom: 10px;
            font-size: 14px;
        }
        .msg { margin-bottom: 10px; }
        .user { color: #00ccff; }
        .deep { color: #00ff00; }
        .time { color: #555; font-size: 11px; }
        #input-area {
            display: flex;
            gap: 10px;
        }
        #cmd {
            flex: 1;
            background: #000;
            border: 2px solid #00ff00;
            color: #00ff00;
            padding: 12px;
            font-family: 'Courier New', monospace;
            font-size: 16px;
            outline: none;
        }
        #send {
            background: #00ff00;
            color: #000;
            border: none;
            padding: 12px 20px;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
        }
        #send:active { background: #00cc00; }
        #status { color: #555; font-size: 12px; margin-bottom: 5px; }
    </style>
</head>
<body>
    <div id="status">● Подключено к D.E.E.P.</div>
    <div id="chat">
        <div class="msg deep">╔══════════════════════════════════╗<br>║  D.E.E.P. Assistant Online  ║<br>╚══════════════════════════════════╝</div>
    </div>
    <div id="input-area">
        <input id="cmd" type="text" placeholder="Введите команду..." autofocus>
        <button id="send" onclick="sendCommand()">▶</button>
    </div>

    <script>
        const chat = document.getElementById('chat');
        const cmd = document.getElementById('cmd');
        const status = document.getElementById('status');

        function addMessage(text, sender) {
            const now = new Date().toLocaleTimeString('ru-RU');
            const color = sender === 'user' ? 'user' : 'deep';
            chat.innerHTML += `<div class="msg ${color}"><span class="time">[${now}]</span><br>${text.replace(/\\n/g, '<br>')}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }

        async function sendCommand() {
            const text = cmd.value.trim();
            if (!text) return;
            
            addMessage(text, 'user');
            cmd.value = '';
            status.textContent = '● Обработка...';
            
            try {
                const res = await fetch('/api/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({cmd: text})
                });
                const data = await res.json();
                addMessage(data.response, 'deep');
                status.textContent = '● Подключено к D.E.E.P.';
            } catch (e) {
                addMessage('[ОШИБКА] Нет связи с сервером', 'deep');
                status.textContent = '● Ошибка подключения';
            }
        }

        cmd.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendCommand();
        });
    </script>
</body>
</html>
"""

@web_app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@web_app.route('/api/ask', methods=['POST'])
def api_ask():
    data = request.json
    cmd = data.get('cmd', '')
    result, sender = process_command(cmd)
    if result:
        return jsonify({'response': result, 'sender': sender})
    return jsonify({'response': 'Готово.', 'sender': 'D.E.E.P.'})

def start_web_server():
    """Запускает веб-сервер в отдельном потоке"""
    print("\n  [*] Веб-сервер запущен!")
    print("  [*] Откройте в браузере: http://localhost:5050")
    
    # Показываем локальный IP для телефона
    import socket
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
        print(f"  [*] С телефона: http://{local_ip}:5050")
    except:
        pass
    
    web_app.run(host='0.0.0.0', port=5050, debug=False)

def start_web_server_only():
    """Запускает только веб-сервер (без основной консоли)"""
    import socket
    
    print("  [*] Веб-сервер запущен!")
    
    # Показываем IP адреса
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
        print(f"  [*] С телефона: http://{local_ip}:5050")
    except:
        pass
    
    web_app.run(host='0.0.0.0', port=5050, debug=False)

# ====== ГЛАВНЫЙ ЦИКЛ ======
def main():
    show_boot_sequence()
    init_session()
    threading.Thread(target=hotkey_listener, daemon=True).start()
    
    tray_icon = create_tray_icon()
    threading.Thread(target=tray_icon.run, daemon=True).start()
    print("  [*] Нажмите Ctrl+G для голосовой команды.")
    print("  [*] Команда 'свернись' чтобы свернуть в трей.")
    print("  [*] Закрывайте через EXIT или иконку в трее.\n")
    
    if sys.platform == 'win32':
        import ctypes
        import signal
        
        def console_handler(ctrl_type):
            if ctrl_type in (2, 5):
                hide_console()
                return True
            return False
        
        ctypes.windll.kernel32.SetConsoleCtrlHandler(
            ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_ulong)(console_handler), 
            True
        )
    
    while True:
        try:
            prompt = get_prompt()
            print(prompt, end='', flush=True)
            user_input = input()
            
            if not user_input.strip():
                continue
            
            print()
            print_box(user_input, "ПОЛЬЗОВАТЕЛЬ")
            result, sender = process_command(user_input)
            
            if result:
                print()
                if sender == "D.E.E.P.":
                    print_box(result, "D.E.E.P.")
                    save_to_history(user_input, result)  # ← ДОБАВЬ ЭТУ СТРОКУ
                    threading.Thread(target=speak, args=(result[:300],), daemon=True).start()
                else:
                    print(result)
                print()
        
        except KeyboardInterrupt:
            print("\n\n  [!] Для выхода используйте команду EXIT.")
        except EOFError:
            # Сворачиваем при закрытии
            print("\n  [*] Сворачиваюсь в трей...")
            hide_console()
            while True:
                time.sleep(1)
        except Exception as e:
            print(f"\n  [КРИТИЧЕСКАЯ ОШИБКА] {safe_encode(str(e))}")

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        print("\n\n  [*] Принудительное завершение.")
