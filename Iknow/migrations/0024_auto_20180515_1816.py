# Generated by Django 2.0.4 on 2018-05-15 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iknow', '0023_auto_20180515_1759'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='replyinfo',
            options={'ordering': ['-re_time']},
        ),
        migrations.AlterField(
            model_name='replyinfo',
            name='re_time',
            field=models.CharField(max_length=60),
        ),
    ]