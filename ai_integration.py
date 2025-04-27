import subprocess

class AIIntegrator:
    def __init__(self, model="deepseek-r1:7b"):
        self.model = model
        self.system_prompt = """أنت مساعد أمني خبير يعمل على كالي لينكس. 
        مهامك:
        - تحليل الطلبات وتحديد الأداة المناسبة
        - توليد أوامر نظام آمنة
        - مراقبة النظام لاكتشاف التهديدات
        الأدوات المتاحة: nmap, sqlmap, nikto, hydra, metasploit"""

    def generate_command(self, user_input):
        try:
            prompt = f"### System:\n{self.system_prompt}\n### User:\n{user_input}"
            result = subprocess.run(
                ['ollama', 'run', self.model],
                input=prompt.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return self._parse_output(result.stdout.decode())
        except Exception as e:
            return f"Error: {str(e)}"

    def _parse_output(self, raw_output):
        # تحليل مخرجات الذكاء الاصطناعي لاستخراج الأوامر
        if "→ التنفيذ:" in raw_output:
            return raw_output.split("→ التنفيذ:")[1].strip()
        return None