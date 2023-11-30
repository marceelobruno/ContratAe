import pickle
import socket
import time

HOST = '127.0.0.1'
PORT = 5000

servidor = (HOST, PORT)

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(servidor)

def menu():
    print("=== ContratAe ===")
    print()
    
    while True:
        try:
            
            login = int(input("digite (1) para ENTRAR | digite (2) para CRIAR CONTA: "))
            print()
            type_user = input("você é ( c ) candidato ou ( r ) recrutador: ( c / r ): ").lower() # -> tratar essa entrada
        
            if login == 1:
                
                if type_user == "c":
                    entar('c', 'login') 
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
            
        except:
            print()
            print("opção inválida")
            print()
            
def entar(type , action):
    
    data_cliente["type"] = type
    
    if action == "login":
        
        data_cliente["nome"] = input('Usuário: ')
        data_cliente["senha"] = input('Senha: ')
        
        try:
            protocol_msg = "GET" # -> verificar se o usuário existe
            cliente_socket.send(protocol_msg.encode('utf-8'))
            
            data_cliente = pickle.dumps(data_cliente)  # -> usando o pickle para transformar em binario
            cliente_socket.send(data_cliente)  # -> enviando via sockets
            
            response_server = cliente_socket.recv(1024)
            print(response_server.decode('utf-8'))
            
        except:
            print('Conexão com o servidor não foi estabelecida corretamente')
        
menu()

protocol_msg = "POST" # -> definindo a flag do protocolo.

data_cliente = {}
data_cliente["nome"] = input("Digite o nome: ")
data_cliente["senha"] = "1234"
data_cliente["type"] = input("Voce é candidato ou recrutador: ").lower()

if data_cliente["type"] == 'candidato':
    data_cliente["email"] = input("Digite o email: ")
    data_cliente["id"] = int(time.time()) # -> Retorna um unixtimestamp para o ID
    print(data_cliente["id"])

elif data_cliente["type"] == 'recrutador':
    data_cliente["nomeEmpresa"] = input('Digite o nome da sua empresa: ')
    data_cliente["usuario"] = input('Digite seu usuário: ')

# -> usando o pickle para transformar em binario
data_cliente = pickle.dumps(data_cliente)  
cliente_socket.send(data_cliente)  # -> enviando via sockets
