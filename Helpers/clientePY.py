import pickle
import socket
from hashlib import sha256

HOST = "127.0.0.1"
PORT = 5000

servidor = (HOST, PORT)

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(servidor)


def menu():
    print("=== ContratAe ===")
    print()

    while True:
        # try:

        login = int(input("digite (1) para ENTRAR | digite (2) para CRIAR CONTA: "))
        print()
        # -> tratar essa entrada
        type_user = input(
            "você é ( c ) candidato ou ( r ) recrutador: ( c / r ): \n"
        ).lower()

        if login == 1:
            if type_user == "c":
                entar(type_user, "login")
                break
            else:
                entar("r", "login")
                break

        elif login == 2:
            if type_user == "c":
                entar("c", "criar")
                break
            else:
                entar("r", "criar")
                break

        # except:
        #     print()
        #     print("opção inválida")
        #     print()


def entar(type, action):
    data_cliente = {}
    data_cliente["type"] = type

    if action == "login":
        while True:
            data_cliente["cpf"] = input("CPF: ")
            data_cliente["senha"] = input("Senha: ")

            try:
                protocol_msg = "GET"  # -> verificar se o usuário existe
                cliente_socket.send(protocol_msg.encode("utf-8"))

                # -> usando o pickle para transformar em binario
                data_cliente = pickle.dumps(data_cliente)
                cliente_socket.send(data_cliente)  # -> enviando via sockets

                response_server = cliente_socket.recv(1024)

                if response_server.decode("utf-8") == "404 Not Found":
                    print("Usuário não encontrado")
                    data_cliente = pickle.loads(data_cliente)

                else:
                    dashborad(type)
                    break

            except:
                print("Conexão com o servidor não foi estabelecida corretamente")

    elif action == "criar":
        while True:
            protocol_msg = "POST"  # -> definindo a flag do protocolo.
            cliente_socket.send(protocol_msg.encode("utf-8"))

            data_cliente = {}
            data_cliente["nome"] = input("Digite o nome: ")
            data_cliente["email"] = input("Digite o email: ")

            senha = input("Digite sua senha: ")
            # hasheando a senha para sha256
            hash_passwd = sha256(senha.encode())
            # convertendo a senha de bytes para hexadecimal
            data_cliente["senha"] = hash_passwd.hexdigest()

            # data_cliente["senha"] = input("Digite sua senha: ")
            data_cliente["type"] = type
            data_cliente["cpf"] = input("Digite seu CPF: ")

            if type == "r":
                data_cliente["usuario"] = input(
                    "Digite seu usuário que será seu identificador para acessar o ContratAe: "
                )
                data_cliente["nomeEmpresa"] = input(
                    "Digite a empresa para a qual você está recrutando: "
                )

            data_cliente = pickle.dumps(data_cliente)  # -> convertendo para bytes
            cliente_socket.send(data_cliente)  # -> enviando via sockets

            response_server = cliente_socket.recv(1024)
            response_server = response_server.decode("utf-8")
            response_server = response_server.split(":")

            if response_server[0] == ("400 Bad Request"):
                print(response_server[1])

            else:
                print(response_server[1])
                dashborad(type)
                break


def dashborad(type):
    user = cliente_socket.recv(1024)  # -> Recebendo o usiario do servidor
    user = pickle.loads(user)

    if type == "c":  # -> aqui ficará a área do candidato
        print(user)


menu()
