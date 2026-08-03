import os
import sys
import time
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import load_config
from core.terminal import show_boot_sequence, get_prompt, print_box
from core.commands import process_command
from core.utils import update_version, init_logger, write_log, log_command
from modules.voice import speak, hotkey_listener
from modules.extras import init_session, save_to_history, check_autostart, create_tray_icon, hide_console as tray_hide, show_notes
from updater import check_update

if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

cfg = load_config()
VERSION = update_version()
init_logger()

def main():
    update_msg = ""
    remote = check_update(cfg)
    if remote and remote != VERSION:
        update_msg = f"  [!] Доступна новая версия: v{remote} (введите update)\n"
    
    show_boot_sequence(cfg, VERSION, update_msg)
    init_session()
    
    notes = show_notes()
    if notes != "Заметок нет.":
        print(f"  {notes}\n")
    
    threading.Thread(target=hotkey_listener, args=(process_command, print_box, get_prompt, cfg, VERSION), daemon=True).start()
    
    tray_icon = create_tray_icon()
    threading.Thread(target=tray_icon.run, daemon=True).start()
    
    if check_autostart():
        print("  [*] Автозагрузка: ВКЛЮЧЕНА")
    print("  [*] Ctrl+G - голос, UPDATE - обновление, HELP - команды\n")
    
    if sys.platform == 'win32':
        import ctypes
        def console_handler(ctrl_type):
            if ctrl_type in (2, 5):
                tray_hide()
                return True
            return False
        ctypes.windll.kernel32.SetConsoleCtrlHandler(
            ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_ulong)(console_handler), True)
    
    while True:
        try:
            print(get_prompt(cfg['ASSISTANT_NAME']), end='', flush=True)
            user_input = input()
            if not user_input.strip():
                continue
            print()
            print_box(user_input, "ПОЛЬЗОВАТЕЛЬ")
            result, sender = process_command(user_input, cfg, VERSION)
            if result:
                print()
                if sender == "D.E.E.P.":
                    print_box(result, "D.E.E.P.")
                    save_to_history(user_input, result)
                    log_command(user_input, result)
                    threading.Thread(target=speak, args=(result[:300],), daemon=True).start()
                else:
                    print(result)
                print()
        except KeyboardInterrupt:
            print("\n\n  [!] Для выхода EXIT.")
        except EOFError:
            tray_hide()
            while True:
                time.sleep(1)
        except Exception as e:
            print(f"\n  [ОШИБКА] {str(e)}")

if __name__ == "__main__":
    main()