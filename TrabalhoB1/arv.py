import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

def criar_no(chave):
    return [chave, None, None]

def inserir(raiz, chave):
    if raiz is None:
        return criar_no(chave)
    if chave < raiz[0]:
        raiz[1] = inserir(raiz[1], chave)
    else:
        raiz[2] = inserir(raiz[2], chave)
    return raiz

def excluir_no(raiz, chave):
    if raiz is None:
        return raiz
    if chave < raiz[0]:
        raiz[1] = excluir_no(raiz[1], chave)
    elif chave > raiz[0]:
        raiz[2] = excluir_no(raiz[2], chave)
    else:
        if raiz[1] is None:
            return raiz[2]
        elif raiz[2] is None:
            return raiz[1]
        temp = menor_no(raiz[2])
        raiz[0] = temp[0]
        raiz[2] = excluir_no(raiz[2], temp[0])
    return raiz

def menor_no(raiz):
    atual = raiz
    while atual[1] is not None:
        atual = atual[1]
    return atual

def adicionar_valor():
    global raiz
    try:
        valor = int(entrada.get())
        raiz = inserir(raiz, valor)
        desenhar_arvore()
    except ValueError:
        messagebox.showerror("Erro", "Digite um número")

def remover_valor():
    global raiz
    try:
        valor = int(entrada.get())
        raiz = excluir_no(raiz, valor)
        desenhar_arvore()
    except ValueError:
        messagebox.showerror("Erro", "Digite um número")

def adicionar_arestas(raiz, G, pos, x=0, y=0, layer=1):
    if raiz is not None:
        G.add_node(raiz[0], pos=(x, y))
        if raiz[1] is not None:
            G.add_edge(raiz[0], raiz[1][0])
            adicionar_arestas(raiz[1], G, pos, x - 1 / layer, y - 1, layer + 1)
        if raiz[2] is not None:
            G.add_edge(raiz[0], raiz[2][0])
            adicionar_arestas(raiz[2], G, pos, x + 1 / layer, y - 1, layer + 1)

def desenhar_arvore():
    G = nx.DiGraph()
    pos = {}
    plt.figure(figsize=(8, 5))
    adicionar_arestas(raiz, G, pos)
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
    plt.show()

# Interface gráfica
raiz = None
janela = tk.Tk()
janela.title("arvore binaria")

entrada = tk.Entry(janela)
entrada.pack()

botao_inserir = tk.Button(janela, text="Inserir", command=adicionar_valor)
botao_inserir.pack()

botao_remover = tk.Button(janela, text="Remover", command=remover_valor)
botao_remover.pack()

janela.mainloop()
