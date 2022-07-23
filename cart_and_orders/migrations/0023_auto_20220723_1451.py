# Generated by Django 3.2.3 on 2022-07-23 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_and_orders', '0022_remove_codes_price_bought_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codes',
            name='price',
            field=models.FloatField(default=0, verbose_name='Price Of This Code'),
        ),
        migrations.AlterField(
            model_name='codes',
            name='profit',
            field=models.FloatField(default=0, verbose_name='Profit From This Code'),
        ),
        migrations.AlterField(
            model_name='codes',
            name='total_profit_calculated_from_sales',
            field=models.FloatField(default=0, verbose_name='Profit From Orders'),
        ),
    ]