# Generated by Django 3.1.2 on 2020-11-03 05:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='date_posted',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
