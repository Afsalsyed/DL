# Generated by Django 5.0.6 on 2024-07-24 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oss', '0010_alter_funder_grant_number_alter_funder_name_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Keywords',
            new_name='Keyword',
        ),
    ]
