import os
from flask import Flask, render_template_string, request
import google.generativeai as genai

app = Flask(__name__)

# إعداد مفتاح الذكاء الاصطناعي من متغيرات Vercel
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    ai_model = genai.GenerativeModel('gemini-pro')
else:
    ai_model = None

# واجهة الهكرز البصرية (HTML + CSS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>رادار فحص الأمان | أحمد الدليمي</title>
    <style>
        body {
            background-color: #030303;
            color: #00ff00;
            font-family: 'Courier New', Courier, monospace;
            padding: 20px;
            text-shadow: 0 0 5px #00ff00;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            border: 1px solid #00ff00;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
            background: rgba(0, 0, 0, 0.9);
        }
        h1 { text-align: center; font-size: 24px; margin-bottom: 30px; color: #ffffff; }
        .data-item { margin: 15px 0; font-size: 16px; border-bottom: 1px dashed rgba(0, 255, 0, 0.3); padding-bottom: 5px; }
        .label { color: #88ff88; font-weight: bold; }
        .value { color: #ffffff; float: left; font-family: sans-serif; }
        .ai-report {
            margin-top: 30px;
            background: rgba(0, 40, 0, 0.3);
            border: 1px solid #00ff00;
            padding: 15px;
            border-radius: 5px;
            line-height: 1.6;
        }
        .footer { text-align: center; margin-top: 40px; font-size: 12px; color: #555; }
    </style>
</head>
<body>
    <div class="container">
        <h1>👾 رادار فحص الأمان الحسابي 👾</h1>
        <p style="text-align:center; color: #ff3333;">⚠️ تم رصد بروتوكولات جهازك بنجاح...</p>
        
        <div class="data-item">
            <span class="label">🌐 عنوان الـ IP الخارجي:</span>
            <span class="value">{{ ip }}</span>
        </div>
        <div class="data-item">
            <span class="label">📱 النظام والمتصفح (User-Agent):</span>
            <span class="value" style="font-size:12px; max-width: 60%; text-align: left; word-break: break-all;">{{ user_agent }}</span>
        </div>
        <div class="data-item">
            <span class="label">🗺️ الموقع التقريبي المتوقع:</span>
            <span class="value">{{ location }}</span>
        </div>

        <div class="ai-report">
            <h3 style="margin-top:0; color:#ffcc00;">📋 تقرير الوعي الأمني (تحليل AI):</h3>
            <p>{{ ai_analysis }}</p>
        </div>
        
        <p style="text-align: center; margin-top: 25px; color: #00ffff;">💡 نصيحة المطور أحمد الدليمي: لا تضغط على روابط مجهولة!</p>
    </div>
    <div class="footer">🔒 Security Awareness Project &copy; 2026</div>
</body>
</html>
"""

@app.route('/')
def home():
    # 1. سحب الـ IP الحقيقي للمستخدم (متوافق مع سيرفرات Vercel)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    # 2. سحب بيانات المتصفح والجهاز
    user_agent = request.headers.get('User-Agent', 'Unknown Device')
    
    # 3. سحب الدولة من سيرفر Vercel تلقائياً
    country = request.headers.get('X-Vercel-IP-Country', 'العراق (تحديد تقريبي)')
    
    # 4. تمرير البيانات لـ Gemini
    ai_analysis = "جاري تحليل الثغرات المحتملة لجهازك ونظام تشغيلك الحين..."
    if ai_model:
        try:
            prompt = f"""
            أنت خبير أمن سيبراني ومساعد للمطور أحمد الدليمي. 
            أمامك بيانات جهاز مستخدم ضغط على رابط أحمد:
            الـ IP: {ip}
            بيانات المتصفح والنظام: {user_agent}
            الموقع: {country}
            
            اكتب تقرير وعي أمني قصير باللغة العربية العامية العراقية المبسطة صدمة للمستخدم. أخبره بنوع نظامه المكتشف (مثلاً أندرويد أو آيفون أو ويندوز)، وعلمه أن الـ IP ماله والموقع مكشوفين لأي رابط يضغط عليه، واعطه نصيحة أمنية سريعة لحماية جهازه من الاختراق بأسلوب احترافي ومثير.
            """
            response = ai_model.generate_content(prompt)
            ai_analysis = response.text
        except Exception as e:
            ai_analysis = f"نظامك مكشوف وموقعك التقريبي المكتشف هو {country}."

    return render_template_string(HTML_TEMPLATE, ip=ip, user_agent=user_agent, location=country, ai_analysis=ai_analysis)

# السطر الخاص بتشغيل التطبيق على سيرفرات Vercel
app.wsgi_app = app.wsgi_app
