from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/search/', views.ProfileSearchView.as_view(), name='profile_search'),
    path('profile/send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('profile/manage_friend_requests/', views.manage_friend_requests, name='manage_friend_requests'),
    path('friends/list/', views.friends_list, name='friends_list'),
]
