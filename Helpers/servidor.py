"""
Servidor
"""

import pickle
import socket
import threading

from DataStructures.ChainingHashTable import ChainingHashTable
from loguru import logger
from users import Candidato, Recrutador

from database import CandidatoDB  # , RecrutadorDB, VagaDB

# from vaga import Vaga

HOST = '127.0.0.1'
PORT = 5000

print("=== Servidor ===\n")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
clientes = {}
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

def handle_client(client_socket):
    pass


def recrutador():
    pass


def candidato(data_cliente, cliente):
    user_candidato = TableCandidatos[
        data_cliente["cpf"]
    ]  # -> recuperando a referencia do objeto candidato
    user_candidato = pickle.dumps(user_candidato)
    cliente.send(user_candidato)  # -> enviando a referencia do objeto para o cliente


def protocol(msg, cliente):
    """
    GET -> Pegar informações de candidaturas, informações de vagas e lista de candidatos (caso Recrutador).
    POST -> Postar informações como vaga, novo usuário ou recrutador.
    DELETE -> Deletar usuários (Recrutador e Candidato) e vagas, ou cancelar candidatura caso usuário.
    EDIT -> Editar informações referentes ao perfil do usuário.
    APPLY -> Referente ao usuário candidatar-se a uma vaga.
    """

    if msg == "GET":
        data_cliente = cliente.recv(1024)
        data_cliente = pickle.loads(data_cliente)

        if data_cliente["type"] == "c":
            # print()
            print(data_cliente["cpf"])
            # print()

            if data_cliente["cpf"] in TableCandidatos:
                protocol_response = "200 Ok"
                cliente.send(protocol_response.encode("utf-8"))

                candidato(data_cliente, cliente)

            else:
                protocol_response = "404 Not Found"
                cliente.send(protocol_response.encode("utf-8"))

        elif data_cliente["type"] == "r":
            pass

    elif msg == "POST":
        # data_cliente: dicionario enviado do cliente para o servidor com as
        # informações de tipo e cada campo de acordo com o tipo
        data_cliente = cliente.recv(1024)

        # -> usando o pickle para decodificar o dicionario
        data_cliente = pickle.loads(data_cliente)

        # print(data_cliente)

        if data_cliente["type"] == "c":
            if data_cliente["cpf"] not in TableCandidatos:
                TableCandidatos[data_cliente["cpf"]] = Candidato(
                    data_cliente["nome"],
                    data_cliente["email"],
                    data_cliente["senha"],
                    data_cliente["cpf"],
                )

                protocol_response = '201 OK: "Candidato cadastrado com Sucesso!"'
                cliente.send(protocol_response.encode("utf-8"))

                # Inserindo os dados do Candidato no Banco de Dados
                candidate = CandidatoDB()
                candidate.insert_candidato(data_cliente["cpf"], data_cliente["nome"],
                    data_cliente["email"], data_cliente["senha"])

                candidato(data_cliente, cliente)

            else:
                protocol_response = '400 Bad Request: "CPF já cadastrado."'
                cliente.send(protocol_response.encode("utf-8"))

            # print(TableCandidatos)
            logger.info(f"Usuario: {data_cliente["cpf"]}")
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
    """_summary_"""
    while True:
        cliente, endereco = server.accept()
        protocol_msg = cliente.recv(1024)
        clientes[cliente] = endereco
        t1 = threading.Thread(
            target=protocol,
            args=(
                protocol_msg.decode("utf-8"),
                cliente,
            ),
        )
        t1.start()

# Retornando os dados da tabela candidato para a hashtable-candidato
get_candidatos_from_db()

runServer()
