from django import forms
from .models import Foo
from .widgets import LocationWidget


class FooForm(forms.ModelForm):
    latlng = forms.CharField(widget=LocationWidget())  # http://djangosnippets.org/snippets/2106/

    class Meta:
        model = Foo
        fields = '__all__'