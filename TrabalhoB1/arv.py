import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

# A CLASSE NO REPRESENTA O CONJUNTO FORMADO PELO VALOR DE UM NÓ PAI(CHAVE) E SEUS FILHOS(ESQUERDA E DIREITA), QUE SÃO OBJETOS DA CLASSE NO
class No:
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None

class Arvore:
     #INICIALIZA UMA ÁRVORE COM RAIZ VAZIA. RAIZ É O ATRIBUTO QUE ARMAZENA UM OBJETO NÓ QUE É O COMEÇO DÁ ÁRVORE.
     #(ENTÃO NA REAL ELA ARMZENA TODOS OS NÓS, PORQUE UM PAI LEVA AO FILHO QUE LEVA AO FILHO DO FILHO E ASSIM POR DIANTE...)
    def __init__(self):
        self.raiz = None #cria o atributo raiz vazio
    
     
     # FUNÇÃO QUE ENCAPSULA A COMPLEXIDADE DE _INSERIR. INSERE UM NÓ , QUE SERÁ A RAIZ CASO ELA AINDA ESTEJA VAZIA
    def inserir(self, chave): 
        if self.raiz is None: # se a raiz for vazia
            self.raiz = No(chave) # cria uma raiz
        else:
            self._inserir(self.raiz, chave) # caso contrário, aplicar _inserir passando a raiz e a chave
    
    # FUNÇÃO QUE INSERE NÓS NA ÁRVORE
    def _inserir(self, raiz, chave):
        if chave < raiz.chave: #se a chave for menor que o valor do nó pai do ciclo de execução atual, então
            if raiz.esquerda is None: # analisa se o filho esquerdo dele é vazio
                raiz.esquerda = No(chave) # se for, cria o filho esquerdo com o valor chave
            else: #se o filho esquerdo não for vazio então
                self._inserir(raiz.esquerda, chave) #_inserir é aplicado passando o filho esquerdo e a chave
        else: #se a chave for maior que o valor do nó pai do ciclo de execução atual
            if raiz.direita is None: #analisa se o filho direito dele é vazio
                raiz.direita = No(chave) #se for, cria o filho direito com o valor chave
            else: #se o filho direito não for vazio
                self._inserir(raiz.direita, chave) #_inserir é aplicado passando o filho direito e a chave
    
    # FUNÇÃO QUE ENCAPSULA A COMPLEXIDADE DE _EXCLUIR.
    def excluir(self, chave):
        self.raiz = self._excluir(self.raiz, chave) # raiz recebe retono de aplicação de _excluir passando a própria raiz e a chave
    
    # FUNÇÃO QUE EXCLUI NÓS
    def _excluir(self, raiz, chave):
        if raiz is None: #analisa se raiz(objeto NO do ciclo de execução atual) é vazia
            return raiz #se for, retorna raiz(o resultado da função é vazio, pois o nó não existe na árvore, ou árvore não possui nenhum nó, por isso retorna a própria raiz vazia)
        if chave < raiz.chave: #se a chave for menor que o valor do nó pai do ciclo de execução atual, então
            raiz.esquerda = self._excluir(raiz.esquerda, chave)#o filho esquerdo recebe retono de aplicação de _excluir passando o própro filho esquerdo e a chave
        elif chave > raiz.chave: #se a chave for maior que o valor do nó pai do ciclo de execução atual, então
            raiz.direita = self._excluir(raiz.direita, chave) #o filho direito recebe retono de aplicação de _excluir passando o própro filho direito e a chave
        else: #se a chave for igual ao valor do nó pai do ciclo de execução atual, então
            if raiz.esquerda is None: #analisa se o filho esquerdo é vazio
                return raiz.direita #se for, retorna o filho direito
            elif raiz.direita is None: # analisa se o filho direito é vazio
                return raiz.esquerda #se for, retorna o filho esquerdo
            temp = self._menor_no(raiz.direita) #se nenhum filho for vazio, cria uma variável temporária, que recebe o retorno de menor_no aplicado ao filho direito
            raiz.chave = temp.chave #o nó pai do ciclo de execução atual é substituído pelo nó pai de temp
            raiz.direita = self._excluir(raiz.direita, temp.chave) #o filho direito recebe o retorno de _excluir passando o próprio filho direito e o nó pai de temp)
        return raiz #retorna a raiz
    
    # FUNÇÃO QUE RETORNA O MENOR NÓ DA ÁRVORE, PASSANDO SEMPRE PELO O FILHO DA ESQUERDA, ATÉ CHEGAR NO NÓ MAIS A ESQUERDA DA ÁRVORE
    def _menor_no(self, raiz): 
        atual = raiz #atual recebe raiz(objeto NO do ciclo de execução atual)
        while atual.esquerda is not None: #enquanto o filho esquerdo de atual não for vazio
            atual = atual.esquerda #atual recebe o filho esquerdo do próprio atual
        return atual #após o fim do while, o menor nó é retornado
    # FUNÇÃO QUE ENCAPSULA A COMPLEXIDADE DE _BUSCAR.
    def buscar(self, chave):
        return self._buscar(self.raiz, chave) # raiz(objeto NO do ciclo de execução atual) recebe retono de aplicação de _buscar passando a própria raiz e a chave
    
    # FUNÇÃO QUE RETORNA UM NÓ EXISTENTE NA ÁRVORE
    def _buscar(self, raiz, chave):
        if raiz is None or raiz.chave == chave: #se o raiz (objeto NO do ciclo de execução atual) for vazio ou o nó pai dele for igual a chave, retorna A raiz
            return raiz
        if chave < raiz.chave: # se a chave for menor que o nó pai da raiz(objeto NO do ciclo de execução atual) então
            return self._buscar(raiz.esquerda, chave) #retorna o retorno de aplicação de _buscar passando o filho esquerdo e a chave
        return self._buscar(raiz.direita, chave) # se a chave for maior que o nó pai da raiz(objeto NO do ciclo de execução atual), retorna o retorno de aplicação de _buscar passando o filho esquerdo e a chave
    
    # FUNÇÃO QUE ENCAPSULA A COMPLEXIDADE DE _CONTA_NOS 
    def contar_nos(self):
        return self._contar_nos(self.raiz) # retona aplicação de _conta_nos passando a própria raiz
    
    # FUNÇÃO QUE CONTA OS NÓS DE UMA ÁRVORE
    def _contar_nos(self, raiz):
        if raiz is None: #se o raiz (objeto NO do ciclo de execução atual) for vazio então
            return 0 # retorne 0(indica que chegou a uma extremidade dá árvore e a pilha da recursão já pode fazer o caminho de volta)
        return 1 + self._contar_nos(raiz.esquerda) + self._contar_nos(raiz.direita) # EXPLICACAO RECURSÃO: ao final da recursão, 
    #a função vai ter olhado toda a sub-árvore da esquerda a toda a sub-árvore da direita e vai ter somado 1 para cada nó em que ela passou.
    # Ou seja, na recursão, cada função retorna 1 ou 0 pra função "de cima", que a chamou, até que no fim o primeiro return seja executado, 
    # que é o que retornará a soma total. 
    
    # FUNÇÃO QUE ENCAPSULA A COMPLEXIDADE DE _CONTA_NAO_FOLHAS
    def contar_nao_folhas(self):
        return self._contar_nao_folhas(self.raiz) # retona aplicação de _conta_nao_folhas passando a própria raiz
    
    # FUNÇÃO QUE CONTA OS NÓS NÃO FOLHA DE UMA ÁRVORE
    def _contar_nao_folhas(self, raiz):
        if raiz is None or (raiz.esquerda is None and raiz.direita is None): #se a raiz (objeto NO do ciclo de execução atual) ou seus dois filhos forem vazio, então
            return 0 # retorna 0, indicando que chegou a um nó folha, que não deve ser contado
        return 1 + self._contar_nao_folhas(raiz.esquerda) + self._contar_nao_folhas(raiz.direita)# # EXPLICACAO RECURSÃO:
        #funciona pois todos os antecessores dos nós folhas serão nós não folhas, que retornam 1. Lógica da recursão é a mesma da de conta_nos
    

