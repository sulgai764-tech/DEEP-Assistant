"""
D.E.E.P. Web Server — отдельный сервер для доступа с телефона
"""
import sys
import os
import socket

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deep_assistant import process_command, safe_encode

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

if __name__ == '__main__':
    print("  [*] Веб-сервер D.E.E.P. запущен!")
    
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
        print(f"  [*] С телефона: http://{local_ip}:5050")
    except:
        pass
    
    web_app.run(host='0.0.0.0', port=5050, debug=False)