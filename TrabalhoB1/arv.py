import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

class No:
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None

class ArvoreBinaria:
    def __init__(self):
        self.raiz = None
    
    def inserir(self, chave):
        self.raiz = self._inserir(self.raiz, chave)
    
    def _inserir(self, raiz, chave):
        if raiz is None:
            return No(chave)
        if chave < raiz.chave:
            raiz.esquerda = self._inserir(raiz.esquerda, chave)
        else:
            raiz.direita = self._inserir(raiz.direita, chave)
        return raiz
    
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
    
class Interface:
    def __init__(self, root):
        self.arvore = ArvoreBinaria()
        self.root = root
        self.root.title("Árvore Binária")
        
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
        total_nos = self.arvore.contar_nos()
        total_nao_folhas = self.arvore.contar_nao_folhas()
        self.contagem_label.config(text=f"Nós: {total_nos} | Não-folhas: {total_nao_folhas}")
    
    def adicionar_valor(self):
        try:
            valor = int(self.entrada.get())
            if self.arvore.buscar(valor) is not None:
                raise ValueError
            self.arvore.inserir(valor)
            self.atualizar_contagem()
            self.desenhar_arvore()
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor válido")
    
    def remover_valor(self):
        try:
            valor = int(self.entrada.get())
            self.arvore.excluir(valor)
            self.atualizar_contagem()
            self.desenhar_arvore()
        except ValueError:
            messagebox.showerror("Erro", "Digite um número")
    
    def localizar_valor(self):
        try:
            valor = int(self.entrada.get())
            no_encontrado = self.arvore.buscar(valor)
            if no_encontrado:
                self.desenhar_arvore_destacado(no_encontrado.chave)
            else:
                messagebox.showinfo("Resultado da pesquisa", "Valor não encontrado na árvore.")
        except ValueError:
            messagebox.showerror("Erro", "Digite um número")
    
    def adicionar_arestas(self, raiz, G, pos, x=0, y=0, layer=1):
        if raiz is not None:
            G.add_node(raiz.chave, pos=(x, y))
            if raiz.esquerda is not None:
                G.add_edge(raiz.chave, raiz.esquerda.chave)
                self.adicionar_arestas(raiz.esquerda, G, pos, x - 1 / layer, y - 1, layer + 1)
            if raiz.direita is not None:
                G.add_edge(raiz.chave, raiz.direita.chave)
                self.adicionar_arestas(raiz.direita, G, pos, x + 1 / layer, y - 1, layer + 1)
    
    def desenhar_arvore(self):
        plt.close('all')
        G = nx.DiGraph()
        self.adicionar_arestas(self.arvore.raiz, G, {})
        pos = nx.get_node_attributes(G, 'pos')
        plt.figure(figsize=(8, 5))
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
