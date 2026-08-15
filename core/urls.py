from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('contas/', include('contas.urls')),
    path('empresas/', include('empresas.urls')),
    path('', home),
]