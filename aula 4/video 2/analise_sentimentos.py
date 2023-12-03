import openai
from openai import *
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(api_key="")
modelo = "gpt-4"

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def analise_sentimento(nome_do_produto):
    prompt_sistema = """
    Você é um analisador de sentimentos de avaliações de produtos.
    Escreva um parágrafo com até 50 palavras resumindo as avaliações e depois atribua qual o sentimento geral para o produto.
    Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

    #### Formato de saída

    Nome do produto: 
    Resumo das avaliações:
    Sentimento geral: [aqui deve ser POSITIVO, NEUTRO ou NEGATIVO]
    Pontos fortes: [3 bullet points]
    Pontos fracos: [3 bullet points]
    """

    prompt_usuario = carrega(f"./dados/avaliacoes-{nome_do_produto}.txt")
    print(f"Iniciando a análise do produto: {nome_do_produto}")

    try:
        resposta = client.completions.create(
            prompt="Hello world",
            model="gpt-3.5-turbo-instruct"
        )
        # resposta = openai.ChatCompletion.create(
        #    model = "gpt-3.5-turbo",
        #    messages = [
        #        {
        #            "role": "system",
        #            "content": prompt_sistema
        #        },
        #        {
        #            "role": "user",
        #            "content": prompt_usuario
        #        }
        #   ]
        # )

        salva(f"./dados/analise-{nome_do_produto}", resposta.choices[0].message.content)
        print("Análise concluída com sucesso!")
    except openai.AuthenticationError as e:
        print(f"Erro de autenticacao: {e}")
    except openai.APIError as e:
        print(f"Erro de API: {e}")
        time.sleep(5)

lista_de_produtos = ["Camisetas de algodão orgânico", "Jeans feitos com materiais reciclados"]
for nome_do_produto in lista_de_produtos:
    analise_sentimento(nome_do_produto)
