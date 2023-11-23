import socket
import threading
from users import Recrutador

HOST = '26.254.64.131'
PORT = 5000

print('=== Servidor ===')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
clientes = {} #hash table

def broadcast(message, client_socket):
   pass

def handle_client(client_socket):
   pass

def recrutador():
    pass

def protocol(msg):
    #GET -> Pegar informações informações de candidaturas, informações de vagas e lista de candidatos(caso Recrutador).
    #POST -> Postar infomações como vaga, novo usuario ou recrutador.
    #DELETE -> Deletar usuários(Recrutador e Candidato) e Vagas, ou cancelar candidatura caso usuário.
    #EDIT -> Editar informações referente ao perfil do usuário.
    #APPLY -> Referente ao usuario candidatar em uma vaga.
    pass

while True:
    cliente, addr = server.accept()
    nome = cliente.recv(1024).decode('utf-8')
    clientes[cliente] = nome
    t1 = threading.Thread(target=handle_client, args=(cliente,))
    t1.start()
    print(clientes)
