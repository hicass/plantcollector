# Generated by Django 4.2.1 on 2023-06-02 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_growingmedia_alter_watering_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='growing_med',
            field=models.ManyToManyField(to='main_app.growingmedia'),
        ),
    ]
