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
            entar(type_user, 'login')
            break

        elif login == 2:
            entar(type_user, 'criar')
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
        if not user.perfil_completo():
            print('Bem-vindo ao ContratAe!\n\nPara continuar é necessário que preencha as demais informações do perfil.')

            cand_area = input('Área de atuação: ')
            listSkills = []
            while True:
                cand_skills = input('Digite suas competências, 1 por vez (Digite "." para encerrar): ')
                if cand_skills == '.':
                    break
                listSkills.append(cand_skills)

            cand_descricao = input('Digite uma breve descrição ( até 140 caracteres ): ')
            cand_cidade = input('Informe sua cidade: ')
            cand_uf = input('Informe seu estado: ')

            user.criar_perfil(listSkills, cand_area, cand_descricao, cand_cidade, cand_uf) 
            print(user)

        while True:
            while True:
                try:
                    print()
                    entrada = input('Digite o que deseja fazer:\n\n1-Ver vagas\n2-Candidatar a vaga\n3-Cancelar candidatura\n4-Ver perfil\n5-Ver candidaturas\n\n')
                    print()
                    assert entrada in ['1','2','3','4','5'], 'Escolha uma opções acima.'
                    break
                except AssertionError as ae:
                    print(ae)
            idVaga = ''
            if entrada == '1':
                protocol_msg = 'GET'
                action = 'verVagas'

            elif entrada == '2':
                protocol_msg = 'APPLY'
                action = 'candidatar'
                while True:
                    try:
                        idVaga = int(input('Digite o id da vaga: '))
                        break
                    except ValueError:
                        print('Digite um número inteiro referente a vaga em questão.')

            elif entrada == '3':
                protocol_msg = 'UNAPPLY'
                action = 'cancelarCand'
                while True:
                    try:
                        idVaga = int(input('Digite o id da vaga: '))
                        break
                    except ValueError:
                        print('Digite um número inteiro referente a vaga em questão.')                

            elif entrada == '4':
                print(user)

            elif entrada == '5':
                protocol_msg = 'GET'
                action = 'verCandidaturas'

            if entrada in ['1','2','3','5']:

                cliente_socket.send(pickle.dumps(protocol_msg))
                data_cliente = {'action': action, 'type': 'c', 'idVaga': idVaga, 'cpf': user.cpf }
                cliente_socket.send(pickle.dumps(data_cliente))

                if action == 'verVagas':

                    response_server = cliente_socket.recv(1024)
                    response_server = pickle.loads(response_server) # -> resposta do servidor

                    if response_server["status"] == "404 Not Found":
                        print(response_server["message"])
                    else:
                        for i in response_server['data']:
                            print(i)

                elif action == 'candidatar' or action == 'cancelarCand':

                    response_server = cliente_socket.recv(1024)
                    response_server = pickle.loads(response_server) # -> resposta do 
                    
                    if response_server['status'] == "200 OK":
                        logger.info(response_server['message'])
                    else:
                        logger.error(response_server['message'])
                    
                elif action == 'verCandidaturas':

                    response_server =  cliente_socket.recv(1024)
                    response_server = pickle.loads(response_server)

                    if response_server['status']  == '200 OK':
                        for vaga in response_server['data']:
                            print(vaga)
                    if response_server['status'] == '404 Not Found':
                        print(response_server['message'])
                

    elif type == 'r':
        logger.info(user)
        print()
        print('Bem-vindo ao ContratAe!')
        print("----------------------")
        protocol_msg = "POST"
        cliente_socket.send(pickle.dumps(protocol_msg))
        print("Crie sua primeira vaga")
        print("----------------------")
        dict_vaga = {}
        dict_vaga["nome_vaga"] = input("Digite o nome da vaga: ")
        dict_vaga["area_vaga"] = input("Digite a área de atuação: ")
        dict_vaga["descricao_vaga"] = input("Digite uma breve descrição: ")
        dict_vaga["quant_candidaturas"] = int(input("Aceita quantas candidaturas? "))
        dict_vaga["salario_vaga"] = input("Digite o salário: ")
        dict_vaga["requisitos"] = []
        while True:
            resquisito_vaga = input('Digite os requisitos da vaga, 1 por vez (Digite "." para encerrar)')
            if resquisito_vaga == '.':
                break
            dict_vaga["requisitos"].append(resquisito_vaga)
        
        data_cliente = {'action': "criar_vaga", 'type': 'r', 'cpf': user.cpf, 'empresa': user.empresa }
        cliente_socket.send(pickle.dumps(data_cliente))
        cliente_socket.send(pickle.dumps(dict_vaga))
        
        response_server = cliente_socket.recv(1024)
        response_server = pickle.loads(response_server)
        logger.info(response_server["message"])
        cliente_socket.close()

run_cliente()
