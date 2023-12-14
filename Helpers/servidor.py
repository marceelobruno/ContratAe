"""
Servidor - Protocolo SPC (Securitas Protocol ContratAe)
"""
import pickle
import socket
import threading

from DataStructures.ChainingHashTable import ChainingHashTable
from DataStructures.ListaSequencialNumPY import Lista
from loguru import logger
from supabase_db import CandidatoDB, RecrutadorDB
from users import Candidato, Recrutador

# from vaga import Vaga

HOST = '0.0.0.0'
PORT = 5000

print("=== Servidor ===\n")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
TableCandidatos = ChainingHashTable()
TableRecrutadores = ChainingHashTable()
ListaVagas = Lista()
mutex = threading.Semaphore(1)


def get_candidatos_from_supabase() -> None:
    """Retornando os dados da tabela Candidato para a hashtable-candidato"""
    candidatos = CandidatoDB()
    data = candidatos.get_all_candidatos()

    for i, candidate in enumerate(data):  # manter o i ao lado do for
        list_candidate = candidate

        TableCandidatos[list_candidate["cpf"]] = Candidato(
            list_candidate["nome"],
            list_candidate["email"],
            list_candidate["senha"],
            list_candidate["cpf"],
            list_candidate["skills"],
            list_candidate["area"],
            list_candidate["descricao"],
            list_candidate["cidade"],
            list_candidate["uf"],
        )

    print(TableCandidatos)
    return logger.info('Candidatos inseridos na HashTable')


def get_recrutadores_from_supabase() -> None:
    """Retornando os dados da tabela recrutador para a hashtable-recrutador"""
    recrutador = RecrutadorDB()
    rec_data = recrutador.get_all_recrutadores()

    for i, recruiter in enumerate(rec_data):  # manter o i ao lado do for
        list_recruiter = recruiter

        TableRecrutadores[list_recruiter["cpf"]] = Recrutador(
            list_recruiter["nome"],
            list_recruiter["email"],
            list_recruiter["senha"],
            list_recruiter["cpf"],
            list_recruiter["empresa"],
        )
    print(TableRecrutadores)
    return logger.info('Recrutadores inseridos na HashTable')


def get_recrutadores_from_db() -> None:
    """Retornando os dados da tabela Candidato para a hashtable-candidato"""
    # recrutador = RecrutadorDB()
    # data = recrutador.get_all_recrutadores()


def handle_client(cliente):

    protocol_msg = cliente.recv(1024)
    protocol_msg = pickle.loads(protocol_msg)
    protocol(protocol_msg,cliente)

def recrutador(data_cliente):
    user_recrutador = TableRecrutadores[data_cliente["cpf"]]  # -> recuperando a referencia do objeto candidato
    if user_recrutador:
        return user_recrutador # -> enviando a referencia do objeto para o cliente
    else:
        return None

def candidato(data_cliente):
    user_candidato = TableCandidatos[data_cliente["cpf"]]  # -> recuperando a referencia do objeto candidato
    if user_candidato:
        return user_candidato # -> enviando a referencia do objeto para o cliente
    else:
        return None

