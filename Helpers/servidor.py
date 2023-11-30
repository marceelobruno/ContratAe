import pickle
import socket
import threading

from DataStructures.ChainingHashTable import ChainingHashTable
from DataStructures.ListaSequencialNumPY import Lista
from users import Candidato, Recrutador
# from vaga import Vaga

HOST = '127.0.0.1'
PORT = 5000

print('=== Servidor ===')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
clientes = {}
TableCandidatos = ChainingHashTable()  # -> hash table
ListaRecrutadores = Lista()
ListaVagas = []


def handle_client(client_socket):
    pass


def recrutador():
    pass


def candidato():
    pass


def protocol(msg, cliente):
    # GET -> Pegar informaÃ§Ãµes informaÃ§Ãµes de candidaturas, informaÃ§Ãµes de vagas e lista de candidatos(caso Recrutador).
    # POST -> Postar infomaÃ§Ãµes como vaga, novo usuario ou recrutador.
    # DELETE -> Deletar usuÃ¡rios(Recrutador e Candidato) e Vagas, ou cancelar candidatura caso usuÃ¡rio.
    # EDIT -> Editar informaÃ§Ãµes referente ao perfil do usuÃ¡rio.
    # APPLY -> Referente ao usuario candidatar em uma vaga.

    if msg == 'POST':

        # data_cliente -> dicionario envidado do cliente para o servidor com as informaÃ§Ãµes de tipo e cada campo de acordo com o tipo
        data_cliente = cliente.recv(1024)
        # -> usando o pickle para decodificar o dicionario
        data_cliente = pickle.loads(data_cliente)

        # print(data_cliente)

        if data_cliente["type"] == "candidato":

            # candidato = Candidato(data_cliente["nome"], data_cliente["email"], data_cliente["senha"]) #-> intanciando um candidato usando as chaves do dicionario enviado pelo cliente.
            # -> adicionando no dicionario o candidato e a chave Ã© o campo id.
            TableCandidatos[data_cliente["id"]] = Candidato(
                data_cliente["nome"], data_cliente["email"], data_cliente["senha"])
            # TableCandidatos.showHashTable()

            # protocol_response = '200 OK: "Candidato cadastrado com Sucesso !"'
            # cliente.send(protocol_response.encode('utf-8'))

            print()
            print('Lista de Candidatos')
            print()

            print(TableCandidatos)

        elif data_cliente["type"] == "recrutador":
            r = Recrutador(data_cliente["nome"],data_cliente["nomeEmpresa"], data_cliente["senha"], data_cliente["usuario"])
            ListaRecrutadores.append(r)
            print(ListaRecrutadores)

            v = r.criar_vaga('teste','TI','dinheiro bom',10,'1300,00', 'cérebro')
            ListaVagas.append(v)

            for i in ListaVagas:
                print(i)


def runServer():
    while True:
        cliente, endereco = server.accept()
        protocol_msg = cliente.recv(1024)
        clientes[cliente] = endereco
        t1 = threading.Thread(target=protocol, args=(
            protocol_msg.decode('utf-8'), cliente,))
        t1.start()

        # NÃ£o estou conseguindo estabelecer dois clientes ao mesmo tempo


runServer()
