import tiktoken

modelo = "gpt-4"
codificador = tiktoken.encoding_for_model(modelo)
lista_de_tokens = codificador.encode("Você é um categorizador de produtos.")
print(lista_de_tokens)
print(len(lista_de_tokens))
custo_entrada_gpt4 = (len(lista_de_tokens)/1000) * 0.03
print(f"\nCusto GPT4: {custo_entrada_gpt4}")

modelo = "gpt-3.5-turbo-1106"
codificador = tiktoken.encoding_for_model(modelo)
lista_de_tokens = codificador.encode("Você é um categorizador de produtos.")
print(lista_de_tokens)
print(len(lista_de_tokens))
custo_entrada_gpt3_5 = (len(lista_de_tokens)/1000) * 0.0010
print(f"\nCusto GPT3.5: {custo_entrada_gpt3_5}")
