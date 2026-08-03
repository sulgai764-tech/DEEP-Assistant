import os
import sys
import time
from datetime import datetime
from core.terminal import type_text, print_box, print_banner, clear_screen
from core.utils import THEMES, save_theme
from modules.voice import listen
from modules.file_opener import open_item
from modules.ai import ask_ai
from modules.ai import search_web
from modules.ai import translate_text
from modules.extras import FAVORITES, show_favorites, get_weather, add_note, delete_note, clear_notes, show_notes, edit_note, get_ips
from modules.extras import check_autostart, enable_autostart, disable_autostart, hide_console
from updater import check_update, do_update

def process_command(cmd, cfg, version):
    cmd = cmd.strip()
    if not cmd:
        return None, None
    lower = cmd.lower()
    if lower.startswith('theme '):
        theme_name = lower[6:].strip()
        if theme_name in THEMES:
            save_theme(theme_name)
            return f"Тема изменена на {theme_name}. Перезапустите ассистента.", "D.E.E.P."
        return f"Доступные темы: {', '.join(THEMES.keys())}", "D.E.E.P."

    if lower == 'theme':
        return f"Темы: {', '.join(THEMES.keys())}\nСмена: theme название", "D.E.E.P."
    
    if len(cmd) == 1 and cmd.isalpha():
        return "Введите команду (HELP для справки).", "D.E.E.P."
    
    if lower in ['update', 'обновление']:
        remote = check_update(cfg)
        if remote and remote != version:
            print(f"\n  [!] Доступна версия v{remote} (текущая v{version})")
            confirm = input("  [*] Установить? (y/n): ").strip().lower()
            if confirm in ['y', 'yes', 'да']:
                do_update(cfg)
                return "Обновление завершено! Перезапустите ассистента.", "D.E.E.P."
            return "Обновление отменено.", "D.E.E.P."
        return f"У вас последняя версия (v{version}).", "D.E.E.P."
    
    if lower in ['help', 'помощь', '?']:
        print("""
ДОСТУПНЫЕ КОМАНДЫ:
  HELP, ?            - справка
  CLEAR, CLS         - очистить экран
  EXIT, QUIT         - выход
  RELOAD, restart    - перезагрузка
  UPDATE             - проверить и установить обновление
  LIST, СПИСОК       - избранные программы
  ГОЛОС, СЛУШАЙ      - голосовой ввод
  Ctrl+G             - быстрая голосовая команда
  СВЕРНИСЬ           - свернуть в трей
  АВТОЗАГРУЗКА       - вкл/откл автозагрузку
  THEME              - список тем
  THEME [тема]       - сменить тему (classic, amber, matrix, ocean)
  TIME, ВРЕМЯ        - дата и время
  VER, ВЕРСИЯ        - версия программы
  IP, МОЙ IP         - локальный и внешний IP
  ПОГОДА             - погода в Москве
  ПОГОДА [город]     - погода в городе
  ЗАМЕТКА [текст]    - сохранить заметку
  ЗАМЕТКИ            - показать все заметки
  ИЗМЕНИ ЗАМЕТКУ [№] [НОВАЯ ЗАПИСЬ] - изменение заметки
  УДАЛИ ЗАМЕТКУ [№]  - удаление заметки
  ОЧИСТИТЬ ЗАМЕТКИ   - очистить все заметки
  ОТКРОЙ [что]       - открыть программу, папку, файл
  ЗАПУСТИ [что]      - запустить программу
  НАЙДИ [запрос]     - поиск в интернете
  ПЕРЕВЕДИ [текст]   - перевод
  Любой вопрос       - ответ через нейросеть
""")
        return None, None
    
    if lower in ['clear', 'cls']:
        clear_screen(cfg['ASSISTANT_NAME'], version)
        print_banner(version)
        return None, None
    
    if lower in ['reload', 'перезапуск', 'restart']:
        type_text("\n  [*] Перезапуск...", float(cfg['TYPO_SPEED']))
        time.sleep(0.3)
        os.execl(sys.executable, sys.executable, *sys.argv)    
    
    if lower in ['exit', 'quit', 'выход']:
        type_text("\n  [*] До свидания!", float(cfg['TYPO_SPEED']))
        sys.exit(0)
    
    if lower in ['свернись', 'в трей', 'hide']:
        hide_console()
        return None, None
    
    if lower in ['time', 'время']:
        return f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}", "D.E.E.P."
    
    if lower in ['ver', 'версия']:
        return f"D.E.E.P. v{version}", "D.E.E.P."
    
    if lower in ['ip', 'мой ip']:
        return get_ips(), "D.E.E.P."
    
    if lower in ['автозагрузка', 'autostart']:
        if check_autostart():
            print("  [*] Автозагрузка включена. Отключить? (y/n): ", end='')
            if input().strip().lower() in ['y', 'yes', 'да']:
                disable_autostart()
                return "Автозагрузка отключена.", "D.E.E.P."
        else:
            print("  [*] Автозагрузка отключена. Включить? (y/n): ", end='')
            if input().strip().lower() in ['y', 'yes', 'да']:
                enable_autostart()
                return "Автозагрузка включена.", "D.E.E.P."
        return None, None
    
    if lower in ['голос', 'слушай']:
        spoken = listen()
        if spoken:
            print_box(spoken, "ПОЛЬЗОВАТЕЛЬ (ГОЛОС)")
            return process_command(spoken, cfg, version)
        return "Не удалось распознать речь.", "D.E.E.P."
    
    if lower in ['list', 'список']:
        show_favorites()
        while True:
            choice = input("  Номер (или EXIT): ").strip().lower()
            if choice in ['exit', 'назад']:
                break
            if choice in FAVORITES:
                target, name = FAVORITES[choice]
                result = open_item(target)
                print(f"\n  [OK] Запущено: {name}")
                break
        return None, None
    
    if lower.startswith('заметка '):
        return add_note(cmd[8:].strip()), "D.E.E.P."

    if lower in ['заметки', 'notes']:
        return show_notes(), "D.E.E.P."
    
    if lower.startswith('измени заметку '):
        parts = cmd.split(maxsplit=2)
        if len(parts) >= 3:
            return edit_note(parts[1], parts[2]), "D.E.E.P."
        return "Используйте: измени заметку [номер] [новый текст]", "D.E.E.P."

    if lower.startswith('удали заметку '):
        return delete_note(cmd[14:].strip()), "D.E.E.P."

    if lower in ['очистить заметки', 'clear notes']:
        return clear_notes(), "D.E.E.P."
    
    if lower.startswith(('открой ', 'запусти ')):
        parts = cmd.split(maxsplit=1)
        if len(parts) > 1:
            result = open_item(parts[1])
            print(f"\n  {result}\n")
            return None, None
    
    if lower.startswith(('найди ', 'поищи ')):
        query = cmd.split(maxsplit=1)[1]
        return search_web(query, cfg, type_text, float(cfg['TYPO_SPEED'])), "D.E.E.P."
    
    if lower.startswith('переведи '):
        return translate_text(cmd[9:].strip()), "D.E.E.P."

    if lower.startswith('погода'):
        parts = cmd.split(maxsplit=1)
        city = parts[1] if len(parts) > 1 else "Москва"
        return get_weather(city), "D.E.E.P."
    
    type_text("  [*] Обрабатываю...", float(cfg['TYPO_SPEED']))
    return ask_ai(cmd, cfg), "D.E.E.P."
