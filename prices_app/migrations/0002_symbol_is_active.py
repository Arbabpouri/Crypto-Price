# Generated by Django 4.2.3 on 2023-08-06 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='symbol',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
