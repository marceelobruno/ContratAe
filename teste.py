import json
import socket
import sys

HOST = '127.0.0.1'
PORT = 5000

servidor = (HOST, PORT)

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente_socket.connect(servidor)

data = {
    "protocol_msg": "cancelarCandidatura",
    "idVaga": "3422",
    "cpf": "08243399321"
}

data_send = json.dumps(data).encode('utf-8')
cliente_socket.send(data_send)  # -> enviando via sockets

response_server = cliente_socket.recv(1024)
response_server = json.loads(response_server.decode('utf-8'))
print(response_server)