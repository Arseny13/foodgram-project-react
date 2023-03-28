# Generated by Django 3.2.18 on 2023-03-27 18:26

import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.CheckConstraint(check=models.Q(('subscriber', django.db.models.expressions.F('user')), _negated=True), name='Нельзя на себя'),
        ),
    ]
