# Generated by Django 5.2 on 2025-05-01 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_modelmetric_flmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flmodel',
            old_name='cross_validation',
            new_name='generalisability',
        ),
        migrations.RemoveField(
            model_name='flmodel',
            name='precision',
        ),
        migrations.AlterField(
            model_name='flmodel',
            name='security',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
