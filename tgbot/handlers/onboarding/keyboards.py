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


def t(text: str) -> str:
    return f"{text}:{time.time()}"
