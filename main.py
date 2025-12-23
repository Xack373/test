import time
import requests
import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

class ScreenStreamApp(App):
    def build(self):
        # Sizning Ngrok manzilingiz
        self.server_url = "https://gwyn-sirenic-alternately.ngrok-free.dev/upload"
        self.headers = {"ngrok-skip-browser-warning": "true"}
        
        # Ekran holatini ko'rsatuvchi interfeys
        self.status_label = Label(text="Streaming: OFF")
        
        # Streamingni alohida oqimda (thread) boshlash
        threading.Thread(target=self.start_stream, daemon=True).start()
        
        return self.status_label

    def start_stream(self):
        while True:
            try:
                # 1. Screenshot olish (Bu qism Buildozer'da Android API bilan bog'lanadi)
                # Hozircha test uchun oddiy rasm yuborish mantiqi:
                img_path = "screenshot.jpg" 
                
                # 2. Serverga yuborish
                with open(img_path, 'rb') as f:
                    files = {'image': f}
                    resp = requests.post(self.server_url, headers=self.headers, files=files)
                
                if resp.status_code == 200:
                    self.status_label.text = "Streaming: ON (Success)"
                else:
                    self.status_label.text = f"Error: {resp.status_code}"
            except Exception as e:
                self.status_label.text = f"Error: {str(e)}"
            
            time.sleep(1) # Har 1 soniyada yuborish

if __name__ == '__main__':
    ScreenStreamApp().run()