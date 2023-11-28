import socket
import threading
import pickle
from ChainingHashTable import ChainingHashTable
from users import Recrutador, Candidato

HOST = '0.0.0.0'
PORT = 5000

print('=== Servidor ===')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
clientes = {}
TableCandidatos = ChainingHashTable() # -> hash table

def handle_client(client_socket):
    pass

def recrutador():
    pass

def candidato():
    pass

def protocol(msg, cliente):
    #GET -> Pegar informaÃ§Ãµes informaÃ§Ãµes de candidaturas, informaÃ§Ãµes de vagas e lista de candidatos(caso Recrutador).
    #POST -> Postar infomaÃ§Ãµes como vaga, novo usuario ou recrutador.
    #DELETE -> Deletar usuÃ¡rios(Recrutador e Candidato) e Vagas, ou cancelar candidatura caso usuÃ¡rio.
    #EDIT -> Editar informaÃ§Ãµes referente ao perfil do usuÃ¡rio.
    #APPLY -> Referente ao usuario candidatar em uma vaga.
    
    if msg == 'POST':
        
        # data_cliente -> dicionario envidado do cliente para o servidor com as informaÃ§Ãµes de tipo e cada campo de acordo com o tipo
        data_cliente = cliente.recv(1024)
        data_cliente = pickle.loads(data_cliente) # -> usando o pickle para decodificar o dicionario
        
        print(data_cliente)
        
        if data_cliente["type"] == "candidato":
            
            #candidato = Candidato(data_cliente["nome"], data_cliente["email"], data_cliente["senha"]) #-> intanciando um candidato usando as chaves do dicionario enviado pelo cliente.
            TableCandidatos[data_cliente["id"]] = Candidato(data_cliente["nome"], data_cliente["email"], data_cliente["senha"])# -> adicionando no dicionario o candidato e a chave Ã© o campo id.
            # TableCandidatos.showHashTable()
            
            # protocol_response = '200 OK: "Candidato cadastrado com Sucesso !"'
            # cliente.send(protocol_response.encode('utf-8'))
            
            print()
            print('Lista de Candidatos')
            print()
            
            print(TableCandidatos)
            
        elif data_cliente["type"] == "recrutador":
            pass
        

def runServer():
    while True:
        cliente, endereco = server.accept()
        protocol_msg = cliente.recv(1024)
        clientes[cliente] = endereco
        t1 = threading.Thread(target=protocol, args=(protocol_msg.decode('utf-8'), cliente,))
        t1.start()
        
        # NÃ£o estou conseguindo estabelecer dois clientes ao mesmo tempo 
        
        
runServer()