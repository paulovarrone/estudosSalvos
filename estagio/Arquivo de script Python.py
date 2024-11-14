from tkinter import *
from tkinter import messagebox
import sqlite3
import requests

# O seguinte modelo foi desenvolvido com tkinter onde manipulo o banco de dados igual um CRUD como exigido.
# Para testar o banco utilizei o DB Browser (SQLite).
# Para enviar as requisições JSON eu abri um servidor flask para receber tais requisições e servirem como API se posteriormente for necessário consumir.
# Deve-se criar uma venv com python -m venv myenv, entrar na venv com myenv/Scripts/activate e utilizar pip install -r requirements.txt para que tudo funcione.
# Com flask e tkinter rodando, basta apertar o botão de exportar JSON no tkinter ao apertar F5 em localhost:5000 o JSON aparecerá com os dados dos clientes que estão no banco.

#utilizando funções para organizar o codigo.

#função de conexao com o banco de dados
#utilizei o DB Bowser for SQLite para vizualisar os dados no banco de dados.
#em todas as funções utilizo conexao.close() para que não deixar conexões abertas, liberar recursos na cpu e evitar deadlocks
def conexao_db():
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()
    return conexao, cursor

#função de adicionar cliente, onde passo como parametro os camos que serão inseridos no tkinter.
#usando o .get() eu consigo extrair os dados que o usuário escreve.
#faço e executo as query's, mostro uma mensagem de confirmação e deleto os campos escritos anteriormente pelo usuário do programa.
#checagem de campos nulos, não permitir o cadastro se houver, todos os campos devem ser preenchidos.
#checagem de erro, se houver erro na conexao com banco, inserção de dados entre outros erros, o programa exibira uma mensagem de erro.
#se não houver erros uma mensagem de sucesso será mostrada ao usuário
def adicionar_db(nome_entry, telefone_entry, email_entry, cpf_entry):
    try:
        conexao, cursor = conexao_db()

        nome = nome_entry.get()
        telefone = telefone_entry.get()
        email = email_entry.get()
        cpf = cpf_entry.get()

        if any(campo == '' for campo in[nome,telefone,email,cpf]):
            messagebox.showerror('ERRO', 'OS CAMPOS NÃO PODEM ESTAR VAZIOS!')
        else:
            query = 'INSERT INTO clientes(nome, telefone, email,cpf) VALUES(?,?,?,?)'
            dados = (nome,telefone,email,cpf)

            cursor.execute(query,dados)
            cursor.execute('commit')

            for deletar in [nome_entry, telefone_entry, email_entry, cpf_entry]:
                deletar.delete(0, END)

            messagebox.showinfo('SUCESSO', 'Cliente cadastrado com sucesso!')

    except Exception as e:
        messagebox.showerror('ERRO', f'CLIENTE NÃO PODE SER CADASTRADO! {str(e)}')

    finally:
        conexao.close()

#função que executa uma query onde seleciona todos os clientes e seus dados do banco.
#mostro todos os dados do cliente em uma listbox.
#se houver algum erro de conexao com o banco ou erro ao recuperar os dados, uma aviso é mostrado na tela.
#se não houver erros uma mensagem de sucesso será mostrada ao usuário
def select_db(lista_db):
    try:
        conexao, cursor = conexao_db()
        query = 'SELECT * FROM clientes'

        cursor.execute(query)

        dados = cursor.fetchall()
        lista_db.delete(0, END)


        for dado in dados:
            lista_db.insert(END, f'Nome: {dado[0]} - Telefone: {dado[1]} - Email: {dado[2]} - CPF: {dado[3]}')
            print(dado)

        return dados
    except Exception as e:
        messagebox.showerror('ERRO', f'ERRO AO BUSCAR OS DADOS! {str(e)}')

    finally:
        conexao.close()

#função de update de dados do cliente, onde é apenas necessario colocar o numero do cpf e o campo que deseja alterar.
#se houver algum erro uma exeção será exbida na tela.
#me deparei com o problema em que se tivessem campos em branco em suas entry's e se eu apenas quisesse alterar um campo, os que ficassem em branco estariam sendo sobrescritos
#assim criei duas listas, uma verifica o que foi alterado e a outra tem o que foi alterado na query, assim solucionando o problema da sobrescrita com campos vazios.
#se não houver erros uma mensagem de sucesso será mostrada ao usuário
def update(nome_entry, telefone_entry, email_entry, cpf_entry):

    try:
        conexao, cursor = conexao_db()

        nome = nome_entry.get()
        telefone = telefone_entry.get()
        email = email_entry.get()
        cpf = cpf_entry.get()

        campos = []
        dados = []

        if nome:
            campos.append('nome = ?')
            dados.append(nome)
        if telefone:
            campos.append('telefone = ?')
            dados.append(telefone)
        if email:
            campos.append('email = ?')
            dados.append(email)  
        if cpf:
            dados.append(cpf)  

        if campos:

            query = f'UPDATE clientes SET {", ".join(campos)} WHERE cpf = ?'
            
            cursor.execute(query,dados)
            cursor.execute('commit')

            for deletar in [nome_entry, telefone_entry, email_entry, cpf_entry]:
                deletar.delete(0, END)

            messagebox.showinfo('SUCESSO', 'Dados alterados com sucesso!')
        else:
            messagebox.showwarning('WARNING', 'Nenhum campo foi alterado!')

    except Exception as e:
        messagebox.showerror('ERRO', f'ERRO AO ALTERAR DADOS! {str(e)}')
    finally:
        conexao.close()

