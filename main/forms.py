from django import forms
from django.forms import FileInput, DateInput
from .models import Place, Serie


class NewPlaceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['latitude'].widget.attrs.update(
            {'min': -90, 'max': 90}
        )
        self.fields['longitude'].widget.attrs.update(
            {'min': -180, 'max': 180}
        )

    class Meta:
        model = Place
        fields = ('name', 'latitude', 'longitude', 'address', 'description', 'photo', 'hashtags', 'is_public')

        widgets = {
            'hashtags': forms.TextInput()
        }


class NewSerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = ('name', 'description', 'photo', 'is_public')

# Create a custom date input field, otherwise would get a plain text field
class DateInput(forms.DateInput):
    input_type = 'date'  # Override the default input type which is text.


class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = {'date_visited': DateInput()}