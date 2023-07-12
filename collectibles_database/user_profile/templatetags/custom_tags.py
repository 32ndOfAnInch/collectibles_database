from django import template
from user_profile.models import Profile, FriendRequest

register = template.Library()

@register.filter
def is_friend(user, friend_id):
    profile = Profile.objects.get(user=user) 
    return profile.friends.filter(id=friend_id).exists()
