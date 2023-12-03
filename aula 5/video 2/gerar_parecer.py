from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

def gera_parecer(transacao):
    print("2. Gerando parecer para transacao ", transacao["id"])
    prompt_sistema = f"""
    Para a seguinte transação, forneça um parecer, apenas se o status dela for de "Possível Fraude". Indique no parecer uma justificativa para que você identifique uma fraude.
    Transação: {transacao}

    ## Formato de Resposta
    "id": "id",
    "tipo": "crédito ou débito",
    "estabelecimento": "nome do estabelecimento",
    "horário": "horário da transação",
    "valor": "R$XX,XX",
    "nome_produto": "nome do produto",
    "localização": "cidade - estado (País)"
    "status": "",
    "parecer" : "Colocar Não Aplicável se o status for Aprovado"
    """

    lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        }
    ]

    resposta = client.chat.completions.create(
        messages = lista_mensagens,
        model=modelo,
    )

    conteudo = resposta.choices[0].message.content
    print("Finalizou a geração de parecer")
    return conteudo