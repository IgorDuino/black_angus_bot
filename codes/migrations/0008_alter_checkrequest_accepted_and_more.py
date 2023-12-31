# Generated by Django 4.2.1 on 2023-12-24 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_remove_user_last_gotten_code_phrase"),
        ("codes", "0007_checkrequest"),
    ]

    operations = [
        migrations.AlterField(
            model_name="checkrequest",
            name="accepted",
            field=models.BooleanField(
                blank=True, default=False, null=True, verbose_name="Принят?"
            ),
        ),
        migrations.AlterField(
            model_name="checkrequest",
            name="processed",
            field=models.BooleanField(
                blank=True, default=False, null=True, verbose_name="Обработан?"
            ),
        ),
        migrations.AlterField(
            model_name="checkrequest",
            name="processed_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Обработан в"
            ),
        ),
        migrations.AlterField(
            model_name="checkrequest",
            name="processed_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="processed_by",
                to="users.user",
                verbose_name="Обработал",
            ),
        ),
    ]
