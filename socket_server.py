import socketio
import eventlet
from threading import Thread
from tools.env_analyzer import EnvironmentAnalyzer

# تهيئة Socket.IO وتحليل البيئة
sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
analyzer = EnvironmentAnalyzer()

def start_socket_server():
    # تشغيل السيرفر في خيط منفصل
    app = socketio.WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('', 5001)), app)

def background_analysis_task():
    """ مهمة دورية لتحليل البيئة وإرسال التنبيهات """
    while True:
        analysis = analyzer.analyze()
        recommendation = analyzer._generate_recommendation(analysis)
        
        # إرسال النتائج لجميع العملاء المتصلين
        sio.emit('env_update', {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'recommendation': recommendation
        })
        
        eventlet.sleep(60)  # كل 60 ثانية

@sio.event
def connect(sid, environ):
    print(f'✅ Client connected: {sid}')
    Thread(target=background_analysis_task).start()

@sio.event
def start_realtime_scan(sid, data):
    target = data.get('target')
    sio.emit('scan_status', {'status': 'started', 'target': target}, room=sid)
    
    # تنفيذ الفحص هنا (مثال باستخدام nmap)
    # ... [كود التنفيذ] ...