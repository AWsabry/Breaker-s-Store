# Generated by Django 3.2.3 on 2022-07-22 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_and_orders', '0019_auto_20220722_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='codes',
            name='total_profit_calculated_from_sales',
            field=models.FloatField(default=0),
        ),
    ]