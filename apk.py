import time
import requests
from kivy.app import App
from jnius import autoclass # Android API ga ulanish uchun

class StreamApp(App):
    def build(self):
        # Server manzilingizni yozing (masalan Ngrok manzili)
        self.server_url = "https://gwyn-sirenic-alternately.ngrok-free.dev/upload"
        # Ngrok ogohlantirishini chetlab o'tish uchun header
        self.headers = {
            "ngrok-skip-browser-warning": "true"
        }
        self.start_streaming()
        return None

    def capture_screen(self):
        # Bu qismda Android Native API orqali MediaProjection ishlatiladi
        # Sodda ko'rinishi: Screenshot olish va yuborish
        pass 

    def start_streaming(self):
        while True:
            # Ekranni rasmga olish va POST qilish
            # requests.post(self.server_url, files={'image': img_data})
            time.sleep(0.5)