import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# المفاتيح
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# عميل OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# اسم البوت كما هو على تيليقرام (صغير وحرف @ مش داخل في المتغير)
BOT_USERNAME = "rahim_ai_bot"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()
    chat_type = update.message.chat.type

    # تجاهل رسائل القروبات إلا إذا تم ذكر اسم البوت أو التاق
    if chat_type in ['group', 'supergroup']:
        if f"@{BOT_USERNAME}" not in message_text and "رحيم" not in message_text:
            return

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي وودود اسمه رحيم."},
                {"role": "user", "content": message_text}
            ]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("حصل خطأ، حاول مرة تانية.")

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()
