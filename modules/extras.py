import os
import sys
import socket
import time
import pystray
import winreg
from PIL import Image, ImageDraw
from datetime import datetime

def get_weather(city="Москва"):
    try:
        import requests
        url = f"https://wttr.in/{city}?format=j1&lang=ru"
        r = requests.get(url, timeout=10)
        data = r.json()
        current = data['current_condition'][0]
        return (f"Погода в {city}:\n"
                f"Температура: {current['temp_C']} C\n"
                f"{current['weatherDesc'][0]['value']}\n"
                f"Ветер: {current['windspeedKmph']} км/ч\n"
                f"Влажность: {current['humidity']}%")
    except:
        return "[ОШИБКА] Не удалось получить погоду."

def _notes_file():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, 'data', 'notes.txt')

def add_note(text):
    with open(_notes_file(), 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now().strftime('%d.%m.%Y %H:%M')}] {text}\n")
    return f"Заметка сохранена: {text}"

def show_notes():
    try:
        with open(_notes_file(), 'r', encoding='utf-8') as f:
            notes = f.read()
        if notes.strip():
            lines = notes.strip().split('\n')
            result = "ЗАМЕТКИ:\n"
            for i, line in enumerate(lines, 1):
                result += f"  [{i}] {line}\n"
            return result
        return "Заметок нет."
    except:
        return "Заметок нет."
    
def edit_note(num, new_text):
    try:
        with open(_notes_file(), 'r', encoding='utf-8') as f:
            lines = f.readlines()
        idx = int(num) - 1
        if 0 <= idx < len(lines):
            old = lines[idx].strip()
            timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
            lines[idx] = f"[{timestamp}] {new_text}\n"
            with open(_notes_file(), 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return f"Заметка [{num}] обновлена:\nБыло: {old}\nСтало: [{timestamp}] {new_text}"
        return "Неверный номер заметки."
    except:
        return "[ОШИБКА] Не удалось изменить заметку."
    
def delete_note(num):
    try:
        with open(_notes_file(), 'r', encoding='utf-8') as f:
            lines = f.readlines()
        idx = int(num) - 1
        if 0 <= idx < len(lines):
            deleted = lines.pop(idx).strip()
            with open(_notes_file(), 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return f"Удалено: {deleted}"
        return "Неверный номер заметки."
    except:
        return "[ОШИБКА] Не удалось удалить заметку."

def clear_notes():
    print("  [!] Удалить ВСЕ заметки? (y/n): ", end='')
    if input().strip().lower() in ['y', 'yes', 'да']:
        with open(_notes_file(), 'w', encoding='utf-8') as f:
            f.write('')
        return "Все заметки удалены."
    return "Отмена."

def get_ips():
    import requests
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    try:
        external_ip = requests.get("https://api.ipify.org", timeout=5).text
    except:
        external_ip = "не определён"
    return f"Локальный IP: {local_ip}\nВнешний IP: {external_ip}"

FAVORITES = {
    '1': ('хром', 'Google Chrome'),
    '2': ('яндекс', 'Yandex Browser'),
    '3': ('стим', 'Steam'),
    '4': ('happ', 'Happ'),
    '5': ('калькулятор', 'Калькулятор'),
    '6': ('блокнот', 'Блокнот'),
    '7': ('проводник', 'Проводник'),
    '8': ('vs code', 'VS Code'),
    '9': ('телеграм', 'Telegram'),
    '10': ('дискорд', 'Discord'),
    '11': ('документы', 'Документы'),
    '12': ('загрузки', 'Загрузки'),
}

def show_favorites():
    print("\nБЫСТРЫЙ ДОСТУП (LIST)\n=======================")
    for key, (cmd, name) in FAVORITES.items():
        print(f"  [{key}] {name}")
    print("\n  Введите номер или EXIT для выхода\n")

SESSION_FILE = None

def init_session():
    global SESSION_FILE
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    history_dir = os.path.join(base, 'data', 'history')
    os.makedirs(history_dir, exist_ok=True)
    SESSION_FILE = os.path.join(history_dir, f"session_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
    with open(SESSION_FILE, 'w', encoding='utf-8') as f:
        f.write(f"D.E.E.P. Assistant - Сессия от {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n{'='*60}\n\n")

def save_to_history(user_msg, deep_response):
    if SESSION_FILE:
        with open(SESSION_FILE, 'a', encoding='utf-8') as f:
            f.write(f"ЗАПРОС [{datetime.now().strftime('%H:%M:%S')}]\n{user_msg}\n\nОТВЕТ\n{deep_response}\n{'-'*60}\n\n")

def check_autostart():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, "DEEP_Assistant")
        winreg.CloseKey(key)
        return True
    except:
        return False

def enable_autostart():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bat_path = os.path.join(base, 'запуск.bat')
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DEEP_Assistant", 0, winreg.REG_SZ, f'"{bat_path}"')
        winreg.CloseKey(key)
        return True
    except:
        return False

def disable_autostart():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "DEEP_Assistant")
        winreg.CloseKey(key)
        return True
    except:
        return False

def create_tray_icon():
    image = Image.new('RGB', (64, 64), color='black')
    draw = ImageDraw.Draw(image)
    draw.rectangle([8, 8, 56, 56], fill='#00ff00', outline='#00cc00', width=2)
    draw.text((18, 12), "D", fill='black')
    def on_show(icon, item): show_console()
    def on_exit(icon, item): icon.stop(); os._exit(0)
    return pystray.Icon("DEEP", image, "D.E.E.P. Assistant", pystray.Menu(
        pystray.MenuItem("Показать", on_show, default=True),
        pystray.MenuItem("Выход", on_exit)))

def show_console():
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 9)

def hide_console():
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)