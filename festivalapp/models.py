# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
import random 
import string
import imghdr


from django.utils import timezone



# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class Seccion(models.Model):
    descripcion = models.CharField(max_length=150)

    def __unicode__(self):
       return self.descripcion



from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, null=True)
    apellidos = models.CharField(max_length=60, null=True)
    telefono = models.CharField(max_length=13, null=True)
    apellidos = models.CharField(max_length=60, null=True)	


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()






from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)






from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email



import uuid

import os

from django.contrib import admin



def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('filmimages/', filename)



import datetime
YEAR_CHOICES = []
for r in range(datetime.datetime.now().year-1, (datetime.datetime.now().year+4)):
    YEAR_CHOICES.append((r,r))


class Pelicula(models.Model):
    titulo = models.CharField(max_length=100, null=True)
    tituloesp = models.CharField(max_length=100, null=True)
    tituloing = models.CharField(max_length=100, null=True)
    duracion= models.IntegerField(null=True)
    video= models.CharField(max_length=15, null=True)
    nacionalidad  =  models.CharField(max_length=100, null=True)
    paisrodaje  =  models.CharField(max_length=100, null=True)
    aniorodaje= models.IntegerField(null=True)
    formatorodaje = models.CharField(max_length=100, null=True)
    montaje = models.CharField(max_length=100, null=True)
    produccion = models.CharField(max_length=100, null=True)
    sonido = models.CharField(max_length=100, null=True)
    musica = models.CharField(max_length=100, null=True)
    idiomaoriginal = models.CharField(max_length=100, null=True)
    subtitulos = models.CharField(max_length=100, null=True)
    actores = models.TextField(null=True)
    enlacevisionado = models.URLField(null=True)
    enlacetrailer = models.URLField(null=True)
    enlaceproyeccion = models.URLField(null=True)
    enlacedescarga = models.URLField(null=True)
    image = models.ImageField(upload_to = get_file_path)
    guion = models.CharField(max_length=1000, null=True)
    sinopsing = models.CharField(max_length=1000, null=True)
    sinopsisesp = models.CharField(max_length=1000, null=True)
    lugarestreno1 = models.CharField(max_length=100, null=True)
    fechaestrenointer = models.DateField(null=True)
    lugarestrenoesp = models.CharField(max_length=100, null=True)
    fechaestrenoesp = models.DateField(null=True)
    web = models.URLField(null=True)
    premios = models.CharField(max_length=500, null=True)
    comentarios = models.CharField(max_length=500, null=True)
    secciones = models.TextField(null=True)
    fecha = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    participante = models.BooleanField(default=False)
    premiada = models.BooleanField(default=False)
    festival = models.IntegerField(default=datetime.datetime.now().year)








def get_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "logo-%s.%s" % (datetime.datetime.now().year, ext)
    return os.path.join('logos/', filename)
from django import forms

class Festival(models.Model):
    logo = models.ImageField("Logo", upload_to = get_logo_path)
    anio = models.IntegerField(_('Año'),  choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    fechinicio =  models.DateField("Fecha inicio de inscripción", default=timezone.now)
    fechinscrip =  models.DateField("Fecha límite de inscripción", default=timezone.now)
    titulo = models.CharField(max_length=100, null=True)
    descripcion = models.TextField("Descripción", max_length=500, default="")
    secciones = models.ManyToManyField(Seccion, blank=True)





    def __unicode__(self):
       return "Festival del " + str(self.anio)











