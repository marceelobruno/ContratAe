"""
Servidor - Protocolo SPC (Securitas Protocol ContratAe)
"""
import json
import socket
import threading

from DataStructures.ChainingHashTable import ChainingHashTable
from DataStructures.ListaSequencialNumPY import Lista
from loguru import logger
from supabase_db import CandidatoDB, RecrutadorDB, VagaDB
from users import Candidato, Recrutador

HOST = '0.0.0.0'
PORT = 5000

print("=== Servidor ===\n")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

TableCandidatos = ChainingHashTable()
TableRecrutadores = ChainingHashTable()
ListaVagas = Lista()
clientes = {}
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

    # print(TableCandidatos)
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
    # print(TableRecrutadores)
    return logger.info('Recrutadores inseridos na HashTable')


def get_vagas_from_supabase() -> list:
    """ Retornando os dados da tabela Vaga para a Lista de Vagas """
    vaga = VagaDB()
    vaga_data = vaga.get_all_vagas()

    for i, vaga in enumerate(vaga_data):
        ListaVagas.append(vaga)

    # print(ListaVagas)
    return logger.info("Vagas inseridas na Lista de Vagas")




def get_vagas_from_supabase_2() -> list:
    user_recrutador = TableRecrutadores[data_cliente["cpf"]]
    vaga_info = data_cliente['vaga_info']

    vagaTemporaria = user_recrutador.criar_vaga(
        vaga_info["nome_vaga"],
        vaga_info["area_vaga"],
        vaga_info["descricao_vaga"],
        vaga_info["quant_candidaturas"],
        user_recrutador.empresa,
        vaga_info["salario_vaga"], vaga_info["requisitos"])
    ListaVagas.append(vagaTemporaria)




def handle_client(cliente, addr=None):
    try:
        data_recv = cliente.recv(1024)
        data_recv_decoded = json.loads(data_recv.decode('utf-8'))
        data_cliente =  data_recv_decoded

        protocol(cliente, data_cliente, addr)

    except json.decoder.JSONDecodeError:
        print(clientes[addr], ' desconectou.')
    except ConnectionResetError:
        print(clientes[addr], ' desconectou.')
    except ConnectionAbortedError:
        print(clientes[addr], ' desconectou.')

def recrutador(data_cliente):
    user_recrutador = TableRecrutadores[data_cliente["cpf"]]  # -> recuperando a referencia do objeto Recrutador
    if user_recrutador:
        return user_recrutador  # -> enviando a referencia do objeto para o cliente
    else:
        return None

def candidato(data_cliente):
    user_candidato = TableCandidatos[data_cliente["cpf"]]  # -> recuperando a referencia do objeto Candidato
    if user_candidato:
        return user_candidato  # -> enviando a referencia do objeto para o cliente
    else:
        return None

def formatar_lista(lista):
    lista_formatada = []
    for i in lista:
        lista_formatada.append(i.dict_vagaMOD())
    return lista_formatada

def procurar_vaga(lista, idVaga):
    try:
        for vaga in lista:
            return vaga if vaga['id'] == idVaga else None
    except:
        for vaga in lista:
            return vaga if vaga.id == idVaga else None


