from users import Candidato

class Vaga:
    def __init__(self, nome, area, descricao, limite, nome_empresa, salario, requisitos):
        self.__nome = nome
        self.__area = area
        self.__descricao = descricao
        self.__limite = limite
        self.__nome_empresa = nome_empresa
        self.__salario = salario
        self.__requisitos = requisitos
        self.__lista_candidaturas = [] #lista do professor vulgo Alex
        
    @property
    def candidatura(self):
        return self.__lista_candidaturas
    
    @candidatura.setter
    def candidatura(Self, candidato: Candidato):
        pass
    
    def __str__(self) -> str:
        pass
    
    