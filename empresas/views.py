from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import PerfilEmpresa
from .forms import CustoEmpresaForm


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


@login_required
def adicionar_custo(request):
    empresa, _ = PerfilEmpresa.objects.get_or_create(
        usuario=request.user,
        defaults={"cnpj": "", "razao_social": request.user.get_full_name() or request.user.username},
    )

    if request.method == "POST":
        form = CustoEmpresaForm(request.POST)
        if form.is_valid():
            custo = form.save(commit=False)
            custo.empresa = empresa
            custo.save()
            return redirect("empresas:custos")
    else:
        form = CustoEmpresaForm()

    return render(request, "empresas/adicionar_custo.html", {"form": form})