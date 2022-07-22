# Generated by Django 3.2.3 on 2022-07-22 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories_and_products', '0007_delete_codes'),
        ('cart_and_orders', '0018_alter_codes_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='codes',
            name='price_bought_by',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='codes',
            name='profit',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='codes',
            name='codeCategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories_and_products.code_categories'),
        ),
    ]
