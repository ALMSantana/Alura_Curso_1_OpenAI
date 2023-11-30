from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

cliente = OpenAI()
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

def analise_sentimento(nome_produto):
    prompt_sistema = f"""
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

        # Formato de Saída

        Nome do Produto:
        Resumo das Avaliações:
        Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Ponto fortes: lista com três bullets
        Pontos fracos: lista com três bullets
    """

    prompt_usuario = carrega(f"./dados/avaliacoes-{nome_produto}.txt")
    print(f"Inicou a análise de sentimentos do produto {nome_produto}")

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

    resposta = cliente.chat.completions.create(
            messages = lista_mensagens,
            model=modelo
        )

    texto_resposta = resposta.choices[0].message.content
    salva(f"./dados/analise-{nome_produto}.txt", texto_resposta)

lista_produtos = ["Camisetas de algodão orgânico", "Maquiagem mineral"]
for nome_produto in lista_produtos:
    analise_sentimento(nome_produto)