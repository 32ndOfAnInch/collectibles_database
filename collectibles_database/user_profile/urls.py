from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/search/', views.ProfileSearchView.as_view(), name='profile_search'),
    path('profile/send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('friends/list/', views.friends_list, name='friends_list'),
    path('notifications/', views.notifications, name='notifications'),
    path('preferences/', views.preferences, name='preferences'),
    path('profile/unfollow_friend/<int:user_id>/', views.unfollow_friend, name='unfollow_friend'),
    path('profile/delete/', views.ProfileDeleteView.as_view(), name='profile_delete'),
    path('delete_confirmation/', views.profile_delete_confirmation, name='profile_delete_confirmation'), # for now it messages that profile succesfully deleted, later it will messages user to confirm delete on email
]
