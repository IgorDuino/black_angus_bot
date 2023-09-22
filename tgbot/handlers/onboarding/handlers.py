from datetime import datetime, timedelta
import logging
import re

from dtb import settings

from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler
from tgbot import states
import tgbot.handlers.onboarding.keyboards as keyboards

from text_manager.models import texts, button_texts
from codes.models import Code, UniqueCode
from users.models import User


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    user = User.get_user(update)
    if user:
        created = False
    else:
        if settings.DISABLE_FOR_NEW_USERS:
            context.bot.send_message(
                chat_id=update.effective_user.id,
                text=texts.disabled_for_new_users,
                parse_mode=ParseMode.HTML,
            )
            return
        user = User(
            user_id=update.effective_user.id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name,
        )
        user.save()
        created = True

    if created:
        start_code = update.message.text.split(" ")[1] if len(update.message.text.split(" ")) > 1 else None
        if start_code:
            referrer = User.objects.filter(user_id=start_code).first()
            if referrer:
                user.deep_link = start_code

    user.is_active = True
    user.save()

    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=texts.start.format(
            code_text=f"Крайний полученный код: <code>{user.last_gotten_code}</code>\n\n"
            if user.last_gotten_code
            else ""
        ),
        reply_markup=keyboards.user_menu(user),
        parse_mode=ParseMode.HTML,
    )

    context.user_data.clear()

    return ConversationHandler.END


def handle_code(update: Update, context: CallbackContext):
    user = User.get_user(update)

    last_gotten_code_phrase = UniqueCode.objects.filter(code=user.last_gotten_code).first()
    if last_gotten_code_phrase:
        last_gotten_code_phrase = last_gotten_code_phrase.phrase_code.phrase

    if last_gotten_code_phrase == update.message.text.strip() and (
        (user.last_gotten_code_time + timedelta(days=3)).timestamp() > datetime.now().timestamp()
    ):
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text=texts.same_code_too_early,
            reply_markup=keyboards.user_menu(user),
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    code = Code.objects.filter(phrase=update.message.text).first()
    if (not code) or (code and (not code.is_valid)):
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text=texts.code_not_found,
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    unique_code = UniqueCode.objects.filter(phrase_code=code, used=False).first()
    if not unique_code:
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text=texts.unique_code_not_found,
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    unique_code.used = True
    unique_code.save()

    code.uses += 1
    code.save()

    user.last_gotten_code = unique_code.code
    user.last_gotten_code_time = datetime.now()
    user.save()

    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=texts.code_successfully_gotten.format(code=user.last_gotten_code),
        reply_markup=keyboards.user_menu(user),
        parse_mode=ParseMode.HTML,
    )

    return ConversationHandler.END


def instructions(update: Update, context: CallbackContext):
    user = User.get_user(update)

    code = UniqueCode.objects.filter(code=user.last_gotten_code).first().phrase_code

    update.callback_query.edit_message_text(
        text=code.instructions.format(code=user.last_gotten_code),
        reply_markup=keyboards.user_menu(user),
        parse_mode=ParseMode.HTML,
    )

    return ConversationHandler.END


def conditions(update: Update, context: CallbackContext):
    user = User.get_user(update)

    code = UniqueCode.objects.filter(code=user.last_gotten_code).first().phrase_code

    update.callback_query.edit_message_text(
        text=code.conditions.format(code=user.last_gotten_code),
        reply_markup=keyboards.user_menu(user),
        parse_mode=ParseMode.HTML,
    )

    return ConversationHandler.END
