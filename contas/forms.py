from django import forms
from .models import ContaPagar


class ContaPagarForm(forms.ModelForm):
    class Meta:
        model = ContaPagar
        fields = ["nome", "valor", "tipo_conta", "detalhes"]
        widgets = {
            "detalhes": forms.Textarea(attrs={"rows": 3, "maxlength": 200}),
        }