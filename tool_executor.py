import subprocess
import shlex
import re
from vulnerabilities_db import KNOWN_VULNERABILITIES

class KaliToolExecutor:
    @staticmethod
    def execute(command_info):
        try:
            command = command_info['command']
            print(f"\n🔧 جارِ تنفيذ: {command}")
            
            result = subprocess.run(
                shlex.split(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=600
            )
            
            target = KaliToolExecutor._extract_target(command)
            domain = KaliToolExecutor._extract_domain(target)
            vulnerabilities = KaliToolExecutor._analyze_output(result.stdout, domain)
            
            return {
                'success': True,
                'tool': command_info['tool'],
                'output': result.stdout,
                'vulnerabilities': vulnerabilities,
                'vulnerabilities_found': len(vulnerabilities) > 0
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def _analyze_output(output, domain):
        vulns = []
        if re.search(r'SQL injection|SQLi', output, re.IGNORECASE):
            vulns.append("ثغرة حقن SQL (SQLi)")
        if re.search(r'XSS|Cross-Site Scripting', output, re.IGNORECASE):
            vulns.append("ثغرة XSS")
        if re.search(r'(\bPHP/5\.|\bApache/2\.4\.(2[0-9]|3[0-9]))', output):
            vulns.append("إصدار قديم مُعرّض للثغرات")
        cve_matches = re.findall(r'CVE-\d{4}-\d{4,7}', output)
        vulns.extend([f"ثغرة مسجلة ({cve})" for cve in cve_matches])
        if not vulns and domain in KNOWN_VULNERABILITIES:
            vulns.extend(KNOWN_VULNERABILITIES[domain])
        return vulns
    
    @staticmethod
    def _extract_target(command_str):
        url_match = re.search(r'(https?://[^\s/]+)', command_str)
        ip_match = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', command_str)
        return url_match.group(1) if url_match else ip_match.group(0) if ip_match else ""
    
    @staticmethod
    def _extract_domain(target):
        if target.startswith('http'):
            return target.split('//')[1].split('/')[0]
        return target