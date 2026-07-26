import re
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8876462233:AAGVHhGhq-p7ObtWxuMX-9fUUPaK6609h6w")
API_URL = "https://patel-number-api.vercel.app/number?number={}"

def to_stylish(text):
    stylish_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ',
        'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ',
        'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ',
        's': 'ꜱ', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ'
    }
    result = ""
    for char in text.lower():
        if char in stylish_map:
            result += stylish_map[char]
        else:
            result += char
    return result

def clean_number(number):
    number = re.sub(r'^\+?91', '', number)
    number = re.sub(r'\D', '', number)
    return number

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"""🔍 {to_stylish('number info bot')}

📌 /num 9876543210
📌 /number 9876543210
📌 Ya sirf number likho

💀 {to_stylish('api by patel')}""",
        parse_mode="Markdown"
    )

async def number_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🔥 Command se number
    if context.args:
        number = clean_number(context.args[0])
    else:
        # 🔥 Sirf number detect
        message_text = update.message.text.strip()
        match = re.search(r'(\+?91)?\s*([6-9]\d{9})', message_text)
        if match:
            number = clean_number(match.group(0))
        else:
            return

    if len(number) != 10:
        await update.message.reply_text(
            f"""❌ {to_stylish('invalid number')}
{to_stylish('10-digit number daalein')}
💀 {to_stylish('api by patel')}""",
            parse_mode="Markdown"
        )
        return

    loading_msg = await update.message.reply_text(
        f"""⏳ {to_stylish('searching...')}
🔍 {to_stylish('database me dhundh rahe hain')}
💀 {to_stylish('api by patel')}""",
        parse_mode="Markdown"
    )

    try:
        response = requests.get(API_URL.format(number), timeout=15)
        data = response.json()

        if data.get("success") and data.get("records"):
            records = data["records"]
            total = data["total_records"]
            
            reply_text = f"""<blockquote>
📱 {to_stylish('number info')}
━━━━━━━━━━━━━━━━━━━━
📞 {to_stylish('number')}: {number}
📊 {to_stylish('total records')}: {total}
━━━━━━━━━━━━━━━━━━━━\n\n"""
            
            for i, rec in enumerate(records, 1):
                reply_text += f"""📌 {to_stylish(f'record #{i}')}
👤 {to_stylish('name')}: {rec.get('NAME', 'N/A')}
📛 {to_stylish('father')}: {rec.get('fname', 'N/A')}
🆔 {to_stylish('aadhaar')}: {rec.get('id', 'N/A')}
🔄 {to_stylish('alternate')}: {rec.get('alt', 'N/A')}
📡 {to_stylish('carrier')}: {rec.get('circle', 'N/A')}
📍 {to_stylish('address')}: {rec.get('ADDRESS', 'N/A')[:80]}
━━━━━━━━━━━━━━━━━━━━\n\n"""
            
            reply_text += f"""💀 {to_stylish('api by patel')}</blockquote>"""
            
            await loading_msg.edit_text(reply_text, parse_mode="HTML")
                
        else:
            await loading_msg.edit_text(
                f"""<blockquote>
❌ {to_stylish('no data found')}
{to_stylish('kisi aur number ki koshish karein')}
💀 {to_stylish('api by patel')}</blockquote>""",
                parse_mode="HTML"
            )

    except Exception as e:
        await loading_msg.edit_text(
            f"""<blockquote>
⚠️ {to_stylish('error')}
{to_stylish(str(e)[:40])}
💀 {to_stylish('api by patel')}</blockquote>""",
            parse_mode="HTML"
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # 🔥 COMMANDS - SAB SE PEHLE ADD KARO
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("num", number_info))      # 🔥 /num command
    app.add_handler(CommandHandler("number", number_info))   # 🔥 /number command
    
    # 🔥 MESSAGE HANDLER - Number detect
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, number_info))

    print("🤖 Bot is running...")
    print("✅ /num, /number, direct number, +91 support")
    app.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()
