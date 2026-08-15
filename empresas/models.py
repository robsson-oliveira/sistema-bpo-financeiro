from django.db import models
from django.contrib.auth.models import User


class PerfilEmpresa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil_empresa")
    cnpj = models.CharField(max_length=14, unique=True)
    razao_social = models.CharField(max_length=150)

    def __str__(self):
        return self.razao_social


class ContaBancariaEmpresa(models.Model):
    BANCO_CHOICES = [
        ("nubank", "Nubank"),
        ("bb", "Banco do Brasil"),
        ("itau", "Itaú"),
    ]
    empresa = models.ForeignKey(PerfilEmpresa, on_delete=models.CASCADE, related_name="contas")
    banco = models.CharField(max_length=20, choices=BANCO_CHOICES)
    pluggy_account_id = models.CharField(max_length=100, unique=True)
    saldo_atual = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("empresa", "banco")


class CustoEmpresa(models.Model):
    CATEGORIA_CHOICES = [
        ("aluguel", "Aluguel"),
        ("fornecedor", "Fornecedor"),
        ("salario", "Salário"),
        ("outro", "Outro"),
    ]
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("pago", "Pago"),
        ("vencido", "Vencido"),
    ]
    empresa = models.ForeignKey(PerfilEmpresa, on_delete=models.CASCADE, related_name="custos")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    descricao = models.CharField(max_length=150)  # ex: "Aluguel sede", "Fornecedor X"
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    vencimento = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pendente")

    class Meta:
        ordering = ["vencimento"]

def cor_caixa(empresa):
    saldo_total = empresa.contas.aggregate(total=models.Sum("saldo_atual"))["total"] or 0
    custo_mensal = empresa.custos.filter(
        status__in=["pendente", "pago"]
    ).aggregate(total=models.Sum("valor"))["total"] or 1  # evita divisão por zero

    multiplo = saldo_total / custo_mensal

    if multiplo > 3:
        return "verde"
    elif multiplo >= 1.3:
        return "amarelo"
    else:
        return "vermelho"