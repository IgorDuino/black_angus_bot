from django.db import models


default_instructions = """Крайний полученный код: <code>{code}</code> Инструкция: Для того, чтобы воспользоваться уникальным сертификат-кодом необходимо забронировать столик в удобном для Вас ресторане по ссылке: 👉🏼 https://gambrinus.ru/pivnierestorani 👉🏼 https://blackangus.rest/bron Или по телефону : «Гамбринус» +7(499)380-87-77 «Black Angus» +7(499)113-00-01 📌 Скидка предоставляется при бронировании стола с пометкой о наличии сертификат-кода. 📌Перед заказом необходимо предъявить уникальный сертификат-код сотруднику ресторана. Срок действия данного сертификат-кода до 31.10.2023 Ознакомиться с меню можно по ссылке: 👉🏼 https://gambrinus.ru/kitchen 👉🏼 https://blackangus.rest/kitchen Также ,от нашей программы лояльности Козырная Карта, мы дарим подарок по кодовому слову: ▫️ MOSGA для получения подарка в «Гамбринус» ▫️ MOSBA для получения подарка в «Black Angus» 💰 Скачать Козырную карту можно по ссылке http://www.trump.ru/ *кодовое слово необходимо ввести в приложении, в разделе промокоды. До встречи в ресторанах сети “Гамбринус” и стейк-хаусе “Black Angus”!"""
default_conditions = """Крайний полученный код: <code>{code}</code> Условия: 🔸 Обязательно быть подписанным на каналы Гамбринус и Блэк Ангус 🔸Уникальный сертификат-код дает право на скидку 50% от счета, но не более 3000 рублей. 🔸 Применяется на все меню в сети ресторанов “Гамбринус” и стейк-хауса “Black Angus” 🔸 Скидка предоставляется при бронировании стола с пометкой наличия уникального сертификат-кода 🔸 Не распространяется на деловые обеды, услугу “с собой” 🔸 Не суммируется с другими скидками, акциями и спецпредложениями. 🔸 Не действует по пятницам Данным сертификат-кодом можно воспользоваться до 31.10.2023 До встречи в ресторанах сети “Гамбринус” и стейк-хаусе “Black Angus”!"""


class Code(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    phrase = models.CharField(max_length=255, verbose_name="Кодовое слово")
    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    max_uses = models.IntegerField(default=0, verbose_name="Лимит использований (0 - без лимита)")  # 0 means unlimited
    uses = models.IntegerField(default=0, verbose_name="Использовано раз")
    instructions = models.TextField(max_length=10000, verbose_name="Инструкции", default=default_instructions)
    conditions = models.TextField(max_length=10000, verbose_name="Условия", default=default_conditions)

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
