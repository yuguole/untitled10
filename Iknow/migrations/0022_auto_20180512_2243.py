# Generated by Django 2.0.4 on 2018-05-12 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Iknow', '0021_auto_20180512_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='askinfo',
            name='ask_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myasks', to='Iknow.UserInfo'),
        ),
    ]