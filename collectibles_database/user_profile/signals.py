from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Profile
from . models import FriendRequest


User = get_user_model()


@receiver(post_save, sender=User)
def sync_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


@receiver(post_save, sender=FriendRequest)
def update_friends(sender, instance, **kwargs):
    if instance.status == 2:  # Friend request is accepted
        instance.sender.profile.friends.add(instance.receiver.profile)
        instance.receiver.profile.friends.add(instance.sender.profile)
