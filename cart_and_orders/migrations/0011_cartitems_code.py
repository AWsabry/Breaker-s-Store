# Generated by Django 3.2.3 on 2022-07-12 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart_and_orders', '0010_remove_order_bromocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='code',
            field=models.ForeignKey(blank=True, default=3, on_delete=django.db.models.deletion.CASCADE, to='cart_and_orders.codes'),
            preserve_default=False,
        ),
    ]
