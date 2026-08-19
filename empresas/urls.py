from django.urls import path
from . import views

app_name = 'empresas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('custos/', views.custos, name='custos'),
    path('custos/adicionar/', views.adicionar_custo, name='adicionar_custo'),
]