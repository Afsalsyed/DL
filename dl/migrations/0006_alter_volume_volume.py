# Generated by Django 5.0.6 on 2024-07-25 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0005_remove_volume_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volume',
            name='volume',
            field=models.IntegerField(unique=True),
        ),
    ]