from accounts.views import profile
from . import views
from geo.views import geo
from django.urls import path

app_name = "main"
urlpatterns = [
    path('', views.index, name='index'),
    path('profile', profile, name='profile'),
    path('places', views.places, name='places'),
    path('add_place', views.add_place, name='add_place'),
    path('place/<int:id>', views.view_place, name='view_place'),
    path('get_places', views.get_places),
    path('geo', geo, name="geo"),

]
