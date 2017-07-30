# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse



# Create your views here.
def index(request):
	return render(request, 'festivalapp/index.html')


def contacto(request):
	return render(request, 'festivalapp/contact-us.html')


def aboutus(request):
	return render(request, 'festivalapp/sobrenosotros.html')

def bases(request):
	return render(request, 'festivalapp/bases.html')
