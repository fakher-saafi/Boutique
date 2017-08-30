# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from requests.api import request

from boutique1.models import Produit
from django.shortcuts import render
from .serializers import ProductCreateUpdateSerializer
# Create your views here.
from rest_framework.generics import (

    CreateAPIView,

    DestroyAPIView,

    ListAPIView,

    RetrieveAPIView,

    UpdateAPIView,

    RetrieveUpdateAPIView,

)


class ProductListAPIView(ListAPIView):
    queryset = Produit.objects.all()

    serializer_class = ProductCreateUpdateSerializer


class ProductRetriveAPIView(RetrieveAPIView):
    queryset = Produit.objects.all()

    serializer_class = ProductCreateUpdateSerializer
    lookup_field ='id'

class DestroyAPIView(DestroyAPIView):
    queryset = Produit.objects.all()

    serializer_class = ProductCreateUpdateSerializer
    lookup_field ='id'

class UpdateAPIView(UpdateAPIView):
    queryset = Produit.objects.all()

    serializer_class = ProductCreateUpdateSerializer
    lookup_field ='id'

class ProductCreateAPIView(CreateAPIView):
    queryset = Produit.objects.all()

    serializer_class = ProductCreateUpdateSerializer

    def perform_create(self, serializer):
        user = self.request.user

        buser = user.buser

        shop = Shop.objects.filter(owner=buser.id)

