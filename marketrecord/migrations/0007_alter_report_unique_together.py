# Generated by Django 5.0.2 on 2024-03-12 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketrecord', '0006_alter_report_season_alter_report_year'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='report',
            unique_together=set(),
        ),
    ]
