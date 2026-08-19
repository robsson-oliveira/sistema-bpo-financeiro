import json
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import PerfilPessoal, ContaPagar
from .forms import ContaPagarForm

@login_required
def contas_a_pagar(request):
    perfil, _ = PerfilPessoal.objects.get_or_create(usuario=request.user, defaults={"cpf": ""})
    lista = perfil.contas_pagar.filter(status="pendente")
    return render(request, "contas/contas_a_pagar.html", {"lista": lista})


@login_required
def adicionar_conta_a_pagar(request):
    perfil, _ = PerfilPessoal.objects.get_or_create(usuario=request.user, defaults={"cpf": ""})

    if request.method == "POST":
        form = ContaPagarForm(request.POST)
        if form.is_valid():
            conta = form.save(commit=False)
            conta.perfil = perfil
            conta.prioridade = perfil.contas_pagar.filter(status="pendente").count()
            conta.save()
            return redirect("contas:contas_a_pagar")
    else:
        form = ContaPagarForm()

    return render(request, "contas/adicionar_conta.html", {"form": form})


@login_required
def contas_pagas(request):
    perfil, _ = PerfilPessoal.objects.get_or_create(usuario=request.user, defaults={"cpf": ""})
    lista = perfil.contas_pagar.filter(status="paga")
    return render(request, "contas/contas_pagas.html", {"lista": lista})


@login_required
def reordenar_contas(request):
    if request.method == "POST":
        dados = json.loads(request.body)
        for indice, conta_id in enumerate(dados.get("ordem", [])):
            ContaPagar.objects.filter(pk=conta_id, perfil__usuario=request.user).update(prioridade=indice)
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False}, status=400)


@login_required
def dashboard(request):
    perfil, _ = PerfilPessoal.objects.get_or_create(usuario=request.user, defaults={"cpf": ""})
    hoje = date.today().replace(day=1)

    contexto = {
        "saldo_contas": perfil.saldo_total_contas(),
        "total_contas_pagar": perfil.total_contas_a_pagar(),
        "poupanca_mes": perfil.poupanca_do_mes(hoje),
    }
    return render(request, "contas/dashboard.html", contexto)


@login_required
def marcar_contas_pagas_bulk(request):
    if request.method == "POST":
        ids = request.POST.getlist("selecionados")
        ContaPagar.objects.filter(pk__in=ids, perfil__usuario=request.user).update(status="paga")
    return redirect("contas:contas_a_pagar")


@login_required
def excluir_contas_bulk(request):
    if request.method == "POST":
        ids = request.POST.getlist("selecionados")
        ContaPagar.objects.filter(pk__in=ids, perfil__usuario=request.user).delete()
    return redirect("contas:contas_a_pagar")