import random

class Recrutador:
    def __init__(self, nome, nome_empresa, senha, nome_usuario):
        self.__nome = nome
        self.__nome_empresa = nome_empresa
        self.__senha = senha
        self.__usuario = nome_usuario
        
    def criar_vaga(self):
        pass
    
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
    
    def ver_vagas(self):
        pass
    
    def candidatar(self):
        pass
    
    def ver_candidaturas(self):
        pass
    
    def cancelar_candidatura(self):
        pass
    
    def editar_perfil(self):
        pass
    
    def __gerar_ID(self):
        pass
    
    def __str__(self) -> str:
        return f"Nome:{self.__nome} email: {self.__email}"