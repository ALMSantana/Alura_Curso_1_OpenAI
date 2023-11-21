from openai import OpenAI
from dotenv import load_dotenv
import os

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

def analisar_transacao(lista_de_transacoes):
  prompt_sistema = """
  Identifique se uma transação é fraudulenta ou não, no sample de dados do usuário.

  O formato de saída deve ser:

  Produto: {valor} - Horário - Cidade/Estado (País) - Estabelecimento Comercial: {nome do estabelecimento} [Status]

  O status pode ser: Possível Fraude ou Aprovada
  """

  lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": lista_de_transacoes
        }
    ]

  resposta = client.chat.completions.create(
      messages = lista_mensagens,
      model=modelo
  )

lista_de_transacoes = carrega("./dados/lista_de_compras_10_clientes.csv")
analisar_transacao(lista_de_transacoes)
