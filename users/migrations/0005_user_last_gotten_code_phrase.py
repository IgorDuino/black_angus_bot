# Generated by Django 4.2.1 on 2023-09-22 12:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_user_options_alter_user_deep_link_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_gotten_code_phrase",
            field=models.CharField(
                blank=True,
                max_length=32,
                null=True,
                verbose_name="Последнее введенное кодовое слово",
            ),
        ),
    ]
