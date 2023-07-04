from django import template
from user_profile.models import Profile  # Import the necessary model(s)

register = template.Library()

@register.filter
def is_friend(user, friend_id):
    profile = Profile.objects.get(user=user)  # Replace 'Profile' with your actual profile model
    return profile.friends.filter(id=friend_id).exists()
