from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import PerfilEmpresa, CustoEmpresa
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
    lista = empresa.custos.exclude(status="pago")
    return render(request, "empresas/custos.html", {"custos": lista})


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


@login_required
def custos_pagos(request):
    empresa, _ = PerfilEmpresa.objects.get_or_create(
        usuario=request.user,
        defaults={"cnpj": "", "razao_social": request.user.get_full_name() or request.user.username},
    )
    lista = empresa.custos.filter(status="pago")
    return render(request, "empresas/custos_pagos.html", {"lista": lista})


@login_required
def marcar_custo_pago(request, pk):
    if request.method == "POST":
        custo = get_object_or_404(CustoEmpresa, pk=pk, empresa__usuario=request.user)
        custo.status = "pago"
        custo.save()
    return redirect("empresas:custos")


@login_required
def excluir_custo(request, pk):
    if request.method == "POST":
        custo = get_object_or_404(CustoEmpresa, pk=pk, empresa__usuario=request.user)
        custo.delete()
    return redirect("empresas:custos")


@login_required
def marcar_custos_pagos_bulk(request):
    if request.method == "POST":
        ids = request.POST.getlist("selecionados")
        CustoEmpresa.objects.filter(pk__in=ids, empresa__usuario=request.user).update(status="pago")
    return redirect("empresas:custos")


@login_required
def excluir_custos_bulk(request):
    if request.method == "POST":
        ids = request.POST.getlist("selecionados")
        CustoEmpresa.objects.filter(pk__in=ids, empresa__usuario=request.user).delete()
    return redirect("empresas:custos")