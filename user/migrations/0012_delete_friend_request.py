# Generated by Django 3.1.3 on 2020-12-14 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_friend_request'),
    ]

    operations = [
        migrations.DeleteModel(
            name='friend_request',
        ),
    ]
