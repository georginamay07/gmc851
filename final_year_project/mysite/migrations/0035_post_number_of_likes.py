# Generated by Django 3.2.9 on 2022-02-23 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0034_rename_likedtags_likedtag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='number_of_likes',
            field=models.IntegerField(default=0),
        ),
    ]
