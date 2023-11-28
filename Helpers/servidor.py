import socket
import threading
import pickle
from users import Recrutador, Candidato

HOST = '0.0.0.0'
PORT = 5000

print('=== Servidor ===')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
clientes = {}
TableCandidatos = {} # -> hash table

def handle_client(client_socket):
    pass

def recrutador():
    pass

def candidato():
    pass

def protocol(msg, cliente):
    #GET -> Pegar informações informações de candidaturas, informações de vagas e lista de candidatos(caso Recrutador).
    #POST -> Postar infomações como vaga, novo usuario ou recrutador.
    #DELETE -> Deletar usuários(Recrutador e Candidato) e Vagas, ou cancelar candidatura caso usuário.
    #EDIT -> Editar informações referente ao perfil do usuário.
    #APPLY -> Referente ao usuario candidatar em uma vaga.
    
    if msg == 'POST':
        print('teste')
        
        # data_cliente -> dicionario envidado do cliente para o servidor com as informações de tipo e cada campo de acordo com o tipo
        data_cliente = cliente.recv(1024)
        data_cliente = pickle.loads(data_cliente) # -> usando o pickle para decodificar o dicionario
        
        print(data_cliente)
        
        if data_cliente["type"] == "candidato":
            
            candidato = Candidato(data_cliente["nome"], data_cliente["email"], data_cliente["senha"]) #-> intanciando um candidato usando as chaves do dicionario enviado pelo cliente.
            TableCandidatos[data_cliente["id"]] = candidato # -> adicionando no dicionario o candidato e a chave é o campo id.
            print(TableCandidatos[data_cliente["id"]])
            
            # protocol_response = '200 OK: "Candidato cadastrado com Sucesso !"'
            # cliente.send(protocol_response.encode('utf-8'))
            
            print()
            print('Lista de Candidatos')
            print()
            
            
        elif data_cliente["type"] == "recrutador":
            pass
        

def runServer():
    while True:
        cliente, endereco = server.accept()
        protocol_msg = cliente.recv(1024)
        clientes[cliente] = endereco
        t1 = threading.Thread(target=protocol, args=(protocol_msg.decode('utf-8'), cliente,))
        t1.start()
        
        # Não estou conseguindo estabelecer dois clientes ao mesmo tempo 
        
        
runServer()