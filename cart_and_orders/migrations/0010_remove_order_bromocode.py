# Generated by Django 3.2.3 on 2022-07-12 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart_and_orders', '0009_auto_20220712_1931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='BromoCode',
        ),
    ]
