# Generated by Django 3.2.9 on 2022-02-19 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0013_auto_20220215_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fave_img', models.ImageField(upload_to='images/tiles/')),
            ],
        ),
        migrations.RemoveField(
            model_name='donation',
            name='fave_image',
        ),
    ]