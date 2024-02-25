from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    Role = apps.get_model('authentications', 'Role')
    for role in Role.ROLE_CHOICES:
        Role.objects.get_or_create(name=role[0])