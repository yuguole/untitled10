# Generated by Django 2.0.4 on 2018-04-11 10:08

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('Iknow', '0005_auto_20180411_1641'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userinfo',
            managers=[
                ('maneger', django.db.models.manager.Manager()),
            ],
        ),
    ]
