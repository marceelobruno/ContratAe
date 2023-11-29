"""
Banco de Dados SQLite3
"""

import sqlite3


class Database(object):
    """_summary_

    Args:
        object (_type_): _description_
    """

    DB_LOCATION = "ContratAe/Database/applicationdb.db"
    # DB_LOCATION = "ContratAe/Helpers/Database/applicationdb.db"

    def __init__(self):
        self.conn = sqlite3.connect(Database.DB_LOCATION)
        self.c = self.conn.cursor()

    def create_table(self):
        """_summary_"""

        # Criando tabela para armazenar dados candidato
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS candidato
            ([ID] INTEGER PRIMARY KEY, [NOME] VARCHAR,
            [EMAIL] VARCHAR, [PASSWORD] VARCHAR)
            ''')

        # Criando tabela para armazenar dados recrutador
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS recrutador
            ([ID] INTEGER PRIMARY KEY, [NOME] VARCHAR,
            [EMAIL] VARCHAR, [PASSWORD] VARCHAR)
            ''')


if __name__ == "__main__":
    test = Database()
    test.create_table()
