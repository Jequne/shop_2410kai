from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from accounts.models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        customer_group, _ = Group.objects.get_or_create(name='Customer')
        instance.groups.add(customer_group)


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Customer')
    Group.objects.get_or_create(name='Manager')
