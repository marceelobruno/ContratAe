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

    DB_LOCATION = "./Database/applicationdb.db"
    # DB_LOCATION = "ContratAe/Helpers/Database/applicationdb.db"

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

        # Criação da tabela de usuários
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            ID INT NOT NULL,
            NOME VARCHAR(100) NOT NULL,
            EMAIL VARCHAR(40) NOT NULL,
            TYPE VARCHAR(15) NOT NULL,
            PRIMARY KEY (ID)
        );
        """)

        # Criação da tabela de senhas
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS senhas (
            ID INT NOT NULL,
            SENHA VARCHAR(256) NOT NULL,
            PRIMARY KEY (ID),
            CONSTRAINT fk_senhas_cliente
                FOREIGN KEY (ID)
                REFERENCES cliente (ID)
                ON DELETE CASCADE
        );
        """)

    def insert_client_data(self, id_num: int, nome: str, email: str, senha: str):
        """_summary_"""
        self.c.execute("INSERT INTO cliente VALUES ('"+str(id_num)+"','"+nome+"', '"+email+"', 'recrutador')")
        self.c.execute("INSERT INTO senhas VALUES ('"+str(id_num)+"','"+senha+"')")
        self.conn.commit()
        self.conn.close()

    def delete_client_data(self, id_num: int):
        """_summary_"""
        self.c.execute(f"DELETE FROM cliente WHERE ID = {id_num}")
        self.conn.commit()
        self.conn.close()

    def get_passwrd_client_data(self, id_num: int):
        """_summary_"""
        self.c.execute(f"SELECT SENHA FROM senhas WHERE ID = {id_num}")
        self.conn.commit()

        # Retorna a senha em str
        return self.c.fetchone()[0]


if __name__ == "__main__":
    import os

    import names

    nomeComp = names.get_last_name()
    email = nomeComp.lower() + '@ymail.com'
    tabelinha = 'candidato'
    senha = secrets.token_hex()
    identificador = os.getpid()
    ident = 25900

    test = Database()
    # test.create_table()

    # Insere Dados
    test.insert_client_data(identificador, nomeComp, email, senha)
    print(identificador, nomeComp)

    # Deleta Dados usando a PK
    # test.delete_client_data(ident)

    # Recupera a senha em formato de hash
    print(test.get_passwrd_client_data(ident),
          type(test.get_passwrd_client_data(ident)))
