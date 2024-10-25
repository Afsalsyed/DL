# Generated by Django 5.0.6 on 2024-07-26 11:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dl', '0007_alter_volume_description_alter_volume_volume'),
        ('oss', '0014_accepted_submission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Published_article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_on_date', models.DateField()),
                ('doi', models.CharField(max_length=255)),
                ('accepted_submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oss.accepted_submission')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dl.issue')),
            ],
        ),
    ]
