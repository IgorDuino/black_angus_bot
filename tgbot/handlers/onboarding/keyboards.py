from typing import List
import time

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from users.models import User

from text_manager.models import button_texts


def     t(text: str) -> str:
    return f"{text}:{time.time()}"


def user_menu(user: User):
    if user.last_gotten_code is None:
        return None

    buttons = [
        InlineKeyboardButton(button_texts.conditions, callback_data=t("conditions")),
        InlineKeyboardButton(button_texts.instructions, callback_data=t("instructions")),
    ]

    return InlineKeyboardMarkup([buttons])
