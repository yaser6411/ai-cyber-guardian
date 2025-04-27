import time
import subprocess
import psutil
from tools.env_analyzer import EnvironmentAnalyzer
from tools.ai_integration import AIIntegrator
from database.db import Database

class TerminalAssistant:
    def __init__(self):
        self.db = Database()
        self.ai = AIIntegrator()
        self.analyzer = EnvironmentAnalyzer()
        self.analyzer.load_historical_data(self._generate_sample_data())

    def _generate_sample_data(self):
        """بيانات تدريب أولية للنموذج"""
        return [
            {'cpu': 20, 'memory': 30, 'network': {'connections': 10}},
            {'cpu': 25, 'memory': 35, 'network': {'connections': 15}},
            {'cpu': 85, 'memory': 90, 'network': {'connections': 150}}  # حالة شاذة
        ]

    def start(self):
        print("🛡️ مساعد الأمن السيبراني الذكي - وضع المراقبة\n")
        while True:
            analysis = self.analyzer.analyze()
            self._display_analysis(analysis)
            
            if analysis['anomaly']:
                self._handle_anomaly(analysis)
            
            time.sleep(60)  # تحديث كل دقيقة

    def _display_analysis(self, data):
        """عرض نتائج التحليل بشكل منسق"""
        print(f"\n📊 [تقرير الأداء] {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"• وحدة المعالجة: {data['cpu']}%")
        print(f"• الذاكرة: {data['memory']}%")
        print(f"• اتصالات الشبكة: {data['network']['connections']}")
        print(f"💡 التوصية: {data['recommendation']}")
        print("-" * 50)

    def _handle_anomaly(self, data):
        """التعامل مع الحالات الشاذة"""
        alert_msg = f"""
        ⚠️ [تنبيه أمني] 
        تم اكتشاف شذوذ في النظام!
        الأسباب المحتملة:
        - استخدام CPU غير طبيعي: {data['cpu']}%
        - استهلاك ذاكرة مرتفع: {data['memory']}%
        - نشاط شبكة مريب: {data['network']['connections']} اتصال
        """
        print(alert_msg)
        self._take_auto_action(data)

    def _take_auto_action(self, data):
        """إجراءات تلقائية للتعامل مع التهديدات"""
        if data['cpu'] > 90:
            print("🛠️ جاري تخفيف الحمل على CPU...")
            subprocess.run(["killall", "-9", "stress"])  # مثال: إيقاف عمليات ثقيلة
            
        if data['network']['connections'] > 100:
            print("🛠️ جاري حظر الاتصالات المشبوهة...")
            subprocess.run(["iptables", "-A", "INPUT", "-j", "DROP"]) 

if __name__ == "__main__":
    assistant = TerminalAssistant()
    assistant.start()