def protocol(protocol_msg, cliente):
    """
    GET -> Pegar informações de candidaturas, informações de vagas e lista de candidatos (caso Recrutador).
    POST -> Postar informações como vaga, novo usuário ou recrutador.
    DELETE -> Deletar usuários (Recrutador e Candidato) e vagas.
    APPLY -> Referente ao usuário candidatar-se a uma vaga.
    UNAPPLY -> Retira a candidatura de uma vaga.
    """
    if protocol_msg == 'GET':
        while True:
            print("entrei", protocol_msg)
            data_cliente = pickle.loads(cliente.recv(1024))
            print(data_cliente)
        
            if data_cliente["type"] == "c":
                if data_cliente['action'] == 'login':
                    user_candidato = candidato(data_cliente)
                    if user_candidato:
                        if user_candidato.senha == data_cliente["senha"]:
                            protocol_response = {"status": "200 Ok", "data": user_candidato}
                            cliente.send(pickle.dumps(protocol_response))
                            handle_client(cliente)
                            break
                        else:
                            protocol_response = {"status": "401 Unauthorized", "message": "Senha inválida !"}
                    else:
                        protocol_response = {"status": "404 Not Found", "message": "Usuário não encontrado !"}
                    
                    cliente.send(pickle.dumps(protocol_response))
                    handle_client(cliente)
                    break

                elif data_cliente['action'] == 'verVagas':
                    if len(ListaVagas) == 0:
                        protocol_response = {"status": "404 Not Found", "message": 'Não há vagas...'}
                        cliente.send(pickle.dumps(protocol_response))
                        handle_client(cliente)
                        break
                    else:
                        protocol_response = {"status": "200 OK", "data": ListaVagas}
                        cliente.send(pickle.dumps(protocol_response))
                        handle_client(cliente)
                        break
                
                elif data_cliente['action'] == 'verCandidaturas':
                    vagasCandidato = TableCandidatos[data_cliente["cpf"]].vagas_aplicadas
                    if len(vagasCandidato) == 0:
                        protocol_response = {"status":"404 Not Found", "message":"Não há candidaturas."}
                        cliente.send(pickle.dumps(protocol_response))
                        handle_client(cliente)
                        break
                    else: 
                        protocol_response = {"status":"200 OK", "data": vagasCandidato }
                        cliente.send(pickle.dumps(protocol_response))
                        handle_client(cliente)
                        break

            elif data_cliente["type"] == "r":
                
                if data_cliente['action'] == 'login':
                    user_recrutador = recrutador(data_cliente)
                    if user_recrutador:
                        if user_recrutador.senha == data_cliente["senha"]:
                            protocol_response = {"status": "200 Ok", "data": user_recrutador}
                            cliente.send(pickle.dumps(protocol_response))
                            handle_client(cliente)
                            break
                        else:
                            protocol_response = {"status": "401 Unauthorized", "message": "Senha inválida !"}
                    else:
                        protocol_response = {"status": "404 Not Found", "message": "Usuário não encontrado !"}
                    
                    cliente.send(pickle.dumps(protocol_response))
            
    elif protocol_msg == 'POST':
        while True:
            print("entrei", protocol_msg)
            data_cliente = cliente.recv(1024) # data_cliente -> dicionario envidado do cliente para o servidor com as informacoes de tipo e cada campo de acordo com o tipo
            data_cliente = pickle.loads(data_cliente) # -> usando o pickle para decodificar o dicionario
            
            if data_cliente["type"] == "c":
                
                if data_cliente['action'] == 'criar':
                    
                    if data_cliente["cpf"] not in TableCandidatos:
                        
                        TableCandidatos[data_cliente["cpf"]] = Candidato(
                            data_cliente["nome"], data_cliente["email"], data_cliente["senha"], data_cliente["cpf"])
                        
                        user_candidato = TableCandidatos[data_cliente["cpf"]]
                        logger.info(f'{user_candidato}')
                        protocol_response = {"status": '201 Created', "data": user_candidato}
                        cliente.send(pickle.dumps(protocol_response))
                        
                        # Inserindo os dados do Candidato no Banco de Dados
                        candidate = CandidatoDB()
                        candidate.insert_candidato(data_cliente["cpf"], data_cliente["nome"],
                        data_cliente["email"], data_cliente["senha"])
                        
                        handle_client(cliente)
                        break

                    else:
                        protocol_response = {"status": "400 Bad Request", "message": "CPF já cadastrado."}
                        cliente.send(pickle.dumps(protocol_response))
                        
            elif data_cliente["type"] == "r":
                
                if data_cliente['action'] == 'criar':
                    
                    if data_cliente["cpf"] not in TableRecrutadores:
            
                        TableRecrutadores[data_cliente["cpf"]] = Recrutador(
                            data_cliente["nome"],
                            data_cliente["nomeEmpresa"],
                            data_cliente["senha"],
                            data_cliente["cpf"],
                        )

                        protocol_response = {"status": '201 Created', "data": TableRecrutadores[data_cliente["cpf"]]}
                        cliente.send(pickle.dumps(protocol_response))
                        
                        # Inserindo os dados do Recrutador no Banco de Dados
                        recruiter = RecrutadorDB()
                        recruiter.insert_recrutador(data_cliente["cpf"], data_cliente["nome"],
                        data_cliente["nomeEmpresa"], data_cliente["email"], data_cliente["senha"])

                        handle_client(cliente)
                        break
                    else:
                        protocol_response = {"status": "400 Bad Request", "message": "CPF já cadastrado."}
                        cliente.send(pickle.dumps(protocol_response))
                        
                elif data_cliente["action"] == "criar_vaga":
                    user_recrutador = TableRecrutadores[data_cliente["cpf"]]
                    vaga_info = pickle.loads(cliente.recv(1024))
                    
                    ListaVagas.append(user_recrutador.criar_vaga(vaga_info["nome_vaga"],
                          vaga_info["area_vaga"],
                          vaga_info["descricao_vaga"],
                          vaga_info["quant_candidaturas"],
                          data_cliente['empresa'],
                          vaga_info["salario_vaga"], vaga_info["requisitos"]))
                    
                    protocol_response = {"status": '201 Created', "message": "Vaga criada !"}
                    cliente.send(pickle.dumps(protocol_response))
                    break

    elif protocol_msg == 'APPLY':
        mutex.acquire()
        while True:
            print("entrei", protocol_msg)
            data_cliente = cliente.recv(1024) 
            data_cliente = pickle.loads(data_cliente)
            print(data_cliente)

            logger.info('entrei')

            idVaga = data_cliente['idVaga']
            for vaga in ListaVagas:
                if vaga.id == idVaga:
                    if vaga.vagaEstaCheia():
                        protocol_response = {"status": "400 Bad Request", "message":'Limite de candidaturas alcançados.'}
                        cliente.send(pickle.dumps(protocol_response))
                        handle_client(cliente)
                        break
                    else:
                        cand = TableCandidatos[data_cliente["cpf"]]
                        cand.candidatar(vaga)
                        vaga.adicionarCandidatura(cand)
                        protocol_response = {"status": "200 OK","message": 'Candidatura registrada com sucesso!'}
                        logger.info(protocol_response["message"])
                        print(cand.vagas_aplicadas)
                        cliente.send(pickle.dumps(protocol_response))
                        handle_client(cliente)
                        break
                
            protocol_response = {"status":"404 Not Found", "message":'Vaga não encontrada.'}
            cliente.send(pickle.dumps(protocol_response))
            mutex.release()
            handle_client(cliente)
            break

    elif protocol_msg == "UNAPPLY":
        mutex.acquire()
        while True:
            print("entrei", protocol_msg)
            data_cliente = cliente.recv(1024) 
            data_cliente = pickle.loads(data_cliente)
            print(data_cliente)

            if data_cliente['type'] == "c":
                logger.info('entrei')
                if data_cliente['action'] == 'cancelarCand':
                    idVaga = data_cliente['idVaga']
                    candi = TableCandidatos[data_cliente["cpf"]]
                    logger.info(candi.vagas_aplicadas)
                    for vaga in candi.vagas_aplicadas:
                        if vaga.id == idVaga:
                            indice_remocao_cand = candi.vagas_aplicadas.busca(vaga)
                            candi.cancelar_candidatura(indice_remocao_cand)

                            indice_remocao_vaga = vaga.lista_candidaturas.busca(candi)
                            vaga.removerCandidatura(indice_remocao_vaga)

                            protocol_response = {'status':"200 OK", 'message': 'Cancelamento efetuado com sucesso.'}
                            cliente.send(pickle.dumps(protocol_response))
                            handle_client(cliente)
                            break
                    protocol_response = {"status":"404 Not Found", "message":'Vaga não encontrada.'}
                    cliente.send(pickle.dumps(protocol_response))
                    mutex.release()
                    handle_client(cliente)
                    break
                        
def run_server():
    while True:
        cliente, addr = server.accept()
        t1 = threading.Thread(target=handle_client, args=(cliente,))
        t1.start()


# Retornando os dados da tabela candidato para a hashtable-candidato
get_candidatos_from_supabase()

get_recrutadores_from_supabase()
# print(TableCandidatos)
print()
print()
# print(TableRecrutadores)
run_server()
