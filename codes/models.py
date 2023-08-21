from django.db import models


class Code(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    phrase = models.CharField(max_length=255, verbose_name="Кодовое слово")
    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    max_uses = models.IntegerField(default=0, verbose_name="Лимит использований (0 - без лимита)")  # 0 means unlimited
    uses = models.IntegerField(default=0, verbose_name="Использовано раз")

    def __str__(self):
        return self.phrase

    class Meta:
        verbose_name = "Кодовое слово"
        verbose_name_plural = "Кодовые слова"

    @property
    def is_valid(self):
        return self.is_active and (self.max_uses == 0 or self.uses < self.max_uses)


class UniqueCode(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    code = models.CharField(max_length=255, unique=True, verbose_name="Уникальный код")
    phrase_code = models.ForeignKey(Code, on_delete=models.CASCADE, verbose_name="Кодовое слово")
    used = models.BooleanField(default=False, verbose_name="Использован?")

    class Meta:
        verbose_name = "Уникальный код"
        verbose_name_plural = "Уникальные коды"
