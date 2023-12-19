# from users import Candidato
import random

# from DataStructures.ListaSequencialNumPY import Lista


class Vaga:
    def __init__(self, nome, area, descricao, quantidade: int, nome_empresa, salario: float, requisitos):
        self.__nome = nome
        self.__id = random.randint(1, 99999)
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

    @property
    def quantidade(self):
        return self.__quantidade

    def adicionarCandidatura(self, candidato):
        self.__lista_candidaturas.append(candidato)
        self.__quantidade -= 1

    # def removerCandidatura(self, key):
    #     self.__lista_candidaturas.pop(key)
    #     self.__quantidade += 1

    # def gerarID(self):
    #     self.__id = random.randint(1, 9999)

    def aumentar_quantidade(self):
        self.__quantidade += 1

    # def mostrarCandidaturas(self):
    #     return self.__lista_candidaturas

    def vagaEstaCheia(self):
        """
        Este método confere se a quantidade de vagas disponíveis 
        estão esgotadas.

        Returns:
            Boolean: Retorna True se estiver cheia, False se não
        """
        return self.__quantidade == 0

    def dict_vaga(self):
        """
        Esse método transforma os dados da vaga em um dicionário.
        Ele é necessário desde que não é possível converter o objeto 
        Vaga( assim como Candidato e Recrutador ) em json.

        Returns:
            dict : o objeto em forma de dicionário 
        """
        vaga_dict = {
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

    def dict_vagaMOD(self):
        """
        Esse método faz a mesma coisa que o superior, mas ele omite 
        o atributo lista_candidaturas. Ao analisar os dados capturados no wireshark, 
        era possível ver o atributo lista_candidaturas (preenchido com as informações dos candidatos)
        trafegando na rede, aumentando o tamanho da mensagem e oferecendo certo perigo
        aos dados dos candidatos. 

        Returns:
            dict : o objeto em forma de dicionário
        """
        vaga_dict = {
            "nome": self.__nome,
            "area": self.__area,
            "id": self.__id,
            "descricao": self.__descricao,
            "quantidade": self.__quantidade,
            "nome_empresa": self.__nome_empresa,
            "salario": self.__salario,
            "requisitos": self.__requisitos,
        }
        return vaga_dict

    def __str__(self) -> str:
        return f"""
------------------------------------
    Nome: {self.__nome}
    ID: {self.__id}
    Área: {self.__area}
    Empresa: {self.__nome_empresa}
    Requisitos: {self.__requisitos}

    Salario: {self.__salario}
    Quantidade de Vagas: {self.__quantidade}
    Descrição: {self.__descricao}
------------------------------------
"""


if __name__ == '__main__':
    v = Vaga('tsi', 'ti', 'adf', 10, 'hsdfiuwshgf', 'fhwiufhw', 'hhdsgf')
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
    print(v)
