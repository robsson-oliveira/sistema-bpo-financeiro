from django.db import models


class SincronizacaoPluggy(models.Model):
    STATUS_CHOICES = [
        ("sucesso", "Sucesso"),
        ("erro", "Erro"),
    ]
    executado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    contas_atualizadas = models.IntegerField(default=0)
    mensagem_erro = models.TextField(blank=True, null=True)


class SaldoHistorico(models.Model):
    """Tabela fato: snapshot diario de saldo, serve pra grafico de evolucao."""
    ORIGEM_CHOICES = [
        ("pessoal", "Pessoal"),
        ("empresa", "Empresa"),
    ]
    origem = models.CharField(max_length=10, choices=ORIGEM_CHOICES)
    conta_id = models.IntegerField()  # referencia ContaBancaria ou ContaBancariaEmpresa
    data_referencia = models.DateField()
    saldo = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        unique_together = ("origem", "conta_id", "data_referencia")