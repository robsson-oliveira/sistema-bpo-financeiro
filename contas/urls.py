from django.urls import path
from . import views

app_name = 'contas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('contas-a-pagar/', views.contas_a_pagar, name='contas_a_pagar'),
    path('contas-a-pagar/adicionar/', views.adicionar_conta_a_pagar, name='adicionar_conta_a_pagar'),
    path('contas-a-pagar/pagar-em-massa/', views.marcar_contas_pagas_bulk, name='marcar_contas_pagas_bulk'),
    path('contas-a-pagar/excluir-em-massa/', views.excluir_contas_bulk, name='excluir_contas_bulk'),
    path('contas-a-pagar/reordenar/', views.reordenar_contas, name='reordenar_contas'),
    path('contas-pagas/', views.contas_pagas, name='contas_pagas'),
]