import datetime

from django.contrib.admin.helpers import checkbox
from django.contrib.auth.models import Permission, User
from django.db import models

def user_directory_path(instance, filename):
    return 'user_{0}/{1}/{2}/{3}/{4}'.format(instance.Boutique.owner.user.username,'Shops', instance.Boutique.nom_boutique,instance.nom_produit,str(filename))
def user_directory_path_four(instance, filename):
    return 'user_{0}/{1}/{2}/{3}'.format(instance.owner.user.username,'Shops', instance.name,str(filename))
def user_directory_path_two(instance, filename):
    return 'user_{0}/{1}/{2}/{3}/{4}'.format(instance.Produit.Boutique.owner.user.username,'Shops', instance.Produit.Boutique.nom_produit,instance.Produit.nom_produit,str(filename))
def user_directory_path_three(instance, filename):
    return 'user_{0}/{1}/{2}'.format(instance.user.username, 'Profile' ,str(filename))
def user_directory_path_five(instance, filename):
    return 'user_{0}/{1}/{2}'.format(instance.owner.user.username, 'Collection' ,str(filename))



class Trader(models.Model):
    PARTICULAR = 'PA'
    SOCIETY = 'SO'

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=2500, null=True)
    picture = models.ImageField(null=True, blank=True, upload_to=user_directory_path_three)
    fb_link = models.CharField(max_length=100)
    instagram_link = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    commercant_type = models.CharField(
        max_length=20,
        blank=True,
        choices=(
            (PARTICULAR, 'Particular'),
            (SOCIETY, 'Society')
        )
    )

    def __str__(self):
        return self.user.username + ' - ' + self.commercant_type

class Boutique(models.Model):
    owner = models.ForeignKey(Trader, on_delete=models.CASCADE,default=0)
    nom_boutique =  models.CharField(max_length=250)
    logo_boutique = models.FileField()

    def __str__(self):
        return self.nom_boutique

class Category(models.Model):
   label = models.CharField(max_length=100)

   def __str__(self):
       return self.label

class Produit(models.Model):
    HAND_MADE = 'HM'
    VINTAGE = 'VTG'
    Boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    owner=models.ForeignKey(Trader,on_delete=models.CASCADE,default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=0)
    nom_produit = models.CharField(max_length=250)
    image_produit = models.FileField()
    secondary_picture1 = models.ImageField(blank=True, null=True, upload_to=user_directory_path)
    secondary_picture2 = models.ImageField(blank=True, null=True, upload_to=user_directory_path)
    secondary_picture3 = models.ImageField(blank=True, null=True, upload_to=user_directory_path)
    prix_produit = models.FloatField()
    description = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=False)
    en_promotion = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    product_type = models.CharField(
        max_length=20,
        blank=True,
        choices=(
            (HAND_MADE, 'Hand Made'),
            (VINTAGE, 'Vintage')
        )
    )

    def __str__(self):
        return self.nom_produit + ' - '



class Collection(models.Model):
    owner = models.ForeignKey(Trader, on_delete=models.CASCADE,default=1)
    produit = models.ManyToManyField(Produit, default=1)
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    image_collection = models.ImageField(blank=True, null=True, upload_to=user_directory_path_five)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.title

class Promotion(models.Model):

    REGULAR = 'Regular'
    FLASH = 'Flash'

    PRODUCT ='PR'
    COLLECTION = 'CO'
    title= models.CharField(max_length=100,default="")
    owner = models.ForeignKey(Trader, on_delete=models.CASCADE, default=1)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE,default=None)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE,default=None,null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    status = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=datetime.datetime.now)
    end_time = models.DateTimeField(default=datetime.datetime.now)
    discount_value = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    tz = models.IntegerField(default=0)
    promotion_type = models.CharField(
        max_length=20,
        blank=True,
        choices=(
            (REGULAR, 'Regular'),
            (FLASH, 'Flash')
        )
    )

    promotion_for = models.CharField(
        max_length=20,
        blank=True,
        choices=(
            (PRODUCT, 'Product'),
            (COLLECTION, 'Collection')
        )
    )



    def __str__(self):
        return self.title