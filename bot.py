import re
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8876462233:AAGVHhGhq-p7ObtWxuMX-9fUUPaK6609h6w"
API_URL = "https://patel-number-api.vercel.app/number?number={}"

# Stylish text converter
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"""🔍 {to_stylish('number info bot')}

📌 /number 9876543210
📌 Ya sirf number likho: 9876543210

💀 {to_stylish('api by patel')}""",
        parse_mode="Markdown"
    )

async def number_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Detect number
    if context.args:
        number = context.args[0]
    else:
        message_text = update.message.text
        match = re.search(r'\b[6-9]\d{9}\b', message_text)
        if match:
            number = match.group()
        else:
            await update.message.reply_text(
                f"""❌ {to_stylish('invalid number')}

{to_stylish('10-digit number daalein')}
💀 {to_stylish('api by patel')}""",
                parse_mode="Markdown"
            )
            return

    # Loading
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
            
            # 🔥 BLACK QUOTE + ALL RECORDS
            reply_text = f"""<blockquote>
📱 {to_stylish('number info')}
━━━━━━━━━━━━━━━━━━━━
📞 {to_stylish('number')}: {number}
📊 {to_stylish('total records')}: {total}
━━━━━━━━━━━━━━━━━━━━\n\n"""
            
            for i, rec in enumerate(records, 1):  # 🔥 ALL RECORDS
                reply_text += f"""📌 {to_stylish(f'record #{i}')}
👤 {to_stylish('name')}: {rec.get('NAME', 'N/A')}
📛 {to_stylish('father')}: {rec.get('fname', 'N/A')}
🆔 {to_stylish('aadhaar')}: {rec.get('id', 'N/A')}
🔄 {to_stylish('alternate')}: {rec.get('alt', 'N/A')}
📡 {to_stylish('carrier')}: {rec.get('circle', 'N/A')}
📍 {to_stylish('address')}: {rec.get('ADDRESS', 'N/A')[:80]}
━━━━━━━━━━━━━━━━━━━━\n\n"""
            
            reply_text += f"""💀 {to_stylish('api by patel')}</blockquote>"""
            
            # 🔥 BLACK QUOTE - Edit loading message with blockquote
            await loading_msg.edit_text(reply_text, parse_mode="HTML")
                
        else:
            await loading_msg.edit_text(
                f"""<blockquote>
❌ {to_stylish('no data found')}

{to_stylish('kisi aur number ki koshish karein')}
💀 {to_stylish('api by patel')}</blockquote>""",
                parse_mode="HTML"
            )

    except requests.exceptions.Timeout:
        await loading_msg.edit_text(
            f"""<blockquote>
⏰ {to_stylish('timeout error')}

{to_stylish('api slow hai, try again')}
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

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"""<blockquote>
❓ {to_stylish('unknown command')}

📌 /start {to_stylish('ya')} {to_stylish('direct number daalein')}
💀 {to_stylish('api by patel')}</blockquote>""",
        parse_mode="HTML"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("number", number_info))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, number_info))
    app.add_handler(MessageHandler(filters.COMMAND, handle_unknown))

    print("🤖 Bot is running with Blockquote + All Records...")
    print("✅ Group + Private supported!")
    app.run_polling()

if __name__ == "__main__":
    main()
