# Generated by Django 3.2.3 on 2022-07-06 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories_and_products', '0006_auto_20220624_1938'),
        ('cart_and_orders', '0002_auto_20220706_2319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='codeCategory',
        ),
        migrations.AddField(
            model_name='cartitems',
            name='codeCategory',
            field=models.ManyToManyField(to='categories_and_products.Code_Categories'),
        ),
    ]
