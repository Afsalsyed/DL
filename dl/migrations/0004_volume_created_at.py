# Generated by Django 5.0.6 on 2024-07-24 17:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0003_alter_volume_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='volume',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
