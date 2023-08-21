# Generated by Django 4.2.1 on 2023-08-21 15:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("text_manager", "0004_alter_text_title"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="buttontext",
            options={
                "verbose_name": "Текст кнопки",
                "verbose_name_plural": "Тексты кнопок",
            },
        ),
        migrations.AlterModelOptions(
            name="text",
            options={"verbose_name": "Текст", "verbose_name_plural": "Тексты"},
        ),
        migrations.AlterField(
            model_name="buttontext",
            name="text",
            field=models.TextField(max_length=5000, verbose_name="Текст"),
        ),
        migrations.AlterField(
            model_name="buttontext",
            name="title",
            field=models.CharField(
                choices=[
                    ("conditions", "conditions"),
                    ("instructions", "instructions"),
                ],
                max_length=255,
                unique=True,
                verbose_name="Название",
            ),
        ),
        migrations.AlterField(
            model_name="text",
            name="text",
            field=models.TextField(max_length=5000, verbose_name="Текст"),
        ),
        migrations.AlterField(
            model_name="text",
            name="title",
            field=models.CharField(
                choices=[
                    ("code_not_found", "code_not_found"),
                    ("code_successfully_gotten", "code_successfully_gotten"),
                    ("conditions", "conditions"),
                    ("disabled_for_new_users", "disabled_for_new_users"),
                    ("instructions", "instructions"),
                    ("new_code_too_early", "new_code_too_early"),
                    ("start", "start"),
                    ("unique_code_not_found", "unique_code_not_found"),
                    ("user_error_message", "user_error_message"),
                ],
                max_length=255,
                unique=True,
                verbose_name="Название",
            ),
        ),
        migrations.AlterModelTable(
            name="buttontext",
            table=None,
        ),
        migrations.AlterModelTable(
            name="text",
            table=None,
        ),
    ]