import os
import django
from telegram import Bot
from telegram.ext import Updater


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtb.settings")
django.setup()

from dtb.settings import (
    TELEGRAM_LOGS_CHAT_ID,
    TELEGRAM_TOKEN,
)
from tgbot.dispatcher import setup_dispatcher


def run_polling(tg_token: str = TELEGRAM_TOKEN):
    updater = Updater(tg_token, use_context=True)
    dp = updater.dispatcher

    dp = setup_dispatcher(dp)

    bot_info = Bot(tg_token).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Polling of '{bot_link}' has started")
    bot = updater.bot
    bot.send_message(
        chat_id=TELEGRAM_LOGS_CHAT_ID,
        text="Bot started",
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    run_polling()
