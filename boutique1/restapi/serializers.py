from rest_framework.serializers import ModelSerializer

from boutique1.models import Produit

class ProductCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Produit

        fields = ['nom_produit', 'description', 'prix_produit', 'image_produit', 'category', 'product_type', 'quantity','secondary_picture1', 'secondary_picture2', 'secondary_picture3', 'is_active']


