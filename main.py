from ai_commander import AICyberCommander
from tool_executor import KaliToolExecutor
import re

def main():
    commander = AICyberCommander()
    
    while True:
        target = input("\n🎯 أدخل الهدف (URL/IP/اسم/رقم هاتف أو 'exit' للخروج): ").strip()
        
        if target.lower() == 'exit':
            break
            
        # تصحيح تلقائي لعناوين URL
        if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', target):
            target = f"http://{target}"
            
        command_info = commander.generate_command(target)
        
        if not command_info:
            print("⚠️ فشل في توليد الأمر، جارِ استخدام nmap كبديل...")
            command_info = {
                'tool': 'nmap',
                'command': f"nmap -sV --script vuln {target}"
            }
            
        result = KaliToolExecutor.execute(command_info)
        
        if result['success']:
            print(f"\n✅ نتائج {result['tool']}:")
            print(result['output'][:500] + "...")  # عرض جزء من المخرجات
            
            if result['vulnerabilities']:
                print("\n🚨 الثغرات المكتشفة:")
                for vuln in result['vulnerabilities']:
                    print(f"- {vuln}")
            else:
                print("\n🔍 لم يتم اكتشاف ثغرات")
        else:
            print(f"\n❌ خطأ: {result['error']}")

if __name__ == "__main__":
    main()