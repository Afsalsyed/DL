# Generated by Django 5.0.6 on 2024-07-26 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0006_alter_volume_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volume',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='volume',
            name='volume',
            field=models.IntegerField(),
        ),
    ]