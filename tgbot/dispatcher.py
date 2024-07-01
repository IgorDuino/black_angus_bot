from telegram.ext import (
    Dispatcher,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    PicklePersistence,
)

from dtb.settings import DEBUG

from tgbot.main import bot
from tgbot.utils import error

from tgbot.handlers.onboarding import handlers as onboarding_handlers


def s(pattern) -> callable:
    def check(string):
        return string.startswith(pattern)

    return check


def setup_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler("start", onboarding_handlers.start, pass_user_data=True))

    dp.add_handler(
        MessageHandler(Filters.text, onboarding_handlers.handle_code, pass_user_data=True)
    )

    dp.add_handler(
        MessageHandler(Filters.photo, onboarding_handlers.handle_image, pass_user_data=True)
    )

    dp.add_handler(CallbackQueryHandler(onboarding_handlers.conditions, pattern=s("conditions")))
    dp.add_handler(
        CallbackQueryHandler(onboarding_handlers.instructions, pattern=s("instructions"))
    )
    dp.add_handler(
        CallbackQueryHandler(
            onboarding_handlers.check_resolve, pattern=s("check_resolve"), pass_user_data=True
        )
    )
    dp.add_handler(
        CallbackQueryHandler(
            onboarding_handlers.check_resolve, pattern=s("check_resolve"), pass_user_data=True
        )
    )
    dp.add_handler(
        CallbackQueryHandler(
            onboarding_handlers.check_subscribed, pattern=s("check_subscribed"), pass_user_data=True
        )
    )

    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    return dp


WORKERS_N = 0 if DEBUG else 4
dispatcher = setup_dispatcher(
    Dispatcher(bot, update_queue=None, workers=WORKERS_N, use_context=True)
)
