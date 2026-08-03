import requests
import subprocess
from core.utils import safe_encode
from duckduckgo_search import DDGS

def check_internet():
    """Проверяет наличие интернета"""
    try:
        requests.get("https://cloudflare.com", timeout=3)
        return True
    except:
        return False

def ask_ollama(prompt):
    """Локальный ИИ через Ollama (без интернета)"""
    try:
        r = requests.post("http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False},
            timeout=30)
        if r.status_code == 200:
            return safe_encode(r.json().get("response", ""))
        return "[ОШИБКА OLLAMA] Модель не ответила"
    except:
        return "[ОШИБКА OLLAMA] Ollama не запущен. Установите: ollama.com"

def ask_cloudflare(prompt, account_id, api_token):
    try:
        sp = "Ты — D.E.E.P., ИИ-ассистент. Отвечай на русском. Кратко, по делу."
        r = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3.1-8b-instruct",
            headers={"Authorization": f"Bearer {api_token}"},
            json={"messages": [{"role": "system", "content": sp}, {"role": "user", "content": prompt}],
                  "max_tokens": 1000, "temperature": 0.7}, timeout=60)
        r.encoding = 'utf-8'
        if r.status_code == 200:
            data = r.json()
            if data.get("success") and "result" in data:
                return safe_encode(data["result"]["response"])
            return f"[ОШИБКА] {safe_encode(str(data)[:200])}"
        return f"[ОШИБКА {r.status_code}] {safe_encode(r.text[:200])}"
    except Exception as e:
        return f"[ОШИБКА CF] {safe_encode(str(e))}"

def ask_ai(prompt, cfg):
    """Выбирает Cloudflare или Ollama в зависимости от интернета"""
    if cfg.get('AI_PROVIDER') == "cloudflare":
        if check_internet():
            return ask_cloudflare(prompt, cfg['CF_ACCOUNT_ID'], cfg['CF_API_TOKEN'])
        else:
            return "[ОФЛАЙН] Нет интернета. Работаю через Ollama... " + ask_ollama(prompt)
    return "[ОШИБКА] Неизвестный AI_PROVIDER."
def search_web(query, cfg, type_text, speed):
    try:
        type_text("  [*] Поиск...", speed)
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return "Ничего не найдено."
        st = "\n\n".join([f"Источник {i+1}: {r['title']}\n{r['href']}\n{r['body']}" for i, r in enumerate(results)])
        type_text("  [*] Анализ...", speed)
        return ask_ai(f"Ответь на русском по источникам. Запрос: {query}\n\n{st}\n\nКратко, со ссылками.", cfg)
    except Exception as e:
        return f"[ОШИБКА ПОИСКА] {safe_encode(str(e))}"

from deep_translator import GoogleTranslator

def translate_text(text):
    try:
        return GoogleTranslator(source='auto', target='ru').translate(text)
    except:
        return "[ОШИБКА ПЕРЕВОДА]"