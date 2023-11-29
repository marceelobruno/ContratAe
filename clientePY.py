import pickle
import socket
import time

HOST = '10.0.149.110'
PORT = 5000

servidor = (HOST, PORT)

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(servidor)

protocol_msg = "POST" # -> definindo a flag do protocolo.
cliente_socket.send(protocol_msg.encode('utf-8'))

data_cliente = {}
data_cliente["nome"] = input("Digite o nome: ")
data_cliente["email"] = input("Digite o email: ")
data_cliente["id"] = int(time.time()) # -> Retorna um unixtimestamp para o ID
data_cliente["type"] = input("Voce é candidato ou recrutador: ").lower()
data_cliente["senha"] = "1234"

# -> usando o pickle para transformar em binario
data_cliente = pickle.dumps(data_cliente)  
cliente_socket.send(data_cliente)  # -> enviando via sockets
