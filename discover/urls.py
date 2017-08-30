from django.conf.urls import url
from . import views

app_name = 'discover'

urlpatterns = [
    url(r'^(?P<filter_by>[a-zA_Z]+)/$', views.produits, name='produits'),
    url(r'^product/(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^products/(?P<boutique_id>[0-9]+)/$', views.detailshop, name='detailshop'),

    #url(r'^discoverProd/$', views.home, name='home'),
    url(r'^discoverProd/(?P<category>[\w\-]+)/$', views.discover, name='discover_category'),
    url(r'^discoverProd/$', views.discover, name='discover'),

]
