from django.conf.urls import url
from . import views

app_name = 'album'

urlpatterns = [

    url(r'^create_album/$',views.create_album,name='create_album'),
    url(r'^my_albums/$',views.my_albums,name='my_albums'),
    url(r'^delete_album/(?P<album_id>[0-9]+)/$', views.delete_album, name='delete_album'),
    url(r'^edit_album/(?P<album_id>[0-9]+)/$', views.edit_album, name='edit_album'),
    url(r'^albumdetails/(?P<album_id>[0-9]+)/$', views.albumdetails, name='albumdetails'),

    url(r'^album_add_picture/(?P<album_id>[0-9]+)/$', views.album_add_picture, name='album_add_picture'),
    url(r'^(?P<picture_id>[0-9]+)/delete_picture/$', views.delete_picture,
        name='delete_picture'),
    url(r'^(?P<picture_id>[0-9]+)/edit_picture/$', views.edit_picture,
        name='edit_picture'),




]
