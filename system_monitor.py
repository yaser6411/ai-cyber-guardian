import psutil
import time

class SystemMonitor:
    @staticmethod
    def start_monitoring():
        print("\n🖥️ بدء مراقبة النظام...")
        while True:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            net = psutil.net_io_counters()
            
            print(f"\n📊 حالة النظام:")
            print(f"- استخدام CPU: {cpu}%")
            print(f"- استخدام الذاكرة: {mem}%")
            print(f"- حركة الشبكة: {net.bytes_sent/1e6:.2f}MB مرسولة")
            
            time.sleep(10)