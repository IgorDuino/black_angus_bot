# Generated by Django 4.2.1 on 2023-09-22 12:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("codes", "0004_code_conditions_code_instructions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="code",
            name="conditions",
            field=models.TextField(
                default="Крайний полученный код: <code>{code}</code><br><br>Условия:<br><br>🔸 Обязательно быть подписанным на каналы Гамбринус и Блэк Ангус<br>🔸Уникальный сертификат-код дает право на скидку 50% от счета, но не более 3000 рублей. <br>🔸 Применяется на все меню в сети ресторанов “Гамбринус” и стейк-хауса “Black Angus”<br>🔸 Скидка предоставляется при бронировании стола с пометкой наличия уникального сертификат-кода<br>🔸 Не распространяется на деловые обеды, услугу “с собой”<br>🔸 Не суммируется с другими скидками, акциями и спецпредложениями.<br>🔸 Не действует по пятницам Данным сертификат-кодом можно воспользоваться до 31.10.2023 До встречи в ресторанах сети “Гамбринус” и стейк-хаусе “Black Angus”!",
                max_length=10000,
                verbose_name="Условия",
            ),
        ),
        migrations.AlterField(
            model_name="code",
            name="instructions",
            field=models.TextField(
                default="Крайний полученный код: <code>{code}</code><br><br>Инструкция:<br>Для того, чтобы воспользоваться уникальным сертификат-кодом необходимо забронировать столик в удобном для Вас ресторане по ссылке: <br>👉🏼 https://gambrinus.ru/pivnierestorani <br>👉🏼 https://blackangus.rest/bron<br><br>Или по телефону:<br>«Гамбринус» +7(499)380-87-77<br>«Black Angus» +7(499)113-00-01<br><br>📌 Скидка предоставляется при бронировании стола с пометкой о наличии сертификат-кода.<br>📌Перед заказом необходимо предъявить уникальный сертификат-код сотруднику ресторана.<br><br>Срок действия данного сертификат-кода до 31.10.2023<br><br>Ознакомиться с меню можно по ссылке:<br>👉🏼 https://gambrinus.ru/kitchen<br>👉🏼 https://blackangus.rest/kitchen<br><br>Также ,от нашей программы лояльности Козырная Карта, мы дарим подарок по кодовому слову:<br><br>▫️ <code>{code}</code> для получения подарка в «Гамбринус» ▫️ <code>{code}</code> для получения подарка в «Black Angus»<br><br>💰 Скачать Козырную карту можно по ссылке http://www.trump.ru/ *кодовое слово необходимо ввести в приложении, в разделе промокоды.<br><br>До встречи в ресторанах сети “Гамбринус” и стейк-хаусе “Black Angus”!",
                max_length=10000,
                verbose_name="Инструкции",
            ),
        ),
    ]
