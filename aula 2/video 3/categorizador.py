from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI()
modelo = "gpt-4"

def categoriza_produtos(nome_produto, lista_categorias_validas):
    print(lista_categorias_validas)
    prompt_sistema = f"""
        Você é um categorizador de produtos.
        Você deve assumir as categorias presentes na lista abaixo.

        # Lista de Categorias Válidas
        {lista_categorias_validas.split(",")}

        # Formato da Saída
        Produto: Nome do Produto
        Categoria: apresente a categoria do produto

        # Exemplo de Saída
        Produto: Escova elétrica com recarga solar
        Categoria: Eletrônicos Verdes
    """

    print(prompt_sistema)

    resposta = cliente.chat.completions.create(
        messages=
        [
            {
                "role": "system",
                "content" : prompt_sistema
            },
            {
                "role": "user",
                "content" : nome_produto
            }
        ],
        model=modelo,
        temperature=0.5,
        max_tokens=300,
        frequency_penalty=1.0
    )

    print(resposta.choices[0].message.content)

categorias_validas = input("Digite as categorias válidas: ")

while(True):
    nome_produto = input("Digite o nome de um produto: ")
    categoriza_produtos(nome_produto, categorias_validas)