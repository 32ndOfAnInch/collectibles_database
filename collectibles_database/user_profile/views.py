from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from . forms import ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .import models
from django.db.models import Q
from django.db.models.query import QuerySet
from typing import Any


User = get_user_model()


@login_required
def profile(request, user_id=None):
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(get_user_model(), id=user_id)
    return render(request, 'user_profile/profile.html', {'user_': user})


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
    return render(request, 'user_profile/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})


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

            # # create a new Profile object for the user
            # profile = models.Profile.objects.create(user=user)
            
            # # save the profile picture if provided
            # profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            # if profile_form.is_valid():
            #     profile_form.save()

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
        return qs


@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    collectible_item = models.CollectibleItem.objects.first()
    if request.method == 'POST':
        friend_request = models.FriendRequest(sender=request.user, receiver=receiver, collectible_item=collectible_item, status=1)
        friend_request.save()
        return redirect('collectibles_list')  # Redirect to a success page or appropriate URL
    return render(request, 'user_profile/send_friend_request.html', {'receiver': receiver})

@login_required
def manage_friend_requests(request):
    if request.method == 'POST':
        friend_request_id = request.POST.get('friend_request_id')
        action = request.POST.get('action')
        friend_request = get_object_or_404(models.FriendRequest, id=friend_request_id, receiver=request.user)
        if action == 'accept':
            friend_request.status = 2  # Update the status to "Accepted"
        elif action == 'reject':
            friend_request.status = 3  # Update the status to "Rejected"
        friend_request.save()
        return redirect('manage_friend_requests')
    friend_requests = models.FriendRequest.objects.filter(receiver=request.user)
    return render(request, 'user_profile/manage_friend_requests.html', {'friend_requests': friend_requests})


@login_required
def friends_list(request):
    user = request.user
    friends = user.profile.friends.all()
    return render(request, 'user_profile/friends_list.html', {'friends': friends})
