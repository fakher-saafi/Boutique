from audioop import reverse

import re
from celery import task
import datetime
from datetime import timedelta
from .tasks import activate,desactivate
from celery import Celery
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.http import request
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import BoutiqueForm, ProduitForm, UserForm, TraderForm, CollectionForm,PromotionForm
from .models import Boutique, Produit, Category, Trader, Collection,Promotion
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.generic import UpdateView
import sys
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user.is_active = False
        user.set_password(password)
        user.save()
        current_site = get_current_site(request)
        message = render_to_string('boutique1/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Activate your account.'
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = UserForm()

    return render(request, 'boutique1/login.html', {'form': form})

def activate1(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
      #  redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')

    else:
        return HttpResponse('Activation link is invalid!')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                shops = Boutique.objects.all()
                products = Produit.objects.all()
                categories = Category.objects.all()
                return render(request, 'boutique1/index.html',
                              {'shops': shops, 'products': products, 'categories': categories})
            else:
                return render(request, 'boutique1/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'boutique1/login.html', {'error_message': 'Invalid login'})
    return render(request, 'boutique1/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'boutique1/index.html', context)


def create_boutique(request):
    if not request.user.is_authenticated():
        return render(request, 'boutique1/login.html')
    elif not hasattr(request.user, 'trader'):
        form = TraderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            trader = form.save(commit=False)
            trader.user = request.user
            trader.save()
            return render(request, 'boutique1/create_boutique.html')
        context = {
            "form_name": "You have to signup as a Trader to continue",
            "form": form,
        }
        return render(request, 'boutique1/form_template2.html', context)
    else:
        form = BoutiqueForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user.trader
            shop.create_date = datetime.datetime.now()
            shop.logo = request.FILES['logo_boutique']
            file_type = shop.logo_boutique.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'shop': shop,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'boutique1/boutique.html', context)
            shop.save()
            shops=Boutique.objects.all()
            return redirect('/myshop/')
        context = {
            "form": form,
        }

        return render(request, 'boutique1/create_boutique.html', context)

@login_required
def create_produit(request, boutique_id):
    form = ProduitForm(request.POST or None, request.FILES or None)
    boutique = get_object_or_404(Boutique, pk=boutique_id)
    if form.is_valid():
        boutiques_produits = boutique.produit_set.all()
        for s in boutiques_produits:
            if s.nom_produit == form.cleaned_data.get("nom_produit"):
                context = {
                    'boutique': boutique,
                    'form': form,
                    'error_message': 'You already added that product',
                }
                return render(request, 'boutique1/create_produit.html', context)
        produit = form.save(commit=False)
        produit.Boutique = boutique
        produit.owner=Trader.objects.get(user=request.user)
        produit.image_produit = request.FILES['image_produit']
        file_type = produit.image_produit.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'produit': produit,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'boutique1/create_produit.html', context)

        produit.save()
        return render(request, 'boutique1/detail.html', {'boutique': boutique})
    context = {
        'boutique': boutique,
        'form': form,
    }
    return render(request, 'boutique1/create_produit.html', context)

@login_required
def delete_boutique(request, boutique_id):
    boutique = Boutique.objects.get(pk=boutique_id)
    boutique.delete()
    boutiques = Boutique.objects.all()
    return render(request, 'boutique1/index.html', {'boutiques': boutiques})
@login_required
def edit_boutique(request, boutique_id):
    boutiquei = get_object_or_404(Boutique, pk=boutique_id)
    form = BoutiqueForm(request.POST or None, request.FILES or None, instance=boutiquei)
    if form.is_valid():
        boutique = form.save(commit=False)
        boutique.save()

        return redirect('/myshop/')
    context = {
        'form': form,
        'boutique': boutiquei
    }
    return render(request, 'boutique1/create_boutique.html', context)


@login_required
def edit_collection(request, collection_id):
    owner = Trader.objects.filter(user=request.user)
    produits = Produit.objects.filter(owner=owner)
    collectioni = get_object_or_404(Collection, pk=collection_id)
    form = CollectionForm(request.POST or None, request.FILES or None, instance=collectioni)
    form.fields['produit'].queryset = produits
    if form.is_valid():
        collection = form.save(commit=False)
        collection.save()
        form.save_m2m()
        return redirect('/mycollections/')
    context = {
        'form': form,
        'collection': collectioni
    }
    return render(request, 'boutique1/create_collection.html', context)

@login_required
def delete_produit(request, boutique_id, produit_id):
    boutique = get_object_or_404(Boutique, pk=boutique_id)
    produit = Produit.objects.get(pk=produit_id)
    produit.delete()
    return render(request, 'boutique1/detail.html', {'boutique': boutique})

@login_required
def delete_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    collection.delete()
    return redirect('/mycollections/')

@login_required
def detail(request, boutique_id):
    boutique = get_object_or_404(Boutique, pk=boutique_id)
    return render(request, 'boutique1/detail.html', {'boutique': boutique})

def home(request):
    boutiques = Boutique.objects.all()
    produit_results = Produit.objects.all()
    query = request.GET.get("site_search")
    if query:
        boutiques = boutiques.filter(
            Q(nom_boutique__icontains=query)
        ).distinct()
        produit_results = produit_results.filter(
            Q(nom_produit__icontains=query)
        ).distinct()
        return render(request, 'boutique1/boutique.html', {
            'boutiques': boutiques,
            'produits': produit_results,
        })
    else:
        return render(request, 'boutique1/index.html', {'boutiques': boutiques, 'produit_list':  produit_results})

def boutiques(request):
    boutiques = Boutique.objects.all()
    if hasattr(request.user, 'trader') and request.user.is_authenticated():
        myboutiques=Boutique.objects.filter(owner__user=request.user)
        produit_results = Produit.objects.all()
        query = request.GET.get("q")
        if query:
            boutiques = boutiques.filter(
                Q(nom_boutique__icontains=query)
            ).distinct()
            produit_results = produit_results.filter(
                Q(nom_produit__icontains=query)
            ).distinct()
            return render(request, 'boutique1/boutique.html', {
                'boutiques': boutiques,
                'produits': produit_results,
                'myboutiques': myboutiques
            })
        else:
            return render(request, 'boutique1/boutique.html', {'boutiques': boutiques,'myboutiques':myboutiques})
    else:
        return render(request, 'boutique1/boutique.html', {'boutiques': boutiques})


def produits(request, filter_by):
    try:
        produit_ids = []
        for boutique in Boutique.objects.all():
            for produit in boutique.produit_set.all():
                produit_ids.append(produit.pk)
        users_songs = Produit.objects.filter(pk__in=produit_ids)
    except Boutique.DoesNotExist:
        users_songs = []
    return render(request, 'boutique1/produits.html', {
        'produit_list': users_songs,
            'filter_by': filter_by,
    })

@login_required
def edit_profile(request):
    form = UserForm(request.POST or None,instance=request.user)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                shops = Boutique.objects.all()
                products = Produit.objects.all()
                categories = Category.objects.all()
                return render(request, 'boutique1/index.html',
                              {'shops': shops, 'products': products, 'categories': categories})
    context = {
        "form": form,
    }
    return render(request, 'boutique1/profile.html', context)

def myshop(request):
    if not request.user.is_authenticated():
        return redirect('/login/')

    else:
        shop = Boutique.objects.filter(owner__user=request.user)
        return render(request, 'boutique1/boutique.html', {'boutiques': shop, 'myboutiques': shop})

def mycollections(request):
    if not request.user.is_authenticated():
        return redirect('/login/')

    else:
        collections = Collection.objects.filter(owner__user=request.user)
        return render(request, 'boutique1/my_collections.html', {'collections': collections})

def myproducts(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    else:
        prod=Produit.objects.filter(owner__user=request.user)
        boutique = get_object_or_404(Boutique,owner__user=request.user)
        return render(request,'boutique1/detail.html',{'produit_list':prod,'boutique':boutique})

def create_collection(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    elif not hasattr(request.user, 'trader'):
        form = TraderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            trader = form.save(commit=False)
            trader.user = request.user
            trader.save()
            return render(request, 'boutique1/create_boutique.html')
        context = {
            "form_name": "You have to signup as a Trader to continue",
            "form": form,
        }
        return render(request, 'boutique1/form_template2.html', context)
    else:
        owner=Trader.objects.filter(user=request.user)
        boutique = get_object_or_404(Boutique, owner=owner)
        produits= Produit.objects.filter(owner=owner)
        if boutique is None:
            return redirect('/create_boutique/')
        elif produits is None:
            return redirect(boutique.id+'/create_produit/')
        else:
            form=CollectionForm(request.POST or None, request.FILES or None)
            form.fields['produit'].queryset=produits
            if form.is_valid():
                collection=form.save(commit=False)
                collection.owner=Trader.objects.get(user=request.user)
                collection.image_collection = request.FILES['image_collection']
                file_type = collection.image_collection.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    context = {
                        'collection': collection,
                        'form': form,
                        'error_message': 'Image file must be PNG, JPG, or JPEG',
                    }
                    return render(request, 'boutique1/create_collection.html', context)

                collection.save()
                form.save_m2m()
                collections=Collection.objects.filter(owner=owner)
                return render(request, 'boutique1/my_collections.html', {'collections': collections,'boutique':boutique})
            context = {

                'form': form,
            }
            return render(request, 'boutique1/create_collection.html', context)

def detail_collection(request,collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    return render(request,'boutique1/detail_collection.html',{'collection':collection})

def delete_coll_produit(request,collection_id,produit_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    produit= get_object_or_404(collection.produit, pk=produit_id)
    collection.produit.remove(produit)
    return redirect('/detail_collection/'+collection_id)

def create_promotion(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    else:
        owner=get_object_or_404(Trader,user=request.user)
        boutique = get_object_or_404(Boutique, owner=owner)
        produits=Produit.objects.filter(owner=owner)
       # collections=Collection.objects.filter(owner=owner)
        form = PromotionForm(request.POST or None, request.FILES or None)
        form.fields['produit'].queryset = produits
       # form.fields['collection'].queryset = collections
        if form.is_valid():
            timezone=request.POST.get('tz')
            Ptype = request.POST.get('promotion_type')
            Fdate=request.POST.get('Fdate')
            Fstart = request.POST.get('Fstart')
            Fend = request.POST.get('Fend')
            print(Ptype)
            promotion = form.save(commit=False)
            promotion.owner = owner
            promotion.collection_id=0
            promotion.tz=timezone
            promotion.promotion_type=Ptype
            if Ptype=="Flash":
                promotion.start_time=datetime.datetime.combine(datetime.date(Fdate),datetime.time(Fstart))
                promotion.end_time=datetime.datetime.combine(datetime.date(Fdate),datetime.time(Fend))
            promotion.save()
            #form.save_m2m()
            start_time = promotion.start_time + timedelta(minutes=int(timezone))
            end_time = promotion.end_time + timedelta(minutes=int(timezone))
            activate.apply_async((promotion.id, promotion.produit.id), eta=start_time)
            
            desactivate.apply_async((promotion.id,promotion.produit.id), eta=end_time)

            # collections = Collection.objects.filter(owner=owner)
            promotions =Promotion.objects.filter(owner__user=request.user)
            context1 = {
                'boutique': boutique,
                'form': form,
                'promotions':promotions
            }
            return render(request, 'boutique1/my_promotions.html', context1)
        context = {
            'boutique':boutique,
            'form': form,
        }
        return render(request, 'boutique1/create_promotion.html', context)

def mypromotions(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    else:
        boutique=get_object_or_404(Boutique,owner__user=request.user)
        owner = get_object_or_404(Trader, user=request.user)
        promotions = Promotion.objects.filter(owner__id=owner.id)
        if 'search' in request.GET:
            query = request.GET.get('search')
            query_list = re.sub("[^\w]", " ", query).split()
            q = Q()
            for word in query_list:
                q |= Q(title__icontains=word)
                promotions = promotions.filter(q)

        page = request.GET.get('page', 1)
        paginator = Paginator(promotions, 4)
        try:
            promotions = paginator.page(page)
        except PageNotAnInteger:
            promotions = paginator.page(1)
        except EmptyPage:
            promotions = paginator.page(paginator.num_pages)

        return render(request, 'boutique1/my_promotions.html', {'boutique': boutique, 'promotions': promotions})


def delete_promotion(request, promotion_id):
    boutique = get_object_or_404(Boutique, owner__user=request.user)
    owner = get_object_or_404(Trader, user=request.user)
    promotion = Promotion.objects.get(id=promotion_id)
    promotion.delete()

    return redirect('/mypromotions/')


def edit_promotion(request, promotion_id):
    owner = get_object_or_404(Trader, user=request.user)
    shop = get_object_or_404(Boutique, owner=owner)
    promotioni = get_object_or_404(Promotion, pk=promotion_id)
    promotions = Promotion.objects.filter(owner=owner)
    collections=Collection.objects.filter(owner=owner)
    form = PromotionForm(request.POST or None, request.FILES or None, instance=promotioni)
    #form.fields['produit'].queryset = produits
    #form.fields['collection'].queryset = collections
    if form.is_valid():
        promotion = form.save(commit=False)
        # product = form.cleaned_data['product']
        # collection.product = product
        promotion.save()

        return render(request, 'boutique1/my_collections.html', {'shop': shop, 'promotions': promotions})
    context = {
        "boutique": shop,
        'form': form,
    }
    return render(request, 'boutique1/create_promotion.html', context)





