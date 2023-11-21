import os
import openai
import dotenv
import json

#
# *********************************************************
#  Desafio: Gerador de e-mails de recomendação de produtos
# *********************************************************
#
# 1. Identificar perfis a partir de uma lista de compras recentes por clientes
# 2. Para cada cliente:
#  2.1. Recomendar 3 produtos para o perfil a partir de uma lista de produtos
#  2.2. Escrever um e-mail de recomendação dos produtos escolhidos com até 3 parágrafos
#

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
  print("1. Iniciando identificação de perfis")
  prompt_sistema = """
  Identifique o perfil de compra para cada cliente a seguir.

  O formato de saída deve ser em JSON:

  {
    "clientes": [
      {
        "nome": "nome do cliente",
        "perfil": "descreva o perfil do cliente em 3 palavras"
      }
    ]
  } 
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
  json_resultado = json.loads(conteudo)
  print("Finalizou identificação de perfis")
  return json_resultado
    
def recomenda_produtos(perfil, lista_de_produtos):
  print("2. Iniciando recomendação de produtos")
  prompt_sistema = f"""
  Você é um recomendador de produtos.
  Considere o seguinte perfil: {perfil}
  Recomende 3 produtos a partir da lista de produtos válidos e que sejam adequados ao perfil informado.
  
  #### Lista de produtos válidos para recomendação
  {lista_de_produtos}

  A saída deve ser apenas o nome dos produtos recomendados em bullet points. 
  """

  resposta = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "system",
        "content": prompt_sistema
      }
    ]
  )

  conteudo = resposta.choices[0].message.content
  print("2. Finalizando a recomendação de produtos")
  return conteudo

def escreve_email(recomendacoes):
  print("3. Escrevendo e-mail de recomendação")
  prompt_sistema = f"""
   Escreva um e-mail recomendando os seguintes produtos para um cliente:
  
  {recomendacoes}
  
  O e-mail deve ter no máximo 3 parágrafos.
  O tom deve ser amigável, informal e descontraído.
  Trate o cliente como alguém próximo e conhecido. 
  """

  resposta = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "system",
        "content": prompt_sistema
      }
    ]
  )

  conteudo = resposta.choices[0].message.content
  print("3. Finalizando a escrita do e-mail")
  return conteudo

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
lista_de_produtos = carrega("./dados/lista_de_produtos.txt")
lista_de_compras_por_cliente = carrega("./dados/lista_de_compras_10_clientes.csv")
perfis = identifica_perfis(lista_de_compras_por_cliente)
for cliente in perfis["clientes"]:
    nome_do_cliente = cliente["nome"]
    print(f"Iniciando recomendação para o cliente {nome_do_cliente}")
    recomendacoes = recomenda_produtos(cliente["perfil"], lista_de_produtos)
    email = escreve_email(recomendacoes)
    salva(f"email-{nome_do_cliente}.txt", email)
