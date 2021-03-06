# Generated by Django 3.2.3 on 2022-07-06 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories_and_products', '0006_auto_20220624_1938'),
        ('cart_and_orders', '0004_auto_20220706_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='code',
            field=models.OneToOneField(default=12, on_delete=django.db.models.deletion.CASCADE, to='categories_and_products.codes'),
            preserve_default=False,
        ),
    ]
