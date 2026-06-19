from flask import Flask, request
import telebot
import os

# التوكن هنخفيه في إعدادات فيرسيل بعدين للأمان
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN, threaded=False)

app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return 'OK', 200
        return 'Invalid Content-Type', 400
    return 'البوت شغال بنجاح على سيرفر Vercel! 🚀'

# أمر البداية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك يا بطل! البوت شغال بنجاح 24 ساعة على Vercel 🚀")

# رد تجريبي على أي رسالة
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"أنا سامعك! رسالتك المكتوبة هي: {message.text}")
