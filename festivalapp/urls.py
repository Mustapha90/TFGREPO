from django.conf.urls import url
from django.conf.urls import include
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
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^sendfilm/$', ContactWizard.as_view([peliculaForm1, peliculaForm2, peliculaForm3]),name='sendfilm'),
    url(r'^peliculas',Peliculas.as_view(), name="peliculas"),
    url(r'^procesar',views.procesar, name="procesar"),   
    url(r'^historial',Historial.as_view(), name="historial"),   
    url(r'^getpelicula',views.getpelicula, name="getpelicula"),
    url(r'^getPelisParticipantes',views.getPelisParticipantes, name="getPelisParticipantes"),
    url(r'^getPrograma',views.getPrograma, name="getPrograma"),
    url(r'^calendar',views.calendar, name="calendar"),
    url(r'^publicarPrograma',views.publicarPrograma, name="publicarPrograma"),
    url(r'^guardarPrograma',views.guardarPrograma, name="guardarPrograma"),
    url(r'^changepass/$', views.changepass, name='changepass'),
    url(r'^perfil',views.perfil, name="perfil"),
    url(r'^editarperfil',views.editarperfil, name="editarperfil"),
    url(r'^changepass_success',views.changepass_success, name="changepass_success"),
    url(r'^mis_peliculas',views.mis_peliculas, name="mis_peliculas"),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
] 





