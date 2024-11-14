from flask import Flask, request, jsonify

# O seguinte modelo foi desenvolvido com tkinter onde manipulo o banco de dados igual um CRUD como exigido.
# Para testar o banco utilizei o DB Browser (SQLite).
# Para enviar as requisições JSON eu abri um servidor flask para receber tais requisições e servirem como API se posteriormente for necessário consumir.
# Deve-se criar uma venv com python -m venv myenv, entrar na venv com myenv/Scripts/activate e utilizar pip install -r requirements.txt para que tudo funcione.
# Com flask e tkinter rodando, basta apertar o botão de exportar JSON no tkinter ao apertar F5 em localhost:5000 o JSON aparecerá com os dados dos clientes que estão no banco.

app = Flask(__name__)

dados_recebidos = {'clientes': []} 

#servidor flask sem nome de rota, pode entrar como localhost:5000
#faço requesição post dos dados do tkinter, a aplicação fica escutando ate apertar o botao de exportar o json no tkinter
#os dados sao recebidos e adicionados em uma lista, retornando os respectivos clientes
#retorna os dados recebidos quando uma requisição GET é feita
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()  
        
        for entry in data:
            dados_recebidos['clientes'].append(entry)  
        
        print(data)  
        return jsonify({'status': 'sucesso', 'data': dados_recebidos}), 200  
    else:
        return jsonify(dados_recebidos), 200  
       

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)