# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import sys  

reload(sys)  
sys.setdefaultencoding('Cp1252')
from django import forms

from django.http import HttpResponse

from festivalapp.models import Profile
from festivalapp.models import User

from festivalapp.forms import peliculaForm2
from festivalapp.models import Pelicula, Programa, Proyeccion

from django.contrib import messages

from django.core.files.storage import FileSystemStorage
from django.template import RequestContext
from festivalapp.forms import ContactForm

import os
from django.conf import settings
from django.shortcuts import render_to_response
from festivalapp.models import Seccion
from festivalapp.models import Festival
from django.core.urlresolvers import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
import datetime
from festivalapp.forms import EditarPerfilForm

# Create your views here.



def getdatos():
    festival_actual = Festival.objects.latest('anio')
    datos={}
    datos['logo'] = festival_actual.logo
    datos['titulo'] = festival_actual.titulo
    datos['descripcion'] = festival_actual.descripcion
    datos['fechinicio'] = festival_actual.fechinicio
    datos['fechinscrip'] = festival_actual.fechinscrip
    datos['anio'] = festival_actual.anio
    return datos



from django.shortcuts import redirect




def index(request):
    datos = getdatos()
    festival_actual = Festival.objects.latest('anio')

    if Programa.objects.filter(festival=festival_actual).exists():
        programa = Programa.objects.get(festival = festival_actual)
        if(programa.visibilidad):
            proyecciones = programa.proyecciones.all().order_by('orderdate')
            visible=True
        else:
            visible=False
            proyecciones = []
    else:
        visible = False
        proyecciones = []
        
    return render(request, 'festivalapp/index.html', {'datos': datos, 'progVisible' : visible, 'proyecciones': proyecciones})



def editarperfil(request):
    datos = getdatos()
    user = User.objects.get(email=request.user) 
    print(user.profile.nombre)
    if request.method == 'POST':
        user.profile.nombre = request.POST['nombre']
        user.profile.apellidos = request.POST['apellidos']
        user.profile.telefono = request.POST['telefono']
        user.profile.direccion = request.POST['direccion']
        user.save()
        request.session['datosG'] = True

        return redirect('perfil')

    else:
        form = EditarPerfilForm(initial={'nombre':user.profile.nombre, 'apellidos': user.profile.apellidos, 'telefono' : user.profile.telefono, 'direccion': user.profile.direccion})

    return render(request, 'festivalapp/editarperfil.html', {'form': form, 'datos' : datos})

from django.core.mail import send_mail

def contacto(request):
    datos = getdatos()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():     
            data = form.cleaned_data
            nombre = data['nombre']
            apellidos = data['apellidos']
            email = data['email']
            asunto = data['asunto']
            mensaje = data['mensaje']


            DEFAULT_FROM_EMAIL='(Festival Cinemistica) Web <no-reply@Cinemistica.com>' 

            send_mail(asunto, mensaje + "Email: " + email + "/n" + "Nombre: " + nombre + "/nApellidos: " + apellidos, DEFAULT_FROM_EMAIL, ['mustapha@correo.ugr.es'], fail_silently=False)

            print(nombre)
            print(apellidos)
            print(email)
            print(asunto)
            print(mensaje)

            return redirect('index')

    else:
        form = ContactForm

    return render(request, 'festivalapp/contact-us.html', {'form': form, 'datos' : datos})




def aboutus(request):
    datos = getdatos()
    return render(request, 'festivalapp/sobrenosotros.html', {'datos': datos})

def bases(request):
    datos = getdatos()
    return render(request, 'festivalapp/bases.html', {'datos': datos})

def galardones(request):
    datos = getdatos()
    return render(request, 'festivalapp/galardones.html', {'datos': datos})



def perfil(request):
    datos = getdatos()
    datosG = request.session.pop('datosG', False)

    return render(request, 'festivalapp/perfil.html', {'datos': datos, 'datosG' : datosG})


def mis_peliculas(request):
    datos = getdatos()
    user = User.objects.get(email=request.user)
    peliculas = Pelicula.objects.filter(usuario=user)


    festival_actual = Festival.objects.latest('anio')

    if Programa.objects.filter(festival=festival_actual).exists():
        programa = Programa.objects.get(festival = festival_actual)
        progPublicado = programa.visibilidad
    else:
        progPublicado = False


    return render(request, 'festivalapp/mispeliculas.html', {'datos': datos, 'peliculas': peliculas, 'progPublicado' : progPublicado})


from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

def changepass(request):
    datos = getdatos()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('changepass_success')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'festivalapp/changepass.html', {
        'form': form, 'datos':datos
    })




def changepass_success(request):
    datos = getdatos()
    return render(request, 'festivalapp/changepass_success.html', {'datos': datos})


from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from festivalapp.forms import SignUpForm

