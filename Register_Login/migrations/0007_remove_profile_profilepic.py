# Generated by Django 3.2.3 on 2022-07-06 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Register_Login', '0006_alter_profile_profilepic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='ProfilePic',
        ),
    ]
