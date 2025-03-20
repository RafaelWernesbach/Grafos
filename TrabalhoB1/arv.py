import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

class No:
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None

class Arvore:
    def __init__(self):
        self.raiz = None
    
    def inserir(self, chave):
        if self.raiz is None:
            self.raiz = No(chave)
        else:
            self._inserir(self.raiz, chave)
    
    def _inserir(self, raiz, chave):
        if chave < raiz.chave:
            if raiz.esquerda is None:
                raiz.esquerda = No(chave)
            else:
                self._inserir(raiz.esquerda, chave)
        else:
            if raiz.direita is None:
                raiz.direita = No(chave)
            else:
                self._inserir(raiz.direita, chave)
    
    def excluir(self, chave):
        self.raiz = self._excluir(self.raiz, chave)
    
    def _excluir(self, raiz, chave):
        if raiz is None:
            return raiz
        if chave < raiz.chave:
            raiz.esquerda = self._excluir(raiz.esquerda, chave)
        elif chave > raiz.chave:
            raiz.direita = self._excluir(raiz.direita, chave)
        else:
            if raiz.esquerda is None:
                return raiz.direita
            elif raiz.direita is None:
                return raiz.esquerda
            temp = self._menor_no(raiz.direita)
            raiz.chave = temp.chave
            raiz.direita = self._excluir(raiz.direita, temp.chave)
        return raiz
    
    def _menor_no(self, raiz):
        atual = raiz
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual
    
    def buscar(self, chave):
        return self._buscar(self.raiz, chave)
    
    def _buscar(self, raiz, chave):
        if raiz is None or raiz.chave == chave:
            return raiz
        if chave < raiz.chave:
            return self._buscar(raiz.esquerda, chave)
        return self._buscar(raiz.direita, chave)
    
    def contar_nos(self):
        return self._contar_nos(self.raiz)
    
    def _contar_nos(self, raiz):
        if raiz is None:
            return 0
        return 1 + self._contar_nos(raiz.esquerda) + self._contar_nos(raiz.direita)
    
    def contar_nao_folhas(self):
        return self._contar_nao_folhas(self.raiz)
    
    def _contar_nao_folhas(self, raiz):
        if raiz is None or (raiz.esquerda is None and raiz.direita is None):
            return 0
        return 1 + self._contar_nao_folhas(raiz.esquerda) + self._contar_nao_folhas(raiz.direita)

class NoGenerico:
    def __init__(self, chave):
        self.chave = chave
        self.filhos = []

class ArvoreGenerica:
    def __init__(self):
        self.raiz = None

    def inserir(self, chave, chave_pai=None):
        novo_no = NoGenerico(chave)
        
        if self.raiz is None:
            self.raiz = novo_no
            return
        
        if chave_pai is None:
            messagebox.showerror("Erro", "A árvore já tem uma raiz. Especifique um nó pai.")
            return
        
        pai = self.buscar(self.raiz, chave_pai)
        if pai:
            pai.filhos.append(novo_no)
        else:
            messagebox.showerror("Erro", "Nó pai não encontrado.")
    
    def buscar(self, raiz, chave):
        if raiz is None:
            return None
        if raiz.chave == chave:
            return raiz
        for filho in raiz.filhos:
            encontrado = self.buscar(filho, chave)
            if encontrado:
                return encontrado
        return None

    def contar_nos(self):
        return self._contar_nos(self.raiz)
    
    def _contar_nos(self, raiz):
        if raiz is None:
            return 0
        total = 1
        for filho in raiz.filhos:
            total += self._contar_nos(filho)
        return total
    
    def contar_nao_folhas(self):
        return self._contar_nao_folhas(self.raiz)
    
    def _contar_nao_folhas(self, raiz):
        if raiz is None or len(raiz.filhos) == 0:
            return 0
        total = 1
        for filho in raiz.filhos:
            total += self._contar_nao_folhas(filho)
        return total

