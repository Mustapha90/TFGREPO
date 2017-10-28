# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


from .models import Question
from .models import Profile
from .models import User
from .models import Pelicula
from .models import Seccion
from .models import Festival
from .models import Programa, Proyeccion




# Register your models here.




admin.site.register(Question)

admin.site.register(User)

admin.site.register(Profile)

admin.site.register(Pelicula)



                                                            

class SeccionInline(admin.TabularInline):
    model = Festival.secciones.through
    extra=0



class FestivalAdmin(admin.ModelAdmin):
    inlines = (SeccionInline,)
    exclude = ('secciones',) #exclude the field you put the inline on so you dont have double fields



admin.site.register(Seccion)

admin.site.register(Festival, FestivalAdmin)


class ProyeccionInline(admin.TabularInline):
    model = Programa.proyecciones.through
    extra=0



class ProgramaAdmin(admin.ModelAdmin):
    inlines = (ProyeccionInline,)
    exclude = ('proyecciones',) #exclude the field you put the inline on so you dont have double fields







admin.site.register(Proyeccion)
admin.site.register(Programa, ProgramaAdmin)

