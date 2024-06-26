from __future__ import annotations

from typing import Union, Optional, Tuple

from django.db import models
from django.db.models import QuerySet, Manager
from telegram import Update
from telegram.ext import CallbackContext

from tgbot.utils.info import extract_user_data_from_update
from utils.models import CreateUpdateTracker, GetOrNoneManager


class AdminUserManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


class User(CreateUpdateTracker):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(
        max_length=32, unique=True, verbose_name="Телеграм ID"
    )  # telegram user_id
    username = models.CharField(
        max_length=32, null=True, blank=True, verbose_name="Телеграм Username"
    )
    is_subscribed = models.BooleanField(default=False, verbose_name="Подписан на каналы?")
    first_name = models.CharField(max_length=256, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=256, null=True, blank=True, verbose_name="Фамилия")
    language_code = models.CharField(
        max_length=8, null=True, blank=True, default="ru", verbose_name="Язык"
    )
    deep_link = models.CharField(max_length=64, null=True, blank=True, verbose_name="Deep Link")
    is_blocked_bot = models.BooleanField(default=False, verbose_name="Заблокировал бота?")

    is_admin = models.BooleanField(default=False, verbose_name="Админ?")

    last_gotten_code = models.CharField(
        max_length=32, null=True, blank=True, verbose_name="Последний полученный код"
    )
    last_gotten_code_time = models.DateTimeField(
        null=True, blank=True, verbose_name="Время получения последнего кода"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активен?")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        if self.username:
            return self.username
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        return str(self.user_id)

    @classmethod
    def get_user(cls, update: Update) -> User:
        try:
            data = extract_user_data_from_update(update)
            return cls.objects.get(user_id=data["user_id"])
        except cls.DoesNotExist:
            return False

    @property
    def tg_str(self) -> str:
        if self.username:
            return f"@{self.username}"
        return f"{self.first_name} {self.last_name}" if self.last_name else f"{self.first_name}"

    @property
    def short_tg_str(self) -> str:
        if self.username:
            return self.username
        return self.user_id

    @classmethod
    def get_or_create(cls, update, context):
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)

        if (
            created
            and context is not None
            and context.args
            and str(context.args[0]).strip() != str(u.user_id).strip()
        ):
            u.deep_link = context.args[0]
            u.asave()

        return u, created
