# Generated by Django 3.2.9 on 2022-01-21 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_auto_20220121_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='published_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]