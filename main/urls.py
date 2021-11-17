from accounts.views import profile
from . import views
from django.urls import path

app_name = "main"
urlpatterns = [
    path('', views.index, name='index'),
    path('profile', profile, name='profile'),
    path('places', views.places, name='places'),
    path('add_place', views.add_place, name='add_place')
]
