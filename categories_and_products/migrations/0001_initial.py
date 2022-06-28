# Generated by Django 3.2.3 on 2022-06-22 17:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code_Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeCategory', models.CharField(blank=True, max_length=250)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, upload_to='categories')),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Games',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gameName', models.CharField(blank=True, max_length=250)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, upload_to='categories')),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Games',
            },
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Promocode', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('percentage', models.FloatField(blank=True, default=0.0, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'PromoCodes',
            },
        ),
        migrations.CreateModel(
            name='Codes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeName', models.CharField(blank=True, max_length=250)),
                ('code', models.CharField(blank=True, max_length=1000)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, upload_to='codes')),
                ('description', models.TextField(blank=True)),
                ('price', models.FloatField(default=0)),
                ('oldPrice', models.FloatField(blank=True, default=0, null=True)),
                ('active', models.BooleanField(default=True)),
                ('Most_Popular', models.BooleanField(default=False)),
                ('Best_Offer', models.BooleanField(default=False)),
                ('New_Products', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('stock', models.IntegerField()),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categories_and_products.code_categories')),
            ],
            options={
                'verbose_name_plural': 'Codes',
            },
        ),
        migrations.AddField(
            model_name='code_categories',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categories_and_products.game'),
        ),
    ]