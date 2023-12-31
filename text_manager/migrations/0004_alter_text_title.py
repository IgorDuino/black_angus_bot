# Generated by Django 4.2.1 on 2023-08-16 13:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("text_manager", "0003_alter_buttontext_title_alter_text_title"),
    ]

    operations = [
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
            ),
        ),
    ]
