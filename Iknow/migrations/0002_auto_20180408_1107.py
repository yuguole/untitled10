# Generated by Django 2.0.4 on 2018-04-08 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iknow', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommentInfo',
        ),
        migrations.DeleteModel(
            name='ReplyInfo',
        ),
        migrations.AddField(
            model_name='askinfo',
            name='ask_lable',
            field=models.ManyToManyField(to='Iknow.LabelInfo'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_label',
            field=models.ManyToManyField(to='Iknow.LabelInfo'),
        ),
    ]
