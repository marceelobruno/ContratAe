import socket
import pickle
import random

HOST = '127.0.0.1'
PORT = 5000

servidor = (HOST, PORT)

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(servidor)

protocol_msg = "POST" # -> definindo a flag do protocolo.
cliente_socket.send(protocol_msg.encode('utf-8'))

data_cliente = {}
data_cliente["nome"] = input("Digite o nome: ")
data_cliente["email"] = input("Digite o email: ")
data_cliente["id"] = random.randint(0, 199999)
data_cliente["type"] = input("Voce é candidato ou recrutador: ").lower()
data_cliente["senha"] = "1234"

data_cliente = pickle.dumps(data_cliente) # -> usando o pickle para tranformar em binario 
cliente_socket.send(data_cliente) # -> enviando via sockets
