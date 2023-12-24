from telegram import Update
from telegram.ext import CallbackContext

from users.models import User


def admin_privileges(func):
    def wrapper(update: Update, context: CallbackContext):
        u = User.get_user(update)
        if not u.is_admin:
            update.message.reply_text("Forbidden")
            return
        return func(update, context)

    return wrapper
