# Generated by Django 5.0.6 on 2024-07-25 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oss', '0011_rename_keywords_keyword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='is_funded',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]