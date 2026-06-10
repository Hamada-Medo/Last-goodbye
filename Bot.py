import asyncio
import logging
import os

from telegram import Update
from telegram.ext import Application, ChatMemberHandler, ContextTypes

# ── Configuration ──────────────────────────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

LEAVE_MESSAGE = (
    "A member left the channel. Leave this Channel and join us in Medify 👋"
)
# ───────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def handle_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fired whenever a chat-member status changes."""
    result = update.chat_member  # ChatMemberUpdated object

    old_status = result.old_chat_member.status  # e.g. "member", "administrator"
    new_status = result.new_chat_member.status  # e.g. "left", "kicked"

    # A member left voluntarily OR was removed (kicked)
    if old_status in ("member", "administrator", "restricted") and new_status in ("left", "kicked"):
        chat_id = result.chat.id
        logger.info(
            "Member left: %s (chat_id=%s)",
            result.old_chat_member.user.full_name,
            chat_id,
        )
        await context.bot.send_message(chat_id=chat_id, text=LEAVE_MESSAGE)


def main() -> None:
    if BOT_TOKEN == "8706710887:AAHRSdBnHSw4dwZszaQjKS8J4i3WL9Ltmm4":
        raise ValueError(
            "Please set your bot token: edit BOT_TOKEN in the script "
            "or export the BOT_TOKEN environment variable."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    # ChatMemberHandler catches both chat_member and my_chat_member updates
    app.add_handler(ChatMemberHandler(handle_chat_member, ChatMemberHandler.CHAT_MEMBER))

    logger.info("Bot is running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=["chat_member"])


if __name__ == "__main__":
    main()
