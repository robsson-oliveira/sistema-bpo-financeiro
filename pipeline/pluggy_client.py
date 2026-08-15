import time

import requests
from decouple import config

PLUGGY_BASE_URL = "https://api.pluggy.ai"


def obter_api_key() -> str:
    """Autentica com CLIENT_ID/SECRET e retorna a API key temporaria da Pluggy."""
    resposta = requests.post(
        f"{PLUGGY_BASE_URL}/auth",
        json={
            "clientId": config("PLUGGY_CLIENT_ID"),
            "clientSecret": config("PLUGGY_CLIENT_SECRET"),
        },
    )
    resposta.raise_for_status()
    return resposta.json()["apiKey"]


def listar_conectores(api_key: str) -> list:
    """Lista os bancos/conectores disponiveis no sandbox (ex: Nubank, BB, Itau simulados)."""
    resposta = requests.get(
        f"{PLUGGY_BASE_URL}/connectors",
        headers={"X-API-KEY": api_key},
        params={"sandbox": "true"},
    )
    resposta.raise_for_status()
    return resposta.json()["results"]


def listar_contas(api_key: str, item_id: str) -> list:
    """Retorna as contas (saldos) de uma conexao ja autorizada (item_id)."""
    resposta = requests.get(
        f"{PLUGGY_BASE_URL}/accounts",
        headers={"X-API-KEY": api_key},
        params={"itemId": item_id},
    )
    resposta.raise_for_status()
    return resposta.json()["results"]

def criar_item_teste(api_key: str, connector_id: int) -> str:
    """Cria uma conexao de teste (fake bank), retorna o item_id."""
    resposta = requests.post(
        f"{PLUGGY_BASE_URL}/items",
        headers={"X-API-KEY": api_key},
        json={
            "connectorId": connector_id,
            "parameters": {
                "user": "user-ok",
                "password": "password-ok",
            },
        },
    )
    resposta.raise_for_status()
    return resposta.json()["id"]

def criar_item_teste(api_key: str, connector_id: int) -> str:
    """Cria uma conexao de teste (fake bank), retorna o item_id."""
    resposta = requests.post(
        f"{PLUGGY_BASE_URL}/items",
        headers={"X-API-KEY": api_key},
        json={
            "connectorId": connector_id,
            "parameters": {
                "user": "user-ok",
                "password": "password-ok",
            },
        },
    )
    resposta.raise_for_status()
    return resposta.json()["id"]

def obter_status_item(api_key: str, item_id: str) -> dict:
    """Retorna o status atual do item (UPDATING, UPDATED, LOGIN_ERROR, etc)."""
    resposta = requests.get(
        f"{PLUGGY_BASE_URL}/items/{item_id}",
        headers={"X-API-KEY": api_key},
    )
    resposta.raise_for_status()
    return resposta.json()


def aguardar_item_pronto(api_key: str, item_id: str, tentativas: int = 15, intervalo: int = 4) -> dict:
    """Faz polling no item ate ele ficar pronto (UPDATED) ou dar erro."""
    for tentativa in range(tentativas):
        item = obter_status_item(api_key, item_id)
        status = item["status"]
        print(f"  tentativa {tentativa + 1}: status = {status}")

        if status == "UPDATED":
            return item
        if status in ("LOGIN_ERROR", "OUTDATED", "ERROR"):
            raise Exception(f"Item falhou com status {status}: {item.get('error')}")

        time.sleep(intervalo)

    raise TimeoutError("Item nao ficou pronto a tempo")