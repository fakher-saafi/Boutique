from django.conf.urls import url,include
from . import views

app_name = 'boutique1'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^boutique/$', views.boutiques, name='boutiques'),
    url(r'^myshop/$', views.myshop, name='myshop'),
    url(r'^mycollections/$', views.mycollections, name='mycollections'),
    url(r'^myproducts/$', views.myproducts, name='myproducts'),
    url(r'^boutique/(?P<boutique_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^produits/(?P<filter_by>[a-zA_Z]+)/$', views.produits, name='produits'),

    url(r'^create_boutique/$', views.create_boutique, name='create_boutique'),
    url(r'^(?P<boutique_id>[0-9]+)/create_produit/$', views.create_produit, name='create_produit'),
    url(r'^(?P<collection_id>[0-9]+)/delete_collection/$', views.delete_collection, name='delete_collection'),
    url(r'^(?P<collection_id>[0-9]+)/(?P<produit_id>[0-9]+)/delete_coll_produit/$', views.delete_coll_produit, name='delete_coll_produit'),
    url(r'^(?P<boutique_id>[0-9]+)/delete_boutique/$', views.delete_boutique, name='delete_boutique'),
    url(r'^(?P<boutique_id>[0-9]+)/edite_boutique/$', views.edit_boutique, name='edit_boutique'),
    url(r'^(?P<collection_id>[0-9]+)/edite_collection/$', views.edit_collection, name='edit_collection'),
    url(r'^(?P<boutique_id>[0-9]+)/delete_produit/(?P<produit_id>[0-9]+)/$', views.delete_produit, name='delete_produit'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate1, name='activate'),
    url(r'^create_collection/$', views.create_collection, name='create_collection'),
    url(r'^detail_collection/(?P<collection_id>[0-9]+)/$', views.detail_collection, name='detail_collection'),

    #----------------------------promotion-------------------------
    url(r'^create_promotion/$', views.create_promotion, name='create_promotion'),
    url(r'^(?P<promotion_id>[0-9]+)/delete_promotion/$', views.delete_promotion, name='delete_promotion'),
    url(r'^edit_promotion/(?P<promotion_id>[0-9]+)/$', views.edit_promotion, name='edit_promotion'),
    url(r'^mypromotions/$', views.mypromotions, name='mypromotions'),
    #-------------------------rest--------------------
    url(r'^rest/', include('boutique1.restapi.urls')),



]
