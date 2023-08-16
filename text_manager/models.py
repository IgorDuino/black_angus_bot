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
    pass


class Texts(metaclass=MetaClass):
    start = "Приветствуем Вас в Телеграм боте"
    user_error_message = "Простите, кажеться чтото пошло не так, попробуйте перезапустить бота командой /start"
    disabled_for_new_users = "Извините, на данный момент отключена регистраия новых пользователей"


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
    )

    text = models.TextField(
        max_length=5000,
        null=False,
        blank=False,
    )


class ButtonText(models.Model):
    class Meta:
        db_table = "button_text_table"

    title = models.CharField(
        max_length=255,
        choices=[(choice, choice) for choice in button_text_choices],
        unique=True,
        null=False,
        blank=False,
    )

    text = models.TextField(
        max_length=5000,
        null=False,
        blank=False,
    )
