from django import forms
from .models import CustoEmpresa


class CustoEmpresaForm(forms.ModelForm):
    class Meta:
        model = CustoEmpresa
        fields = ["descricao", "categoria", "valor", "vencimento"]
        widgets = {
            "vencimento": forms.DateInput(attrs={"type": "date"}),
        }