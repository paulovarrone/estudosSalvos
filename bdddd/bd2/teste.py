import tkinter as tk


def main():

    root = tk.Tk()
    root.title("Sistema de Estoque")

    root.iconbitmap("un.ico")
    root['bg'] = '#0b5884'
    root.resizable(0, 0)


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

    btn_remover_secao = tk.Button(root, text="Remover Seção", font=("Arial", 15), bg='white', bg='white', command=lambda: remover_secao(entry_secao, lista_estoque))
    btn_remover_secao.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

    lista_estoque = tk.Listbox(root, font=("Arial", 13), height=22, width=50)
    lista_estoque.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="sn")

    root.mainloop()


main()