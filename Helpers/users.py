from DataStructures.ListaSequencialNumPY import Lista
from vaga import Vaga

class Recrutador:
    def __init__(self, nome, nome_empresa, senha, cpf):
        self.__nome = nome
        self.__nome_empresa = nome_empresa
        self.__senha = senha
        self.__cpf = cpf

    @property
    def nome(self):
        return self.__nome

    @property
    def cpf(self):
        return self.__cpf
    
    def criar_vaga(self, nome, area, descricao, limite, salario, requisitos):
        return Vaga(
            nome, area, descricao, limite, self.__nome_empresa, salario, requisitos
        )

    def deletar_vaga(self):
        pass

class Candidato:
    def __init__(
        self,
        nome: str,
        email: str,
        senha: str,
        cpf: str,
        skills: str = None,
        area: str = None,
        descricao: str = None,
        cidade: str = None,
        uf: str = None,
    ):
        self.__nome = nome
        self.__email = email
        self.__senha = senha
        self.__cpf = cpf

        self.__skills = skills  # [None]
        self.__area = area  # ""
        self.__descricao = descricao  # ""
        self.__cidade = cidade  # ""
        self.__uf = uf  # ""
        self.__id = ""  # <----Adicionar no servidor
        self.__vagas_aplicadas = Lista()

    @property
    def nome(self):
        return self.__nome

    @property
    def vagas_aplicadas(self):
        return self.__vagas_aplicadas

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value


    def ver_vagas(self): # <---servidor
        pass

    def candidatar(self, vaga: Vaga):
        return self.__vagas_aplicadas.append(vaga)

    def ver_candidaturas(self):
        return self.__vagas_aplicadas  # <----Printar o objeto inteiro ou só o nome?

    def cancelar_candidatura(self, key):  # <----------APLICAR TRATAMENTO DE ERRO!!
        posicao = self.__vagas_aplicadas.busca(key)
        return self.__vagas_aplicadas.remover(posicao)

    def criar_perfil(
        self, skills: list, area: str, descricao: str, cidade: str, uf: str
    ):
        self.__skills = skills
        self.__area = area
        self.__descricao = descricao
        self.__cidade = cidade
        self.__uf = uf

    def __str__(self) -> str:  # <---------Opção Ver perfil do menu do cliente.
        return f"""
        Nome: {self.__nome}                         CPF: {self.__cpf}
        Email: {self.__email}
        Senha: {self.__senha}
        Skills: {self.__skills}
        Area: {self.__area}
        Descricao: {self.__descricao}
        Cidade: {self.__cidade}
        Uf: {self.__uf} 
        skills:{self.__skills}

""" 
    


if __name__ == "__main__":
    c = Candidato("luiz", "lf", 1234, 100)
    # c.vagas_aplicadas.append('casa')
    # c.vagas_aplicadas.append('predio')
    # c.vagas_aplicadas.append('ifpb')
    # print(c.ver_candidaturas())
    # c.cancelar_candidatura('predio')
    # print(c.ver_candidaturas())
    c.criar_perfil(["bahia", "city", "flamengo"])
    print(c)
