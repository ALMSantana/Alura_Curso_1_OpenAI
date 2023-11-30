from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

def gera_recomendacoes(transacao):
    print("3. Gerando recomendações baseadas na transação")
    prompt_sistema = f"""
    Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes da transação da Transação: {transacao}

    As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-Fraude" ou "Realizar Verificação Manual".
    Elas devem ser escrito no formato técnico.

    Inclua também uma classificação do tipo de fraude, se aplicável. 
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
    print("Finalizou a geração de recomendação")
    return conteudo


# Carrega o dataset de transações
transacoes = carrega_csv("dados/transacoes.csv")
transacoes_avaliadas = analisar_transacao(transacoes)

# Gera recomendações para cada transação
for transacao in transacoes_avaliadas["transacoes"]:
    id_transacao = transacao["id"]
    produto_transacao = transacao["nome_produto"]
    status_transacao = transacao["status"]
    if status_transacao == "Possível Fraude":
        parecer = gera_parecer(transacao)
        recomendacao = gera_recomendacoes(parecer)
        salva(f"transacao-{id_transacao}-{produto_transacao}-{status_transacao}.txt", recomendacao)

