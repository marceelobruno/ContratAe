import random
import time
from vaga import Vaga

class Recrutador:
    def __init__(self, nome, nome_empresa, senha, nome_usuario):
        self.__nome = nome
        self.__nome_empresa = nome_empresa
        self.__senha = senha
        self.__usuario = nome_usuario
    
    @property
    def nome(self):
        return self.__nome
    @property
    def usuario(self):
        return self.__usuario
    
    def criar_vaga(self, nome, area, descricao, limite, salario, requisitos):
        return Vaga(nome,area,descricao,limite, self.__nome_empresa, salario, requisitos )
        
    
    def deletar_vaga(Self):
        pass
    
class Candidato:
    def __init__(self, nome, email, senha):
        self.__nome = nome
        self.__email = email
        self.__senha = senha
        
        self.__skills = [None]
        self.__area = None
        self.__descricao = None
        self.__cidade = None
        self.__uf = None
        self.__id = None
        self.__vagas_aplicadas = []
    
    @property
    def nome(self):
        return self.__nome

    def ver_vagas(self):
        pass
    # def candidatar(self, vaga: Vaga):
    #     pass
    
    def ver_candidaturas(self):
        return self.__vagas_aplicadas
        
    
    def cancelar_candidatura(self):
        pass
    
    def criar_perfil(self, skills:list, area, descricao, cidade, uf):
        pass
    
    # def __gerar_ID(self):
    #     self.__id = int(time.time())

    
    def __str__(self) -> str:
        return f"Nome:{self.__nome} email: {self.__email}"