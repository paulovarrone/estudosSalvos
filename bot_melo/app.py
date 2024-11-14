import os
from groq import Groq
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify


load_dotenv()

app = Flask(__name__)

@app.route('/chat')
def ajuda():
    return render_template('chat.html')


@app.route('/resposta', methods=['POST'])
def resposta():
    try:
        wpp = "https://wa.me/5545991129701"

        mordomo = f"""
                    Você tem a necessidade de guardar informações da empresa para que possam ser respondidas pelo nosso consumidor, tais como:
                    Onde vocês estão localizados? Somos uma loja virtual localizados em Foz do iguaçu.
                    Qual o telefone de contato? Clique aqui e entre em contato <a href="{wpp}" target="_blank"><img class="wpp" src="../static/img/wpp.png" alt=""></a> fale diretamente com um vendedor.
                    Produtos? Temos uma variedade de produtos, tais como: Cordyceps, Juba de Leão, Reishi, Chaga, Turkey Tail e Psilocybe Cubensis.
                    Qual o frete para minha cidade? Para calcular o frete para sua cidade, basta entrar na aba "frete" e inserir seu CEP. Isso permitirá que você obtenha uma estimativa precisa do custo de envio para sua localização.
                    Quais são os serviços? Trabalhamos com o envio de produtos a base de cogumelos medicinais para todo o Brasil

                    Não responda o que vier antes da resposta.
                    Se não houver uma respota coerente a pergunta você deve extreitamente responder, isso inclui se não entender a pergunta: Não tenho conhecimento sobre sua pergunta. Entre em contato com um vendedor pelo WhatsApp clicando no icone <a href="{wpp}" target="_blank"><img class="wpp" src="../static/img/wpp.png" alt=""></a> 

                    Resposta: Entre em contato com um vendedor pelo WhatsApp clicando no icone <a href="{wpp}" target="_blank"><img class="wpp" src="../static/img/wpp.png" alt=""></a> 

                    
                    """

        conteudo = f"""Você trabalha para a empresa, cogumelos da fronteira. Nesta empresa vendemos Cordyceps, Juba de Leão, Reishi, Chaga, Turkey Tail e Psilocybe Cubensis, 
        Você deve responder exatamente como escrito em {mordomo}."""

        pergunta = request.form['pergunta']


        client = Groq(api_key=os.environ.get("GROQ_API"))

        chat_completion = client.chat.completions.create(
            
            messages=[
                    {"role": "system", "content": conteudo},
                    {"role": "user", "content": pergunta},
                    {"role": "assistant", "content": mordomo}
                ],
            model="llama-3.1-70b-versatile",
            temperature=0,
            max_tokens=1024,
            top_p=1,
            stop=None
        )



        resposta = chat_completion.choices[0].message.content

        return jsonify({
            "pergunta": pergunta,
            "resposta": resposta
        })
    except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
