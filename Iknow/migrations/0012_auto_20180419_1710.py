# Generated by Django 2.0.4 on 2018-04-19 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iknow', '0011_auto_20180419_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labelinfo',
            name='lb_title',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
