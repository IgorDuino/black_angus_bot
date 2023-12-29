from datetime import datetime, timedelta
import logging

from dtb import settings

from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler
import tgbot.handlers.onboarding.keyboards as keyboards

from text_manager.models import texts
from codes.models import Code, UniqueCode, CheckRequest, UniqueGiftCode
from users.models import User

from django.db.models import Q


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    user, created = User.get_or_create(update, context)

    if created:
        start_code = (
            update.message.text.split(" ")[1] if len(update.message.text.split(" ")) > 1 else None
        )
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
    user, _ = User.get_or_create(update, context)

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
    user, _ = User.get_or_create(update, context)

    code = UniqueCode.objects.filter(code=user.last_gotten_code).first()

    if not code:
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text=texts.start,
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    code = code.phrase_code

    update.callback_query.edit_message_text(
        text=code.instructions.format(code=user.last_gotten_code),
        reply_markup=keyboards.user_menu(user),
        parse_mode=ParseMode.HTML,
    )

    return ConversationHandler.END


def conditions(update: Update, context: CallbackContext):
    user = User.get_user(update)

    code = UniqueCode.objects.filter(code=user.last_gotten_code).first()

    if not code:
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text=texts.start,
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    code = code.phrase_code

    update.callback_query.edit_message_text(
        text=code.conditions.format(code=user.last_gotten_code),
        reply_markup=keyboards.user_menu(user),
        parse_mode=ParseMode.HTML,
    )

    return ConversationHandler.END


def handle_image(update: Update, context: CallbackContext):
    user, _ = User.get_or_create(update, context)

    if UniqueGiftCode.objects.filter(used=False).count() == 0:
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text=texts.sorry_gift_codes_ended,
            reply_markup=keyboards.user_menu(user),
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    file_unique_id = update.message.photo[-1].file_unique_id
    file_id = update.message.photo[-1].file_id

    if CheckRequest.objects.filter(Q(file_unique_id=file_unique_id) | Q(fileid=file_id)).exists():
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text=texts.image_already_sent,
            reply_markup=keyboards.user_menu(user),
            parse_mode=ParseMode.HTML,
        )
        return ConversationHandler.END

    check_request = CheckRequest.objects.create(
        file_unique_id=file_unique_id,
        message_id=update.message.message_id,
        fileid=file_id,
        user=user,
    )

    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=texts.image_successfully_gotten,
        reply_markup=keyboards.user_menu(user),
        parse_mode=ParseMode.HTML,
    )

    context.bot.send_photo(
        chat_id=settings.TELEGRAM_CHECK_CHAT_ID,
        photo=update.message.photo[-1].file_id,
        caption=f"Пользователь @{user.username} ({user.user_id}) отправил чек на модерацию",
        reply_markup=keyboards.check_image(check_request.id),
    )

    return ConversationHandler.END


def check_resolve(update: Update, context: CallbackContext):
    if update.effective_chat.id != settings.TELEGRAM_CHECK_CHAT_ID:
        return

    user = User.get_user(update)

    cdata = update.callback_query.data.split(":")

    decision = cdata[1]
    request_id = int(cdata[-2])

    check_request = CheckRequest.objects.get(id=request_id)

    if decision == "decline":
        check_request.accepted = False
        check_request.processed = True
        check_request.processed_by = user
        check_request.processed_at = datetime.now()
        check_request.save()

        update.callback_query.edit_message_caption(
            caption=f"Запрос #{request_id} отклонен модератором {user.tg_str} в "
            f"{check_request.processed_at.strftime('%d.%m.%Y %H:%M')}",
        )

        try:
            context.bot.send_message(
                chat_id=check_request.user.user_id,
                text="Ваш чек был отклонен",
                reply_to_message_id=check_request.message_id,
            )
        except Exception as e:
            try:
                context.bot.send_message(
                    chat_id=check_request.user.user_id,
                    text="Ваш чек был отклонен",
                )
            except Exception as e:
                pass

        return ConversationHandler.END

    gift_type = int(cdata[-3])

    check_request.accepted = True
    check_request.processed = True
    check_request.processed_by = user
    check_request.processed_at = datetime.now()
    check_request.save()

    update.callback_query.edit_message_caption(
        caption=f"Запрос #{request_id} принят модератором {user.tg_str} в "
        f"{check_request.processed_at.strftime('%d.%m.%Y %H:%M')}",
    )
    code = UniqueGiftCode.objects.filter(gift_type=gift_type, used=False).first()
    if not code:
        context.bot.send_message(
            chat_id=settings.TELEGRAM_CHECK_CHAT_ID,
            text=f"Клиенту {check_request.user.tg_str} не был отправлен код, так как они закончились",
        )
        try:
            context.bot.send_message(
                chat_id=check_request.user.user_id,
                text=texts.sorry_gift_codes_ended,
                reply_to_message_id=check_request.message_id,
            )
        except Exception as e:
            pass

    code.used = True
    code.save()

    if gift_type == 1:
        text = texts.check_resolve_success_1.format(code=code.code)
    else:
        text = texts.check_resolve_success_2.format(code=code.code)

    try:
        context.bot.send_message(
            chat_id=check_request.user.user_id,
            text=text,
            reply_to_message_id=check_request.message_id,
        )
    except Exception as e:
        try:
            context.bot.send_message(
                chat_id=check_request.user.user_id,
                text=text,
            )
        except Exception as e:
            pass

    return ConversationHandler.END
