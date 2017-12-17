"""mankatoexpenses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.urls import path
from django.conf.urls import url, include
from expenses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index, name = 'index'),
    url(r'^index/$', views.index, name = 'index'),
    url(r'^edit/$', views.edit),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$',views.login_user, name='login'),
    #url(r'^logout/$', views.logoutUser, name='logout'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^transaction/$', views.transaction, name='transaction'),
]
