"""Fin4All URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name="logout"),
    path('add_recommendation/<str:username>', views.add_recommendation, name='add_recommendation'),
    path('read_recommendation/<str:username>', views.read_recommendation, name='read_recommendation'),
    path('modify_portfolio/<str:username>', views.modify_portfolio, name='modify_portfolio'),
    path('read_portfolio/<str:username>', views.read_portfolio, name='read_portfolio'),
]
