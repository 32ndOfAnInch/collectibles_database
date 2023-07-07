from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('collectibles_list/', views.CollectiblesListView.as_view(), name='collectibles_list'),
    path('friend_collectibles_list/<int:user_id>/', views.FriendCollectiblesListView.as_view(), name='friend_collectibles_list'),
    path('collectibles/update/<int:pk>/', views.UpdateItemView.as_view(), name='update_item'),
    path('collectibles/create/', views.CreateItemView.as_view(), name='create_new_item'),
    path('collectibles/delete/<int:pk>/', views.DeleteItemView.as_view(), name='delete_item'),
    path('get_values/', views.get_values, name='get_values'),
]