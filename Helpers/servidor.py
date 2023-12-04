"""
Servidor
"""

import pickle
import socket
import threading
from loguru import logger
from DataStructures.ChainingHashTable import ChainingHashTable
from loguru import logger
from users import Candidato, Recrutador
import os
from cliente import run

from database import CandidatoDB  # , RecrutadorDB, VagaDB

# from vaga import Vaga

HOST = '0.0.0.0'
PORT = 5000

print("=== Servidor ===\n")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
TableCandidatos = ChainingHashTable()
TableRecrutadores = ChainingHashTable()
ListaVagas = []

def get_candidatos_from_db() -> None:
    """Retornando os dados da tabela candidato para a hashtable-candidato"""
    candidatos = CandidatoDB()
    data = candidatos.get_all_candidato()

    candidato_dict = {}

    for i, candidate in enumerate(data):  # manter o i ao lado do for
        lista_candidatos = candidate
        candidato_dict = {"cpf": str(lista_candidatos[0]),
                          "nome": lista_candidatos[1],
                          "email": lista_candidatos[2],
                          "senha": lista_candidatos[3],
                          "skills": lista_candidatos[4],
                          "area": lista_candidatos[5],
                          "descricao": lista_candidatos[6],
                          "cidade": lista_candidatos[7],
                          "uf": lista_candidatos[8],
                        }

        TableCandidatos[candidato_dict["cpf"]] = Candidato(
            candidato_dict["nome"],
            candidato_dict["email"],
            candidato_dict["senha"],
            candidato_dict["cpf"],
            candidato_dict["skills"],
            candidato_dict["area"],
            candidato_dict["descricao"],
            candidato_dict["cidade"],
            candidato_dict["uf"],
        )

    # print(TableCandidatos)
    return logger.info('Candidatos inseridos na HashTable')

def handle_client(cliente):
    protocol_msg = cliente.recv(1024)
    protocol(cliente, protocol_msg.decode('utf-8'))
    
def recrutador():
    pass

def candidato(data_cliente, cliente):
    user_candidato = TableCandidatos[
        data_cliente["cpf"]
    ]  # -> recuperando a referencia do objeto candidato
    user_candidato = pickle.dumps(user_candidato)
    cliente.send(user_candidato)  # -> enviando a referencia do objeto para o cliente

def protocol(protocol_msg, cliente):
    """
    GET -> Pegar informações de candidaturas, informações de vagas e lista de candidatos (caso Recrutador).
    POST -> Postar informações como vaga, novo usuário ou recrutador.
    DELETE -> Deletar usuários (Recrutador e Candidato) e vagas, ou cancelar candidatura caso usuário.
    EDIT -> Editar informações referentes ao perfil do usuário.
    APPLY -> Referente ao usuário candidatar-se a uma vaga.
    """
    if protocol_msg == 'GET':
        data_cliente = pickle.loads(cliente.recv(1024))
    
        if data_cliente["type"] == "c":
            protocol_response = candidato(data_cliente)
            cliente.send(pickle.dumps(protocol_response))
        else:
            protocol_response = recrutador(data_cliente)
            cliente.send(pickle.dumps(protocol_response))
        
    elif protocol_msg == 'POST':

        data_cliente = cliente.recv(1024) # data_cliente -> dicionario envidado do cliente para o servidor com as informaÃ§Ãµes de tipo e cada campo de acordo com o tipo
        data_cliente = pickle.loads(data_cliente) # -> usando o pickle para decodificar o dicionario

        if data_cliente["type"] == "c":
            if data_cliente["cpf"] not in TableCandidatos:
                TableCandidatos[data_cliente["cpf"]] = Candidato(
                    data_cliente["nome"], data_cliente["email"], data_cliente["senha"], data_cliente["cpf"])
                
                user_candidato = TableCandidatos[data_cliente["cpf"]]
                logger.info(f'{user_candidato}')
                protocol_response = {"status": '201 Created', "data": user_candidato}
                cliente.send(pickle.dumps(protocol_response))
                
            else:
                protocol_response = {"status": "400 Bad Request", "message": "CPF já cadastrado."}
                cliente.send(pickle.dumps(protocol_response))

            print(TableCandidatos)

        elif data_cliente["type"] == "r":
            r = Recrutador(
                data_cliente["nome"],
                data_cliente["nomeEmpresa"],
                data_cliente["senha"],
                data_cliente["cpf"],
            )

            TableRecrutadores[data_cliente["cpf"]] = r

            # v = r.criar_vaga('teste','TI','dinheiro bom',10,'1300,00', 'cérebro')
            # ListaVagas.append(v)

            # for i in ListaVagas:
            #     print(i)


def runServer():
    if os.name == 'nt':  # Verifica se é Windows
        threading.Thread(target=run).start()
    else:
        pid = os.fork()
        if pid == 0:
            run()
    while True:
        cliente, addr = server.accept()
        t1 = threading.Thread(target=handle_client, args=(cliente,))
        t1.start()

# Retornando os dados da tabela candidato para a hashtable-candidato
get_candidatos_from_db()
runServer()

