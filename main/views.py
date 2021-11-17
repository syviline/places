from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .models import Place
from .forms import NewPlaceForm
from django.core.exceptions import ObjectDoesNotExist
import json

PLACES_PER_PAGE = 12

REPLACE_CHARS = '()!.,/;[]-=+_'

# Create your views here.

@login_required
def index(request):
    vars = {'title': 'Обзор'}
    return render(request, 'main/discover.html', vars)


@login_required
def places(request):
    places = Place.objects.filter(user=request.user)
    vars = {'title': 'Мои места', 'places': places}
    return render(request, 'main/places.html', vars)


@login_required
def get_places(request):
    if request.method == 'GET':
        search = request.GET.get('search', None)
        page = int(request.GET.get('page', 1))
        places = Place.objects
        if search:
            places = places.filter(search__icontains=search.strip().lower())
        else:
            places = places.all()
        places = places.order_by('-id')[(page-1)*PLACES_PER_PAGE:page*PLACES_PER_PAGE]
        placesarr = []
        for i in places:
            placesarr.append({'id': i.id, 'name': i.name, 'photo': i.photo.url, 'description': i.description[:15]})
        return HttpResponse(json.dumps(placesarr))
    else:
        return HttpResponseNotAllowed(['GET'])


@login_required
def add_place(request):
    form = NewPlaceForm()
    if request.method == 'POST':
        form = NewPlaceForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.photo = form.cleaned_data['photo']
            obj.user = request.user
            obj.hashtags = " ".join(obj.hashtags.replace('#', ' ').split())
            obj.search = form.cleaned_data['name'].lower() + ' ' + form.cleaned_data['description'].lower() + ' ' + obj.hashtags.lower()
            for i in REPLACE_CHARS:
                obj.search.replace(i, ' ')
            obj.save()
            return redirect('place/' + str(obj.id))
        else:
            vars = {'title': 'Добавить место', 'form': form}
            return render(request, 'main/add_place.html', vars)
    vars = {'title': 'Добавить место', 'form': form}
    return render(request, 'main/add_place.html', vars)


@login_required
def view_place(request, id):
    try:
        place = Place.objects.get(id=id)
        if not place.is_public and place.user != request.user:
            return redirect('main:index')
    except Place.DoesNotExist:
        return redirect('main:index')
    vars = {'title': place.name, 'place': place}
    return render(request, 'main/view_place.html', vars)


