from flask import Flask, request, Response
import cv2
import numpy as np
import os

app = Flask(__name__)
last_frame = None

# Rasmlar saqlanadigan papka (ixtiyoriy)
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

@app.route('/upload', methods=['POST'])
def upload():
    global last_frame
    if 'image' in request.files:
        file = request.files['image'].read()
        # Rasmni xotiraga o'qish (cv2 uchun)
        nparr = np.frombuffer(file, np.uint8)
        last_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Rasmni kompyuterga saqlash
        cv2.imwrite('screenshots/last_screen.jpg', last_frame)
        return "OK", 200
    return "Rasm topilmadi", 400

def generate():
    while True:
        if last_frame is not None:
            # MJPEG formatida oqim yaratish
            ret, buffer = cv2.imencode('.jpg', last_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Brauzerda jonli ko'rish uchun sahifa
    return """
    <html>
        <head><title>Live Screen Stream</title></head>
        <body style="background: #222; color: white; text-align: center;">
            <h1>Android Ekran Oqimi</h1>
            <img src="/video_feed" style="width: 300px; border: 2px solid #00ff00;">
            <p>Oxirgi rasm 'screenshots' papkasiga saqlandi.</p>
        </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Server ishga tushdi: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)