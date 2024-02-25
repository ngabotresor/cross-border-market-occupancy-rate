# signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

LOCATIONS = ['Rubavu', 'Rusizi', 'Karongi', 'Nyamasheke', 'Burera', 'Akanyaru', 'Nyabihu'] 

@receiver(post_migrate)
def create_locations(sender, **kwargs):
    Location = apps.get_model('marketrecord', 'Location')
    for location_name in LOCATIONS:
        Location.objects.get_or_create(name=location_name)