#função de deletar o cliente do banco, apenas é necessário digitar seu cpf que o cliente será apagado.
#se houver algum erro, uma exceção será mostrada na tela para o usuário.
#se nao houver erros uma mensagem de sucesso será mostrada ao usuário
def deletar(cpf_entry):
    try:
        conexao, cursor = conexao_db()

        cpf = cpf_entry.get()

        query = 'DELETE FROM clientes where cpf = ?'
        dados = (cpf,)

        cursor.execute(query, dados)
        cursor.execute('commit')
    
        cpf_entry.delete(0, END)

        messagebox.showwarning('REMOVIDO', 'Cliente removido com sucesso!')

    except Exception as e:
        messagebox.showwarning('ERRO', f'ERRO AO REMOVER CLIENTE! {str(e)}')
    
    finally:
        conexao.close()

#usando a função select_db ja existente para fazer a conexao, e pega todos os dados cadastrados do banco de dados
#os dados sao adcionados a uma lista com suas respectivas chaves e valores.
#a lista data é enviada como um JSON em uma requisição POST para localhost:5000, onde nosso servidor web flask está ligado esperando uma chamada
#se houver algum erro, uma exceção será mostrada na tela para o usuário.
#se nao houver erros uma mensagem de sucesso será mostrada ao usuário
def exportar_json(lista_db):
    try:
        
        colunas = select_db(lista_db)

        data = []

        for col in colunas:
            data.append(
                {
                    'nome': col[0],
                    'telefone': col[1],
                    'email': col[2],
                    'cpf': col[3]
                }
            )

        
        response = requests.post('http://127.0.0.1:5000/', json=data)

        if response.status_code == 200:
            messagebox.showinfo('SUCESSO', 'JSON EXPORTADO PARA http://localhost:5000/')
        else:
            messagebox.showerror('ERRO', 'JSON NÃO PODE SER EXPORTADO!')

    except Exception as e:
        messagebox.showerror('ERRO', f'JSON NÃO PODE SER EXPORTADO! {str(e)}')
    

#aqui é o main do programa onde eu utilizo o tkinter para executar o programa, dando-se um titulo e ajustando o tamanho da tela.
#utilizo variáveis organizadas para mostrar o label(textos que aparecem na tela) e suas entry's(campos de preenchimento).
#place é uma função cartesiana(eixos X e Y) que me permite movimentar as peças na posição da tela do tkinter
#utilizo botoes para acionar as funções criadas acima, o uso do command é para executar as funções e a do lambda é essencial para funções com parametros, onde eu devo executalas
#quando clico no botao e nao quando o programa e banco sao conctados.
#o main então, se torna a cara do programa
def main():
    i = Tk()
    i.title('teste estagio')
    i.geometry('500x500')

    #nome, telefone, email, cpf

    nome_label = Label(i, text='Nome: ')
    nome_label.place(x=10, y=10)
    nome_entry = Entry(i)
    nome_entry.place(x=100, y=10)

    telefone_label = Label(i, text='Telefone: ')
    telefone_label.place(x=10, y=40)
    telefone_entry = Entry(i)
    telefone_entry.place(x=100, y=40)

    email_label = Label(i, text='Email: ')
    email_label.place(x=10, y=70)
    email_entry = Entry(i)
    email_entry.place(x=100, y=70)

    cpf_label = Label(i, text='CPF: ')
    cpf_label.place(x=10, y=100)
    cpf_entry = Entry(i)
    cpf_entry.place(x=100, y=100)

    btn_select = Button(i, text='Selecionar', command=lambda: select_db(lista_db))
    btn_select.place(x=10, y=140)

    btn_cadastro = Button(i, text='Cadastro', command=lambda: adicionar_db(nome_entry, telefone_entry, email_entry, cpf_entry))
    btn_cadastro.place(x=100, y=140)

    btn_update = Button(i, text='Alterar Dados', command=lambda: update(nome_entry, telefone_entry, email_entry, cpf_entry))
    btn_update.place(x=180, y=140)

    btn_remover = Button(i, text='Remover cliente', command=lambda: deletar(cpf_entry))
    btn_remover.place(x=290, y=140)

    btn_json = Button(i, text='Exportar dados JSON', command=lambda: exportar_json(lista_db))
    btn_json.place(x=300, y=50)

    lista_db = Listbox(i, width=100, height=50)
    lista_db.place(x=10, y=200)

    i.mainloop()

if __name__ == "__main__":
    main()