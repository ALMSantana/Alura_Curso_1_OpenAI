from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import pandas as pd

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

# *********************************************************
#  Desafio: Avaliar se uma transação financeira é fraudulenta ou não
# *********************************************************

def carrega_csv(nome_do_arquivo):
    try:
        return pd.read_csv(nome_do_arquivo)
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")
        return None
    
def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def analisar_transacao(lista_de_transacoes):
    print("1. Iniciando a avaliação de transações")
    prompt_sistema = """
    Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada". 
    Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

    Cada nova transação deve ser inserida dentro da lista do JSON. Adote o formato de resposta abaixo.

    # Formato Saída 
    {
        "transacoes": [
            {
            "id": "id",
            "tipo": "crédito ou débito",
            "estabelecimento": "nome do estabelecimento",
            "horario": "horário da transação",
            "valor": "R$XX,XX",
            "nome_produto": "nome do produto",
            "localizacao": "cidade - estado (País)"
            "status": ""
            },
        ]
    } 
    """

    lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": f"Considere o CSV abaixo, onde cada linha é uma transação diferente: {lista_de_transacoes}. Sua resposta deve adotar o #Formato de Resposta (apeans um json sem outros comentários)"
        }
    ]

    resposta = client.chat.completions.create(
        messages = lista_mensagens,
        model=modelo,
        temperature=0
    )

    conteudo = resposta.choices[0].message.content.replace("'", '"')
    print("\Conteúdo:", conteudo)
    json_resultado = json.loads(conteudo)
    print("\nJSON:", json_resultado)
    return json_resultado

def gera_parecer(transacao):
    print("2. Gerando parecer para transacao ", transacao["id"])
    prompt_sistema = f"""
    Para a seguinte transação, forneça um parecer, apenas se o status dela for de "Possível Fraude". Indique no parecer uma justificativa para que você identifique uma fraude.
    Transação: {transacao}

    ## Formato de Resposta
    "id": "id",
    "tipo": "crédito ou débito",
    "estabelecimento": "nome do estabelecimento",
    "horario": "horário da transação",
    "valor": "R$XX,XX",
    "nome_produto": "nome do produto",
    "localizacao": "cidade - estado (País)"
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


