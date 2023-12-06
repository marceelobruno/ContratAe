import pickle
import socket
from loguru import logger
from hashlib import sha256

HOST = '127.0.0.1'
PORT = 5000

servidor = (HOST, PORT)

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(servidor)

def run_cliente():
    print("=== ContratAe ===")
    print()

    while True:
        # try:

        login = int(
            input("digite (1) para ENTRAR | digite (2) para CRIAR CONTA: "))
        print()
        # -> tratar essa entrada
        type_user = input(
            "você é ( c ) candidato ou ( r ) recrutador: ( c / r ): ").lower()

        if login == 1:

            if type_user == "c":
                entar(type_user, 'login')
                break
            else:
                entar('r', 'login')
                break

        elif login == 2:

            if type_user == "c":
                entar('c', 'criar')
                break
            else:
                entar('r', 'criar')
                break

        # except:
        #     print()
        #     print("opção inválida")
        #     print()

def entar(type, action):
    
    if action == "login":
        # -> verificar se o usuário existe
        protocol_msg = "GET"
        cliente_socket.send(protocol_msg.encode('utf-8'))
        
        while True:
            data_cliente = {}
            data_cliente["type"] = type
            data_cliente["cpf"] = input('CPF: ')
            # hasheando a senha para sha256
            hash_passwd = sha256(input("senha: ").encode())
            # convertendo a senha de bytes para hexadecimal
            data_cliente["senha"] = hash_passwd.hexdigest()

            try:
                # -> usando o pickle para transformar em binario
                cliente_socket.send(pickle.dumps(data_cliente))  # -> enviando via sockets

                response_server = pickle.loads(cliente_socket.recv(1024))
                
                if response_server["status"] == "404 Not Found" or response_server["status"] == "401 Unauthorized":
                    print(response_server["message"])
                    
                else:
                    dashborad(response_server["data"], type)
                    break

            except:
                print('Conexão com o servidor não foi estabelecida corretamente')

    elif action == "criar":
        protocol_msg = "POST"  # -> definindo a flag do protocolo.
        cliente_socket.send(protocol_msg.encode('utf-8'))
        while True:
            data_cliente = {}
            data_cliente["nome"] = input("Digite o nome: ")
            data_cliente["email"] = input("Digite o email: ")
            data_cliente["cpf"] = input("Digite seu CPF: ")
            data_cliente["type"] = type
            
            # hasheando a senha para sha256
            hash_passwd = sha256(input("Digite sua senha: ").encode())
            # convertendo a senha de bytes para hexadecimal
            data_cliente["senha"] = hash_passwd.hexdigest()
            
            if type == "r":
                data_cliente["nomeEmpresa"] = input("Digite a empresa para a qual você está recrutando: ")
                
            cliente_socket.send(pickle.dumps(data_cliente))  # -> envian via sockets
            response_server = cliente_socket.recv(1024)
            response_server = pickle.loads(response_server) # -> resposta do servidor
        
            if response_server["status"] == "400 Bad Request":
                print(response_server["message"])
                
            else:
                dashborad(response_server["data"] ,type) # -> chamando a função principal do cliente
                break
        
def dashborad(user, type):
    
    if type == "c": # -> aqui ficará a área do candidato
        print(user)
    
    else: # -> área do recrutador
        pass
    
run_cliente()