# A CLASSE NOGENERICO REPRESENTA O CONJUNTO FORMADO PELO VALOR DE UM NÓ PAI(CHAVE) 
# E SEUS FILHOS, QUE SÃO UMA LISTA DE OBJETOS DA CLASSE NOGENERICO
# (ASSIM O NÓ RAIZ TEM SUA LISTA DE FILHOS E CADA FILHO TEM SUA LISTA DE FILHOS E ASSIM POR DIANTE...)
class NoGenerico:
    def __init__(self, chave):
        self.chave = chave
        self.filhos = []


class ArvoreGenerica:
    #INICIALIZA UMA ÁRVORE GENÉRICA COM RAIZ VAZIA. RAIZ É O ATRIBUTO QUE ARMAZENA UM OBJETO NÓ QUE É O COMEÇO DÁ ÁRVORE.
     #(ENTÃO NA REAL ELA ARMZENA TODOS OS NÓS, PORQUE UM PAI LEVA AO FILHO QUE LEVA AO FILHO DO FILHO E ASSIM POR DIANTE...)
    def __init__(self):
        self.raiz = None

    # FUNÇÃO QUE INSERE NÓS NA ÁRVORE E INTERAGE COM A INTERFACE
    def inserir(self, chave, chave_pai=None):
        if self.buscar(self.raiz, chave) is not None: # se a aplicação de buscar passando a raiz e a chave não retornar vazio, então
            messagebox.showerror("Erro", "Valor já existe na árvore.") #quer dizer que o valor já existe na árvore
        
        # variável novo_no recebe um no criado com a chave
        novo_no = NoGenerico(chave)
        
        if self.raiz is None: # se raiz for vazia, então
            self.raiz = novo_no # faça o novo nó ser a raiz e
            return # retorne vazio
        
        if chave_pai is None: # se a chave do nó pai não for informada então
            messagebox.showerror("Erro", "A árvore já tem uma raiz. Especifique um nó pai.") #avise que ela deve ser informada
            return
        
        pai = self.buscar(self.raiz, chave_pai) # tendo sido informada a chave_pai, a variável pai recebe o retorno de buscar passando a raiz e a chave_pai
        if pai: #se pai não for vazio, então
            pai.filhos.append(novo_no) #pai adota novo_no pra sua lista de filhos
        else: #se pai for vazio então
            messagebox.showerror("Erro", "Nó pai não encontrado.")#informa que o pai não foi encontrado
    
    #FUNÇÃO QUE RETORNA UM NÓ EXISTENTE NA ÁRVORE
    def buscar(self, raiz, chave):
        if raiz is None: #se a raiz(objeto NOGENERICO do ciclo de execução atual) for vazia, retorne vazio.
            return None
        if raiz.chave == chave: #se o valor do nó pai da raiz(objeto NOGENERICO do ciclo de execução atual), foi igual a chave, então
            return raiz #retorne a raiz(objeto NOGENERICO do ciclo de execução atual)
        for filho in raiz.filhos:#se os ifs forem pulados, entra um for,
            encontrado = self.buscar(filho, chave) # que aplica a função buscar passando nela cada filho e o valor da chave,
            if encontrado: #até que o filho com chave correspondente seja encontrado
                return encontrado
        return None # caso o ñ seja encontrado um filho com chave correspondente, retorna vazio

    # FUNÇÃO QUE ENCAPSULA A COMPLEXIDADE DE _CONTA_NOS
    def contar_nos(self):
        return self._contar_nos(self.raiz)
    
    # FUNÇÃO QUE CONTA OS NÓS DE UMA ÁRVORE
    def _contar_nos(self, raiz):
        if raiz is None: #se o raiz (objeto NOGENERICO do ciclo de execução atual) for vazio então
            return 0 # retorne 0(indica que chegou a uma extremidade dá árvore e a pilha da recursão já pode fazer o caminho de volta)
        total = 1 # esse 1 é o nó raiz, que fará parte da soma
        for filho in raiz.filhos: # para cada filho de raiz(objeto NOGENERICO do ciclo de execução atual)
            total += self._contar_nos(filho) #faça total receber o retorno de conta_nos passando o filho
        return total # cada função retorna 1 ou 0 pra função "de cima", que a chamou, até que no fim o primeiro return seja executado, 
    # que é o que retornará a soma total. 
    
    # FUNÇÃO QUE ENCAPSULA A COMPLEXIDADE DE _CONTA_NAO_FOLHAS
    def contar_nao_folhas(self):
        return self._contar_nao_folhas(self.raiz)
    
    # FUNÇÃO QUE CONTA NÓS NÃO FOLHA
    def _contar_nao_folhas(self, raiz):
        if raiz is None or len(raiz.filhos) == 0: #se a raiz (objeto NOGENERICO do ciclo de execução atual) ou sua lista de filhos for vazio, então
            return 0 # retorna 0, indicando que chegou a um nó folha, que não deve ser contado
        total = 1 # esse 1 é o nó raiz, que fará parte da soma, já que é um nó não folha(o if teria pego ele se fosse nó folha)
        for filho in raiz.filhos: # para cada filho de raiz(objeto NOGENERICO do ciclo de execução atual)
            total += self._contar_nao_folhas(filho) #faça total receber o retorno de conta_nao_folhas passando o filho
        return total # cada função retorna 1 ou 0 pra função "de cima", que a chamou, até que no fim o primeiro return seja executado, 
    # que é o que retornará a soma total.