def protocol(cliente, data_cliente, addr):
    """
    GET -> Pegar informações de candidaturas, informações de vagas e lista de candidatos (caso Recrutador).
    POST -> Postar informações como vaga, novo usuário ou recrutador.
    DELETE -> Deletar usuários (Recrutador e Candidato) e vagas.
    APPLY -> Referente ao usuário candidatar-se a uma vaga.
    UNAPPLY -> Retira a candidatura de uma vaga.
    """

    if data_cliente["protocol_msg"] == 'LOGIN':

        print("entrei", data_cliente["protocol_msg"])

        if data_cliente["type"] == "c":
            user_candidato = candidato(data_cliente)
            if user_candidato:
                if user_candidato.senha == data_cliente["senha"]:
                    protocol_response = {'status': '200 OK', 'message': 'Candidato autenticado.', 'data': data_cliente['cpf']}

                    logger.info(f'Candidato {data_cliente["cpf"]} autenticado.')
                    data_send = json.dumps(protocol_response).encode('utf-8')
                    cliente.send(data_send)
                    handle_client(cliente, addr)

                else:
                    protocol_response = {"status": "401 Unauthorized", "message": "Senha inválida !"}
            else:
                protocol_response = {"status": "404 Not Found", "message": "Usuário não encontrado !"}

            cliente.send(json.dumps(protocol_response).encode('utf-8'))
            handle_client(cliente, addr)

        elif data_cliente["type"] == "r":
                user_recrutador = recrutador(data_cliente)
                if user_recrutador:
                    if user_recrutador.senha == data_cliente["senha"]:
                        protocol_response = {"status": "200 Ok", "message":'Recrutador', "data": data_cliente['cpf']}

                        logger.info(f'Recrutador {data_cliente["cpf"]} autenticado.')
                        cliente.send(json.dumps(protocol_response).encode('utf-8'))
                        handle_client(cliente, addr)
                    else:
                        protocol_response = {"status": "401 Unauthorized", "message": "Senha inválida !"}
                else:
                    protocol_response = {"status": "404 Not Found", "message": "Usuário não encontrado !"}
                
                cliente.send(json.dumps(protocol_response).encode('utf-8'))
                handle_client(cliente, addr)

    #  -------------- VER VAGAS ----------------
    elif data_cliente['protocol_msg'] == 'verVagas':

        logger.info(f'Candidato {data_cliente["cpf"]} requisitou {data_cliente["protocol_msg"]}')

        if len(ListaVagas) == 0:
            protocol_response = {"status": "404 Not Found", "message": 'Não há vagas cadastradas...'}
            cliente.send(json.dumps(protocol_response).encode('utf-8'))
            handle_client(cliente, addr)

        else:
            lista_formatada = formatar_lista(ListaVagas)
            protocol_response = {"status": "200 OK", "data": lista_formatada}
            cliente.send(json.dumps(protocol_response).encode('utf-8'))
            handle_client(cliente, addr)

    # ------------------------ VER CANDIDATURAS ----------------------
    elif data_cliente['protocol_msg'] == 'verCandidaturas':

        logger.info(f'Cliente {data_cliente["cpf"]} requisitou {data_cliente["protocol_msg"]}')

        if data_cliente['type'] == 'c':
            vagasCandidato = TableCandidatos[data_cliente["cpf"]].vagas_aplicadas
            # #Essa expressão 
            # for vaga in vagasCandidato:
            #     vaga.pop('lista_candidaturas')
            print(vagasCandidato)

            if len(vagasCandidato) == 0:
                protocol_response = {"status":"404 Not Found", "message":"Você não se candidatou a nenhuma vaga."}
                cliente.send(json.dumps(protocol_response).encode('utf-8'))
                handle_client(cliente, addr)
            else: 
                protocol_response = {"status":"200 OK", "data": vagasCandidato }
                cliente.send(json.dumps(protocol_response).encode('utf-8'))
                handle_client(cliente, addr)

        elif data_cliente['type'] == 'r':
            vaga = procurar_vaga(ListaVagas, data_cliente['idVaga'])

            if vaga == None:
                protocol_response = {"status": '404 Not Found', "message": 'Vaga não encontrada.'}
                cliente.send(json.dumps(protocol_response).encode('utf-8'))
                handle_client(cliente,addr)

            elif len(vaga.lista_candidaturas) == 0:
                protocol_response = {"status": '404 Not Found', "message": 'Sua vaga não possui candidaturas.'}
                cliente.send(json.dumps(protocol_response).encode('utf-8'))
                handle_client(cliente,addr)
            else:
                protocol_response = {"status":"200 OK", "data": vaga.lista_candidaturas }
                cliente.send(json.dumps(protocol_response).encode('utf-8'))
                handle_client(cliente, addr)

    # -----------VER PERFIL-------------
    elif data_cliente['protocol_msg'] == 'verPerfil':

        logger.info(f'Candidato {data_cliente["cpf"]} requisitou {data_cliente["protocol_msg"]}')

        usuario = TableCandidatos[data_cliente["cpf"]]
        usuario_info = usuario.dict_user()
        protocol_response = {"status": "200 OK", "data": usuario_info}

        data_send = json.dumps(protocol_response).encode('utf-8')
        cliente.send(data_send)
        handle_client(cliente, addr)

    # -------------------------- CRIAR -----------------------------
    elif data_cliente['protocol_msg'] == 'CRIAR':

        logger.info(f'Cliente {data_cliente["cpf"]} requisitou {data_cliente["protocol_msg"]}')

        print("entrei", data_cliente['protocol_msg'])

        if data_cliente["type"] == "c":
            if data_cliente["cpf"] not in TableCandidatos:
                TableCandidatos[data_cliente["cpf"]] = Candidato(
                    data_cliente["nome"], data_cliente["email"], data_cliente["senha"], data_cliente["cpf"])

                user_candidato = TableCandidatos[data_cliente["cpf"]]
                logger.info(f'Candidato {user_candidato.cpf} criado.')
                protocol_response = {"status": '201 Created', 'message': 'Usuario criado.', "data": data_cliente['cpf']}
                cliente.send(json.dumps(protocol_response).encode('utf-8'))

                # Inserindo os dados do Candidato no Banco de Dados
                candidate = CandidatoDB()
                candidate.insert_candidato(
                    data_cliente["cpf"], data_cliente["nome"],
                    data_cliente["email"], data_cliente["senha"])

                handle_client(cliente, addr)

            else:
                protocol_response = {"status": "400 Bad Request", "message": "CPF já cadastrado."}
                cliente.send(json.dumps(protocol_response).encode('utf-8'))
                handle_client(cliente, addr)
                    
        elif data_cliente["type"] == "r":

                if data_cliente["cpf"] not in TableRecrutadores:

                    TableRecrutadores[data_cliente["cpf"]] = Recrutador(
                        data_cliente["nome"],
                        data_cliente['email'],
                        data_cliente["senha"],
                        data_cliente["cpf"],
                        data_cliente["empresa"]
                    )

                    protocol_response = {"status": '201 Created', "message": "Usuário criado.", 'data': data_cliente['cpf']}
                    cliente.send(json.dumps(protocol_response).encode('utf-8'))
                    
                    # Inserindo os dados do Recrutador no Banco de Dados
                    recruiter = RecrutadorDB()
                    recruiter.insert_recrutador(
                        data_cliente["cpf"], data_cliente["nome"],
                        data_cliente["empresa"], data_cliente["email"], data_cliente["senha"])
                    handle_client(cliente, addr)
                else:
                    protocol_response = {"status": "400 Bad Request", "message": "CPF já cadastrado."}
                    cliente.send(json.dumps(protocol_response).encode('utf-8'))
                    handle_client(cliente, addr)

    # ---------------------- CRIAR VAGA ----------------------
    elif data_cliente["protocol_msg"] == "criar_vaga":

        user_recrutador = TableRecrutadores[data_cliente["cpf"]]
        vaga_info = data_cliente['vaga_info']

        vagaTemporaria = user_recrutador.criar_vaga(
            vaga_info["nome_vaga"],
            vaga_info["area_vaga"],
            vaga_info["descricao_vaga"],
            vaga_info["quant_candidaturas"],
            user_recrutador.empresa,
            vaga_info["salario_vaga"], vaga_info["requisitos"])

        ListaVagas.append(vagaTemporaria)
        logger.info(f'Vaga criada! - ID: {vagaTemporaria.id}')

        # Inserindo os dados da Vaga no Banco de Dados
        VagaDB().insert_vaga(
            vagaTemporaria.id,
            vaga_info["nome_vaga"],
            user_recrutador.cpf,
            vaga_info["area_vaga"],
            vaga_info["descricao_vaga"],
            vaga_info["quant_candidaturas"],
            user_recrutador.empresa,
            vaga_info["salario_vaga"],
            vaga_info["requisitos"],)

        print(ListaVagas)

        protocol_response = {"status": '201 Created', "message": "Vaga criada!", 'data': int(vagaTemporaria.id)}
        cliente.send(json.dumps(protocol_response).encode('utf-8'))
        handle_client(cliente, addr)

    # --------------- CANDIDATAR --------------------
    elif data_cliente['protocol_msg'] == 'candidatar':
        mutex.acquire()
        print("entrei", data_cliente['protocol_msg'])
        # logger.info('entrei')

        idVaga = data_cliente['idVaga']
        cand = TableCandidatos[data_cliente["cpf"]].dict_user()
        cpf_cand = cand['cpf']

        if len(ListaVagas) == 0:
            protocol_response = {"status": "404 Not Found", "message": 'Não há vagas cadastradas...'}
            cliente.send(json.dumps(protocol_response).encode('utf-8'))
            mutex.release()
            handle_client(cliente, addr)


        for vaga in ListaVagas:
            if vaga.id == idVaga:
                if vaga.vagaEstaCheia():
                    protocol_response = {"status": "400 Bad Request", "message": 'Limite de candidaturas alcançados.'}
                    cliente.send(json.dumps(protocol_response).encode('utf-8'))
                    mutex.release()
                    handle_client(cliente, addr)
                else:
                    if cand in vaga.lista_candidaturas:
                        protocol_response = {"status": "400 Bad Request", "message": 'Você já se candidatou a essa vaga.'}
                        cliente.send(json.dumps(protocol_response).encode('utf-8'))
                        mutex.release()
                        handle_client(cliente, addr)

                    cand = TableCandidatos[data_cliente["cpf"]]

                    vaga.adicionarCandidatura(cand.dict_user())
                    cand.candidatar(vaga.dict_vagaMOD())

                    # Cadastra em uma vaga determinado candidato na tabela Candidaturas
                    CandidatoDB().candidatar_se(cpf_cand, idVaga)

                    protocol_response = {"status": "200 OK", "message": 'Candidatura registrada com sucesso!'}
                    logger.info(protocol_response["message"])
                    # print(cand.vagas_aplicadas)
                    cliente.send(json.dumps(protocol_response).encode('utf-8'))
                    mutex.release()
                    handle_client(cliente, addr)
            
        protocol_response = {"status": "404 Not Found", "message": 'Vaga não encontrada.'}
        cliente.send(json.dumps(protocol_response).encode('utf-8'))
        mutex.release()
        handle_client(cliente, addr)

    # ---------------------- CANCELAR CANDIDATURA --------------------------
    elif data_cliente['protocol_msg'] == "cancelarCandidatura":
        # mutex.acquire()
            print("entrei", data_cliente['protocol_msg'])

            cand_ = TableCandidatos[data_cliente["cpf"]].dict_user()
            cpf_cand_ = cand_['cpf']

            idVaga = data_cliente['idVaga']
            candi = TableCandidatos[data_cliente["cpf"]]
            lista_candi = candi.vagas_aplicadas

            info_vaga = procurar_vaga(lista_candi, idVaga)
            if info_vaga:

                info_vaga['lista_candidaturas'].remove(candi.dict_user())
                candi.cancelar_candidatura(info_vaga)
                info_vaga2 = procurar_vaga(ListaVagas, idVaga)
                info_vaga2.aumentar_quantidade()

                protocol_response = {'status': "200 OK", 'message': 'Cancelamento efetuado com sucesso!'}

                # Cancelando determinada candidatura para um Candidato
                CandidatoDB().delete_candidatura(cpf_cand_, idVaga)

                cliente.send(json.dumps(protocol_response).encode('utf-8'))
                handle_client(cliente, addr)
            else:
                protocol_response = {"status": "404 Not Found", "message": 'Vaga não encontrada.'}
                cliente.send(json.dumps(protocol_response).encode('utf-8'))
                # mutex.release()
                handle_client(cliente, addr)

    # --------------------- VERIFICAR -------------------------
    elif data_cliente['protocol_msg'] == "VERIFICAR":
        usuario = TableCandidatos[data_cliente["cpf"]]

        if usuario.perfil_completo():
            data_send = {'status':'200 OK', 'message':'Seu perfil está completo.'}
        else:
            data_send = {'status':'406 Incomplete', 'message':'Seu perfil está incompleto.'}
        cliente.send(json.dumps(data_send).encode('utf-8'))
        handle_client(cliente, addr)

    # --------------------- COMPLETAR PERFIL ------------------
    elif data_cliente['protocol_msg'] == "completarPerfil":
        usuario = TableCandidatos[data_cliente["cpf"]]

        usuario.criar_perfil(data_cliente['skills'], data_cliente['area'], data_cliente['descricao'],data_cliente['cidade'], data_cliente['uf'])
        
        # Inserindo as informações complementares do Candidato no Banco de Dados
        candidate = CandidatoDB()
        candidate.completar_perfil_candidato(
            data_cliente["cpf"], data_cliente['skills'], data_cliente['area'],
            data_cliente['descricao'], data_cliente['cidade'], data_cliente['uf'])

        print(usuario)
        protocol_response = {'status': "201 Criado", 'message': 'Seu perfil está completo.'}
        cliente.send(json.dumps(protocol_response).encode('utf-8'))
        handle_client(cliente, addr)

def run_server():
    get_candidatos_from_supabase()
    get_recrutadores_from_supabase()
    # get_vagas_from_supabase()

    while True:
        cliente, addr = server.accept()
        print(cliente, ' conectou.')
        clientes[addr] = cliente
        t1 = threading.Thread(target=handle_client, args=(cliente, addr))
        t1.start()

# Retornando os dados da tabela candidato para a hashtable-candidato
# get_candidatos_from_supabase()
# get_recrutadores_from_supabase()
# print(TableCandidatos)


# print(TableRecrutadores)
run_server()
get_recrutadores_from_supabase()
