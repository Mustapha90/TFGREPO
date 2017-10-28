"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
#from festivalapp.views import getdatos
from django.contrib.auth.views import (
    password_change,
    password_change_done,
)


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/festivalapp/')),
    url(r'^festivalapp/', include('festivalapp.urls')),
    url(r'^admin/', admin.site.urls),
   # url(r'^login/$', auth_views.login,{'extra_context':{'datos': getdatos()}}, name='login'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^accounts/password/change/$', password_change, {
        'template_name': 'registration/password_change_form.html'}, 
        name='password_change'),
    url(r'^accounts/password/change/done/$', password_change_done, 
        {'template_name': 'registration/password_change_done.html'},
        name='password_change_done'),

    url(r'^logout/$', auth_views.logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




