import os
import sys
import socket

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import load_config
from core.utils import update_version
from core.commands import process_command
from core.utils import update_version
from modules.ai import ask_ai, search_web, translate_text
from flask import Flask, request, jsonify, render_template_string

cfg = load_config()
VERSION = update_version()
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
        body { background: #0a0a0a; color: #00ff00; font-family: 'Courier New', monospace; height: 100vh; display: flex; flex-direction: column; padding: 10px; }
        #chat { flex: 1; overflow-y: auto; border: 2px solid #00ff00; padding: 10px; margin-bottom: 10px; font-size: 14px; }
        .msg { margin-bottom: 10px; }
        .user { color: #00ccff; }
        .deep { color: #00ff00; }
        .time { color: #555; font-size: 11px; }
        #input-area { display: flex; gap: 10px; }
        #cmd { flex: 1; background: #000; border: 2px solid #00ff00; color: #00ff00; padding: 12px; font-family: 'Courier New', monospace; font-size: 16px; outline: none; }
        #send { background: #00ff00; color: #000; border: none; padding: 12px 20px; font-weight: bold; font-size: 16px; cursor: pointer; }
    </style>
</head>
<body>
    <div id="status">● Подключено к D.E.E.P.</div>
    <div id="chat"><div class="msg deep">D.E.E.P. Assistant Online</div></div>
    <div id="input-area">
        <input id="cmd" type="text" placeholder="Введите запрос..." autofocus>
        <button id="send" onclick="sendCommand()">▶</button>
    </div>
    <script>
        const chat = document.getElementById('chat');
        const cmd = document.getElementById('cmd');
        const status = document.getElementById('status');
        async function sendCommand() {
            const text = cmd.value.trim();
            if (!text) return;
            chat.innerHTML += `<div class="msg user"><span class="time">[${new Date().toLocaleTimeString('ru-RU')}]</span><br>${text}</div>`;
            cmd.value = '';
            status.textContent = '● Обработка...';
            try {
                const res = await fetch('/api/ask', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cmd:text})});
                const data = await res.json();
                chat.innerHTML += `<div class="msg deep"><span class="time">[${new Date().toLocaleTimeString('ru-RU')}]</span><br>${data.response.replace(/\\n/g,'<br>')}</div>`;
                status.textContent = '● Подключено к D.E.E.P.';
                chat.scrollTop = chat.scrollHeight;
            } catch(e) { status.textContent = '● Ошибка'; }
        }
        cmd.addEventListener('keypress', e => { if(e.key==='Enter') sendCommand(); });
    </script>
</body>
</html>
"""

def process_web_command(cmd):
    """Обработка команд с веб-сервера (только безопасные)"""
    cmd = cmd.strip()
    if not cmd:
        return "Введите запрос."
    
    lower = cmd.lower()
    
    # Запрещённые команды
    forbidden = ['открой', 'запусти', 'покажи', 'выполни', 'exit', 'quit', 'выход', 
                 'свернись', 'hide', 'tray', 'clear', 'cls', 'update', 'обновление',
                 'автозагрузка', 'голос', 'слушай']
    
    for word in forbidden:
        if lower.startswith(word):
            return "[ДОСТУП ЗАПРЕЩЁН] Эта команда недоступна через веб-интерфейс."
    
    # Разрешённые команды
    if lower in ['help', 'помощь', '?']:
        return "Доступные команды: поиск в интернете (найди ...), перевод (переведи ...), любой вопрос к нейросети."
    
    if lower in ['time', 'время']:
        from datetime import datetime
        return f"Текущая дата и время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
    
    if lower in ['ver', 'версия']:
        return f"D.E.E.P. v{VERSION}"
    
    # Поиск
    if lower.startswith(('найди ', 'поищи ')):
        query = cmd.split(maxsplit=1)[1]
        return search_web(query, cfg, lambda *a, **k: None, 0)
    
    # Перевод
    if lower.startswith('переведи '):
        return translate_text(cmd[9:].strip())
    
    # Всё остальное — запрос к нейросети
    return ask_ai(cmd, cfg)

@web_app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@web_app.route('/api/ask', methods=['POST'])
def api_ask():
    data = request.json
    cmd = data.get('cmd', '')
    result = process_web_command(cmd)
    return jsonify({'response': result or 'Готово.'})

if __name__ == '__main__':
    print("  [*] Веб-сервер D.E.E.P. запущен!")
    print("  [*] Внимание: открытие программ через сервер запрещено.")
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
        print(f"  [*] С телефона: http://{local_ip}:5050")
    except:
        pass
    web_app.run(host='0.0.0.0', port=5050, debug=False)