# Generated by Django 4.2.17 on 2024-12-11 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_hotel'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='latitude',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='longitude',
            field=models.CharField(max_length=32, null=True),
        ),
    ]