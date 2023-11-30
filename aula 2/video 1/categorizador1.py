from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI()
modelo = "gpt-4"

resposta = cliente.chat.completions.create(
    messages=[
        {
            "role":"system",
            "content":"Classifique o produto abaixo em uma das categorias: Higiene Pessoal, Moda ou Casa e de uma descrição da categoria."
        },
        {
            "role":"user",
            "content":"Escova de dentes de bambu"
        }
    ],
    model=modelo,
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    n=3
)

for contador in range(0,3):
    print(resposta.choices[contador].message.content)