def signup(request):
    datos = getdatos()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.nombre = form.cleaned_data.get('nombre')
            user.profile.apellidos = form.cleaned_data.get('apellidos')
            user.profile.direccion = form.cleaned_data.get('direccion')
            user.profile.telefono = form.cleaned_data.get('telefono')
            user.save()
            raw_password = form.cleaned_data.get('password1')
          # messages.success(request, 'Form submission successful')
            user = authenticate(username=user.email, password=raw_password)
            #login(request, user)
            return render_to_response('festivalapp/thankyou.html', {'datos': datos})
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form, 'datos' : datos})

from django.http import HttpResponseRedirect



def sendfilm(request):
    datos = getdatos()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.nombre = form.cleaned_data.get('nombre')
            user.profile.apellidos = form.cleaned_data.get('apellidos')
            user.profile.direccion = form.cleaned_data.get('direccion')
            user.profile.telefono = form.cleaned_data.get('telefono')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.email, password=raw_password)
            #login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'festivalapp/sendfilm.html', {'form': form, 'datos' : datos})


def sendfilm_success(request):
    datos = getdatos()
    return render(request, 'festivalapp/sendfilm_success.html', {'datos': datos})

from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import DefaultStorage
from django_countries import countries
import operator
from collections import defaultdict



class ContactWizard(SessionWizardView):
    datos = getdatos()
    template_name = "festivalapp/sendfilm.html"
    file_storage = DefaultStorage()
    secciones_list = []


    def get_form(self, step=None, data=None, files=None):
        form = super(ContactWizard, self).get_form(step, data, files)

        #determine the step if not given
        if step is None:
            step = self.steps.current

        if step == "2":
            festival_actual = Festival.objects.latest('anio')
            self.secciones_list = [(str(seccion.id), seccion.descripcion) for seccion in festival_actual.secciones.all()]

            form.fields['secciones'] = forms.MultipleChoiceField(error_messages={'required': 'Debe seleccionar al menos dos secciones por film'},label='Secciones a las que se inscribe el film',choices=self.secciones_list, widget=forms.CheckboxSelectMultiple(), help_text='(máximo 2 secciones por film)')            ## Pass the data when initing the form, which is the POST
            ## data if the got_form function called during a post
            ## or the self.storage.get_step_data(form_key) if the form wizard
            ## is validating this form again in the render_done methodform 

        return form


    def done(self, form_list, **kwargs):
        form_data =[form.cleaned_data for form in form_list]

        form_data[0]['nacionalidad'] = dict(countries)[form_data[0]['nacionalidad']]
        form_data[0]['paisrodaje'] = dict(countries)[form_data[0]['paisrodaje']]

        dic_list= {}
        for v, k in self.secciones_list:
            dic_list[v]=k
 
        aux=[]

        for seccion in form_data[2]['secciones']:
            aux.append(dic_list[seccion])
        


        strdb=';'.join(aux)

        form_data[2]['secciones']=strdb


        campos = {}
        campos.update(form_data[0])
        campos.update(form_data[1])
        campos.update(form_data[2])

        p = Pelicula.objects.create(**campos)
        p.usuario = self.request.user   
        p.festival=datos['anio']
        p.save();
        
        return render(self.request, 'festivalapp/sendfilm_success.html', {'form_data': form_data}, {'datos': datos})




from festivalapp.models import Pelicula
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
 

     
class Peliculas(ListView):
    datos = getdatos()

    model = Pelicula
    template_name = 'festivalapp/peliculas.html'
    context_object_name = 'peliculas'

    def get_queryset(self, **kwargs):
        festival_actual = Festival.objects.latest('anio')
        filtro = self.request.GET.get('filtro', None)

        if filtro == 'pendiente':
            return Pelicula.objects.filter(festival =festival_actual.anio,  participante=False)
        if filtro == 'participante':
            return Pelicula.objects.filter(festival =festival_actual.anio,participante=True)
        if filtro == 'premiada':
            return Pelicula.objects.filter(festival =festival_actual.anio,premiada=True)
        if filtro == 'todas':
            return Pelicula.objects.all()
        if filtro == None:
            return Pelicula.objects.filter(festival =festival_actual.anio,participante=False)
    


    def get_context_data(self, **kwargs):
        datos = getdatos()
        context = super(Peliculas, self).get_context_data(**kwargs)
        context['datos'] = datos
        return context



