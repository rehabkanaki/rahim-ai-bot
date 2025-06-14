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

# قراءة المتغيرات البيئية
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# إعداد عميل OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# الدالة الرئيسية لمعالجة الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    chat_type = update.message.chat.type
    bot_username = (await context.bot.get_me()).username.lower()

    # الشرط: في القروبات فقط، لازم تحتوي الرسالة على @اسم_البوت أو كلمة "رحيم"
    if chat_type in ['group', 'supergroup']:
        if f"@{bot_username}" not in message_text.lower() and "رحيم" not in message_text.lower():
            return  # تجاهل الرسالة

    try:
        # إرسال الرسالة إلى ChatGPT
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

# تشغيل التطبيق
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()
