# Generated by Django 2.2.12 on 2020-05-07 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200507_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='brand',
            name='search',
            field=models.BooleanField(default=True),
        ),
    ]