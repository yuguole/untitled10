# Generated by Django 2.0.4 on 2018-05-12 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Iknow', '0020_auto_20180505_1802'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='askinfo',
            options={'ordering': ['-ask_time']},
        ),
    ]
