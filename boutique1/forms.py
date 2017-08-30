from django import forms
from django.http import request

from .models import Boutique, Produit, Trader, Collection, Promotion
from django.contrib.auth.models import User

class BoutiqueForm(forms.ModelForm):

    class Meta:
        model = Boutique
        fields = ['nom_boutique', 'logo_boutique']


class ProduitForm(forms.ModelForm):

    class Meta:
        model = Produit
        fields = ['nom_produit', 'description', 'prix_produit', 'image_produit', 'category' ,'product_type','quantity','secondary_picture1','secondary_picture2','secondary_picture3','is_active']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password' ]

class TraderForm(forms.ModelForm):

    class Meta:
        model = Trader
        fields = ['picture', 'commercant_type', 'description', 'fb_link', 'instagram_link', 'location']

class CollectionForm(forms.ModelForm):
    produit = forms.ModelMultipleChoiceField(
        queryset=Produit.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        model = Collection
        fields =['title','image_collection','produit','description','is_active']

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['title','promotion_type', 'produit', 'discount_value', 'start_time', 'end_time']