import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# إعداد التسجيل (اللوغ)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# إعداد مفاتيح API
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# إنشاء عميل OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# تعريف الدالة التي تتعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    bot_username = (await context.bot.get_me()).username

    # لو الرسالة في قروب واسم البوت ما موجود فيها ولا كلمة "رحيم" → تجاهل
    if update.message.chat.type in ['group', 'supergroup']:
        if f"@{bot_username}" not in message and "رحيم" not in message:
            return

    try:
        # إرسال الرسالة لـ ChatGPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي وودود اسمه رحيم."},
                {"role": "user", "content": message}
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
