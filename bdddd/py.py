import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_table():
    db_conn = sqlite3.connect("estoque.db")
    db_cursor = db_conn.cursor()
    db_cursor.execute('''CREATE TABLE IF NOT EXISTS estoque (
                            id INTEGER PRIMARY KEY,
                            produto TEXT NOT NULL,
                            quantidade INTEGER NOT NULL)''')
    db_conn.commit()
    db_conn.close()

def adicionar_produto(entry_produto, entry_quantidade, lista_estoque):
    produto = entry_produto.get()
    quantidade = entry_quantidade.get()

    if produto and quantidade:
        db_conn = sqlite3.connect("estoque.db")
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT * FROM estoque WHERE produto=?", (produto,))
        existing_product = db_cursor.fetchone()

        if existing_product:
            nova_quantidade = existing_product[2] + int(quantidade)
            if nova_quantidade <= 0:
                db_cursor.execute("DELETE FROM estoque WHERE produto=?", (produto,))
            else:
                db_cursor.execute("UPDATE estoque SET quantidade=? WHERE produto=?", (nova_quantidade, produto))
        else:
            db_cursor.execute("INSERT INTO estoque (produto, quantidade) VALUES (?, ?)", (produto, quantidade))

        db_conn.commit()
        db_conn.close()
        mostrar_estoque(lista_estoque)
        entry_produto.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

def mostrar_estoque(lista_estoque):
    db_conn = sqlite3.connect("estoque.db")
    db_cursor = db_conn.cursor()
    lista_estoque.delete(0, tk.END)
    db_cursor.execute("SELECT * FROM estoque")
    estoque = db_cursor.fetchall()
    for item in estoque:
        lista_estoque.insert(tk.END, f"{item[1]} - {item[2]} unidades")
    db_conn.close()

def main():
    root = tk.Tk()
    root.title("Sistema de Estoque")

    create_table()

    label_produto = tk.Label(root, text="Produto:")
    label_produto.grid(row=0, column=0, padx=5, pady=5)

    entry_produto = tk.Entry(root)
    entry_produto.grid(row=0, column=1, padx=5, pady=5)

    label_quantidade = tk.Label(root, text="Quantidade:")
    label_quantidade.grid(row=1, column=0, padx=5, pady=5)

    entry_quantidade = tk.Entry(root)
    entry_quantidade.grid(row=1, column=1, padx=5, pady=5)

    btn_adicionar = tk.Button(root, text="Adicionar Produto", command=lambda: adicionar_produto(entry_produto, entry_quantidade, lista_estoque))
    btn_adicionar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    lista_estoque = tk.Listbox(root)
    lista_estoque.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    mostrar_estoque(lista_estoque)

    root.mainloop()

if __name__ == "__main__":
    main()
