class Vaga:
    def __init__(self, nome, cpf_recrutador, idVaga, area, descricao, quantidade: int, nome_empresa, salario: float, requisitos):
        self.__nome = nome
        self.__id = idVaga
        self.__cpf_recrutador = cpf_recrutador
        self.__area = area
        self.__descricao = descricao
        self.__quantidade = quantidade
        self.__nome_empresa = nome_empresa
        self.__salario = salario
        self.__requisitos = requisitos
        self.__lista_candidaturas = [] 

    @property
    def nome(self):
        return self.__nome

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = value
    
    @property
    def cpf_recrutador(self):
        return self.__cpf_recrutador
    
    @property
    def lista_candidaturas(self):
        return self.__lista_candidaturas

    @property
    def quantidade(self):
        return self.__quantidade

    def adicionarCandidatura(self, candidato:dict)->None:
        """
        Adiciona um dicionário contendo as informações do candidato
        na self.__lista_candidaturas. E diminui a quantidade de vagas
        disponíveis em 1.

        Args:
            candidato (dict): candidato a ser adicionado. 
        """
        self.__lista_candidaturas.append(candidato)
        self.__quantidade -= 1

    def removerCandidatura(self, elemento:dict)-> None:
        """
        Remove o conteúdo do candidato da self.__lista_candidaturas.
        Aumenta a quantidade de vagas em 1.

        Args:
            elemento (dict): candidato a ser removido.
        """
        self.__lista_candidaturas.remove(elemento)
        self.__quantidade += 1

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
            "id_vaga": self.__id,
            "descricao": self.__descricao,
            "quantidade": self.__quantidade,
            "nome_empresa": self.__nome_empresa,
            "salario": self.__salario,
            "requisito": self.__requisitos,
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


