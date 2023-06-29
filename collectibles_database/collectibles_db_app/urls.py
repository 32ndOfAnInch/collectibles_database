from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('collectibles_list/', views.CollectiblesListView.as_view(), name='collectibles_list'),
]