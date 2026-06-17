import os
from flask import Flask, request, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# إعداد الـ API Key
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    ai_model = genai.GenerativeModel('gemini-pro')
else:
    ai_model = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>رادار فحص الأمان | أبو بكر الحارث</title>
    <style>
        body { background-color: #030303; color: #00ff00; font-family: 'Courier New', monospace; padding: 20px; text-shadow: 0 0 5px #00ff00; text-align: center; }
        .container { max-width: 600px; margin: 50px auto; border: 1px solid #00ff00; padding: 20px; background: rgba(0, 0, 0, 0.9); box-shadow: 0 0 15px rgba(0, 255, 0, 0.2); }
        h1 { color: #ffffff; }
        .data-item { margin: 15px 0; font-size: 16px; border-bottom: 1px dashed rgba(0, 255, 0, 0.3); padding-bottom: 5px; text-align: right; }
        .label { color: #88ff88; font-weight: bold; }
        .value { color: #ffffff; float: left; font-family: sans-serif; }
        .ai-report { margin-top: 30px; background: rgba(0, 40, 0, 0.3); border: 1px solid #00ff00; padding: 15px; border-radius: 5px; text-align: right; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>👾 رادار فحص الأمان الحسابي 👾</h1>
        <p style="color: #ff3333;">⚠️ تم رصد بروتوكولات جهازك بنجاح...</p>
        
        <div class="data-item"><span class="label">🌐 عنوان الـ IP الخارجي:</span><span class="value">{{ ip }}</span></div>
        <div class="data-item"><span class="label">📱 النظام والمتصفح:</span><span class="value" style="font-size:11px;">{{ user_agent }}</span></div>
        <div class="data-item"><span class="label">🗺️ الموقع التقريبي:</span><span class="value">{{ location }}</span></div>

        <div class="ai-report">
            <h3 style="margin-top:0; color:#ffcc00;">📋 تقرير الوعي الأمني (تحليل AI):</h3>
            <p>{{ ai_analysis }}</p>
        </div>
        <p style="margin-top: 25px; color: #00ffff;">💡 نصيحة المطور: لا تضغط على روابط مجهولة!</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
    user_agent = request.headers.get('User-Agent', 'Unknown Device')
    country = request.headers.get('X-Vercel-IP-Country', 'العراق (تحديد تقريبي)')
    
    ai_analysis = f"نظامك مكشوف وموقعك التقريبي المكتشف هو {country}."
    if ai_model:
        try:
            prompt = f"أكتب نصيحة وعي أمني قصيرة جداً ومثيرة بالعامية العراقية للمستخدم صاحب هذا الـ IP: {ip} ونظامه: {user_agent} تخبره أن بياناته مكشوفة."
            response = ai_model.generate_content(prompt)
            ai_analysis = response.text
        except:
            pass

    return render_template_string(HTML_TEMPLATE, ip=ip, user_agent=user_agent, location=country, ai_analysis=ai_analysis)
