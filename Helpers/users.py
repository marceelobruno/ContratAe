from DataStructures.ListaSequencialNumPY import Lista
from vaga import Vaga

class Recrutador:
    def __init__(self, nome: str, email: str, senha: str, cpf: str, nome_empresa = None):
        self.__nome = nome
        self.__email = email
        self.__nome_empresa = nome_empresa
        self.__senha = senha
        self.__cpf = cpf

    @property
    def nome(self):
        return self.__nome

    @property
    def cpf(self):
        return self.__cpf
    
    @property
    def senha(self):
        return self.__senha
    
    def criar_vaga(self, nome, area, descricao, quantidade, salario, requisitos):
        return Vaga(
            nome, area, descricao, quantidade, self.__nome_empresa, salario, requisitos
        )

    def dict_user(self):
        user_dict = {
            "nome": self.__nome,
            "email": self.__email,
            "cpf": self.__cpf,
            "nome_empresa": self.__nome_empresa
        }

        return user_dict

    def deletar_vaga(self):
        pass

    def __str__(self) -> str:  # <---------Opção Ver perfil do menu do cliente.
        return f"""
        Nome: {self.__nome}                         CPF: {self.__cpf}
        Email: {self.__email}
        Empresa: {self.__nome_empresa}
        Senha: {self.__senha}
"""
class Candidato:
    def __init__(
        self,
        nome: str,
        email: str,
        senha: str,
        cpf: str,
        skills: list = None,
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
        self.__vagas_aplicadas = []

    @property
    def nome(self):
        return self.__nome
    
    @property
    def senha(self):
        return self.__senha

    @property
    def vagas_aplicadas(self):
        return self.__vagas_aplicadas

    @property
    def cpf(self):
        return self.__cpf


    def candidatar(self, vaga: Vaga):#<-----em análise
        return self.__vagas_aplicadas.append(vaga)
    
    def ver_candidaturas(self)->None:
        """Mostra as candidaturas efetuadas pelo candidato.
        """
        return self.__vagas_aplicadas
            
    
    def cancelar_candidatura(self,key:str) -> None: #<----------APLICAR TRATAMENTO DE ERRO!!
        """Remove a vaga especifíca da lista de vagas aplicadas. 

        Args:
            key (str): Atributo nome do objeto Vaga. 

        Returns:
            None
        """
        for i in range(len(self.__vagas_aplicadas)):
            if self.__vagas_aplicadas[i].nome == key:
                posicao = i
                break
        self.__vagas_aplicadas.pop(posicao)
    
    def criar_perfil(self, skills:list, area:str, descricao:str, cidade:str, uf:str ):#<-----em análise
        self.__skills = skills
        self.__area = area
        self.__descricao = descricao
        self.__cidade = cidade
        self.__uf = uf
        
    def perfil_completo(self):
        if self.__skills and self.__area and self.__descricao:
            return True
        else:
            return False
    
    def dict_user(self):
        user_dict = {
            "nome": self.__nome,
            "email": self.__email,
            "cpf": self.__cpf,
            "skills": self.__skills,
            "area": self.__area,
            "descricao": self.__descricao,
            "cidade": self.__cidade,
            "uf": self.__uf,
        }

        return user_dict

    def __str__(self) -> str:  # <---------Opção Ver perfil do menu do cliente.
        return f"""
        Nome: {self.__nome}                         
        CPF: {self.__cpf}
        Email: {self.__email}
        Skills: {self.__skills}
        Area: {self.__area}
        Descricao: {self.__descricao}
        Cidade: {self.__cidade}
        Uf: {self.__uf} 
""" 
    


if __name__ == "__main__":
    c = Candidato('luiz','lf',1234,100)
    # c.vagas_aplicadas.append('casa')
    # c.vagas_aplicadas.append('predio')
    # c.vagas_aplicadas.append('ifpb')
    # print(c.ver_candidaturas())
    # c.cancelar_candidatura('predio')
    # print(c.ver_candidaturas())
    c.criar_perfil(['bahia','city','flamengo'])
    print(c)