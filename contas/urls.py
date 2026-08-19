from django.urls import path
from . import views

app_name = 'contas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('contas-a-pagar/', views.contas_a_pagar, name='contas_a_pagar'),
    path('contas-a-pagar/adicionar/', views.adicionar_conta_a_pagar, name='adicionar_conta_a_pagar'),
    path('contas-a-pagar/<int:pk>/pagar/', views.marcar_conta_paga, name='marcar_conta_paga'),
    path('contas-a-pagar/<int:pk>/excluir/', views.excluir_conta, name='excluir_conta'),
    path('contas-a-pagar/reordenar/', views.reordenar_contas, name='reordenar_contas'),
    path('contas-pagas/', views.contas_pagas, name='contas_pagas'),
]