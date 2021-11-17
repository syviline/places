from django.shortcuts import render
from .forms import FooForm


# Create your views here.
def geo(request):
    vars = {'title': 'Карта место', 'form': FooForm}
    return render(request, 'main/geo.html', vars)
