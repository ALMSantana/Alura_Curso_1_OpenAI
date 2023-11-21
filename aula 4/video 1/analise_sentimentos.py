from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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

nome_do_produto = "Tapete de yoga"

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

lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": prompt_usuario
        }
    ]

resposta = client.chat.completions.create(
    messages = lista_mensagens,
    model=modelo
)

salva(f"./dados/analise-{nome_do_produto}", resposta.choices[0].message.content)
