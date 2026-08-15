from django.db import models
from django.contrib.auth.models import User


class PerfilPessoal(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil_pessoal")
    cpf = models.CharField(max_length=11, unique=True)
    imagem_fundo = models.URLField(blank=True, null=True)
    fonte_escolhida = models.CharField(max_length=50, default="Inter")

    def saldo_total_contas(self):
        return self.contas.aggregate(total=models.Sum("saldo_atual"))["total"] or 0

    def total_a_receber(self):
        return self.entradas.filter(recebido=False).aggregate(total=models.Sum("valor"))["total"] or 0

    def poupanca_do_mes(self, mes_referencia):
        poupanca = self.poupancas.filter(mes_referencia=mes_referencia).first()
        return poupanca.valor_guardado if poupanca else 0

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username


class ContaBancaria(models.Model):
    BANCO_CHOICES = [
        ("nubank", "Nubank"),
        ("bb", "Banco do Brasil"),
        ("itau", "Itaú"),
    ]
    perfil = models.ForeignKey(PerfilPessoal, on_delete=models.CASCADE, related_name="contas")
    banco = models.CharField(max_length=20, choices=BANCO_CHOICES)
    pluggy_account_id = models.CharField(max_length=100, unique=True)
    saldo_atual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("perfil", "banco")


class EntradaPrevista(models.Model):
    perfil = models.ForeignKey(PerfilPessoal, on_delete=models.CASCADE, related_name="entradas")
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_prevista = models.DateField()
    recebido = models.BooleanField(default=False)


class Poupanca(models.Model):
    perfil = models.ForeignKey(PerfilPessoal, on_delete=models.CASCADE, related_name="poupancas")
    mes_referencia = models.DateField()  # sempre dia 1 do mes, ex: 2026-08-01
    valor_guardado = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ("perfil", "mes_referencia")

