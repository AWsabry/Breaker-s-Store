# Generated by Django 3.2.3 on 2022-07-06 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Register_Login', '0005_alter_profile_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ProfilePic',
            field=models.ImageField(null=True, upload_to='profile/'),
        ),
    ]
