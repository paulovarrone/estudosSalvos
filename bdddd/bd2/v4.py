import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_tables():
    db_conn = sqlite3.connect("estoque.db")
    db_cursor = db_conn.cursor()

    db_cursor.execute('''CREATE TABLE IF NOT EXISTS sessoes (
                            id INTEGER PRIMARY KEY,
                            nome TEXT NOT NULL)''')

    db_cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
                            id INTEGER PRIMARY KEY,
                            nome TEXT NOT NULL,
                            sessao_id INTEGER NOT NULL,
                            FOREIGN KEY(sessao_id) REFERENCES sessoes(id))''')

    db_cursor.execute('''CREATE TABLE IF NOT EXISTS estoque (
                            id INTEGER PRIMARY KEY,
                            produto_id INTEGER NOT NULL,
                            quantidade INTEGER NOT NULL,
                            FOREIGN KEY(produto_id) REFERENCES produtos(id))''')

    db_conn.commit()
    db_conn.close()

def obter_sessoes():
    db_conn = sqlite3.connect("estoque.db")
    db_cursor = db_conn.cursor()

    db_cursor.execute("SELECT id, nome FROM sessoes")
    sessoes = db_cursor.fetchall()

    db_conn.close()
    return sessoes

def adicionar_produto(entry_produto, entry_quantidade, entry_sessao, lista_estoque):
    produto = entry_produto.get()
    quantidade = entry_quantidade.get()
    sessao = entry_sessao.get()

    if produto and quantidade and sessao:
        db_conn = sqlite3.connect("estoque.db")
        db_cursor = db_conn.cursor()

        # Verificar se a sessão existe
        db_cursor.execute("SELECT id FROM sessoes WHERE nome=?", (sessao,))
        sessao_info = db_cursor.fetchone()
        if not sessao_info:
            # Se a seção não existir, adicioná-la
            db_cursor.execute("INSERT INTO sessoes (nome) VALUES (?)", (sessao,))
            sessao_id = db_cursor.lastrowid
        else:
            sessao_id = sessao_info[0]

        # Verificar se o produto existe na seção
        db_cursor.execute("SELECT id FROM produtos WHERE nome=? AND sessao_id=?", (produto, sessao_id))
        produto_info = db_cursor.fetchone()
        if not produto_info:
            # Se o produto não existir na seção, adicioná-lo
            db_cursor.execute("INSERT INTO produtos (nome, sessao_id) VALUES (?, ?)", (produto, sessao_id))
            produto_id = db_cursor.lastrowid
        else:
            produto_id = produto_info[0]

        # Atualizar o estoque do produto
        db_cursor.execute("SELECT quantidade FROM estoque WHERE produto_id=?", (produto_id,))
        existing_quantity = db_cursor.fetchone()
        if existing_quantity:
            nova_quantidade = existing_quantity[0] + int(quantidade)
            db_cursor.execute("UPDATE estoque SET quantidade=? WHERE produto_id=?", (nova_quantidade, produto_id))
        else:
            db_cursor.execute("INSERT INTO estoque (produto_id, quantidade) VALUES (?, ?)", (produto_id, quantidade))

        db_conn.commit()
        db_conn.close()
        mostrar_estoque(lista_estoque)
        entry_produto.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)
        entry_sessao.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

def mostrar_estoque(lista_estoque):
    lista_estoque.delete(0, tk.END)

    sessoes = obter_sessoes()
    
    if not sessoes:
        lista_estoque.insert(tk.END, "Nenhuma sessão encontrada.")
        return

    for sessao in sessoes:
        lista_estoque.insert(tk.END, (f" "))
        lista_estoque.insert(tk.END, (f"------------------------------ {sessao[1]} ------------------------------ "))
        lista_estoque.insert(tk.END, (f" "))
        
        db_conn = sqlite3.connect("estoque.db")
        db_cursor = db_conn.cursor()

        db_cursor.execute("SELECT produtos.nome, estoque.quantidade FROM produtos INNER JOIN estoque ON produtos.id = estoque.produto_id WHERE produtos.sessao_id=?", (sessao[0],))
        produtos = db_cursor.fetchall()

        if not produtos:
            lista_estoque.insert(tk.END, "Nenhum produto encontrado nesta sessão.")
        else:
            for produto in produtos:
                lista_estoque.insert(tk.END, (f"{produto[0]} - {produto[1]} unidades"))

        db_conn.close()

def remover_sessao(entry_sessao, lista_estoque):
    sessao = entry_sessao.get()

    if sessao:
        db_conn = sqlite3.connect("estoque.db")
        db_cursor = db_conn.cursor()

        db_cursor.execute("SELECT id FROM sessoes WHERE nome=?", (sessao,))
        sessao_info = db_cursor.fetchone()
        if sessao_info:
            sessao_id = sessao_info[0]
            db_cursor.execute("DELETE FROM estoque WHERE produto_id IN (SELECT id FROM produtos WHERE sessao_id=?)", (sessao_id,))
            db_cursor.execute("DELETE FROM produtos WHERE sessao_id=?", (sessao_id,))
            db_cursor.execute("DELETE FROM sessoes WHERE id=?", (sessao_id,))
            db_conn.commit()
            db_conn.close()
            mostrar_estoque(lista_estoque)
            entry_sessao.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "A sessão especificada não existe.")
    else:
        messagebox.showerror("Erro", "Por favor, especifique a sessão que deseja remover.")

def main():
    root = tk.Tk()
    root.title("Sistema de Estoque")

    root.iconbitmap("un.ico")
    root['bg'] = '#0b5884'
    root.resizable(0, 0)

    create_tables()

    label_produto = tk.Label(root, text="Produto:", font=("Arial", 15), bg='white')
    label_produto.grid(row=0, column=0, padx=20, pady=20)

    entry_produto = tk.Entry(root, font=("Arial", 15))
    entry_produto.grid(row=0, column=1, padx=20, pady=20)

    label_quantidade = tk.Label(root, text="Quantidade:", font=("Arial", 15), bg='white')
    label_quantidade.grid(row=1, column=0, padx=20, pady=20)

    entry_quantidade = tk.Entry(root, font=("Arial", 15))
    entry_quantidade.grid(row=1, column=1, padx=20, pady=20)

    label_sessao = tk.Label(root, text="Sessão:", font=("Arial", 15), bg='white')
    label_sessao.grid(row=2, column=0, padx=20, pady=20)

    entry_sessao = tk.Entry(root, font=("Arial", 15))
    entry_sessao.grid(row=2, column=1, padx=20, pady=20)

    btn_adicionar = tk.Button(root, text="Adicionar ou Remover Produto", font=("Arial", 15), bg='white', command=lambda: adicionar_produto(entry_produto, entry_quantidade, entry_sessao, lista_estoque))
    btn_adicionar.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    btn_remover_sessao = tk.Button(root, text="Remover Sessão", font=("Arial", 15), bg='white', command=lambda: remover_sessao(entry_sessao, lista_estoque))
    btn_remover_sessao.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

    lista_estoque = tk.Listbox(root, font=("Arial", 13), height=22, width=55)
    lista_estoque.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="sn")

    mostrar_estoque(lista_estoque)

    root.mainloop()


if __name__ == "__main__":
    main()
