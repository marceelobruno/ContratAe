# from users import Candidato
from DataStructures.ListaSequencialNumPY import Lista
import random
class Vaga:
    def __init__(self, nome, area, descricao, quantidade:int, nome_empresa, salario, requisitos):
        self.__nome = nome
        self.__id = random.randint(1,9999) 
        self.__area = area
        self.__descricao = descricao
        self.__quantidade = quantidade
        self.__nome_empresa = nome_empresa
        self.__salario = salario
        self.__requisitos = requisitos
        self.__lista_candidaturas = []  # lista do professor vulgo Alex
    
    @property
    def nome(self):
        return self.__nome
    @property
    def id(self):
        return self.__id
    @property
    def lista_candidaturas(self):
        return self.__lista_candidaturas
    
    def adicionarCandidatura(self,candidato):
        self.__lista_candidaturas.append(candidato)
        self.__quantidade -=1
    
    def removerCandidatura(self,key):
        self.__lista_candidaturas.pop(key)
        self.__quantidade +=1

    def gerarID(self):
        self.__id = random.randint(1,9999)


    def mostrarCandidaturas(self):
        return self.__lista_candidaturas
    
    def vagaEstaCheia(self):
        return self.__quantidade == 0
    
    def dict_vaga(self):
        vaga_dict =  {
            "nome": self.__nome,
            "area": self.__area,
            "id": self.__id,
            "descricao": self.__descricao,
            "quantidade": self.__quantidade,
            "nome_empresa": self.__nome_empresa,
            "salario": self.__salario,
            "requisitos": self.__requisitos,
            "lista_candidaturas": self.__lista_candidaturas
        }
        return vaga_dict
        
    
    def __str__(self) -> str:
        return f"""
------------------------------------
    Nome: {self.__nome}
    ID: {self.__id}
    Area: {self.__area}
    Empresa: {self.__nome_empresa} 
    Requisitos: {self.__requisitos}

    Salario: {self.__salario}
    Quantidade de Vagas: {self.__quantidade}
    Descrição: {self.__descricao}
------------------------------------
"""
    
if __name__ == '__main__':
    v = Vaga('tsi','ti','adf',10,'hsdfiuwshgf','fhwiufhw', 'hhdsgf')
    # c = Candidato('luiz','lf','1234')
    # d = Candidato('lucas','lf','1234')
    # e = Candidato('marcelo','lf','1234')
    # f = Candidato('bruno','lf','1234')
    # v.adicionarCandidatura(c)
    # v.adicionarCandidatura(d)
    # v.adicionarCandidatura(e)
    # v.adicionarCandidatura(f)
    # print(v.mostrarCandidaturas())
    print(v)
    v.gerarID()
    print(v)
