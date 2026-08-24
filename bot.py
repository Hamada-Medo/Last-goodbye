from datetime import timezone
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]  # set this in Railway's Variables tab — never hardcode it
MY_CHAT_ID = 940770584


def format_header(msg):
    user = msg.from_user
    name = user.full_name if user else "Unknown"

    username = f"@{user.username}" if user and user.username else "no username"
    user_id = user.id if user else "no id"

    date = msg.date.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    return f"📌 {name} ({username}) | ID: {user_id}\n🕒 {date}\n\n"


async def mirror(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg:
        return

    header = format_header(msg)

    try:
        # TEXT
        if msg.text:
            await context.bot.send_message(
                chat_id=MY_CHAT_ID,
                text=header + msg.text
            )

        # PHOTO
        elif msg.photo:
            await context.bot.send_photo(
                chat_id=MY_CHAT_ID,
                photo=msg.photo[-1].file_id,
                caption=header + (msg.caption or "")
            )

        # VIDEO
        elif msg.video:
            await context.bot.send_video(
                chat_id=MY_CHAT_ID,
                video=msg.video.file_id,
                caption=header + (msg.caption or "")
            )

        # DOCUMENT
        elif msg.document:
            await context.bot.send_document(
                chat_id=MY_CHAT_ID,
                document=msg.document.file_id,
                caption=header + (msg.caption or "")
            )

        # AUDIO
        elif msg.audio:
            await context.bot.send_audio(
                chat_id=MY_CHAT_ID,
                audio=msg.audio.file_id,
                caption=header + (msg.caption or "")
            )

        # VOICE
        elif msg.voice:
            await context.bot.send_voice(
                chat_id=MY_CHAT_ID,
                voice=msg.voice.file_id,
                caption=header
            )

        # STICKER
        elif msg.sticker:
            await context.bot.send_sticker(
                chat_id=MY_CHAT_ID,
                sticker=msg.sticker.file_id
            )
            await context.bot.send_message(
                chat_id=MY_CHAT_ID,
                text=header + f"[Sticker: {msg.sticker.emoji or ''}]"
            )

        else:
            await context.bot.send_message(
                chat_id=MY_CHAT_ID,
                text=header + "[Unsupported message type]"
            )

    except Exception as e:
        await context.bot.send_message(
            chat_id=MY_CHAT_ID,
            text=f"❌ Error:\n{e}"
        )


app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, mirror))

app.run_polling(allowed_updates=["message"])