class Historial(ListView):
    datos = getdatos()
    model = Pelicula
    template_name = 'festivalapp/historial.html'
    context_object_name = 'peliculas'

    def get_queryset(self, **kwargs):
        filtro = self.request.GET.get('filtro', None)
        festival = self.request.GET.get('festival', None)

        if filtro == 'registrada':
            return Pelicula.objects.filter(participante=False, festival=festival)
        if filtro == 'participante':
            return Pelicula.objects.filter(participante=True, festival=festival)
        if filtro == 'premiada':
            return Pelicula.objects.filter(premiada=True, festival=festival)
        if filtro == 'todas':
            return Pelicula.objects.filter(festival=festival)
        if filtro == None:
            return Pelicula.objects.filter(participante=False, festival=festival)
    


    def get_context_data(self, **kwargs):
        datos = getdatos()
        context = super(Historial, self).get_context_data(**kwargs)
        context['datos'] = datos
        festivales = Festival.objects.values('anio').distinct()
        selectedf = self.request.GET.get('festival', None)

        context['festivales'] = festivales
        context['selectedf'] = str(selectedf)
        filtro = self.request.GET.get('filtro', None)
        if(filtro == None):
            filtro="registrada"
        context['filtro'] = filtro

        return context



def calendar(request):
    datos = getdatos()
    festival_actual = Festival.objects.latest('anio')
    peliculas = Pelicula.objects.filter(participante=True, festival=festival_actual.anio)

    if Programa.objects.filter(festival=festival_actual).exists():
        programa = Programa.objects.get(festival = festival_actual)
        visible = programa.visibilidad
    else:
        visible = False



    if(visible):
        proyecciones = programa.proyecciones.all()

    else:
        proyecciones=[]
        

    return render(request, 'festivalapp/calendar.html', {'datos': datos, 'visible' : visible, 'proyecciones' : proyecciones})



import json

from django.core import serializers




def procesar(request):
    id_ = request.POST['id']
    operacion = request.POST['operacion']

    pelicula = Pelicula.objects.get(pk = int(request.POST['id']))
    if operacion == "quitar":
        pelicula.participante=False
    elif operacion == "incluir":
        pelicula.participante=True
    elif operacion == "quitarpremio":
        pelicula.premiada=False
    elif operacion == "premiar":
        pelicula.premiada=True
    

    pelicula.save()
    
    payload = {'success': True}
    return HttpResponse(json.dumps(payload), content_type='application/json')


def getpelicula(request):
    id_ = request.POST['id']


    pelicula = Pelicula.objects.get(pk = int(request.POST['id']))
 

    data = serializers.serialize('json', [pelicula,])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data, content_type='application/json')




def getPelisParticipantes(request):
    festival_actual = Festival.objects.latest('anio')
    participantes = Pelicula.objects.filter(participante=True, festival=festival_actual.anio)
 
    print(participantes)


    data = serializers.serialize('json', participantes)

    return HttpResponse(data, content_type='application/json')


def getPrograma(request):
    festival_actual = Festival.objects.latest('anio')

    if Programa.objects.filter(festival=festival_actual).exists():
        programa = Programa.objects.get(festival=festival_actual)
    else:
        programa = Programa.objects.create(festival=festival_actual)
        p.save()


    proyecciones = programa.proyecciones.all()



    data = serializers.serialize('json', proyecciones)

    return HttpResponse(data, content_type='application/json')

from django.utils import timezone

def guardarPrograma(request):
    proyecciones = request.body
    festival_actual = Festival.objects.latest('anio')

   
    if Programa.objects.filter(festival=festival_actual).exists():
        prog = Programa.objects.get(festival=festival_actual)
    else:
        prog = Programa.objects.create(festival=festival_actual)


    Proyeccion.objects.filter(prog=prog).delete()
    proyecciones = json.loads(proyecciones)

    Programa.proyecciones.through.objects.all().delete()
    Proyeccion.objects.filter(programa=prog).delete()


    for proyeccion in proyecciones:
         p = Proyeccion.objects.create(pelicula=Pelicula.objects.get(pk=proyeccion['pelicula']))

         p.fecha = datetime.datetime.strptime(str(proyeccion['fecha']), "%d/%m/%Y").date()
         p.horaInicio = proyeccion['horaInicio']
         p.horaFin = proyeccion['horaFin']
         p.prog = prog
         horaF = datetime.datetime.strptime(p.horaInicio, '%H:%M').time()
         p.orderdate = timezone.make_aware(datetime.datetime.combine(p.fecha, horaF), timezone.get_current_timezone())


         p.save();
         prog.proyecciones.add(p)


    prog.save()
    
    
    data = 1
    return HttpResponse(data, content_type='application/json')



def publicarPrograma(request):
    publicar = request.body
    festival_actual = Festival.objects.latest('anio')
    programa = Programa.objects.get(festival = festival_actual)

    if(publicar == "true"):
        programa.visibilidad = True
    else:
        programa.visibilidad = False

    programa.save()
          
    data = 1
    return HttpResponse(data, content_type='application/json')







def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": "10000000.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('your-return-view')),
        "cancel_return": request.build_absolute_uri(reverse('your-cancel-view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)


