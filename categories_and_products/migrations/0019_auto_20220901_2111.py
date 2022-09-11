# Generated by Django 3.2.3 on 2022-09-01 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories_and_products', '0018_auto_20220828_1853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code_categories',
            name='instruction',
        ),
        migrations.AddField(
            model_name='game',
            name='instruction',
            field=models.TextField(blank=True, default=' ', help_text='Write a guide for installing the codes in the game platfrom'),
        ),
    ]