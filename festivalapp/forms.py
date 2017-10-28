# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from festivalapp.models import User
from django.db import models
from django.core.validators import URLValidator
from django.forms.extras.widgets import SelectDateWidget
from datetime import date
from festivalapp.models import Seccion



INTEGER_CHOICES= [tuple([x,x]) for x in range(2000,date.today().year+1)]



class SignUpForm(UserCreationForm):
    nombre = forms.CharField(max_length=30, required=False, help_text='', label='Nombre')
    apellidos = forms.CharField(max_length=60, required=False, help_text='', label='Apellidos')
    telefono = forms.CharField(max_length=13, required=False, help_text='', label='Telefono')
    direccion = forms.CharField(max_length=100, required=False, help_text='', label='Dirección')


    class Meta:
        model = User
        fields = ('nombre', 'apellidos', 'telefono','email', 'direccion', 'password1', 'password2')



    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )





class EditarPerfilForm(forms.Form):
    nombre = forms.CharField(max_length=30, required=True, help_text='', label='Nombre')
    apellidos = forms.CharField(max_length=60, required=True, help_text='', label='Apellidos')
    telefono = forms.CharField(max_length=13, required=True, help_text='', label='Telefono')
    direccion = forms.CharField(max_length=100, required=True, help_text='', label='Dirección')


    def clean(self):
        cleaned_data = super(EditarPerfilForm, self).clean()




class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=30, required=True, help_text='', label='Nombre')
    apellidos = forms.CharField(max_length=60, required=True, help_text='', label='Apellidos')
    email = forms.EmailField(label='Email')
    asunto = forms.CharField(max_length=180, required=True, help_text='', label='Asunto')
    mensaje = forms.CharField(widget=forms.Textarea)


    def clean(self):
        cleaned_data = super(ContactForm, self).clean()


VIDEO= [
    ('color', 'Color'),
    ('blancoynegro', 'Blanco y negro'),
    ('ambos', 'Ambos'),
    ]
from django_countries.fields import CountryField
from django_countries import countries




class peliculaForm1(forms.Form):
    titulo = forms.CharField(max_length=100, required=False, label='Título original')
    tituloesp = forms.CharField(max_length=100, required=False, label='Título en español')
    tituloing = forms.CharField(max_length=100, required=False, label='Título en inglés')
    duracion= forms.IntegerField(required=False,min_value=10, max_value=180, label='Duración en minutos')
    video= forms.CharField(required=False,label='Formato del video', widget=forms.Select(choices=VIDEO))
    nacionalidad  =  forms.ChoiceField(required=False,label='Nacionalidad del film', choices=list(countries), initial='ES')
    paisrodaje  =  forms.ChoiceField(required=False,label='País de rodaje', choices=list(countries), initial='ES')
    aniorodaje= forms.IntegerField(required=False, label="Año de rodaje", widget=forms.Select(choices=INTEGER_CHOICES))
    formatorodaje = forms.CharField(max_length=100, required=False, help_text='', label='Formato de rodaje')
    montaje = forms.CharField(max_length=100, required=False, help_text='', label='Montaje')
    produccion = forms.CharField(max_length=100, required=False, help_text='', label='Producción')
    sonido = forms.CharField(max_length=100, required=False, help_text='', label='Sonido')
    musica = forms.CharField(max_length=100, required=False, help_text='', label='Música')
    idiomaoriginal = forms.CharField(max_length=100, required=False, help_text='', label='Idioma original')
    subtitulos = forms.CharField(max_length=100, required=False, help_text='', label='Idioma de los subtítulos')
    actores = forms.CharField(required=False,help_text='Nombres completos de actores (actor1, actor2, actor3 ...)', widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "10", }), label='Actores')
   


class peliculaForm2(forms.Form):
    enlacevisionado = forms.URLField(required=False, label='Enlace de visionado')
    enlacetrailer = forms.URLField(required=False, label='Enlace de trailer')
    enlaceproyeccion = forms.URLField(required=False, label='Enlace de descarga para proyección')
    enlacedescarga = forms.URLField(required=False, label='Enlace descarga material gráfico', help_text='(carpeta tipo Drop Box con foto del director, fotos del film, poster)')
    image = forms.ImageField(required=False, label='Fotografía')






class peliculaForm3(forms.Form):
    guion = forms.CharField(required=False,help_text='', widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "10", }), label='Guión')
    sinopsing = forms.CharField(required=False,help_text='', widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "10", }), label='Sinopsis en Inglés')
    sinopsisesp = forms.CharField(required=False,help_text='', widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "10", }), label='Sinopsis en Español')
    lugarestreno1 = forms.CharField(max_length=100, required=False, label='Lugar de estreno internacional')
    fechaestrenointer = forms.DateField(required=False, label='Fecha de estreno internacional', widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    lugarestrenoesp = forms.CharField(max_length=100, required=False, label='Lugar de estreno en españa')
    fechaestrenoesp = forms.DateField(required=False, label='Fecha de estreno en españa', widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    web = forms.URLField(required=False, label='Web')
    premios = forms.CharField(required=False,help_text='', widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "5", }), label='Premios obtenidos')
    comentarios = forms.CharField(required=False,help_text='', widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "6", }), label='Comentarios')
    secciones = forms.MultipleChoiceField()




    def clean_secciones(self):
        if len(self.cleaned_data['secciones']) > 2:
            raise forms.ValidationError('No puede seleccionar más de dos secciones por film')
        return self.cleaned_data['secciones']





    
