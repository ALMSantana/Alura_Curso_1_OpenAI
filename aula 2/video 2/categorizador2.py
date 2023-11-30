from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI()
modelo = "gpt-4"

prompt_sistema = """
    Você é um categorizador de produtos.
    Você deve assumir as categorias presentes na lista abaixo.

    # Lista de Categorias Válidas
    - Moda Sustentável
    - Produtos para o Lar
    - Beleza Natural
    - Eletrônicos Verdes

    # Formato da Saída
    Produto: Nome do Produto
    Categoria: apresente a categoria do produto

    # Exemplo de Saída
    Produto: Escova elétrica com recarga solar
    Categoria: Eletrônicos Verdes
"""

print("Informe um novo produto: ")
prompt_usuario = input()

resposta = cliente.chat.completions.create(
    messages=
    [
        {
            "role": "system",
            "content" : prompt_sistema
        },
        {
            "role": "user",
            "content" : prompt_usuario
        }
    ],
    model=modelo,
    temperature=0.5,
    max_tokens=300,
    frequency_penalty=1.0
)

print(resposta.choices[0].message.content)