# Generated by Django 2.0.4 on 2018-04-19 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iknow', '0008_auto_20180416_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='askinfo',
            name='ask_details',
            field=models.CharField(blank=True, default='..', max_length=600),
        ),
        migrations.AlterField(
            model_name='askinfo',
            name='ask_lable',
            field=models.ManyToManyField(blank=True, default='生活', to='Iknow.LabelInfo'),
        ),
    ]