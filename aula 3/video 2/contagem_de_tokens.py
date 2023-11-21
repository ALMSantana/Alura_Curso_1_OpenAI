import tiktoken

modelo = "gpt-4"
codificador = tiktoken.encoding_for_model(modelo)
lista_de_tokens = codificador.encode("Você é um categorizador de produtos.")
print(lista_de_tokens)
print(len(lista_de_tokens))
custo_entrada = (len(lista_de_tokens)/1000) * 0.0015
print(f"Custo: {custo_entrada}")

