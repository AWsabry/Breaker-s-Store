# Generated by Django 3.2.3 on 2022-07-22 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart_and_orders', '0016_alter_cartitems_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivered',
        ),
    ]
