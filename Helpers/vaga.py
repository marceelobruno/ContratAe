# from users import Candidato
from DataStructures.ListaSequencialNumPY import Lista

class Vaga:
    def __init__(self, nome, area, descricao, limite:int, nome_empresa, salario, requisitos):
        self.__nome = nome
        self.__area = area
        self.__descricao = descricao
        self.__limite = limite
        self.__nome_empresa = nome_empresa
        self.__salario = salario
        self.__requisitos = requisitos
        self.__lista_candidaturas = Lista() #lista do professor vulgo Alex
    
    @property
    def nome(self):
        return self.__nome
    
    def adicionarCandidatura(self,candidato):
        self.__lista_candidaturas.append(candidato.nome)

    def mostrarCandidaturas(self):
        return self.__lista_candidaturas
    
    def __str__(self) -> str:
        return f""" 
------------------------------------
    Nome: {self.__nome}
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
