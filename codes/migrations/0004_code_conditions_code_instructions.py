# Generated by Django 4.2.1 on 2023-09-22 12:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("codes", "0003_alter_code_options_alter_uniquecode_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="code",
            name="conditions",
            field=models.TextField(
                default="Крайний полученный код: <code>{code}</code> Условия: 🔸 Обязательно быть подписанным на каналы Гамбринус и Блэк Ангус 🔸Уникальный сертификат-код дает право на скидку 50% от счета, но не более 3000 рублей. 🔸 Применяется на все меню в сети ресторанов “Гамбринус” и стейк-хауса “Black Angus” 🔸 Скидка предоставляется при бронировании стола с пометкой наличия уникального сертификат-кода 🔸 Не распространяется на деловые обеды, услугу “с собой” 🔸 Не суммируется с другими скидками, акциями и спецпредложениями. 🔸 Не действует по пятницам Данным сертификат-кодом можно воспользоваться до 31.10.2023 До встречи в ресторанах сети “Гамбринус” и стейк-хаусе “Black Angus”!",
                max_length=10000,
                verbose_name="Условия",
            ),
        ),
        migrations.AddField(
            model_name="code",
            name="instructions",
            field=models.TextField(
                default="Крайний полученный код: <code>{code}</code> Инструкция: Для того, чтобы воспользоваться уникальным сертификат-кодом необходимо забронировать столик в удобном для Вас ресторане по ссылке: 👉🏼 https://gambrinus.ru/pivnierestorani 👉🏼 https://blackangus.rest/bron Или по телефону : «Гамбринус» +7(499)380-87-77 «Black Angus» +7(499)113-00-01 📌 Скидка предоставляется при бронировании стола с пометкой о наличии сертификат-кода. 📌Перед заказом необходимо предъявить уникальный сертификат-код сотруднику ресторана. Срок действия данного сертификат-кода до 31.10.2023 Ознакомиться с меню можно по ссылке: 👉🏼 https://gambrinus.ru/kitchen 👉🏼 https://blackangus.rest/kitchen Также ,от нашей программы лояльности Козырная Карта, мы дарим подарок по кодовому слову: ▫️ MOSGA для получения подарка в «Гамбринус» ▫️ MOSBA для получения подарка в «Black Angus» 💰 Скачать Козырную карту можно по ссылке http://www.trump.ru/ *кодовое слово необходимо ввести в приложении, в разделе промокоды. До встречи в ресторанах сети “Гамбринус” и стейк-хаусе “Black Angus”!",
                max_length=10000,
                verbose_name="Инструкции",
            ),
        ),
    ]
