# Generated by Django 3.2.9 on 2021-11-18 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20211118_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='serie',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]
