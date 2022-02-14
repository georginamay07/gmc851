# Generated by Django 3.2.9 on 2022-02-01 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reppassword',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]