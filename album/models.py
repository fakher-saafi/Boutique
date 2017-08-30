# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from boutique1.models import Trader,Produit
from django.contrib.auth.models import Permission, User
from django.db import models
def user_directory_path_one(instance, filename):
    return 'user_{0}/{1}/{2}/{3}'.format(instance.owner.user.username, 'album',instance.title ,str(filename))
def user_directory_path_two(instance, filename):
    return 'user_{0}/{1}/{2}/{3}'.format('aa', 'album','zz' ,str(filename))
# Create your models here.
class album(models.Model):
    owner = models.ForeignKey(Trader, on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    image_album = models.ImageField(blank=True, null=True, upload_to=user_directory_path_one)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.title

class picture(models.Model):
    album=models.ForeignKey(album,on_delete=models.CASCADE,default=0)
    title = models.CharField(max_length=1000)
    image = models.ImageField(blank=True, null=True, upload_to=user_directory_path_two)
    description = models.CharField(max_length=1000,null=True,)
    created_at = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.title
