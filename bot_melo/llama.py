from ollama import Client

mordomo = """
            Você tem a necessidade de guardar informações da empresa para que possam ser respondidas pelo nosso consumidor, tais como:
            Onde vocês estão localizados? -Estamos localizados em Fóz do iguaçu.
            Qual o telefone de contato? -O telefone de contato é 21 11123-4678
            Quais produtos da loja? -Temos uma variedade de produtos, tais como: Cordyceps, Juba de Leão, Reishi, Chaga, Turkey Tail e heitor
            Qual o frete para minha cidade? -Entre na aba frete e calcule seu frete utilizando seu cep.

            nao responda o que vier antes da resposta.
            """

conteudo = f"""Você trabalha para a empresa, cogumelos da fronteira. Nesta empresa vendemos Cordyceps, Juba de Leão, Reishi, Chaga, Turkey Tail e Psilocybe Cubensis, 
Você deve responder exatamente como está escrito em {mordomo}, nao mude nenhuma frase e nao respota nada antes de -."""

pergunta = input("Digite sua pergunta: ")

proxies = {
            'http://': None,
            'https://': None
        }

client = Client(host='http://localhost:11434', proxies=proxies)
chat_completion = client.chat(
    
    messages=[
            {"role": "system", "content": conteudo},
            {"role": "user", "content": pergunta},
            {"role": "assistant", "content": mordomo}
        ],
    model="llama3.1",
)

print(chat_completion['message'])
