import os
import openai
import dotenv

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

def identifica_perfis(lista_de_compras_por_cliente):
  prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
  """

  resposta = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "system",
        "content": prompt_sistema
      },
      {
        "role": "user",
        "content": lista_de_compras_por_cliente
      }
    ]
  )

  conteudo = resposta.choices[0].message.content
  return conteudo
    

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

lista_de_compras_por_cliente = carrega("./dados/lista_de_compras_10_clientes.csv")
identifica_perfis(lista_de_compras_por_cliente)
