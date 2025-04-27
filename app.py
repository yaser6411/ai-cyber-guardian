from flask import Flask, render_template
import threading
from realtime.socket_server import start_socket_server
from tools.env_analyzer import EnvironmentAnalyzer

app = Flask(__name__)

# تهيئة محلل البيئة
analyzer = EnvironmentAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # الحصول على بيانات التحليل
    env_data = analyzer.analyze()
    return render_template('dashboard.html', data=env_data)

def start_flask():
    app.run(port=5000, use_reloader=False)

if __name__ == '__main__':
    # تشغيل Flask في خيط منفصل
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()
    
    # تشغيل Socket.IO في الخيط الرئيسي
    start_socket_server()