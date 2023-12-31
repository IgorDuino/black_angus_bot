# Generated by Django 4.2.1 on 2023-08-21 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("codes", "0002_remove_uniquecode_is_active_uniquecode_used"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="code",
            options={
                "verbose_name": "Кодовое слово",
                "verbose_name_plural": "Кодовые слова",
            },
        ),
        migrations.AlterModelOptions(
            name="uniquecode",
            options={
                "verbose_name": "Уникальный код",
                "verbose_name_plural": "Уникальные коды",
            },
        ),
        migrations.AlterField(
            model_name="code",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="code",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Активен?"),
        ),
        migrations.AlterField(
            model_name="code",
            name="max_uses",
            field=models.IntegerField(
                default=0, verbose_name="Лимит использований (0 - без лимита)"
            ),
        ),
        migrations.AlterField(
            model_name="code",
            name="phrase",
            field=models.CharField(max_length=255, verbose_name="Кодовое слово"),
        ),
        migrations.AlterField(
            model_name="code",
            name="uses",
            field=models.IntegerField(default=0, verbose_name="Использовано раз"),
        ),
        migrations.AlterField(
            model_name="uniquecode",
            name="code",
            field=models.CharField(max_length=255, unique=True, verbose_name="Уникальный код"),
        ),
        migrations.AlterField(
            model_name="uniquecode",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="uniquecode",
            name="phrase_code",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="codes.code",
                verbose_name="Кодовое слово",
            ),
        ),
        migrations.AlterField(
            model_name="uniquecode",
            name="used",
            field=models.BooleanField(default=False, verbose_name="Использован?"),
        ),
    ]
