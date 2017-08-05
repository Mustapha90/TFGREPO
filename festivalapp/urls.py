from django.conf.urls import url
from django.conf.urls import include


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contacto/$', views.contacto, name='contacto'),
    url(r'^aboutus/$', views.aboutus, name='aboutus'),
    url(r'^bases/$', views.bases, name='bases'),
    url(r'^galardones/$', views.galardones, name='galardones'),
]

