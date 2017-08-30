from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max,Min
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from boutique1.models import Boutique, Produit, Category, Promotion
from wishlist.models import wish_category
from django.http import request
import re  # for spiltting words with regex


def produits(request, filter_by):
    try:
        produit_ids = []
        for boutique in Boutique.objects.all():
            for produit in boutique.produit_set.all():
                produit_ids.append(produit.pk)
        users_songs = Produit.objects.filter(pk__in=produit_ids)
    except Boutique.DoesNotExist:
        users_songs = []
    return render(request, 'discover.html', {
        'produit_list': users_songs,
            'filter_by': filter_by,
    })

def detail(request, product_id):
    produit = get_object_or_404(Produit, pk=product_id)
    return render(request, 'product_detail.html', {'produit': produit})

def detailshop(request, boutique_id):

    produit = Produit.objects.filter(Boutique__id=boutique_id)
    boutique = get_object_or_404(Boutique, pk=boutique_id)
    return render(request, 'discover_shop.html', {'boutique': boutique,'products': produit})

def discover(request, category=''):
    timezone = request.POST.get('tz')
    promotions=Promotion.objects.filter(is_active=True)
    product_list = Produit.objects.filter(is_active=True)
    categories = Category.objects.all()
    wish_categorys=wish_category.objects.filter(user=request.user)
    counter = []
    header = ''

    for c in categories:
        counter.append((c, product_list.filter(category=c).count()))

        # SEARCH
    if 'site_search' in request.GET:  # If a search is happening
        query = request.GET.get('site_search')
        query_list = re.sub("[^\w]", " ", query).split()
        q = Q()
        for word in query_list:
            q |= Q(nom_produit__icontains=word) | Q(description__icontains=word)
        product_list = product_list.filter(q)
        header = '- search = ' + query + ' - '

    # if price range defined
    if (('min' in request.GET) and ('max' in request.GET)):
        max_p = int(request.GET.get('max'))
        min_p = int(request.GET.get('min'))

        q = Q(prix_produit__lte=max_p) & Q(prix_produit__gte=min_p)
        product_list = product_list.filter(q)
        print(q)
        header += '- price in = [' + str(min_p) + ', ' + str(max_p) + '] -'

    # if price range defined
    if ('product_type' in request.GET):
        product_type = request.GET.get('product_type')

        q = Q(product_type=product_type)
        product_list = product_list.filter(q)
        if product_type == 'VTG':
            product_type_label = 'Vintage'
        elif product_type == 'HM':
            product_type_label = 'Hand made'
        print(Produit.VINTAGE)
        header += '- product type = ' + str(product_type_label) + ' -'

    # counting result elements by category
    counter = []
    for c in categories:
        counter.append((c, product_list.filter(category=c).count()))

    # if we are filtering by category
    if ('categorie' in request.GET):
        category =request.GET.get('categorie')
        product_list = product_list.filter(category__label=category)
        header += '- category filter = ' + str(category) + ' -'

    if ('sort_by' in request.GET):
        ordering = request.GET.get('sort_by')
        if ordering == 'recent':
            product_list = product_list.order_by('create_date')
        elif ordering == 'Low - High Price':
            product_list = product_list.order_by('prix_produit')
        elif ordering == 'High - Low Price':
            product_list = product_list.order_by('-prix_produit')
        elif ordering == 'A - Z Order':
            product_list = product_list.order_by('nom_produit')
        elif ordering == 'Z - A Order':
            product_list = product_list.order_by('-nom_produit')
        header += '- ordered by ' + str(ordering) + ' -'
    else:
        product_list.order_by('create_date')
        header += '- ordered by recent -'

    max_price = product_list.aggregate(Max('prix_produit'))
    min_price = product_list.aggregate(Min('prix_produit'))

    print(max_price, min_price)

    # PAGINATION
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 6)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'header': header,
        'counter': counter,
        'products': products,
        'categories': categories,
        'max_price': max_price,
        'min_price': min_price,
        'promotions': promotions,
        'wish_categorys':wish_categorys,
    }
    return render(request, 'discover.html', context)



