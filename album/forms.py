from django import forms
from django.http import request
from boutique1.models import Produit
from .models import album,picture


class AlbumForm(forms.ModelForm):

    class Meta:
        model = album
        fields = ['title', 'image_album','description','is_active']

class PictureForm(forms.ModelForm):

    class Meta:
        model = picture
        fields = ['title','image','description']


