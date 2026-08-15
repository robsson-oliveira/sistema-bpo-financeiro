import os
import time
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from pipeline.pluggy_client import obter_api_key, criar_item_teste, aguardar_item_pronto, listar_contas

api_key = obter_api_key()
print("API KEY OBTIDA:", api_key[:20], "...")

item_id = criar_item_teste(api_key, connector_id=2)
print("ITEM CRIADO:", item_id)

print("Aguardando sincronizacao (polling)...")
aguardar_item_pronto(api_key, item_id)

contas = listar_contas(api_key, item_id)
print(f"\n{len(contas)} contas encontradas:")
for c in contas:
    print(f"- {c['name']} | saldo: {c['balance']} | tipo: {c['type']}")