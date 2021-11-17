from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Place
from .forms import NewPlaceForm
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

@login_required
def index(request):
    _vars = {'title': 'Обзор'}
    return render(request, 'main/discover.html', _vars)


@login_required
def places(request):
    _places = Place.objects.all()
    print(_places)
    _vars = {'title': 'Мои места', 'places': _places}
    return render(request, 'main/places.html', _vars)


@login_required
def add_place(request):
    form = NewPlaceForm()
    if request.method == 'POST':
        form = NewPlaceForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.photo = form.cleaned_data['photo']
            obj.user = request.user
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
    except Place.DoesNotExist:
        return redirect('main:index')
    vars = {'title': 'Добавить место', 'place': place}
    return render(request, 'main/view_place.html', vars)