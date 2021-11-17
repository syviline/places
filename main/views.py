from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Place

# Create your views here.

@login_required
def index(request):
    vars = {'title': 'Обзор'}
    return render(request, 'main/discover.html', vars)


@login_required
def places(request):
    places = Place.objects.all()
    vars = {'title': 'Мои места', 'places': places}
    return render(request, 'main/places.html', vars)