import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

class No:
    def __init__(self, chave):
        self.chave = chave  # valor do nó
        self.esquerda = None  # ponteiro para o filho esquerdo
        self.direita = None  # ponteiro para o filho direito

class ArvoreBinaria:
    def __init__(self):
        self.raiz = None  # raiz da árvore inicializada como vazia

    def inserir(self, chave):
        self.raiz = self._inserir_rec(self.raiz, chave)  # chama o método recursivo

    def _inserir_rec(self, no, chave):
        if no is None:
            return No(chave)  # se não houver nó, cria um novo nó
        if chave < no.chave:
            no.esquerda = self._inserir_rec(no.esquerda, chave)  # insere na subárvore esquerda
        else:
            no.direita = self._inserir_rec(no.direita, chave)  # insere na subárvore direita
        return no

    def excluir(self, chave):
        self.raiz = self._excluir_rec(self.raiz, chave)  # chama o método recursivo

    def _excluir_rec(self, no, chave):
        if no is None:
            return no  # retorna se a árvore for vazia
        if chave < no.chave:
            no.esquerda = self._excluir_rec(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self._excluir_rec(no.direita, chave)
        else:
            if no.esquerda is None:
                return no.direita  # substitui pelo filho direito se não houver esquerdo
            elif no.direita is None:
                return no.esquerda  # substitui pelo filho esquerdo se não houver direito
            temp = self._menor_no(no.direita)  # encontra o menor valor da subárvore direita
            no.chave = temp.chave  # substitui pelo sucessor
            no.direita = self._excluir_rec(no.direita, temp.chave)
        return no

    def _menor_no(self, no):  # encontra o menor nó da subárvore
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda  # percorre a esquerda até encontrar o menor valor
        return atual

    def buscar(self, chave):
        return self._buscar_rec(self.raiz, chave)  # chama a busca recursiva

    def _buscar_rec(self, no, chave):
        if no is None or no.chave == chave:
            return no  # retorna o nó se encontrado ou None se não existir
        if chave < no.chave:
            return self._buscar_rec(no.esquerda, chave)  # busca na subárvore esquerda
        return self._buscar_rec(no.direita, chave)  # busca na subárvore direita

    def contar_nos(self):
        return self._contar_nos_rec(self.raiz)  # chama a contagem recursiva

    def _contar_nos_rec(self, no):
        if no is None:
            return 0
        return 1 + self._contar_nos_rec(no.esquerda) + self._contar_nos_rec(no.direita)  # soma a raiz + filhos

    def contar_nao_folhas(self):
        return self._contar_nao_folhas_rec(self.raiz)  # chama a contagem recursiva

    def _contar_nao_folhas_rec(self, no):
        if no is None:
            return 0
        if no.esquerda is not None or no.direita is not None:
            return 1 + self._contar_nao_folhas_rec(no.esquerda) + self._contar_nao_folhas_rec(no.direita)  # conta nós não folha
        return 0

class Interface:
    def __init__(self, raiz):
        self.arvore = ArvoreBinaria()  # cria a árvore
        self.janela = raiz
        self.janela.title("Árvore Binária")

        self.entrada = tk.Entry(raiz)  # campo de entrada de valores
        self.entrada.pack()

        self.botao_inserir = tk.Button(raiz, text="Inserir", command=self.adicionar_valor)  # botão para inserir
        self.botao_inserir.pack()

        self.botao_remover = tk.Button(raiz, text="Remover", command=self.remover_valor)  # botão para remover
        self.botao_remover.pack()

        self.botao_localizar = tk.Button(raiz, text="Localizar", command=self.localizar_valor)  # botão para localizar
        self.botao_localizar.pack()

        self.contagem_label = tk.Label(raiz, text="Nós: 0 | Não-folhas: 0")  # exibição da contagem
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

    def desenhar_arvore(self):
        plt.close('all')
        G = nx.DiGraph()
        self.adicionar_arestas(self.arvore.raiz, G)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
        plt.show()

    def desenhar_arvore_destacado(self, no_destacado):
        plt.close('all')
        G = nx.DiGraph()
        self.adicionar_arestas(self.arvore.raiz, G)
        pos = nx.spring_layout(G)
        node_colors = ['lightblue' if node != no_destacado else 'yellow' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=10, font_weight='bold')
        plt.show()

raiz_tk = tk.Tk()
Interface(raiz_tk)
raiz_tk.mainloop()
