from groq import Groq
import os



mordomo = """
                    Você tem a necessidade de guardar informações da empresa para que possam ser respondidas pelo nosso consumidor, tais como:
                    Onde vocês estão localizados? Somos uma loja virtual localizados em Foz do iguaçu.
                    Qual o telefone de contato? Clique aqui e entre em contato fale diretamente com um vendedor.
                    Produtos? Temos uma variedade de produtos, tais como: Cordyceps, Juba de Leão, Reishi, Chaga, Turkey Tail e Psilocybe Cubensis.
                    Qual o frete para minha cidade? Para calcular o frete para sua cidade, basta entrar na aba "frete" e inserir seu CEP. Isso permitirá que você obtenha uma estimativa precisa do custo de envio para sua localização.
                    Quais são os serviços? Trabalhamos com o envio de produtos a base de cogumelos medicinais para todo o Brasil

                    Não responda o que vier antes da resposta.
                    Se não houver uma respota coerente a pergunta você deve extreitamente responder, isso inclui se não entender a pergunta: Não tenho conhecimento sobre sua pergunta. Entre em contato com um vendedor pelo WhatsApp clicando no icone 

                    Resposta: Entre em contato com um vendedor pelo WhatsApp clicando no icone 

                    
                    """

conteudo = f"""Você trabalha para a empresa, cogumelos da fronteira. Nesta empresa vendemos Cordyceps, Juba de Leão, Reishi, Chaga, Turkey Tail e Psilocybe Cubensis, 
        Você deve responder exatamente como escrito em {mordomo}."""

pergunta = input('Digite pergunta: ')

client = Groq(api_key=os.environ.get("GROQ_API"))
stream = client.chat.completions.create(
    
            messages=[
                    {"role": "system", "content": conteudo},
                    {"role": "user", "content": pergunta},

                ],
    model="llama3-8b-8192",
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stop=None,
    stream=True,
)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:  # Only print if content is not None
        print(content, end='')