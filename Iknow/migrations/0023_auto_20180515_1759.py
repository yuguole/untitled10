# Generated by Django 2.0.4 on 2018-05-15 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iknow', '0022_auto_20180512_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='askinfo',
            name='ask_time',
            field=models.CharField(max_length=60),
        ),
    ]
