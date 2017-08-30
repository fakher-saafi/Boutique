# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from boutique1.models import Trader,Produit
from django.contrib.auth.models import Permission, User
from django.db import models
def user_directory_path_five(instance, filename):
    return 'user_{0}/{1}/{2}/{3}'.format(instance.user.username, 'wish_category' ,instance.title,str(filename))
# Create your models here.
class wish_category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    image_category = models.ImageField(blank=True, null=True, upload_to=user_directory_path_five)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.title

class wish_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    wish_category=models.ForeignKey(wish_category,on_delete=models.CASCADE,default=0)
    produit=models.ForeignKey(Produit,on_delete=models.CASCADE,default=0)

    class Meta:
        unique_together = ('user', 'wish_category', 'produit')