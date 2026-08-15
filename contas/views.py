from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import PerfilPessoal


@login_required
def dashboard(request):
    perfil, _ = PerfilPessoal.objects.get_or_create(
        usuario=request.user,
        defaults={"cpf": ""},
    )

    hoje = date.today().replace(day=1)  # primeiro dia do mes atual

    contexto = {
        "saldo_contas": perfil.saldo_total_contas(),
        "total_a_receber": perfil.total_a_receber(),
        "poupanca_mes": perfil.poupanca_do_mes(hoje),
    }
    return render(request, "contas/dashboard.html", contexto)