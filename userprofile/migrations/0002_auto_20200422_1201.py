# Generated by Django 2.2.6 on 2020-04-22 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nikename',
            field=models.CharField(max_length=20),
        ),
    ]