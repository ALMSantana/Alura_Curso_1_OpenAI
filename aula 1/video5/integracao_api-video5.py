from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

lista_mensagens = [
                {
                    "role": "system",
                    "content": "Gere nomes de produtos fictícios sem descrição de acordo com a requisição do usuário."
                },
                {
                    "role": "user",
                    "content": "Gere 5 produtos"
                }
            ]

resposta = client.chat.completions.create(
    messages = lista_mensagens,
    model=modelo,
)

print(resposta)
