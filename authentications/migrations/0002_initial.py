# Generated by Django 5.0.2 on 2024-02-25 01:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentications', '0001_initial'),
        ('marketrecord', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='marketrecord.location'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentications.role'),
        ),
    ]
