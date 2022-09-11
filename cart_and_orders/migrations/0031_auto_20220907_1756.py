# Generated by Django 3.2.3 on 2022-09-07 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_and_orders', '0030_auto_20220907_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Success', 'Success')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='codes',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Success', 'Success')], max_length=50),
        ),
    ]