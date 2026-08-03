import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.utils import load_theme, colorize
import time
import textwrap
from datetime import datetime
from core.utils import safe_encode


def clear_screen(name="D.E.E.P.", version="0.0.0"):
    os.system('cls' if os.name == 'nt' else 'clear')
    if os.name == 'nt':
        os.system(f'title {name} v{version}')

def type_text(text, speed=0.01, end='\n'):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if speed > 0:
            time.sleep(speed)
    sys.stdout.write(end)
    sys.stdout.flush()

def print_banner(version="0.0.0", update_msg=""):
    banner = f"""
 ╔════════════════════════════════════════════════════════════════╗
 ║                                                                ║
 ║   ██████╗ ███████╗███████╗██████╗     ██████╗ ███████╗██████╗  ║
 ║   ██╔══██╗██╔════╝██╔════╝██╔══██╗   ██╔═══██╗██╔════╝██╔══██╗ ║
 ║   ██║  ██║█████╗  █████╗  ██████╔╝   ██║   ██║███████╗██████╔╝ ║
 ║   ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝    ██║   ██║╚════██║██╔═══╝  ║
 ║   ██████╔╝███████╗███████╗██║        ╚██████╔╝███████║██║      ║
 ║   ╚═════╝ ╚══════╝╚══════╝╚═╝         ╚═════╝ ╚══════╝╚═╝      ║
 ║                                                                ║
 ║            Digital Electronic Expert Processor                 ║
 ║                      v{version}                                   ║
 ╚════════════════════════════════════════════════════════════════╝
{update_msg}"""
    for line in banner.split('\n'):
        print(line)
        time.sleep(0.02)

def show_boot_sequence(cfg, version, update_msg=""):
    clear_screen(cfg['ASSISTANT_NAME'], version)
    print_banner(version, update_msg)
    print()
    for msg, delay in [("Инициализация ядра", 0.3), ("Загрузка модулей", 0.4),
                        ("Подключение нейросети", 0.5), ("Калибровка поиска", 0.3),
                        ("Загрузка команд", 0.3), ("Готов к работе", 0.2)]:
        type_text(f"  [>] {msg}... ", 0.02, end='')
        time.sleep(delay)
        type_text("OK", 0.01)
    bw = int(cfg['BOX_WIDTH'])
    print("\n  " + "=" * (bw - 4))
    type_text(f"  Запуск: {datetime.now().strftime('%d.%m.%Y %H:%M')}", 0.02)
    type_text("  Введите HELP для списка команд.", 0.01)
    print("  " + "=" * (bw - 4) + "\n")

def get_prompt(name="D.E.E.P."):
    return f"{name} [{datetime.now().strftime('%H:%M:%S')}]> "

def wrap_text(text, width):
    text = safe_encode(text)
    lines = []
    for p in text.split('\n'):
        if not p.strip():
            lines.append('')
        else:
            lines.extend(textwrap.wrap(p, width=width) or [''])
    return lines

theme = load_theme()

def print_box(text, sender, box_width=66):
    text = safe_encode(text)
    now = datetime.now().strftime('%H:%M:%S')
    
    if sender == "D.E.E.P.":
        if text.startswith('[ОШИБКА]'):
            border_color = 'red'
        elif text.startswith('[OK]'):
            border_color = 'green'
        else:
            border_color = theme['ai']
    else:
        border_color = theme['user']
    
    header = f" {sender} [{now}] "
    inner = box_width - 4
    
    print(colorize("╔" + "═" * (box_width - 2) + "╗", border_color))
    print(colorize("║" + header.ljust(box_width - 2) + "║", border_color))
    print(colorize("╠" + "═" * (box_width - 2) + "╣", border_color))
    for line in wrap_text(text, inner):
        print(colorize("║ " + line.ljust(box_width - 3) + "║", border_color))
    print(colorize("╚" + "═" * (box_width - 2) + "╝", border_color))