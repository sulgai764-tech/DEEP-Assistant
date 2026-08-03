import os
import sys
import json
import hashlib
import unicodedata
import traceback
from datetime import datetime

# ====== БЕЗОПАСНАЯ КОДИРОВКА ======
def safe_encode(text):
    if not text:
        return ""
    result = []
    for char in text:
        code = ord(char)
        if code > 0xFFFF:
            continue
        elif 0x2500 <= code <= 0x257F or 0x0400 <= code <= 0x04FF:
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

# ====== ВЕРСИЯ ======
def get_file_hash(filepath):
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def update_version():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    version_file = os.path.join(base, 'data', 'version.txt')
    hash_file = os.path.join(base, 'data', '.codehash')
    os.makedirs(os.path.join(base, 'data'), exist_ok=True)
    current_hash = get_file_hash(os.path.join(base, 'deep_assistant.py'))
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
        major, minor, patch = 2, 1, 0
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
    return f"{major}.{minor}.{patch}"

# ====== ЛОГГЕР ======
LOG_FILE = None

def init_logger():
    global LOG_FILE
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(base, 'data', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    LOG_FILE = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y-%m-%d')}.txt")
    def log_exception(exc_type, exc_value, exc_tb):
        if issubclass(exc_type, KeyboardInterrupt):
            return
        msg = f"[{datetime.now().strftime('%H:%M:%S')}] КРИТИЧЕСКАЯ ОШИБКА:\n"
        msg += ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        write_log("CRITICAL", msg)
    sys.excepthook = log_exception
    write_log("INFO", "Сессия начата")

def write_log(level, message):
    if LOG_FILE:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {level}: {message}\n")

def log_command(user_input, result):
    write_log("CMD", f"USER: {user_input}")
    if result:
        write_log("CMD", f"DEEP: {result[:100]}")

# ====== ЦВЕТА И ТЕМЫ ======
COLORS = {
    'reset': '\033[0m',
    'green': '\033[92m',
    'red': '\033[91m',
    'yellow': '\033[93m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'orange': '\033[38;5;208m',
}

THEMES = {
    'classic': {'system': 'green', 'error': 'red', 'warning': 'yellow', 'success': 'green', 'ai': 'white', 'user': 'cyan', 'border': 'green'},
    'amber': {'system': 'orange', 'error': 'red', 'warning': 'yellow', 'success': 'orange', 'ai': 'white', 'user': 'orange', 'border': 'orange'},
    'matrix': {'system': 'green', 'error': 'red', 'warning': 'green', 'success': 'green', 'ai': 'green', 'user': 'green', 'border': 'green'},
    'ocean': {'system': 'cyan', 'error': 'red', 'warning': 'yellow', 'success': 'cyan', 'ai': 'white', 'user': 'cyan', 'border': 'cyan'},
}

def load_theme():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    theme_file = os.path.join(base, 'data', 'theme.json')
    try:
        with open(theme_file, 'r') as f:
            theme_name = json.load(f).get('theme', 'classic')
            return THEMES.get(theme_name, THEMES['classic'])
    except:
        return THEMES['classic']

def save_theme(theme_name):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    theme_file = os.path.join(base, 'data', 'theme.json')
    os.makedirs(os.path.dirname(theme_file), exist_ok=True)
    with open(theme_file, 'w') as f:
        json.dump({'theme': theme_name}, f)

def colorize(text, color_name):
    return f"{COLORS.get(color_name, '')}{text}{COLORS['reset']}"