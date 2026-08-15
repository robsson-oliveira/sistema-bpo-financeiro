from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import PerfilEmpresa


@login_required
def dashboard(request):
    empresa, _ = PerfilEmpresa.objects.get_or_create(
        usuario=request.user,
        defaults={"cnpj": "", "razao_social": request.user.get_full_name() or request.user.username},
    )

    contexto = {
        "empresa": empresa,
        "saldo_total": empresa.saldo_total_contas(),
        "custo_mensal": empresa.custo_mensal_total(),
        "cor_caixa": empresa.cor_caixa(),
    }
    return render(request, "empresas/dashboard.html", contexto)


@login_required
def custos(request):
    empresa, _ = PerfilEmpresa.objects.get_or_create(
        usuario=request.user,
        defaults={"cnpj": "", "razao_social": request.user.get_full_name() or request.user.username},
    )
    return render(request, "empresas/custos.html", {"custos": empresa.custos.all()})