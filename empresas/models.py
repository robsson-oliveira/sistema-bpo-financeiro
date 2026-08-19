from django.db import models
from django.contrib.auth.models import User
from datetime import date


class PerfilEmpresa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil_empresa")
    cnpj = models.CharField(max_length=14, unique=True)
    razao_social = models.CharField(max_length=150)

    def saldo_total_contas(self):
        return self.contas.aggregate(total=models.Sum("saldo_atual"))["total"] or 0

    def custo_mensal_total(self):
        return self.custos.filter(
            status__in=["pendente", "pago"]
        ).aggregate(total=models.Sum("valor"))["total"] or 0

    def cor_caixa(self):
        saldo_total = self.saldo_total_contas()
        custo_mensal = self.custo_mensal_total() or 1

        multiplo = saldo_total / custo_mensal

        if multiplo > 3:
            return "verde"
        elif multiplo >= 1.3:
            return "amarelo"
        else:
            return "vermelho"

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
    descricao = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    vencimento = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pendente")
    
    class Meta:
        ordering = ["vencimento"]

    def dias_para_vencer(self):
        return (self.vencimento - date.today()).days

    def cor_vencimento(self):
        dias = self.dias_para_vencer()
        if dias > 20:
            return "verde"
        elif dias >= 10:
            return "amarelo"
        else:
            return "vermelho"

    def __str__(self):
        return self.descricao