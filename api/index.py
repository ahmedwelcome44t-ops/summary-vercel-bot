import os
from flask import Flask, request
import telebot
import google.generativeai as genai

# إعداد Flask وتليجرام
app = Flask(__name__)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN, threaded=False)

# إعداد ذكاء Gemini الاصطناعي - تم التحديث للنموذج المستقر والأحدث
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

@app.route('/api', methods=['POST'])
def respond():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    return "Invalid", 400

# رسالة الترحيب /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك يا بطل! أنا بوت الذكاء الاصطناعي التعليمي الخاص بك 🧠✨\n\nأنا جاهز الآن لشرح المناهج وتلخيص الدروس والإجابة على أي سؤال يخطر في بالك. أرسل لي سؤالك أو الدرس الذي تريد شرحه لنبدأ فوراً! 🚀")

# معالجة أي رسالة وبعتها لـ Gemini
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # توجيه الـ AI ليكون مساعد تعليمي متميز لطلاب الثانوية
        prompt = f"أنت مساعد تعليمي ذكي وخبير في مناهج الثانوية العامة. يرجى الإجابة على سؤال الطالب بشكل مبسط جداً، منظم، ومشجع باللغة العربية:\n{message.text}"
        
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        # طباعة كود الخطأ لو حدثت مشكلة مجدداً
        bot.reply_to(message, f"يا غالي حصلت مشكلة في الاتصال بجوجل، والسبب هو:\n\n{str(e)}")

@app.route('/')
def index():
    return "Bot is running perfectly!"
