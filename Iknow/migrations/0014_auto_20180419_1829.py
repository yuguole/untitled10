# Generated by Django 2.0.4 on 2018-04-19 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iknow', '0013_auto_20180419_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='askinfo',
            name='ask_lable',
            field=models.ManyToManyField(blank=True, to='Iknow.LabelInfo'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_label',
            field=models.ManyToManyField(blank=True, to='Iknow.LabelInfo'),
        ),
    ]
