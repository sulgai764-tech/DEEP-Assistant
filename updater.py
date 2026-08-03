import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import urllib.request

def check_update(cfg):
    repo = cfg.get('GITHUB_REPO', 'sulgai764-tech/DEEP-Assistant')
    try:
        url = f"https://raw.githubusercontent.com/{repo}/main/data/version.txt"
        response = urllib.request.urlopen(url, timeout=5)
        return response.read().decode('utf-8').strip()
    except:
        return None

def do_update(cfg):
    repo = cfg.get('GITHUB_REPO', 'sulgai764-tech/DEEP-Assistant')
    raw = f"https://raw.githubusercontent.com/{repo}/main"
    files = ["deep_assistant.py", "server.py", "updater.py"]
    modules = ["ai.py", "search.py", "translate.py", "voice.py", "file_opener.py", 
               "autostart.py", "tray_manager.py", "favorites.py", "history.py"]
    core = ["config.py", "terminal.py", "commands.py", "version.py", "utils.py"]
    
    base = os.path.dirname(os.path.abspath(__file__))
    
    print("\n  [*] Скачиваю обновление...")
    for f in files:
        try:
            urllib.request.urlretrieve(f"{raw}/{f}", os.path.join(base, f))
            print(f"  [OK] {f}")
        except:
            print(f"  [!] {f}")
    for f in modules:
        try:
            urllib.request.urlretrieve(f"{raw}/modules/{f}", os.path.join(base, 'modules', f))
            print(f"  [OK] modules/{f}")
        except:
            pass
    for f in core:
        try:
            urllib.request.urlretrieve(f"{raw}/core/{f}", os.path.join(base, 'core', f))
            print(f"  [OK] core/{f}")
        except:
            pass
    
    print("  [*] Обновление завершено! Перезапустите ассистента.\n")