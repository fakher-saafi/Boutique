# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from album.models import album
from .models import album,picture
from boutique1.models import Trader
from boutique1.forms import TraderForm
from .forms import AlbumForm,PictureForm
# Create your views here.
def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'boutique1/login.html')
    elif not hasattr(request.user, 'trader'):
        form = TraderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            trader = form.save(commit=False)
            trader.user = request.user
            trader.save()
            return render(request, 'create_album.html')
        context = {
            "form_name": "You have to signup as a Trader to continue",
            "form": form,
        }
        return render(request, 'boutique1/form_template2.html', context)
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        owner = get_object_or_404(Trader,user=request.user)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner =owner
            album.save()
            return redirect('/album/my_albums/')
        context = {
            "form": form,
        }
        return render(request, 'create_album.html', context)


def my_albums(request):
    if not request.user.is_authenticated():
        return render(request, 'boutique1/login.html')
    else:
        owner = get_object_or_404(Trader, user=request.user)
        albums=album.objects.filter(owner=owner)

        # PAGINATION
        page = request.GET.get('page', 1)
        paginator = Paginator(albums, 6)
        try:
            albums = paginator.page(page)
        except PageNotAnInteger:
            albums = paginator.page(1)
        except EmptyPage:
            albums = paginator.page(paginator.num_pages)
        return render(request,'my_albums.html',{'albums':albums})


def delete_album(request,album_id):
    owner = get_object_or_404(Trader, user=request.user)
    alb = album.objects.get(pk=album_id)
    alb.delete()
    albums = album.objects.filter(owner=owner)
    return render(request, 'my_albums.html', {'albums': albums})


def edit_album(request,album_id):
    albumi = get_object_or_404(album, pk=album_id)
    form = AlbumForm(request.POST or None, request.FILES or None, instance=albumi)
    if form.is_valid():
        alb = form.save(commit=False)
        alb.save()

        return redirect('/album/my_albums/')
    context = {
        'form': form,
        'album': album,
    }
    return render(request, 'create_album.html', context)


def albumdetails(request,album_id):
    alb = get_object_or_404(album, pk=album_id)
   # pics = picture.objects.filter(album_id=album_id).values_list('produit_id')
    pics = picture.objects.filter(album_id=album_id)

    # PAGINATION
    page = request.GET.get('page', 1)
    paginator = Paginator(pics, 6)
    try:
        pics = paginator.page(page)
    except PageNotAnInteger:
        pics = paginator.page(1)
    except EmptyPage:
        pics = paginator.page(paginator.num_pages)

    return render(request, 'discover_album.html', {'album': alb, 'pictures': pics})

#----------------------picture-------------------

def album_add_picture(request,album_id):
    alb=get_object_or_404(album, pk=album_id)
    form = PictureForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        pic = form.save(commit=False)
        pic.album=alb
        pic.save()
        return redirect('/album/albumdetails/'+str(album_id))
    context = {
        "form": form,
    }
    return render(request, 'create_picture.html', context)

def delete_picture(request,picture_id):
    pic = picture.objects.get(pk=picture_id)
    album_id=pic.album.id
    pic.delete()
    pics = picture.objects.filter(album_id=album_id)
    return redirect('/album/albumdetails/'+str(album_id), {'pictures': pics})


def edit_picture(request,picture_id):
    pici = get_object_or_404(picture, pk=picture_id)
    album_id = pici.album.id
    form = AlbumForm(request.POST or None, request.FILES or None, instance=pici)
    if form.is_valid():
        pic = form.save(commit=False)
        pic.save()

        return redirect('/album/albumdetails/' + str(album_id))
    context = {
        'form': form,
        'picture': pici,
    }
    return render(request, 'create_picture.html', context)