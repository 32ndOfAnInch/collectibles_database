from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DeleteView, ListView

from . import models
from .forms import ProfileUpdateForm, UserPreferencesForm, UserUpdateForm

User = get_user_model()


@login_required
def profile(request, user_id=None):
    if user_id == None:
        user_ = request.user
        return render(request, 'user_profile/profile.html', {'user_': user_})
    else:
        user_ = get_object_or_404(User, id=user_id)
        is_friend_request_sent = models.FriendRequest.objects.filter(
            sender=request.user, receiver=user_, status__in=[1, 2]).exists()
        return render(
            request, 'user_profile/profile.html', {'user_': user_, 'is_friend_request_sent': is_friend_request_sent}
            )


@login_required
@csrf_protect
def profile_update(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(
        request, 'user_profile/profile_update.html', {'user_form': user_form, 'profile_form': profile_form}
        )


@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        messages.info(request, 'In order to sign up, you need to logout first')
        return redirect('index')
    if request.method == "POST":
        error = False
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if not username or len(username) < 3 or User.objects.filter(username=username).exists():
            error = True
            messages.error(request, 'Username is too short or already exists.')
        if not email or len(email) < 3 or User.objects.filter(email=email).exists():
            error = True
            messages.error(request, 'Email is invalid or user with this email already exists.')
        if not password or not password_confirm or password != password_confirm or len(password) < 8:
            error = True
            messages.error(request, "Password must be at least 8 characters long and match.")
        if not error:
            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)
            user.save()

            messages.success(request, "User registration successful!")
            return redirect('login')
    return render(request, 'user_profile/signup.html')


class ProfileSearchView(LoginRequiredMixin, ListView):
    model = models.Profile
    template_name = 'user_profile/profile_search.html'
    context_object_name = 'profile_search'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(
                Q(user__username__icontains=query)
            )
        else:
            qs = qs.none()
        return qs

# It deletes user with profile. When I tried to delete profile first, user was left
class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    # model = models.Profile
    model = User
    template_name = 'user_profile/profile_delete.html'
    context_object_name = 'profile_delete'
    success_url = reverse_lazy('profile_delete_confirmation')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        try:
            # deletes the profile
            user.delete()
            
            # log off
            logout(request)

            # redirects to the confirmation page, for now it shows success message, but in future I will try to make email confirmation method to prevent accidental user deletion
            return redirect(self.success_url)

        except Exception as e:
            # Handle the exception, e.g., display an error message
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('profile_delete_failure')


def profile_delete_confirmation(request):
    return render(request, 'registration/profile_delete_confirmation.html')

@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    # Prevent sending friend request to oneself
    if receiver == request.user:
        return redirect('profile', user_id=receiver.id)
    
    # Prevent sending friend request to existing friends
    if request.user.profile.friends.filter(id=user_id).exists():
        return redirect('profile', user_id=receiver.id)

    collectible_item = models.CollectibleItem.objects.first()
    if request.method == 'POST':
        friend_request = models.FriendRequest(
            sender=request.user, receiver=receiver, collectible_item=collectible_item, status=1
            )
        friend_request.save()
        messages.success(request, "A friend request was sent to the user. Once they accept, you will able to see each other collectibles")
        return redirect('profile', user_id=receiver.id)  # Redirect to a success page or appropriate URL
    return render(request, 'user_profile/send_friend_request.html', {'receiver': receiver})


@login_required
def friends_list(request):
    user = request.user
    friends = user.profile.friends.all()
    return render(request, 'user_profile/friends_list.html', {'friends': friends})


@login_required
def notifications(request, user_id=None):
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(get_user_model(), id=user_id)

    friend_requests = user.received_request.filter(status=1)  # Filter only pending friend requests

    if request.method == 'POST':
        friend_request_id = request.POST.get('friend_request_id')
        action = request.POST.get('action')
        friend_request = get_object_or_404(models.FriendRequest, id=friend_request_id, receiver=request.user)

        if action == 'accept':
            friend_request.status = 2  # Update the status to "Accepted"
            messages.success(request, "You have accepted friend request")
        elif action == 'reject':
            friend_request.status = 3  # Update the status to "Rejected"

        friend_request.save()
        return redirect('notifications')

    return render(
        request, 'user_profile/notifications.html', {'user_': user, 'friend_requests': friend_requests}
        )

@login_required
def preferences(request):

    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=request.user.profile)


        if form.is_valid():
            form.save()
            messages.success(request, _('Settings saved!'))
            return redirect('preferences')
        
        # light/dark theme handling
        if 'color_theme' in request.POST:
            theme = request.POST['color_theme']
            if theme in dict(models.Profile.COLOR_THEME_CHOICES):
                request.user.profile.color_theme = theme
                request.user.profile.save()
                return redirect('preferences')

    else:
        form = UserPreferencesForm(instance=request.user.profile)

    return render(request, 'user_profile/preferences.html',
                  {'form': form, 'user_profile': request.user.profile, 'color_theme': request.user.profile.color_theme})


@login_required
@transaction.atomic
def unfollow_friend(request, user_id):
    user_to_unfollow = models.Profile.objects.get(user_id=user_id)
    current_user_profile = request.user.profile

    if request.method == 'POST':
        # Remove the friendship from both sides
        current_user_profile.friends.remove(user_to_unfollow)
        user_to_unfollow.friends.remove(current_user_profile)
        # Delete related FriendRequest instances
        models.FriendRequest.objects.filter(
            sender=current_user_profile.user, receiver=user_to_unfollow.user
            ).delete()
        models.FriendRequest.objects.filter(
            sender=user_to_unfollow.user, receiver=current_user_profile.user
            ).delete()

        messages.success(request, "You unfollowed the user.")
        return redirect('profile', user_id=user_id)

    context = {
        'receiver': user_to_unfollow.user
    }
    return render(request, 'user_profile/unfollow_friend.html', context)