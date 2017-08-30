from django.conf.urls import url
from . import views

app_name = 'wishlist'

urlpatterns = [

    url(r'^create_wishcategory/$',views.create_wish_category,name='create_wish_category'),
    url(r'^my_categorys/$',views.my_categorys,name='my_categorys'),
    url(r'^delete_category/(?P<category_id>[0-9]+)/$', views.delete_category, name='delete_category'),
    url(r'^edit_category/(?P<category_id>[0-9]+)/$', views.edit_category, name='edit_category'),
    url(r'^category_add_product/(?P<category_id>[0-9]+)/$', views.create_wish_list, name='create_wish_list'),
    url(r'^add_product/(?P<category_id>[0-9]+)/(?P<prod_id>[0-9]+)/$', views.addprod, name='addprod'),
    url(r'^categoryProds/(?P<category_id>[0-9]+)/$', views.detailcategory, name='detailcategory'),
    url(r'^(?P<category_id>[0-9]+)/(?P<produit_id>[0-9]+)/delete_wishlist_produit/$', views.delete_category_produit,
        name='delete_category_produit'),

    url(r'^wishlist/$',views.create_wish_list,name='create_wish_list'),


]
