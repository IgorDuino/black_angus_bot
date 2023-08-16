from functools import wraps
from typing import Dict, Callable

import telegram
from telegram import Update

from tgbot.main import bot


def extract_user_data_from_update(update: Update) -> Dict:
    """python-telegram-bot's Update instance --> User info"""
    user = update.effective_user.to_dict()

    return dict(
        user_id=user["id"],
        is_blocked_bot=False,
        **{
            k: user[k]
            for k in ["username", "first_name", "last_name", "language_code"]
            if k in user and user[k] is not None
        },
    )
