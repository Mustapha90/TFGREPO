from django.conf.urls import url
from django.conf.urls import include


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contacto/$', views.contacto, name='contacto'),
]

