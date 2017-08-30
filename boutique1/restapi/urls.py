
from django.conf.urls import url

from boutique1.restapi.views import ProductCreateAPIView, ProductListAPIView, ProductRetriveAPIView, UpdateAPIView, \
    DestroyAPIView

app_name = 'restapi'

urlpatterns = [
    url(r'^list/$', ProductListAPIView.as_view(), name='list'),
    url(r'^Create/$', ProductCreateAPIView.as_view(), name='list'),
    url(r'^detail/(?P<id>[0-9]+)/$', ProductRetriveAPIView.as_view(), name='detail'),
    url(r'^update/(?P<id>[0-9]+)/$', UpdateAPIView.as_view(), name='detail'),
    url(r'^delete/(?P<id>[0-9]+)/$', DestroyAPIView.as_view(), name='delete'),




]





