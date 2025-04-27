import ollama
import json
import re

class AICyberCommander:
    def __init__(self):
        self.tools = {
            'nmap': 'nmap -sV --script vuln {target}',
            'nikto': 'nikto -h {target} -Tuning x567',
            'sqlmap': 'sqlmap -u {target} --risk=3 --level=5 --batch',
            'whatweb': 'whatweb -v -a=3 {target}',
            'theharvester': 'theHarvester -d {target} -b all'
        }
        
    def generate_command(self, target):
        prompt = f"""
        {{
            "instruction": "اختر أداة من القائمة: {list(self.tools.keys())}",
            "examples": [
                {{"input": "http://example.com", "output": {{"tool": "nikto", "command": "nikto -h http://example.com"}}}},
                {{"input": "192.168.1.1", "output": {{"tool": "nmap", "command": "nmap -sV 192.168.1.1"}}}}
            ],
            "input": "{target}"
        }}
        """
        
        try:
            response = ollama.generate(
                model='deepseek-r1:7b',
                prompt=prompt,
                format='json',
                options={'temperature': 0.1}
            )
            
            json_str = response['response'].split('```json')[1].split('```')[0].strip()
            command_data = json.loads(json_str)
            return {
                'tool': command_data['tool'],
                'command': self.tools[command_data['tool']].format(target=target)
            }
            
        except Exception as e:
            print(f"⚠️ خطأ في توليد الأمر: {str(e)}")
            return None