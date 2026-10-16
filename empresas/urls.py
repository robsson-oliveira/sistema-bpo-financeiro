from django.urls import path
from . import views

app_name = 'empresas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('custos/', views.custos, name='custos'),
    path('custos/adicionar/', views.adicionar_custo, name='adicionar_custo'),
    path('custos/pagar-em-massa/', views.marcar_custos_pagos_bulk, name='marcar_custos_pagos_bulk'),
    path('custos/excluir-em-massa/', views.excluir_custos_bulk, name='excluir_custos_bulk'),
    path('custos-pagos/', views.custos_pagos, name='custos_pagos'),
]