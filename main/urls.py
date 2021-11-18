
from . import views
from django.urls import path

app_name = "main"
urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('places', views.places, name='places'),
    path('add_place', views.add_place, name='add_place'),
    path('add_serie', views.add_serie, name='add_serie'),
    path('place/<int:id>', views.view_place, name='view_place'),
    path('serie/<int:id>', views.view_serie, name='view_serie'),
    path('get_places', views.get_places),
    path('get_series', views.get_series),
    path('remove_from_serie/<int:serieid>/<int:placeid>', views.remove_from_serie),
    path('edit_place/<int:placeid>', views.edit_place, name='edit_place'),
    path('delete_place/<int:placeid>', views.delete_place),
    path('search', views.global_search, name='search'),
]
