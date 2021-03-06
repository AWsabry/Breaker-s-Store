# Generated by Django 3.2.3 on 2022-06-22 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories_and_products', '0003_auto_20220622_1921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='image',
        ),
        migrations.AddField(
            model_name='game',
            name='background_image',
            field=models.ImageField(blank=True, upload_to='games'),
        ),
        migrations.AddField(
            model_name='game',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='games'),
        ),
    ]
