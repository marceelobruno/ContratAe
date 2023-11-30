import numpy as np

class ListaException(Exception):
    def __init__(self,mensagem):
        super().__init__(mensagem)


class Lista:
    """A classe Pilha implementa a estrutura de dados "Pilha".
       Técnica: <Encadeamento/Sequencial>
       A classe foi desenvolvida de maneira a permitir que qualquer tipo de dado
       seja armazenado como carga de um nó.

     Atributos:
     ---------------------
        *definir a lista de atributos*
    """
    def __init__(self, size:int=10):
        """ Construtor padrão da classe Pilha sem argumentos. Ao instanciar
            um objeto do tipo Pilha, esta iniciará vazia. 
        """
        self.__array = np.full(size,any,dtype=object)
        self.__posAtual = -1
        
    def estaVazia(self)->bool:
        """ Método que verifica se a pilha está vazia .

        Returns:
            boolean: True se a pilha estiver vazia, False caso contrário.

        Examples:
            p = Pilha()
            ...   # considere que temos internamente na pilha [10,20,30,40]<- topo
            if(p.estaVazia()): 
               # instrucoes quando a pilha estiver vazia
        """
        return self.__posAtual == -1

    def estaCheia(self)->bool:
        """ Método que verifica se a pilha está vazia .

        Returns:
            boolean: True se a pilha estiver vazia, False caso contrário.

        Examples:
            p = Pilha()
            ...   # considere que temos internamente na pilha [10,20,30,40]<- topo
            if(p.estaVazia()): 
               # instrucoes quando a pilha estiver vazia
        """
        return self.__posAtual == len(self.__array)-1


    def __len__(self)->int:
        """ Método que retorna a quantidade de elementos existentes na pilha

        Returns:
            int: um número inteiro que determina o número de elementos existentes na pilha

        Examples:
            p = Pilha()
            ...   # considere que temos internamente a pilha [10,20,30,40]<- p
            print (p.tamanho()) # exibe 4
        """ 
        return self.__posAtual + 1

    def elemento(self, posicao:int)->any:
        """ Método que recupera a carga armazenada em um determinado elemento da pilha

        Args:
            posicao (int): um número correpondente à ordem do elemento existente.
                           Sentido: da base em direção ao topo
        
        Returns:
            Any: a carga armazenada no elemento correspondente à posição indicada.

        Raises:
            PilhaException: Exceção lançada quando uma posição inválida é
                  fornecida pelo usuário. São inválidas posições que se referem a:
                  (a) números negativos
                  (b) zero
                  (c) número natural correspondente a uma posição  que excede a
                      quantidade de elementos da lista.                      
        Examples:
            p = Pilha()
            ...   # considere que temos internamente a pilha [10,20,30,40]<-topo
            posicao = 5
            print (p.elemento(3)) # exibe 30
        """
        try:
            assert self.estaVazia() == False, 'Lista está vazia'
            assert posicao > 0 and posicao <= len(self), f'Posição {posicao} é inválida para a lista com {len(self)} elementos'
            return self.__array[posicao-1]
        except AssertionError as ae:
            raise ListaException(ae)
                
    def busca(self, key:any)->int:
        """ Método que retorna a posicao ordenada, dentro da pilha, em que se
            encontra uma chave passado como argumento. No caso de haver mais de uma
            ocorrência do valor, a primeira ocorrência será retornada.
            O ordenamento que determina a posição é da base para o topo.

        Args:
            key (any): um item de dado que deseja procurar na pilha
        
        Returns:
            int: um número inteiro representando a posição, na pilha, em que foi
                 encontrada a chave.

        Raises:
            PilhaException: Exceção lançada quando o argumento "key"
                  não está presente na pilha.

        Examples:
            p = Pilha()
            ...   # considere que temos internamente a lista [10,20,30,40]<-topo
            print (p.elemento(40)) # exibe 4
        """
        for i in range(len(self)):
            if self.__array[i] == key:
                return i+1
        raise ListaException(f'A chave {key} não está presente na lista')


    def inserir(self, posicao:int, carga:any):
        """ Método que adiciona um novo elemento ao topo da pilha

        Args:
            carga (any): a carga que será armazenada no novo elemento do topo da pilha.

        Examples:
            p = Pilha()
            ...   # considere a pilha  [10,20,30,40]<-topo
            p.empilha(50)
            print(p)  # exibe [10,20,30,40,50]
        """
        try:
            assert not self.estaCheia(), 'Lista está cheia'
            assert posicao > 0 and posicao <= len(self)+1, f'Posição {posicao} é inválida para a lista com {len(self)} elementos'
            
            for i in range(self.__posAtual+1,posicao-1 ,-1):
                self.__array[i] = self.__array[i-1]
            self.__array[posicao-1] = carga
            self.__posAtual += 1

        except AssertionError as ae:
            raise ListaException(ae)


    def append(self, carga:any):
        self.inserir(len(self)+1, carga)


    def remover(self, posicao:int)->any:
        """ Método que remove um elemento do topo da pilha e retorna
            sua carga correspondente.
    
        Returns:
           any: a carga armazenada no elemento removido

        Raises:
            PilhaException: Exceção lançada quando se tenta remover algo de uma pilha vazia
                    
        Examples:
            p = Pilha()
            ...   # considere a pilha [10,20,30,40]<-topo
            dado = p.desemplha()
            print(p) # exibe [10,20,30]
            print(dado) # exibe 40
        """
        try:
            assert not self.estaVazia(), 'Lista está vazia'
            assert posicao > 0 and posicao <= len(self), f'Posição {posicao} é inválida para a lista com {len(self)} elementos'

            carga = self.__array[posicao-1]

            for i in range(posicao-1, len(self)-1):
                self.__array[i] = self.__array[i+1]


            self.__posAtual -= 1
            return carga
        except AssertionError as ae:
            raise ListaException(ae)

        

        
    def __str__(self)->str:
        """ Método que retorna a ordenação atual dos elementos da pilha, do
            topo em direção à base

        Returns:
           str: a carga dos elementos da pilha, do topo até a base
        """  
        s = 'inicio->[ '
        for i in range(len(self)):
            s += f'{self.__array[i]}, '
        s = s.rstrip(', ')
        s += ' ]'
        return s

        

 
