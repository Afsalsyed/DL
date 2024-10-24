# Generated by Django 5.0.6 on 2024-07-15 11:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oss', '0004_article_type_article_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('grant_number', models.CharField(max_length=50)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funders', to='oss.submission')),
            ],
        ),
    ]
