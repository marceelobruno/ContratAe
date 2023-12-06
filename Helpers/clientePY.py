import pickle
import socket
import time
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
        while True:
            try:
                login = int(input("digite (1) para ENTRAR | digite (2) para CRIAR CONTA: "))
                print()
                assert login in [1,2], 'Por favor, digite (1) para ENTRAR ou (2) para CRIAR CONTA.'
                break  
            except AssertionError as ae:
                print(ae)
            except ValueError:
                print('Digite uma das opções acima.')

        while True:
            try:
                type_user = input(
                    "você é ( c ) candidato ou ( r ) recrutador: ( c / r ): \n"
                ).lower()
                assert type_user in ['c','r'], 'Por favor, escolha entre (c) candidato ou (r) recrutador.' 
                break
            except AssertionError as ae:
                print(ae)

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
        # cliente_socket.send(protocol_msg.encode('utf-8'))
        cliente_socket.send(pickle.dumps(protocol_msg))
        
        while True:
            data_cliente = {}
            data_cliente["type"] = type
            data_cliente['action'] = 'login'
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
                    dashboard(response_server["data"], type)
                    break

            except:
                print('Conexão com o servidor não foi estabelecida corretamente')

    elif action == "criar":
        protocol_msg = "POST"  # -> definindo a flag do protocolo.
        # cliente_socket.send(protocol_msg.encode('utf-8'))
        cliente_socket.send(pickle.dumps(protocol_msg))
        while True:
            data_cliente = {}
            data_cliente["nome"] = input("Digite o nome: ")
            data_cliente["email"] = input("Digite o email: ")
            data_cliente["cpf"] = input("Digite seu CPF: ")
            data_cliente["type"] = type
            data_cliente['action'] = 'criar'
            
            # hasheando a senha para sha256
            hash_passwd = sha256(input("Digite sua senha: ").encode())
            # convertendo a senha de bytes para hexadecimal
            data_cliente["senha"] = hash_passwd.hexdigest()
            
            if type == "r":
                data_cliente["nomeEmpresa"] = input("Digite a empresa para a qual você está recrutando: ")
                
            cliente_socket.send(pickle.dumps(data_cliente)) # -> envian via sockets
            response_server = cliente_socket.recv(1024)
            response_server = pickle.loads(response_server) # -> resposta do servidor
        
            if response_server["status"] == "400 Bad Request":
                print(response_server["message"])
                
            else:
                dashboard(response_server["data"] ,type) # -> chamando a função principal do cliente
                break


def dashboard(user, type):
    
    if type == "c": # -> aqui ficará a área do candidato
        print(user)
        entrada = input("""
        1-Ver vagas
        2-Candidatar a vaga
        3-Ver perfil
        
""")
        if entrada == '1':
            protocol_msg = 'GET'
            action = 'verVagas'

        elif entrada == '2':
            protocol_msg = 'APPLY'
            action = 'candidatar'

        elif entrada == '3':
            protocol_msg = 'GET'
            action = 'verPerfil'

        cliente_socket.send(pickle.dumps(protocol_msg))
        data_cliente = {'action':action, 'type': 'c'}
        cliente_socket.send(pickle.dumps(data_cliente))

        if action == 'verVagas':
            
            response_server = cliente_socket.recv(1024)
            response_server = pickle.loads(response_server) # -> resposta do servidor
        
            if response_server["status"] == "404 Not Found":
                print(response_server["message"])
            else:
                print(response_server['data'])


        

    elif type == 'r':
        pass
        

    
run_cliente()
