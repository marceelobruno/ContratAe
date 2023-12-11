"""
Banco de Dados SQLite3
"""

import secrets
import sqlite3

from loguru import logger

# from pprint import pprint


class Database:
    """_summary_

    Args:
        object (_type_): _description_
    """

    DB_PATH = "./Database/applicationdb.db"

    def __init__(self):
        # Criando conexões com o banco
        self.conn = sqlite3.connect(Database.DB_PATH)
        self.c = self.conn.cursor()

    def create_tables(self):
        """_summary_"""
        # Criação da tabela Candidato
        self.c.execute(
            """
        CREATE TABLE IF NOT EXISTS [candidato] (
            ID INT NOT NULL,
            NOME VARCHAR(120) NOT NULL,
            EMAIL VARCHAR(40) NOT NULL,
            SENHA VARCHAR(128) NOT NULL,
            SKILLS VARCHAR(140),
            AREA VARCHAR(120),
            DESCRICAO VARCHAR(300),
            CIDADE VARCHAR(40),
            UF CHAR(2),
            -- APLICACOES,
            PRIMARY KEY (ID)
        );
        """
        )

        # Criação da tabela Recrutador
        self.c.execute(
            """
        CREATE TABLE IF NOT EXISTS [recrutador] (
            ID INT NOT NULL,
            NOME VARCHAR(120) NOT NULL,
            EMPRESA VARCHAR(80) NOT NULL,
            EMAIL VARCHAR(40) NOT NULL,
            SENHA VARCHAR(128) NOT NULL,
            PRIMARY KEY (ID)
        );
        """
        )

        # Criação da tabela Vagas
        self.c.execute(
            """
        CREATE TABLE IF NOT EXISTS [vaga] (
            ID INT NOT NULL,
            NOME VARCHAR(120) NOT NULL,
            ID_RECRUTADOR INT NOT NULL,
            AREA VARCHAR(40) NOT NULL,
            DESCRICAO VARCHAR(300) NOT NULL,
            LIMITE INT NOT NULL,
            NOME_EMPRESA VARCHAR(100) NOT NULL,
            SALARIO DECIMAL(10,2) NOT NULL,
            REQUISITO VARCHAR(140) NOT NULL,
            -- LISTA_CANDIDATURAS,
            PRIMARY KEY (ID)
            CONSTRAINT fk_recrutador
                FOREIGN KEY (ID_RECRUTADOR)
                REFERENCES recrutador (ID)
                ON DELETE CASCADE
        );
        """
        )
        logger.info("Tabelas criadas")


