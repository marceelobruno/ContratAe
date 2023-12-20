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
    def empresa(self):
        return self.__nome_empresa
    
    @property
    def senha(self):
        return self.__senha
    
    def criar_vaga(self, nome:str, idVaga, area:str, descricao:str, quantidade:int, empresa:str, salario:float, requisitos:list):
        """
        Método responsável por criar um objeto Vaga no servidor.
        Recebe os parâmetros do objeto Vaga e retorna o próprio objeto. 

        Args:
            nome (str): nome da vaga.
            idVaga (int): id da vaga.
            area (str): area da vaga.
            descricao (str): descrição da vaga.
            quantidade (int): quantidade de candidaturas aceitas na vaga.
            empresa (str): empresa associada a vaga.
            salario (float): salário apresentado na vaga.
            requisitos (list): requisitos prévios na vaga.

        Returns:
            Vaga: Retorna o objeto Vaga. 
        """
        return Vaga(
            nome, self.__cpf, idVaga, area, descricao, quantidade, empresa, salario, requisitos
        )

    def dict_user(self):
        """
        Método que traduz as informações do recrutador para 
        dicionário.

        Returns:
            dict: Informações do objeto Recrutador em um 
            dicionário.
        """
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
        Nome: {self.__nome}                         
        CPF: {self.__cpf}
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


    def candidatar(self, vaga:dict) -> None:#<-----em análise
        """
        Método qua adiciona uma vaga (em formato de dicionário)
        na lista de vagas aplicadas do candidato.

        Args:
            vaga (dict): vaga em formato de dicionário.
        """
        self.__vagas_aplicadas.append(vaga)
    
    def ver_candidaturas(self)->None:
        """Mostra as candidaturas efetuadas pelo candidato.
        """
        return self.vagas_aplicadas

    def cancelar_candidatura(self,elemento:dict) -> None: #<----------APLICAR TRATAMENTO DE ERRO!!
        """Remove a vaga especifíca da lista de vagas aplicadas. 

        Args:
            elemento (any): dicionário vaga a ser retirado da
            lista de vagas aplicadas. 

        Returns:
            None
        """
        self.vagas_aplicadas.remove(elemento)
    
    def criar_perfil(self, skills:list, area:str, descricao:str, cidade:str, uf:str )->None:
        """
        Método que adiciona as informações secundárias ao 
        perfil do candidato.

        Args:
            skills (list): lista de competências do candidato.
            area (str): area que o candidato almeija a vaga.
            descricao (str): breve descricao sobre o candidato.
            cidade (str): cidade que o candidato reside.
            uf (str): estado que o candidato reside.
        """
        self.__skills = skills
        self.__area = area
        self.__descricao = descricao
        self.__cidade = cidade
        self.__uf = uf
        
    def perfil_completo(self):
        """
        Método que verifica se o perfil do candidato contém
        as informações secundárias.

        Returns:
            True: Se os atributos forem diferentes de None.
            False: Se os atributos forem None.
        """
        if self.__skills != None and self.__area != None and self.__descricao != None:
            return True
        else:
            return False
    
    def dict_user(self):
        """
        Método que traduz as informações do candidato para 
        dicionário.

        Returns:
            dict: Informações do objeto Candidato em um 
            dicionário.
        """
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

    def __str__(self) -> str:  # <-------- Opção Ver perfil do menu do cliente.
        return f"""

        Nome: {self.__nome}
        CPF: {self.__cpf}
        Email: {self.__email}
        Skills: {self.__skills}
        Area: {self.__area}
        Descricao: {self.__descricao}
        Cidade: {self.__cidade}
        UF: {self.__uf}
"""