class Interface:
    def __init__(self, root):
        self.arvore_binaria = Arvore()  # Inicializa uma árvore binária
        self.arvore_generica = ArvoreGenerica()  # Inicializa uma árvore genérica
        self.root = root  # A variável root representa a janela principal do Tkinter
        self.root.title("Árvore")  # Define o título da janela

        self.tipo_arvore = tk.StringVar(value="binaria")  # Cria uma variável para controlar o tipo de árvore (binária ou genérica)
        
        # Criação de dois botões de opção (radiobuttons) para selecionar entre árvore binária e genérica
        self.radio_binaria = tk.Radiobutton(root, text="Árvore Binária", variable=self.tipo_arvore, value="binaria")
        self.radio_binaria.pack()
        
        self.radio_generica = tk.Radiobutton(root, text="Árvore Genérica", variable=self.tipo_arvore, value="generica")
        self.radio_generica.pack()

        # Entrada para inserir valores
        self.entrada = tk.Entry(root)
        self.entrada.pack()
        
        # Botões para interação com a árvore
        self.botao_inserir = tk.Button(root, text="Inserir", command=self.adicionar_valor)
        self.botao_inserir.pack()
        
        self.botao_remover = tk.Button(root, text="Remover", command=self.remover_valor)
        self.botao_remover.pack()
        
        self.botao_localizar = tk.Button(root, text="Localizar", command=self.localizar_valor)
        self.botao_localizar.pack()
        
        # Rótulo para mostrar contagem de nós e nós não-folhas
        self.contagem_label = tk.Label(root, text="Nós: 0 | Não-folhas: 0")
        self.contagem_label.pack()
    
    def atualizar_contagem(self):
        # Atualiza a contagem de nós e não-folhas com base no tipo de árvore selecionado
        if self.tipo_arvore.get() == "binaria":
            total_nos = self.arvore_binaria.contar_nos()
            total_nao_folhas = self.arvore_binaria.contar_nao_folhas()
        else:
            total_nos = self.arvore_generica.contar_nos()
            total_nao_folhas = self.arvore_generica.contar_nao_folhas()
        
        # Atualiza o rótulo de contagem na interface
        self.contagem_label.config(text=f"Nós: {total_nos} | Não-folhas: {total_nao_folhas}")
    
    def adicionar_valor(self):
        try:
            if self.tipo_arvore.get() == "binaria":
                valor = int(self.entrada.get())  # Obtém o valor inserido na entrada de texto
                if self.arvore_binaria.buscar(valor) is not None:  # Verifica se o valor já existe na árvore
                    raise ValueError
                self.arvore_binaria.inserir(valor)  # Insere o valor na árvore binária
            else:
                valores = self.entrada.get().split(',')  # Para a árvore genérica, insere o valor e chave do pai
                valor = int(valores[0])  # O valor do nó
                chave_pai = int(valores[1]) if len(valores) > 1 else None  # A chave do nó pai (se fornecida)
                
                if chave_pai is not None and self.arvore_generica.buscar(self.arvore_generica.raiz, chave_pai) is None:
                    raise ValueError
                
                self.arvore_generica.inserir(valor, chave_pai)  # Insere na árvore genérica
            
            # Atualiza a contagem de nós e desenha a árvore após a inserção
            self.atualizar_contagem()
            self.desenhar_arvore()
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor válido no formato correto")
    
    def remover_valor(self):
        try:
            valor = int(self.entrada.get())  # Obtém o valor a ser removido
            if self.tipo_arvore.get() == "binaria":
                self.arvore_binaria.excluir(valor)  # Remove o valor da árvore binária
            else:
                messagebox.showerror("Erro", "Remoção não suportada para árvore genérica")
            
            # Atualiza a contagem de nós e desenha a árvore após a remoção
            self.atualizar_contagem()
            self.desenhar_arvore()
        except ValueError:
            messagebox.showerror("Erro", "Digite um número")
    
    def localizar_valor(self):
        try:
            valor = int(self.entrada.get())  # Obtém o valor a ser localizado
            if self.tipo_arvore.get() == "binaria":
                no_encontrado = self.arvore_binaria.buscar(valor)  # Busca o valor na árvore binária
                if no_encontrado:
                    messagebox.showinfo("Resultado da pesquisa", "Valor encontrado na árvore.")
                    self.desenhar_arvore_destacado(no_encontrado.chave)  # Desenha a árvore destacando o nó encontrado
                else:
                    messagebox.showinfo("Resultado da pesquisa", "Valor não encontrado na árvore.")
            else:
                no_encontrado = self.arvore_generica.buscar(self.arvore_generica.raiz, valor)  # Busca o valor na árvore genérica
                if no_encontrado:
                    messagebox.showinfo("Resultado da pesquisa", "Valor encontrado na árvore.")
                    self.desenhar_arvore_destacado(no_encontrado.chave)
                else:
                    messagebox.showinfo("Resultado da pesquisa", "Valor não encontrado na árvore.")
        except ValueError:
            messagebox.showerror("Erro", "Digite um número")
    
    def adicionar_arestas(self, raiz, G, pos, x=0, y=0, layer=1):
        # Função recursiva para adicionar arestas (conexões) entre os nós da árvore
        if raiz is not None:
            G.add_node(raiz.chave, pos=(x, y))  # Adiciona um nó ao gráfico
            if isinstance(raiz, No):
                # Para árvore binária, conecta os nós à esquerda e à direita
                if raiz.esquerda is not None:
                    G.add_edge(raiz.chave, raiz.esquerda.chave)
                    self.adicionar_arestas(raiz.esquerda, G, pos, x - 1 / layer, y - 1, layer + 1)
                if raiz.direita is not None:
                    G.add_edge(raiz.chave, raiz.direita.chave)
                    self.adicionar_arestas(raiz.direita, G, pos, x + 1 / layer, y - 1, layer + 1)
            elif isinstance(raiz, NoGenerico):
                # Para árvore genérica, conecta todos os filhos do nó
                for i, filho in enumerate(raiz.filhos):
                    G.add_edge(raiz.chave, filho.chave)
                    self.adicionar_arestas(filho, G, pos, x + (i - len(raiz.filhos) / 2) / layer, y - 1, layer + 1)
    
    def desenhar_arvore(self, no_destacado=None):
        # Função para desenhar a árvore utilizando o `matplotlib` e `networkx`
        plt.close('all')
        G = nx.DiGraph()  # Cria um gráfico direcionado
        if self.tipo_arvore.get() == "binaria":
            self.adicionar_arestas(self.arvore_binaria.raiz, G, {})  # Adiciona as arestas da árvore binária
        else:
            self.adicionar_arestas(self.arvore_generica.raiz, G, {})  # Adiciona as arestas da árvore genérica
        
        pos = nx.get_node_attributes(G, 'pos')  # Obtém as posições dos nós
        plt.figure(figsize=(8, 5))  # Define o tamanho da figura
        # Define as cores dos nós: vermelho para o nó destacado
        node_colors = ['lightblue' if node != no_destacado else 'red' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=10, font_weight='bold')  # Desenha a árvore
        plt.show()  # Exibe o gráfico
    
    def desenhar_arvore_destacado(self, chave):
        # Função que desenha a árvore destacando o nó com a chave fornecida
        self.desenhar_arvore(no_destacado=chave)

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
