import logging

from telegram import Update
from telegram.ext import Application, ChatMemberHandler, CommandHandler, ContextTypes

BOT_TOKEN = "8706710887:AAHRSdBnHSw4dwZszaQjKS8J4i3WL9Ltmm4"

LEAVE_MESSAGE = (
    "هعمل نفسي مش شايف"
)

CHANNEL_ID = -1002227504339  # 🔴 Replace with your actual channel ID

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

member_counts: dict[int, int] = {}


async def on_startup(app) -> None:
    try:
        count = await app.bot.get_chat_member_count(CHANNEL_ID)
        member_counts[CHANNEL_ID] = count
        logger.info("Startup — cached member count for %s: %s", CHANNEL_ID, count)
    except Exception as e:
        logger.warning("Could not fetch member count on startup: %s", e)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Awaiting Changes")


async def handle_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = update.chat_member
    chat_id = result.chat.id

    try:
        current_count = await context.bot.get_chat_member_count(chat_id)
    except Exception as e:
        logger.warning("Could not fetch member count: %s", e)
        return

    previous_count = member_counts.get(chat_id)

    logger.info(
        "Chat %s — previous count: %s, current count: %s",
        chat_id, previous_count, current_count,
    )

    if previous_count is not None and current_count < previous_count:
        logger.info("Member count decreased in chat %s, sending message.", chat_id)
        await context.bot.send_message(chat_id=chat_id, text=LEAVE_MESSAGE, parse_mode="Markdown")

    member_counts[chat_id] = current_count


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).post_init(on_startup).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatMemberHandler(handle_chat_member, ChatMemberHandler.CHAT_MEMBER))

    logger.info("Bot is running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=["chat_member", "message"])


if __name__ == "__main__":
    main()
