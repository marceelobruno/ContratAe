# from users import Candidato
from DataStructures.ListaSequencialNumPY import Lista
import random

class Vaga:
    def __init__(self, nome, area, descricao, limite:int, nome_empresa, salario, requisitos):
        self.__nome = nome
        self.__id = random.randint(1,9999) 
        self.__area = area
        self.__descricao = descricao
        self.__limite = limite
        self.__nome_empresa = nome_empresa
        self.__salario = salario
        self.__requisitos = requisitos
        self.__lista_candidaturas = Lista(self.__limite) #lista do professor vulgo Alex
    
    @property
    def nome(self):
        return self.__nome
    @property
    def id(self):
        return self.__id
    
    def adicionarCandidatura(self,candidato):
        self.__lista_candidaturas.append(candidato.cpf)
        self.__limite += 1

    def mostrarCandidaturas(self):
        return self.__lista_candidaturas
    
    def vagaEstaCheia(self):
        return self.__lista_candidaturas.estaCheia()
    

    def dict_user(self):
        return {
            "nome": self.__nome,
            "area": self.__area,
            "descricao": self.__descricao,
            "limite": self.__limite,
            "nome_empresa": self.__nome_empresa,
            "salario": self.__salario,
            "requisitos": self.__requisitos,
            "lista_candidaturas": self.__lista_candidaturas
        }

        return user_dict
    
    def __str__(self) -> str:
        return f""" 
------------------------------------
    Nome: {self.__nome}
    ID: {self.__id}
    Area: {self.__area}
    Empresa: {self.__nome_empresa}
    Requisitos: {self.__requisitos}

    Salario: {self.__salario}
    Limite de Vagas: {self.__limite}
    Descrição: {self.__descricao}
------------------------------------
"""
    
# if __name__ == '__main__':
#     v = Vaga('tsi','ti','adf','fsr','hsdfiuwshgf','fhwiufhw', 'hhdsgf')
#     c = Candidato('luiz','lf','1234')
#     d = Candidato('lucas','lf','1234')
#     e = Candidato('marcelo','lf','1234')
#     f = Candidato('bruno','lf','1234')
#     v.adicionarCandidatura(c)
#     v.adicionarCandidatura(d)
#     v.adicionarCandidatura(e)
#     v.adicionarCandidatura(f)
#     print(v.mostrarCandidaturas())
