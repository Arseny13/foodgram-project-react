# Generated by Django 3.2.18 on 2023-03-29 09:29

from django.db import migrations

import food.models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_auto_20230329_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=food.models.CollorUpperField(default='#FFFFFF', image_field=None, max_length=18, samples=None, unique=True),
        ),
    ]