class Interface:
    def __init__(self, root):
        self.arvore_binaria = Arvore()
        self.arvore_generica = ArvoreGenerica()
        self.root = root
        self.root.title("Árvore")
        
        self.tipo_arvore = tk.StringVar(value="binaria")
        
        self.radio_binaria = tk.Radiobutton(root, text="Árvore Binária", variable=self.tipo_arvore, value="binaria")
        self.radio_binaria.pack()
        
        self.radio_generica = tk.Radiobutton(root, text="Árvore Genérica", variable=self.tipo_arvore, value="generica")
        self.radio_generica.pack()
        
        self.entrada = tk.Entry(root)
        self.entrada.pack()
        
        self.botao_inserir = tk.Button(root, text="Inserir", command=self.adicionar_valor)
        self.botao_inserir.pack()
        
        self.botao_remover = tk.Button(root, text="Remover", command=self.remover_valor)
        self.botao_remover.pack()
        
        self.botao_localizar = tk.Button(root, text="Localizar", command=self.localizar_valor)
        self.botao_localizar.pack()
        
        self.contagem_label = tk.Label(root, text="Nós: 0 | Não-folhas: 0")
        self.contagem_label.pack()
    
    def atualizar_contagem(self):
        if self.tipo_arvore.get() == "binaria":
            total_nos = self.arvore_binaria.contar_nos()
            total_nao_folhas = self.arvore_binaria.contar_nao_folhas()
        else:
            total_nos = self.arvore_generica.contar_nos()
            total_nao_folhas = self.arvore_generica.contar_nao_folhas()
        self.contagem_label.config(text=f"Nós: {total_nos} | Não-folhas: {total_nao_folhas}")
    
    def adicionar_valor(self):
        try:
            if self.tipo_arvore.get() == "binaria":
                valor = int(self.entrada.get())
                if self.arvore_binaria.buscar(valor) is not None:
                    raise ValueError
                self.arvore_binaria.inserir(valor)
            else:
                valores = self.entrada.get().split(',')
                valor = int(valores[0])
                chave_pai = int(valores[1]) if len(valores) > 1 else None
                if chave_pai is not None and self.arvore_generica.buscar(self.arvore_generica.raiz, chave_pai) is None:
                    raise ValueError
                self.arvore_generica.inserir(valor, chave_pai)
            self.atualizar_contagem()
            self.desenhar_arvore()
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor válido no formato correto")
    
    def remover_valor(self):
        try:
            valor = int(self.entrada.get())
            if self.tipo_arvore.get() == "binaria":
                self.arvore_binaria.excluir(valor)
            else:
                messagebox.showerror("Erro", "Remoção não suportada para árvore genérica")
            self.atualizar_contagem()
            self.desenhar_arvore()
        except ValueError:
            messagebox.showerror("Erro", "Digite um número")
    
    def localizar_valor(self):
        try:
            valor = int(self.entrada.get())
            if self.tipo_arvore.get() == "binaria":
                no_encontrado = self.arvore_binaria.buscar(valor)
                if no_encontrado:
                    self.desenhar_arvore_destacado(no_encontrado.chave)
                else:
                    messagebox.showinfo("Resultado da pesquisa", "Valor não encontrado na árvore.")
            else:
                no_encontrado = self.arvore_generica.buscar(self.arvore_generica.raiz, valor)
                if no_encontrado:
                    messagebox.showinfo("Resultado da pesquisa", "Valor encontrado na árvore.")
                else:
                    messagebox.showinfo("Resultado da pesquisa", "Valor não encontrado na árvore.")
        except ValueError:
            messagebox.showerror("Erro", "Digite um número")
    
    def adicionar_arestas(self, raiz, G, pos, x=0, y=0, layer=1):
        if raiz is not None:
            G.add_node(raiz.chave, pos=(x, y))
            if isinstance(raiz, No):
                if raiz.esquerda is not None:
                    G.add_edge(raiz.chave, raiz.esquerda.chave)
                    self.adicionar_arestas(raiz.esquerda, G, pos, x - 1 / layer, y - 1, layer + 1)
                if raiz.direita is not None:
                    G.add_edge(raiz.chave, raiz.direita.chave)
                    self.adicionar_arestas(raiz.direita, G, pos, x + 1 / layer, y - 1, layer + 1)
            elif isinstance(raiz, NoGenerico):
                for i, filho in enumerate(raiz.filhos):
                    G.add_edge(raiz.chave, filho.chave)
                    self.adicionar_arestas(filho, G, pos, x + (i - len(raiz.filhos) / 2) / layer, y - 1, layer + 1)
    
    def desenhar_arvore(self, no_destacado=None):
        plt.close('all')
        G = nx.DiGraph()
        if self.tipo_arvore.get() == "binaria":
            self.adicionar_arestas(self.arvore_binaria.raiz, G, {})
        else:
            self.adicionar_arestas(self.arvore_generica.raiz, G, {})
        pos = nx.get_node_attributes(G, 'pos')
        plt.figure(figsize=(8, 5))
        node_colors = ['lightblue' if node != no_destacado else 'red' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=10, font_weight='bold')
        plt.show()
    
    def desenhar_arvore_destacado(self, chave):
        self.desenhar_arvore(no_destacado=chave)

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
