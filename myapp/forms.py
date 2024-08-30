from django import forms
from .models import Peliculas

class CreateNewPelicula(forms.ModelForm):
    class Meta:
        model = Peliculas
        fields = ['name', 'description', 'image', 'genere']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'input'}),
            'image': forms.FileInput(attrs={'class': 'input'}),
            'genere':forms.TextInput(attrs={'class': 'input'}),
        }

