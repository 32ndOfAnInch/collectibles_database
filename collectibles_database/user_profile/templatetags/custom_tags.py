from django import template
from user_profile.models import Profile, FriendRequest
from django.templatetags.static import static

register = template.Library()

@register.filter
def is_friend(user, friend_id):
    profile = Profile.objects.get(user=user) 
    return profile.friends.filter(id=friend_id).exists()


@register.filter
def has_pending_friend_requests(user):
    return FriendRequest.objects.filter(receiver=user, status=1).exists()


@register.simple_tag
def get_profile_picture(user):
    if user.profile and user.profile.picture:
        return user.profile.picture.url
    else:
        return static('collectibles/img/generic_user_logo.jpg')