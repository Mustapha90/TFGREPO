# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import sys  

reload(sys)  
sys.setdefaultencoding('Cp1252')
from django import forms

from django.http import HttpResponse

from festivalapp.models import Profile

from festivalapp.forms import peliculaForm2
from festivalapp.models import Pelicula

from django.contrib import messages

from django.core.files.storage import FileSystemStorage
from django.template import RequestContext

import os
from django.conf import settings
from django.shortcuts import render_to_response
from festivalapp.models import Seccion
from festivalapp.models import Festival
from django.core.urlresolvers import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm


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


datos = getdatos()

def index(request):
    return render(request, 'festivalapp/index.html', {'datos': datos})


def contacto(request):
	return render(request, 'festivalapp/contact-us.html', {'datos': datos})


def aboutus(request):
	return render(request, 'festivalapp/sobrenosotros.html', {'datos': datos})

def bases(request):
	return render(request, 'festivalapp/bases.html', {'datos': datos})

def galardones(request):
	return render(request, 'festivalapp/galardones.html', {'datos': datos})


from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from festivalapp.forms import SignUpForm

def signup(request):
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
    return render(request, 'registration/registration_form.html', {'form': form}, {'datos': datos})

from django.http import HttpResponseRedirect



def sendfilm(request):
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
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'festivalapp/sendfilm.html', {'form': form}, {'datos': datos})


def sendfilm_success(request):
    return render(request, 'festivalapp/sendfilm_success.html', {'datos': datos})

from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import DefaultStorage
from django_countries import countries
import operator
from collections import defaultdict



class ContactWizard(SessionWizardView):
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
    model = Pelicula
    template_name = 'festivalapp/peliculas.html'
    context_object_name = 'peliculas'

    def get_queryset(self, **kwargs):
        filtro = self.request.GET.get('filtro', None)

        if filtro == 'pendiente':
            return Pelicula.objects.filter(participante=False)
        if filtro == 'participante':
            return Pelicula.objects.filter(participante=True)
        if filtro == 'premiada':
            return Pelicula.objects.filter(premiada=True)
        if filtro == 'todas':
            return Pelicula.objects.all()
        if filtro == None:
            return Pelicula.objects.filter(participante=False)
    


    def get_context_data(self, **kwargs):
        context = super(Peliculas, self).get_context_data(**kwargs)
        context['datos'] = datos
        return context



class Historial(ListView):
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
    return render(request, 'festivalapp/calendar.html', {'datos': datos})



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


