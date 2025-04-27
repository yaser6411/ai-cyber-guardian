import psutil
import numpy as np
from datetime import datetime, timedelta
from .anomaly_detector import AnomalyDetector

class EnvironmentAnalyzer:
    def __init__(self):
        self.detector = AnomalyDetector()
        self.historical_data = []

    def load_historical_data(self, data):
        """تحميل البيانات التاريخية للتدريب"""
        self.detector.train(data)
        
    def analyze(self):
        """تحليل شامل للنظام"""
        current_stats = self._collect_data()
        is_anomaly = self.detector.detect_anomaly(current_stats)
        
        return {
            **current_stats,
            'anomaly': is_anomaly,
            'recommendation': self._generate_recommendation(current_stats)
        }

    def _collect_data(self):
        """جمع البيانات الحالية"""
        return {
            'cpu': psutil.cpu_percent(interval=1),
            'memory': psutil.virtual_memory().percent,
            'network': {
                'connections': len(psutil.net_connections()),
                'bytes_sent': psutil.net_io_counters().bytes_sent
            }
        }

    def _generate_recommendation(self, data):
        """توليد توصيات ذكية"""
        recommendations = []
        
        # تحليل CPU
        if data['cpu'] > 90:
            recommendations.append("إنذار: تحميل CPU حرج!")
        elif data['cpu'] > 70:
            recommendations.append("تحذير: CPU تحت ضغط عالي")
            
        # تحليل الذاكرة
        if data['memory'] > 90:
            recommendations.append("إنذار: الذاكرة ممتلئة!")
        elif data['memory'] > 70:
            recommendations.append("تحذير: استهلاك ذاكرة مرتفع")
            
        # تحليل الشبكة
        if data['network']['connections'] > 100:
            recommendations.append("إنذار: نشاط شبكة غير عادي")
            
        return " || ".join(recommendations) if recommendations else "الحالة طبيعية"