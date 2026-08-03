import threading
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 0.9)
for v in engine.getProperty('voices'):
    if 'russian' in v.name.lower() or 'irina' in v.name.lower():
        engine.setProperty('voice', v.id)
        break

speak_lock = threading.Lock()

def speak(text):
    if not speak_lock.acquire(blocking=False):
        return
    try:
        clean = text.replace('╔', '').replace('╗', '').replace('║', '').replace('╚', '').replace('╝', '').replace('═', '').replace('╠', '').replace('╣', '')
        clean = clean.replace('[OK]', 'Открыто').replace('[ОШИБКА]', 'Ошибка').replace('[*]', '')
        engine.say(clean[:300])
        engine.runAndWait()
    except:
        pass
    finally:
        speak_lock.release()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n  Говорите...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            return r.recognize_google(audio, language="ru-RU")
        except:
            return None

def hotkey_listener(process_command, print_box, get_prompt, cfg, version):
    import keyboard
    def on_ctrl_g():
        if hasattr(hotkey_listener, 'running') and hotkey_listener.running:
            return
        hotkey_listener.running = True
        print("\n  Ctrl+G — Говорите...")
        spoken = listen()
        if spoken:
            print(f"  Вы: {spoken}")
            print()
            print_box(spoken, "ПОЛЬЗОВАТЕЛЬ (ГОЛОС)")
            result, sender = process_command(spoken, cfg, version)
            if result:
                print()
                if sender == "D.E.E.P.":
                    print_box(result, "D.E.E.P.")
                    threading.Thread(target=speak, args=(result[:300],), daemon=True).start()
                else:
                    print(result)
                print()
            print(get_prompt(), end='', flush=True)
        hotkey_listener.running = False
    keyboard.add_hotkey('ctrl+g', on_ctrl_g)