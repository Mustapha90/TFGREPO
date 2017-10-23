from django.conf.urls import url
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from forms import peliculaForm1, peliculaForm2, peliculaForm3
from views import ContactWizard
from festivalapp.views import Peliculas, Historial
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contacto/$', views.contacto, name='contacto'),
    url(r'^aboutus/$', views.aboutus, name='aboutus'),
    url(r'^bases/$', views.bases, name='bases'),
    url(r'^galardones/$', views.galardones, name='galardones'),
    url(r'^login$', auth_views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^sendfilm/$', ContactWizard.as_view([peliculaForm1, peliculaForm2, peliculaForm3]),name='sendfilm'),
    url(r'^peliculas',Peliculas.as_view(), name="peliculas"),
    url(r'^procesar',views.procesar, name="procesar"),   
    url(r'^historial',Historial.as_view(), name="historial"),   
    url(r'^getpelicula',views.getpelicula, name="getpelicula"),
    url(r'^calendar',views.calendar, name="calendar"),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
] 





