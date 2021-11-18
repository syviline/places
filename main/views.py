from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from .models import Place, Serie
from .forms import NewPlaceForm, NewSerieForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import json

PLACES_PER_PAGE = 8

REPLACE_CHARS = '()!.,/;[]-=+_'

# Create your views here.

@login_required
def index(request):
    popularplaces = Place.objects.filter(is_public=True).order_by('-views')[:PLACES_PER_PAGE]
    newplaces = Place.objects.filter(is_public=True).order_by('-id')[:PLACES_PER_PAGE]
    vars = {'title': 'Обзор', 'popular': popularplaces, 'new': newplaces}
    return render(request, 'main/discover.html', vars)


@login_required
def places(request):
    places = Place.objects.all()
    vars = {'title': 'Мои места', 'places': places}
    return render(request, 'main/places.html', vars)


@login_required
def get_places(request):
    if request.method == 'GET':
        search = request.GET.get('search', None)
        page = int(request.GET.get('page', 1))
        is_global = request.GET.get('global', False)
        if is_global:
            places = Place.objects.filter(is_public=True)
        else:
            places = Place.objects.filter(user=request.user)
        elementsAmount = 0
        if search:
            places = places.filter(search__icontains=search.strip().lower())
        elementsAmount = len(places)
        if is_global:
            places = places.order_by('-views')[(page-1)*PLACES_PER_PAGE:page*PLACES_PER_PAGE]
        else:
            places = places.order_by('-id')[(page-1)*PLACES_PER_PAGE:page*PLACES_PER_PAGE]
        placesarr = []
        for i in places:
            placesarr.append({'id': i.id, 'name': i.name[:15] + ('...' if len(i.name) > 15 else ''), 'photo': i.photo.url, 'description': i.description[:35] + '...'})
        return HttpResponse(json.dumps({'pagesAmount': elementsAmount // PLACES_PER_PAGE + 1, 'places': placesarr}))
    else:
        return HttpResponseNotAllowed(['GET'])


@login_required
def get_series(request):
    if request.method == 'GET':
        search = request.GET.get('search', None)
        page = int(request.GET.get('page', 1))
        is_global = request.GET.get('global', False)
        if is_global:
            series = Serie.objects.filter(is_public=True)
        else:
            series = Serie.objects.filter(user=request.user)
        elementsAmount = 0
        if search:
            series = series.filter(search__icontains=search.strip().lower())
        elementsAmount = len(series)
        if is_global:
            series = series.order_by('-views')[(page - 1) * PLACES_PER_PAGE:page * PLACES_PER_PAGE]
        else:
            series = series.order_by('-id')[(page-1)*PLACES_PER_PAGE:page*PLACES_PER_PAGE]
        seriesarr = []
        for i in series:
            seriesarr.append({'id': i.id, 'name': i.name, 'description': i.description, 'photo': i.photo.url})
        return HttpResponse(json.dumps({'pageAmount': elementsAmount // PLACES_PER_PAGE + 1, 'series': seriesarr}))
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
            obj.hashtags = " ".join(obj.hashtags.lower().replace('#', ' ').split())
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
    if place.user != request.user:
        place.views += 1
        place.save()
    a = request.GET.get('series', None)
    if a:
        serie = Serie.objects.get(id=a)  # AIzaSyApS9XpQZIbN-U9_2r3cTsXfREPDKP5kPc
        if place not in serie.places.all():
            serie.places.add(place)
            return redirect('/place/' + str(place.id) + '?msg=Место успешно добавлено!')
        else:
            return redirect('/place/' + str(place.id) + '?msg=Это место уже есть в серии!')
    msg = request.GET.get('msg', None)
    hashtags = place.hashtags.split()
    series = Serie.objects.filter(user=request.user)
    place.latitude = str(place.latitude).replace(',', '.')
    place.longitude = str(place.longitude).replace(',', '.')
    vars = {'title': place.name, 'place': place, 'series': series, 'msg': msg, 'hashtags': hashtags}
    return render(request, 'main/view_place.html', vars)


@login_required
def add_serie(request):
    form = NewSerieForm()
    if request.method == 'POST':
        form = NewSerieForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.photo = form.cleaned_data['photo']
            obj.user = request.user
            obj.search = form.cleaned_data['name'].lower() + ' ' + form.cleaned_data['description'].lower()
            for i in REPLACE_CHARS:
                obj.search.replace(i, ' ')
            obj.save()
            return redirect('serie/' + str(obj.id))
        else:
            vars = {'title': 'Добавить серию', 'form': form}
            return render(request, 'main/add_serie.html', vars)
    vars = {'title': 'Добавить серию', 'form': form}
    return render(request, 'main/add_serie.html', vars)


@login_required
def view_serie(request, id):
    serie = Serie.objects.get(id=id)
    if serie.user != request.user and not serie.is_public:
        return redirect('main:index')
    if serie.user != request.user:
        serie.views += 1
        serie.save()
    places = []
    for i in serie.places.all():
        places.append({'id': i.id, 'name': i.name, 'description': i.description, 'photo': i.photo.url, 'latitude': float(i.latitude), 'longitude': float(i.longitude)})
    vars = {'title': serie.name, 'serie': serie, 'places': json.dumps(places)}
    return render(request, 'main/view_serie.html', vars)


@login_required
def remove_from_serie(request, serieid, placeid):
    serie = Serie.objects.get(id=serieid)
    if serie.user != request.user:
        return HttpResponseForbidden()
    place = Place.objects.get(id=placeid)
    serie.places.remove(place)
    return HttpResponse('ok')


@login_required
def edit_place(request, placeid):
    place = Place.objects.get(id=placeid)
    if place.user != request.user:
        return redirect('main:index')
    form = NewPlaceForm(instance=place)
    if request.method == 'POST':
        form = NewPlaceForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            oldphoto = place.photo
            newplace = form.save(commit=False)
            if form.cleaned_data['photo'] != 'user_images/default.jpg':
                newplace.photo = oldphoto
            newplace.save()
            return redirect('/place/' + str(place.id))
        else:
            vars = {'title': place.name, 'form': form, 'place': place}
            return render(request, 'main/edit_place.html', vars)
    vars = {'title': place.name, 'form': form, 'place': place}
    return render(request, 'main/edit_place.html', vars)


@login_required
def delete_place(request, placeid):
    place = Place.objects.get(id=placeid)
    if place.user == request.user:
        place.delete()
    return redirect('places')


@login_required
def global_search(request):
    vars = {'title': 'Глобальный поиск', 'search': request.GET.get('search', None)}
    return render(request, 'main/global_search.html', vars)

@login_required
def profile(request):
    success = request.GET.get('success', None)
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/profile?success=1')
        else:
            vars = {'title': 'Профиль', 'success': success, 'form': form}
            return render(request, 'accounts/profile.html', vars)
    vars = {'title': 'Профиль', 'success': success, 'form': form}
    return render(request, 'accounts/profile.html', vars)