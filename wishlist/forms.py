from django import forms
from django.http import request
from boutique1.models import Produit
from .models import wish_category,wish_list
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):

    class Meta:
        model = wish_category
        fields = ['title', 'image_category','description','is_active']

class WishlistForm(forms.ModelForm):
    produit = forms.ModelMultipleChoiceField(
        queryset=Produit.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        model = wish_list
        fields = ['wish_category','produit']


class WishlistForm1(forms.ModelForm):

    class Meta:
        model = wish_list
        fields = ['wish_category']
