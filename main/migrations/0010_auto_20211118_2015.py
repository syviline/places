# Generated by Django 3.2.9 on 2021-11-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20211118_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='latitude',
            field=models.DecimalField(decimal_places=40, max_digits=45),
        ),
        migrations.AlterField(
            model_name='place',
            name='longitude',
            field=models.DecimalField(decimal_places=40, max_digits=45),
        ),
    ]
