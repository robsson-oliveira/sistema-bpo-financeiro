from django.urls import path
from . import views

app_name = 'empresas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('custos/', views.custos, name='custos'),
    path('custos/adicionar/', views.adicionar_custo, name='adicionar_custo'),
    path('custos/<int:pk>/pagar/', views.marcar_custo_pago, name='marcar_custo_pago'),
    path('custos/<int:pk>/excluir/', views.excluir_custo, name='excluir_custo'),
    path('custos-pagos/', views.custos_pagos, name='custos_pagos'),
    path('custos/pagar-em-massa/', views.marcar_custos_pagos_bulk, name='marcar_custos_pagos_bulk'),
    path('custos/excluir-em-massa/', views.excluir_custos_bulk, name='excluir_custos_bulk'),
]   