# Generated by Django 5.0.2 on 2024-03-24 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketrecord', '0012_component'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='report',
            unique_together={('market', 'season', 'year')},
        ),
    ]
