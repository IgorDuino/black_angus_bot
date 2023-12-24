from django.db import models


class MetaClass(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if not attr_name.startswith("__"):
                attrs[attr_name] = AttributeDescriptor(attr_name, attr_value)
        return super().__new__(cls, name, bases, attrs)


class MetaClassButton(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if not attr_name.startswith("__"):
                attrs[attr_name] = AttributeDescriptorButton(attr_name, attr_value)
        return super().__new__(cls, name, bases, attrs)


class AttributeDescriptor:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __get__(self, instance, owner):
        if instance is None:
            return self.value

        if Text.objects.filter(title=self.name).exists():
            return Text.objects.get(title=self.name).text
        else:
            new_text = Text(title=self.name, text=self.value)
            new_text.save()
            return new_text.text


class AttributeDescriptorButton:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __get__(self, instance, owner):
        if instance is None:
            return self.value

        if ButtonText.objects.filter(title=self.name).exists():
            return ButtonText.objects.get(title=self.name).text
        else:
            new_text = ButtonText(title=self.name, text=self.value)
            new_text.save()
            return new_text.text


class ButtonTexts(metaclass=MetaClassButton):
    conditions = "Условия"
    instructions = "Инструкция"


class Texts(metaclass=MetaClass):
    start = "{code_text}Приветствуем Вас в Телеграм боте сети ресторанов “Гамбринус” 🍻 и стейк-хауса “Black Angus” 🥩 . Для получения заветного сертификата на 3 000р. на посещение одного из наших ресторанов Вам необходимо ввести кодовое слово:"
    user_error_message = (
        "Простите, кажеться чтото пошло не так, попробуйте перезапустить бота командой /start"
    )
    disabled_for_new_users = "Извините, на данный момент отключена регистраия новых пользователей"
    code_not_found = "Неверное ключевое слово"
    unique_code_not_found = "Извините, все коды уже разобраны, скоро мы загрузим новые"
    same_code_too_early = (
        "Вы уже использовали данное кодовое слово в течении последних 3ех дней, попробуйте позже"
    )
    code_successfully_gotten = (
        "Принято🔥! Ваш уникальный код: {code}\nЧто с ним делать, читайте ниже"
    )


text_choices = [attr for attr in dir(Texts) if not attr.startswith("__")]
button_text_choices = [attr for attr in dir(ButtonTexts) if not attr.startswith("__")]


texts = Texts()
button_texts = ButtonTexts()


class Text(models.Model):
    class Meta:
        db_table = "text_table"

    title = models.CharField(
        max_length=255,
        choices=[(choice, choice) for choice in text_choices],
        unique=True,
        null=False,
        blank=False,
        verbose_name="Название",
    )

    text = models.TextField(
        max_length=5000,
        null=False,
        blank=False,
        verbose_name="Текст",
    )

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"


class ButtonText(models.Model):
    class Meta:
        db_table = "button_text_table"

    title = models.CharField(
        max_length=255,
        choices=[(choice, choice) for choice in button_text_choices],
        unique=True,
        null=False,
        blank=False,
        verbose_name="Название",
    )

    text = models.TextField(
        max_length=5000,
        null=False,
        blank=False,
        verbose_name="Текст",
    )

    class Meta:
        verbose_name = "Текст кнопки"
        verbose_name_plural = "Тексты кнопок"
