# Generated by Django 3.2.9 on 2022-02-19 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0019_comment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='published_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