class CandidatoDB(Database):
    """Descricao"""

    def __init__(self) -> None:
        super().__init__()

    def insert_candidato(
        self,
        id_num: int,
        nome: str,
        e_mail: str,
        passwd: str,
        skills: str = None,
        area: str = None,
        descricao: str = None,
        cidade: str = None,
        uf: str = None,
    ) -> None:
        """_summary_"""

        self.c.execute(
            """INSERT INTO candidato
                       (ID, NOME, EMAIL, SENHA, SKILLS, AREA, DESCRICAO, CIDADE, UF)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (id_num, nome, e_mail, passwd, skills, area, descricao, cidade, uf),
        )
        self.conn.commit()
        self.conn.close()
        logger.info(f"Candidato: {id_num} {nome} inserido no Bando de Dados!")

    def delete_candidato(self, id_num: int) -> None:
        """_summary_"""
        self.c.execute(f"DELETE FROM candidato WHERE ID = {id_num}")
        self.conn.commit()
        self.conn.close()
        logger.info(f"Candidato deletado: {id_num}")

    def get_candidato_passwrd(self, id_num: int) -> str:
        """_summary_"""
        self.c.execute(f"SELECT SENHA FROM candidato WHERE ID = {id_num}")
        self.conn.commit()
        logger.info(f"\nSenha informada para o Candidato: {id_num}")
        # Retorna a senha em str
        return self.c.fetchone()[0]

    def get_all_candidato(self) -> tuple:
        """Retorna todos os dados da tabela candidato"""
        self.c.execute("SELECT * FROM candidato")
        self.conn.commit()
        logger.info("Retornando todos registros da tabela Candidato")
        # Retorna todos os registros da tabela candidato em uma tupla
        return self.c.fetchall()


class RecrutadorDB(Database):
    """Descricao"""

    def __init__(self) -> None:
        super().__init__()

    def insert_recrutador(
        self, id_num: int, nome: str, empresa: str, e_mail: str, passwd: str
    ) -> None:
        """_summary_"""
        self.c.execute(
            """INSERT INTO recrutador
                       (ID, NOME, EMPRESA, EMAIL, SENHA)
                       VALUES (?, ?, ?, ?, ?)""",
            (id_num, nome, empresa, e_mail, passwd),
        )
        self.conn.commit()
        self.conn.close()
        logger.info(f"Recrutador cadastrado: {id_num} {nome}")

    def delete_recrutador(self, id_num: int) -> str:
        """_summary_"""
        self.c.execute(f"DELETE FROM recrutador WHERE ID = {id_num}")
        self.conn.commit()
        self.conn.close()
        logger.info(f"Recrutador deletado: {id_num}")

    def get_recrutador_passwrd(self, id_num: int) -> str:
        """_summary_"""
        self.c.execute(f"SELECT SENHA FROM recrutador WHERE ID = {id_num}")
        self.conn.commit()
        logger.info(f"Senha informada para o Recrutador: {id_num}")
        # Retorna a senha em str
        return self.c.fetchone()[0]

    def get_all_recrutador(self) -> tuple:
        """### Retorna todos os dados da tabela Recrutador"""
        self.c.execute("SELECT * FROM recrutador")
        self.conn.commit()
        logger.info("Retornando todos registros da tabela Recrutador")
        # Retorna todos os registros da tabela recrutador em uma tupla
        return self.c.fetchall()


class VagaDB(Database):
    """Descricao"""

    def __init__(self) -> None:
        super().__init__()

    def insert_vaga(
        self,
        id_vaga: int,
        nome: str,
        id_recrutador: int,
        area: str,
        descricao: str,
        limite: int,
        empresa: str,
        salario: float,
        requisito: str,
    ) -> None:
        """_summary_"""

        self.c.execute(
            """INSERT INTO vaga
                       (ID, NOME, ID_RECRUTADOR, AREA, DESCRICAO, LIMITE, NOME_EMPRESA, SALARIO, REQUISITO)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                id_vaga,
                nome,
                id_recrutador,
                area,
                descricao,
                limite,
                empresa,
                salario,
                requisito,
            ),
        )
        self.conn.commit()
        self.conn.close()

        logger.info(f"Vaga cadastrada: {id_vaga} {nome}")

    def delete_vaga(self, id_vaga: int) -> str:
        """_summary_"""
        self.c.execute(f"DELETE FROM vaga WHERE ID = {id_vaga}")
        self.conn.commit()
        self.conn.close()

        logger.info(f"Vaga deletada: {id_vaga}")

    def get_all_vaga(self) -> tuple:
        """_summary_"""
        self.c.execute("SELECT * FROM vaga")
        self.conn.commit()

        logger.info("Retornando todos registros da tabela Vaga")
        # Retorna todos os registros da tabela vaga em uma tupla
        return self.c.fetchall()


if __name__ == "__main__":
    import random

    import names
    from validate_docbr import CPF

    cpf = CPF()

    while True:
        pf = cpf.generate()
        if len(pf) < 11:
            pf = cpf.generate()
        break

    identificador = pf  # int(time.time())
    firstNAme = names.get_first_name()
    lastName = names.get_last_name()
    nomeComp = firstNAme + " " + lastName
    email = firstNAme.lower() + "_" + lastName.lower() + "@yahoo.com"
    company = names.get_first_name() + " " + "Company"
    tabelinha = "candidato"
    senha = secrets.token_hex()
    ident = 77755588899

    idVaga = os.getpid()
    idRecrut = 88533305621
    nomeVaga = "Desenvolvedor Pleno"
    areaVaga = "Desenvolvedor de Softwares"
    descVaga = "Testar sistemas"
    limiteVaga = 10
    salarioVaga = "4500.00"
    requisitoVaga = "Python, Django"

    dt = Database()
    candidato = CandidatoDB()
    recrutador = RecrutadorDB()
    vaga = VagaDB()

    # Cria as tabelas caso não existam
    # dt.create_tables()

    # VALIDANDO MÉTODOS DA CLASSE CANDIDATO
    candidato.insert_candidato(identificador, nomeComp, email, senha, 'Bussiness Inteligence,  QlickSense', 'TI', 'Analista', 'Jampa', 'PB')
    # candidato.delete_candidato(ident)
    # print(candidato.get_candidato_passwrd(ident))
    # print(
    #     "CANDIDATOS:\n",
    #     candidato.get_all_candidato(),
    #     type(candidato.get_all_candidato()),
    # )

    # VALIDANDO MÉTODOS DA CLASSE RECRUTADOR
    # recrutador.insert_recrutador(identificador, nomeComp, company, email, senha)
    # recrutador.delete_recrutador(ident)
    # print(recrutador.get_recrutador_passwrd(ident))
    # print('RECRUTADORES:\n', recrutador.get_all_recrutador())

    # VALIDANDO MÉTODOS DA CLASSE VAGA
    # vaga.insert_vaga(
    #     idVaga,
    #     nomeVaga,
    #     idRecrut,
    #     areaVaga,
    #     descVaga,
    #     limiteVaga,
    #     company,
    #     salarioVaga,
    #     requisitoVaga,
    # )
    # vaga.delete_vaga(2440)
    # print('VAGAS:\n', vaga.get_all_vaga())
