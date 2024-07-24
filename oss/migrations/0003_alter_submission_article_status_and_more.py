# Generated by Django 5.0.6 on 2024-07-12 16:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oss', '0002_alter_submission_abstract_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='article_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='oss.article_status'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='article_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='oss.article_type'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='submission',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='oss.category'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='coi_describe',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='journal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='oss.journal'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submitted_on',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
