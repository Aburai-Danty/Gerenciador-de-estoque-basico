import tkinter as tk
from tkinter import messagebox, filedialog
import pickle
import xml.etree.ElementTree as ET

class Produto:
    def __init__(self, codigo, nome, quantidade):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade

class EstoqueApp:
    def __init__(self):
        self.estoque = Estoque()

        self.root = tk.Tk()
        self.root.title("Gerenciador de Estoque")
        self.root.geometry("450x250")

        def remover_produto(self):
            codigo = self.codigo_entry.get()

            if not codigo:
                messagebox.showinfo("Campo vazio", "Digite um código válido.")
                return

            codigo = int(codigo)

            quantidade = int(self.quantidade_entry.get())

            if self.estoque.remover_produto(codigo, quantidade):
                messagebox.showinfo("Produto removido", "Quantidade removida do estoque.")
            else:
                messagebox.showinfo("Produto não encontrado",
                                    "O produto não foi encontrado no estoque ou a "
                                    "quantidade solicitada é maior do que a disponível.")

            self.codigo_entry.delete(0, tk.END)
            self.quantidade_entry.delete(0, tk.END)

        self.codigo_label = tk.Label(self.root, text="Código do Produto:")
        self.codigo_label.grid(row=0, column=0)
        self.codigo_entry = tk.Entry(self.root)
        self.codigo_entry.grid(row=0, column=1, pady=5)

        self.nome_label = tk.Label(self.root, text="Nome do Produto:")
        self.nome_label.grid(row=1, column=0)
        self.nome_entry = tk.Entry(self.root)
        self.nome_entry.grid(row=1, column=1, pady=5)

        self.quantidade_label = tk.Label(self.root, text="Quantidade Produto:")
        self.quantidade_label.grid(row=2, column=0)
        self.quantidade_entry = tk.Entry(self.root)
        self.quantidade_entry.grid(row=2, column=1, pady=5)

        self.adicionar_button = tk.Button(self.root, text="Adicionar ao Estoque",
                                          command=self.adicionar_produto, width=35)
        self.adicionar_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.remover_button = tk.Button(self.root, text="Remover do estoque",
                                        command=self.remover_produto, width=35)
        self.remover_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.listar_button = tk.Button(self.root, text="Produtos cadastrados Estoque",
                                       command=self.listar_produtos, width=35)
        self.listar_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.salvar_button = tk.Button(self.root, text="Salvar Estoque",
                                       command=self.salvar_estoque, width=35)
        self.salvar_button.grid(row=6, column=0, columnspan=2, pady=5)

        self.selecionar_button = tk.Button(self.root, text="Selecionar Arquivo",
                                           command=self.selecionar_arquivo, width=35)
        self.selecionar_button.grid(row=6, column=0, columnspan=2, pady=5)

        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.root.mainloop()

    def selecionar_arquivo(self):
        filename = filedialog.askopenfilename(filetypes=[("Arquivos XML", "*.xml")])
        if filename:
            self.ler_arquivo_xml(filename)

    def adicionar_produto(self):
        codigo = int(self.codigo_entry.get())
        nome = self.nome_entry.get()
        quantidade = int(self.quantidade_entry.get())

        produto = Produto(codigo, nome, quantidade)
        self.estoque.adicionar_produto(produto)

        messagebox.showinfo("Produto adicionado", "Produto adicionado ao estoque.")
        self.codigo_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)

    def remover_produto(self):
        codigo = self.codigo_entry.get()

        if not codigo:
            messagebox.showinfo("Campo vazio", "Digite um código válido.")
            return

        codigo = int(codigo)

        quantidade = self.quantidade_entry.get()

        if not quantidade:
            messagebox.showinfo("Campo vazio", "Digite uma quantidade válida.")
            return

        quantidade = int(quantidade)

        if self.estoque.remover_produto(codigo, quantidade):
            messagebox.showinfo("Produto removido", "Quantidade removida do estoque.")
        else:
            messagebox.showinfo("Produto não encontrado", "O produto não foi encontrado no estoque ou a quantidade"
                                                          " solicitada é maior do que a disponível.")

        self.codigo_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)

    def listar_produtos(self):
        if len(self.estoque.produtos) == 0:
            messagebox.showinfo("Estoque vazio", "O estoque está vazio.")
        else:
            info_estoque = "Produtos no estoque:\n\n"
            for produto in self.estoque.produtos:
                info_estoque += f"Código: {produto.codigo} | Nome: {produto.nome} " \
                                f"| Quantidade: {produto.quantidade}\n"
            messagebox.showinfo("Estoque", info_estoque)

    def salvar_estoque(self):
        if len(self.estoque.produtos) == 0:
            messagebox.showinfo("Estoque vazio", "Não há produtos no estoque para salvar.")
            return

        filename = "estoque.pickle"
        with open(filename, "wb") as file:
            pickle.dump(self.estoque, file)
        messagebox.showinfo("Estoque salvo", f"O estoque foi salvo no arquivo '{filename}'.")

class Estoque:
    def __init__(self):
        self.produtos = []

    def ler_arquivo_xml(self, filename):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            for produto_xml in root.findall("produto"):
                codigo = int(produto_xml.find("codigo").text)
                nome = produto_xml.find("nome").text
                quantidade = int(produto_xml.find("quantidade").text)

                produto = Produto(codigo, nome, quantidade)
                self.estoque.adicionar_produto(produto)

            messagebox.showinfo("Arquivo XML lido", "O arquivo XML foi lido com sucesso.")
        except ET.ParseError:
            messagebox.showerror("Erro de leitura", "O arquivo XML selecionado não pôde ser lido corretamente.")

    def adicionar_produto(self, produto):
        self.produtos.append(produto)
        print("Produto adicionado ao estoque.")

    def remover_produto(self, codigo, quantidade):
        for produto in self.produtos:
            if produto.codigo == codigo:
                if produto.quantidade >= quantidade:
                    produto.quantidade -= quantidade
                    return True
                else:
                    return False

        return False

    def somar_produtos_mesmo_codigo(self):
        produtos_agrupados = {}
        for produto in self.produtos:
            if produto.codigo in produtos_agrupados:
                produtos_agrupados[produto.codigo].quantidade += produto.quantidade
            else:
                produtos_agrupados[produto.codigo] = produto

        self.produtos = list(produtos_agrupados.values())

        self.produtos = []
        for nome, quantidade in produtos_agrupados.items():
            produto = Produto(len(self.produtos) + 1, nome, quantidade)
            self.produtos.append(produto)


# Iniciar a aplicação
estoque_app = EstoqueApp()