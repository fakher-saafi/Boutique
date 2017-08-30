from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
from .models import Promotion,Produit
from django.shortcuts import render, get_object_or_404


from celery import shared_task

@task(name="sum_two_numbers")
def add(x,y):
 return x+y

@task(name="multiply_two_numbers")
def mul(x, y):
 total = x * (y * random.randint(3, 100))
 return total

@task(name="sum_list_numbers")
def xsum(numbers):
 return sum(numbers)

@task(name="activate")
def activate(promotion_id,produit_id):
 promotion=get_object_or_404(Promotion,pk=promotion_id)
 produit = get_object_or_404(Produit, pk=produit_id)
 produit.en_promotion=True
 produit.save()
 promotion.is_active=True
 promotion.save()
 if promotion.is_active:
  return 1
 else:
  return 0

@task(name="desactivate")
def desactivate(promotion_id,produit_id):
 promotion=get_object_or_404(Promotion,pk=promotion_id)
 produit = get_object_or_404(Produit, pk=produit_id)
 produit.en_promotion=False
 produit.save()
 promotion.is_active=False
 promotion.save()
 if promotion.is_active:
  return 1
 else:
  return 0
