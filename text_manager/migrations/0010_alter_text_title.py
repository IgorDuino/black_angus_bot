# Generated by Django 4.1.3 on 2023-12-28 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_manager', '0009_alter_text_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='title',
            field=models.CharField(choices=[('check_resolve_success_1', 'check_resolve_success_1'), ('check_resolve_success_2', 'check_resolve_success_2'), ('code_not_found', 'code_not_found'), ('code_successfully_gotten', 'code_successfully_gotten'), ('disabled_for_new_users', 'disabled_for_new_users'), ('image_already_sent', 'image_already_sent'), ('image_successfully_gotten', 'image_successfully_gotten'), ('same_code_too_early', 'same_code_too_early'), ('sorry_gift_codes_ended', 'sorry_gift_codes_ended'), ('start', 'start'), ('unique_code_not_found', 'unique_code_not_found'), ('user_error_message', 'user_error_message')], max_length=255, unique=True, verbose_name='Название'),
        ),
    ]
