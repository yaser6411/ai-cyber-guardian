from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
        self.is_trained = False

    def train(self, historical_data):
        """تدريب النموذج على بيانات تاريخية"""
        X = np.array([
            [item['cpu'], item['memory'], item['network']['connections']]
            for item in historical_data
        ])
        self.model.fit(X)
        self.is_trained = True

    def detect_anomaly(self, current_stats):
        """كشف الشذوذ في البيانات الحالية"""
        if not self.is_trained:
            return False
            
        X = np.array([[
            current_stats['cpu'],
            current_stats['memory'],
            current_stats['network']['connections']
        ]])
        
        return self.model.predict(X)[0] == -1