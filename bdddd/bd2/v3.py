import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_tables():
    db_conn = sqlite3.connect("estoque.db")
    db_cursor = db_conn.cursor()

    db_cursor.execute('''CREATE TABLE IF NOT EXISTS secoes (
                            id INTEGER PRIMARY KEY,
                            nome TEXT NOT NULL)''')

    db_cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
                            id INTEGER PRIMARY KEY,
                            nome TEXT NOT NULL,
                            secao_id INTEGER NOT NULL,
                            FOREIGN KEY(secao_id) REFERENCES secoes(id))''')

    db_cursor.execute('''CREATE TABLE IF NOT EXISTS estoque (
                            id INTEGER PRIMARY KEY,
                            produto_id INTEGER NOT NULL,
                            quantidade INTEGER NOT NULL,
                            FOREIGN KEY(produto_id) REFERENCES produtos(id))''')

    db_conn.commit()
    db_conn.close()

def obter_secoes():
    db_conn = sqlite3.connect("estoque.db")
    db_cursor = db_conn.cursor()

    db_cursor.execute("SELECT id, nome FROM secoes")
    secoes = db_cursor.fetchall()

    db_conn.close()
    return secoes

def adicionar_produto(entry_produto, entry_quantidade, entry_secao, lista_estoque):
    produto = entry_produto.get()
    quantidade = entry_quantidade.get()
    secao = entry_secao.get()

    if produto and quantidade and secao:
        db_conn = sqlite3.connect("estoque.db")
        db_cursor = db_conn.cursor()

        # Verificar se a seção existe
        db_cursor.execute("SELECT id FROM secoes WHERE nome=?", (secao,))
        secao_info = db_cursor.fetchone()
        if not secao_info:
            # Se a seção não existir, adicioná-la
            db_cursor.execute("INSERT INTO secoes (nome) VALUES (?)", (secao,))
            secao_id = db_cursor.lastrowid
        else:
            secao_id = secao_info[0]

        # Verificar se o produto existe na seção
        db_cursor.execute("SELECT id FROM produtos WHERE nome=? AND secao_id=?", (produto, secao_id))
        produto_info = db_cursor.fetchone()
        if not produto_info:
            # Se o produto não existir na seção, adicioná-lo
            db_cursor.execute("INSERT INTO produtos (nome, secao_id) VALUES (?, ?)", (produto, secao_id))
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
        entry_secao.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

def mostrar_estoque(lista_estoque):
    lista_estoque.delete(0, tk.END)

    secoes = obter_secoes()
    
    if not secoes:
        lista_estoque.insert(tk.END, "Nenhuma seção encontrada.")
        return

    for secao in secoes:
        lista_estoque.insert(tk.END, (f"------------------------------------------------------------------------ {secao[1]} ------------------------------------------------------------------------"))

        db_conn = sqlite3.connect("estoque.db")
        db_cursor = db_conn.cursor()

        db_cursor.execute("SELECT produtos.nome, estoque.quantidade FROM produtos INNER JOIN estoque ON produtos.id = estoque.produto_id WHERE produtos.secao_id=?", (secao[0],))
        produtos = db_cursor.fetchall()

        if not produtos:
            lista_estoque.insert(tk.END, "Nenhum produto encontrado nesta seção.")
        else:
            for produto in produtos:
                lista_estoque.insert(tk.END, (f"{produto[0]} - {produto[1]} unidades"))

        db_conn.close()

def remover_secao(entry_secao, lista_estoque):
    secao = entry_secao.get()

    if secao:
        db_conn = sqlite3.connect("estoque.db")
        db_cursor = db_conn.cursor()

        db_cursor.execute("SELECT id FROM secoes WHERE nome=?", (secao,))
        secao_info = db_cursor.fetchone()
        if secao_info:
            secao_id = secao_info[0]
            db_cursor.execute("DELETE FROM estoque WHERE produto_id IN (SELECT id FROM produtos WHERE secao_id=?)", (secao_id,))
            db_cursor.execute("DELETE FROM produtos WHERE secao_id=?", (secao_id,))
            db_cursor.execute("DELETE FROM secoes WHERE id=?", (secao_id,))
            db_conn.commit()
            db_conn.close()
            mostrar_estoque(lista_estoque)
            entry_secao.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "A seção especificada não existe.")
    else:
        messagebox.showerror("Erro", "Por favor, especifique a seção que deseja remover.")

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

    label_secao = tk.Label(root, text="Seção:", font=("Arial", 15), bg='white')
    label_secao.grid(row=2, column=0, padx=20, pady=20)

    entry_secao = tk.Entry(root, font=("Arial", 15))
    entry_secao.grid(row=2, column=1, padx=20, pady=20)

    btn_adicionar = tk.Button(root, text="Adicionar ou Remover Produto", font=("Arial", 15), bg='white', command=lambda: adicionar_produto(entry_produto, entry_quantidade, entry_secao, lista_estoque))
    btn_adicionar.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    btn_remover_secao = tk.Button(root, text="Remover Seção", font=("Arial", 15), bg='white', command=lambda: remover_secao(entry_secao, lista_estoque))
    btn_remover_secao.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

    lista_estoque = tk.Listbox(root, font=("Arial", 13), height=25, width=100)
    lista_estoque.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="sn")

    mostrar_estoque(lista_estoque)

    root.mainloop()


if __name__ == "__main__":
    main()
