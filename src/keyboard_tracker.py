import rx
from pynput import keyboard
import threading

class KeyboardTracker:
    def __init__(self):
        self.subject = rx.subject.Subject() 
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener_thread = threading.Thread(target=self.listener.start)  

    def start(self):
        self.listener_thread.start()

    def on_press(self, key):
        try:
            key_name = key.char if hasattr(key, 'char') else str(key)
            self.subject.on_next(f"Key pressed: {key_name}") 
            if key == keyboard.Key.esc:  
                self.subject.on_complete()  
                self.listener.stop()  
        except Exception as e:
            self.subject.on_error(e) 

    def on_release(self, key):
        try:
            key_name = key.char if hasattr(key, 'char') else str(key)
            self.subject.on_next(f"Key released: {key_name}") 
            if key == keyboard.Key.esc:  
                self.subject.on_complete() 
                self.listener.stop()  
        except Exception as e:
            self.subject.on_error(e) 

    def stop(self):
        self.listener.stop()
        self.listener_thread.join()
