# Generated by Django 3.2.9 on 2021-11-17 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20211117_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]
