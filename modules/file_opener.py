import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import string
from pathlib import Path

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
        except:
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
        except:
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
        'хром': 'chrome.exe', 'chrome': 'chrome.exe',
        'happ': 'Happ.exe', 'хап': 'Happ.exe',
        'яндекс': 'browser.exe', 'яндекс браузер': 'browser.exe',
        'firefox': 'firefox.exe', 'мозилла': 'firefox.exe',
        'edge': 'msedge.exe',
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
        'vs code': 'code.exe', 'vscode': 'code.exe',
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
    for env in ['ProgramFiles', 'ProgramFiles(x86)', 'LOCALAPPDATA', 'APPDATA']:
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