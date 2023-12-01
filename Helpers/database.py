"""
Banco de Dados SQLite3
"""

import secrets
import sqlite3

from loguru import logger


class Database():
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
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS [candidato] (
            ID INT NOT NULL,
            NOME VARCHAR(120) NOT NULL,
            EMAIL VARCHAR(40) NOT NULL,
            --TYPE VARCHAR(15) NOT NULL,
            SKILLS VARCHAR(100) NOT NULL,
            AREA VARCHAR(100) NOT NULL,
            DESCRICAO VARCHAR(250) NOT NULL,
            CIDADE VARCHAR(50) NOT NULL,
            UF CHAR(2) NOT NULL,
            SENHA VARCHAR(256) NOT NULL,
            -- APLICACOES,
            PRIMARY KEY (ID)
        );
        """)

        # Criação da tabela Recrutador
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS [recrutador] (
            ID INT NOT NULL,
            NOME VARCHAR(120) NOT NULL,
            EMPRESA VARCHAR(120) NOT NULL,
            EMAIL VARCHAR(40) NOT NULL,
            SENHA VARCHAR(256) NOT NULL,
            --TYPE VARCHAR(15) NOT NULL,
            -- NOME_USUARIO VARCHAR(30) NOT NULL,
            PRIMARY KEY (ID)
        );
        """)

        # Criação da tabela Vagas
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS [vaga] (
            ID INT NOT NULL,
            NOME VARCHAR(120) NOT NULL,
            ID_RECRUTADOR INT NOT NULL
            AREA VARCHAR(40) NOT NULL,
            DESCRICAO VARCHAR(250) NOT NULL,
            LIMITE INT NOT NULL,
            NOME_EMPRESA VARCHAR(100) NOT NULL,
            SALARIO DECIMAL(10,2) NOT NULL,
            REQUISITO VARCHAR(100) NOT NULL,
            -- LISTA_CANDIDATURAS,
            PRIMARY KEY (ID)
            CONSTRAINT fk_recrutador
                FOREIGN KEY (ID_RECRUTADOR)
                REFERENCES recrutador (ID)
                ON DELETE CASCADE
        );
        """)
        logger.info("Tabelas criadas")


class CandidatoDB(Database):
    """ Descricao """
    def __init__(self) -> None:
        super().__init__()

    def insert_candidato(self, id_num: int, nome: str, e_mail: str,
                         skills: str, area: str, descricao: str,
                         cidade: str, uf: str, passwd: str) -> None:
        """_summary_"""

        self.c.execute("""INSERT INTO candidato
                       (ID, NOME, EMAIL, SKILLS, AREA, DESCRICAO, CIDADE, UF, SENHA)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (id_num, nome, e_mail, skills,
                        area, descricao, cidade, uf, passwd))
        self.conn.commit()
        self.conn.close()
        logger.info(f"Candidato cadastrado: {id_num} {nome}")

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
        logger.info(f"Senha informada para o Candidato: {id_num}")
        # Retorna a senha em str
        return self.c.fetchone()[0]

    def get_all_candidato(self) -> tuple:
        """_summary_"""
        self.c.execute("SELECT * FROM candidato")
        self.conn.commit()
        logger.info("Retornando todos registros da tabela Candidato")
        # Retorna todos os registros da tabela candidato em uma tupla
        return self.c.fetchall()


class RecrutadorDB(Database):
    """ Descricao """
    def __init__(self) -> None:
        super().__init__()

    def insert_recrutador(self, id_num: int, nome: str, empresa: str,
                          e_mail: str, passwd: str) -> None:
        """_summary_"""
        self.c.execute("""INSERT INTO recrutador
                       (ID, NOME, EMPRESA, EMAIL, SENHA)
                       VALUES (?, ?, ?, ?, ?)""",
                       (id_num, nome, empresa, e_mail, passwd))
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
        """_summary_"""
        self.c.execute("SELECT * FROM recrutador")
        self.conn.commit()
        logger.info("Retornando todos registros da tabela Recrutador")
        # Retorna todos os registros da tabela recrutador em uma tupla
        return self.c.fetchall()


class VagaDB(Database):
    """ Descricao """
    def __init__(self) -> None:
        super().__init__()

    def insert_vaga(self, id_vaga: int, nome: str, area: str,
                    descricao: str, limite: int, empresa: str,
                    salario: float, requisito: str) -> None:
        """_summary_"""

        self.c.execute("""INSERT INTO vaga
                       (ID, NOME, AREA, DESCRICAO, LIMITE, NOME_EMPRESA, SALARIO, REQUISITO)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                       (id_vaga, nome, area, descricao,
                        limite, empresa, salario, requisito))
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
    import os

    import names
    from validate_docbr import CPF

    cpf = CPF()

    firstNAme = names.get_first_name()
    lastName = names.get_last_name()
    nomeComp = firstNAme + ' ' + lastName
    email = firstNAme.lower() + '_' + lastName.lower() + '@yahoo.com'
    company = names.get_first_name() + ' ' + 'Inc'
    tabelinha = 'candidato'
    senha = secrets.token_hex()
    identificador = cpf.generate()   # int(time.time())
    ident = 2533189472

    idVaga = os.getpid()
    idRecrut = 4956572808
    nomeVaga = 'Pessoa Engenheira de Machine Learning Sênior'
    areaVaga = 'Machine Learning'
    descVaga = 'Sua missão será desenvolver, programar e testar sistemas de aprendizado de máquinas'
    limiteVaga = 10
    salarioVaga = '12500.00'
    requisitoVaga = 'Python fluente e Desenvolver Modelos e algoritmos de Machine Learning'

    dt = Database()
    candidato = CandidatoDB()
    recrutador = RecrutadorDB()
    vaga = VagaDB()

    # Cria as tabelas caso não existam
    dt.create_tables()

    # VALIDANDO MÉTODOS DA CLASSE CANDIDATO
    # candidato.insert_candidato(identificador, nomeComp, email, 'trabalhador', 'Analista', '5 anos na profissão', 'Cabedelo', 'PB', senha)
    # candidato.delete_candidato(ident)
    # print(candidato.get_candidato_passwrd(ident))
    # print('CANDIDATOS:\n', candidato.get_all_candidato(), type(candidato.get_all_candidato()))

    # VALIDANDO MÉTODOS DA CLASSE RECRUTADOR
    # recrutador.insert_recrutador(identificador, nomeComp, company, email, senha)
    # recrutador.delete_recrutador(ident)
    # print(recrutador.get_recrutador_passwrd(ident))
    # print('RECRUTADORES:\n', recrutador.get_all_recrutador())

    # VALIDANDO MÉTODOS DA CLASSE VAGA
    # vaga.insert_vaga(idVaga, nomeVaga, areaVaga, descVaga, limiteVaga, company, salarioVaga, requisitoVaga)
    # vaga.delete_vaga(2440)
    # print('VAGAS\n', vaga.get_all_vaga())
