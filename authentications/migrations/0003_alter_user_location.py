# Generated by Django 5.0.2 on 2024-02-29 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0002_initial'),
        ('marketrecord', '0002_remove_reportrecord_status_report_status_report_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketrecord.location'),
        ),
    ]
