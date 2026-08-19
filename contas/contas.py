from django.urls import path
from . import views

app_name = 'contas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]