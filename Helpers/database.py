"""
Banco de Dados SQLite3
"""
import secrets
import sqlite3


class Database():
    """_summary_

    Args:
        object (_type_): _description_
    """

    DB_PATH = "./Database/applicationdb.db"

    def __init__(self):
        self.conn = sqlite3.connect(Database.DB_PATH)
        self.c = self.conn.cursor()

    def create_table(self):
        """_summary_"""

        # Criação da tabela de clientes
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
        self.c.execute("INSERT INTO cliente VALUES ('" +
                       str(id_num)+"','"+nome+"', '"+email+"', 'candidato')")

        self.c.execute("INSERT INTO senhas VALUES ('" +
                       str(id_num)+"','"+senha+"')")

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
    import time

    import names

    firstNAme = names.get_first_name()
    lastName = names.get_last_name()
    nomeComp = firstNAme + ' ' + lastName
    email = firstNAme.lower() + '_' + lastName.lower() + '@vagas.com'
    tabelinha = 'candidato'
    senha = secrets.token_hex()
    identificador = int(time.time())
    ident = 1701266446

    test = Database()
    test.create_table()

    # Insere Dados
    test.insert_client_data(identificador, nomeComp, email, senha)
    print(identificador, nomeComp)

    # Deleta Dados usando a PK
    # test.delete_client_data(ident)

    # Recupera a senha em formato de hash
    # print(test.get_passwrd_client_data(ident),
    #       type(test.get_passwrd_client_data(ident)))
