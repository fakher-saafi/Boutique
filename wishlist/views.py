# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import wish_category,wish_list
from .forms import CategoryForm,WishlistForm
from boutique1.models import Produit
# Create your views here.

def create_wish_category(request):
    if not request.user.is_authenticated():
        return render(request, 'boutique1/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('/discoverProd/')
        context = {
            "form": form,
        }
        return render(request, 'create_wishcategory.html', context)


def my_categorys(request):
    if not request.user.is_authenticated():
        return render(request, 'boutique1/login.html')
    else:
        categorys=wish_category.objects.filter(user=request.user)
        # PAGINATION
        page = request.GET.get('page', 1)
        paginator = Paginator(categorys, 6)
        try:
            categorys = paginator.page(page)
        except PageNotAnInteger:
            categorys = paginator.page(1)
        except EmptyPage:
            categorys = paginator.page(paginator.num_pages)
        return render(request,'my_wishcategorys.html',{'categorys':categorys})

def delete_category(request, category_id):
    category = wish_category.objects.get(pk=category_id)
    category.delete()
    categorys=wish_category.objects.filter(user=request.user)
    return render(request, 'my_wishcategorys.html',{'categorys':categorys})

def edit_category(request, category_id):
    categoryi = get_object_or_404(wish_category, pk=category_id)
    form = CategoryForm(request.POST or None, request.FILES or None, instance=categoryi)
    if form.is_valid():
        category = form.save(commit=False)
        category.save()

        return redirect('/wish/my_categorys/')
    context = {
        'form': form,
        'category': categoryi
    }
    return render(request, 'boutique1/create_boutique.html', context)


def addprod(request,category_id,prod_id):
    ws=wish_category.objects.all()
    category=get_object_or_404(wish_category,pk=category_id)
    prod=get_object_or_404(Produit,pk=prod_id)
    if not request.user.is_authenticated():
        return render(request, 'boutique1/login.html')
    elif not ws:
        redirect('/wish/create_wishcategory/')
    else:
        try:
            wishlist=wish_list()
            wishlist.user = request.user
            wishlist.produit=prod
            wishlist.wish_category=category
            wishlist.save()
          #  return redirect('/discoverProd/')
        except Exception as e:
            msg=e
        return redirect('/wish/categoryProds/'+str(category_id))

def detailcategory(request, category_id):
    category = get_object_or_404(wish_category, pk=category_id)
    produit = wish_list.objects.filter(wish_category=category).values_list('produit_id')
    pro=Produit.objects.filter(pk__in=produit)

    # PAGINATION
    page = request.GET.get('page', 1)
    paginator = Paginator(pro, 6)
    try:
        pro = paginator.page(page)
    except PageNotAnInteger:
        pro = paginator.page(1)
    except EmptyPage:
        pro = paginator.page(paginator.num_pages)

    return render(request,  'discover_wishlist.html', {'category': category,'products': pro})

def delete_category_produit(request,category_id,produit_id):
    produit=wish_list.objects.filter(user=request.user)
    q = Q(wish_category_id=category_id) & Q(produit_id=produit_id)
    product = produit.filter(q)
    product.delete()
    return redirect('/wish/categoryProds/' + str(category_id))



def create_wish_list(request,category_id):
    ws=wish_category.objects.all()
    category=get_object_or_404(wish_category,pk=category_id)
    if not request.user.is_authenticated():
        return render(request, 'boutique1/login.html')
    elif not ws:
        redirect('/wish/create_wishcategory/')
    else:
        form = WishlistForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            wishlist = form.save(commit=False)
            wishlist.user = request.user
            wishlist.save()
          #  return redirect('/discoverProds/')
        context = {
            "form": form,
            "category":category,
        }

        return render(request,'add_to_wishlist.html',context)