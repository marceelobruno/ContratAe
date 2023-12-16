import socket
import json
import re 
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
        while True:
            protocol_msg = "LOGIN"
            while True:
                cpf = input('CPF: ')
                if all(cpf.isdigit() for cpf in cpf):
                    break
                else:
                    print('O CPF é inválido')
            # hasheando a senha para sha256
            hash_passwd = sha256(input("senha: ").encode('utf-8'))
            # convertendo a senha de bytes para hexadecimal
            senha = hash_passwd.hexdigest()

            data = {
                "protocol_msg" : protocol_msg,
                "type": type,
                "cpf" : cpf,
                "senha" : senha
            }
            #transforma a data em json
            data_send = json.dumps(data).encode('utf-8')
            cliente_socket.send(data_send)  # -> enviando via sockets
            

            response_server = cliente_socket.recv(1024)
            response_server = json.loads(response_server.decode('utf-8'))
            
            if response_server["status"] == "404 Not Found" or response_server["status"] == "401 Unauthorized":
                print(response_server["message"])
                
            else:
                dashboard(response_server['data'],type)
                break

            # except:
            #     print('Conexão com o servidor não foi estabelecida corretamente')

    elif action == "criar":
        protocol_msg = "CRIAR"  # -> definindo a flag do protocolo.
        # cliente_socket.send(protocol_msg.encode('utf-8''utf-8'))
        # cliente_socket.send(json.dumps(protocol_msg))
        while True:

            nome = input("Digite o nome: ")
            email = input("Digite o email: ")
            cpf = input("Digite seu CPF: ")

            # hasheando a senha para sha256
            hash_passwd = sha256(input("Digite sua senha: ").encode('utf-8'))
            # convertendo a senha de bytes para hexadecimal
            senha = hash_passwd.hexdigest()

            empresa = ''
            if type == "r":
                empresa = input("Digite a empresa para a qual você está recrutando: ")

            data_cliente ={
                'protocol_msg': protocol_msg,
                'nome': nome,
                'email':email,
                'cpf':cpf,
                'type':type,
                'senha':senha,
                'empresa':empresa
            }

            data_send = json.dumps(data_cliente).encode('utf-8')
            cliente_socket.send(data_send) # -> envian via sockets
            
            response_server = cliente_socket.recv(1024)
            response_server = json.loads(response_server.decode('utf-8')) # -> resposta do servidor
        
            if response_server["status"] == "400 Bad Request":
                print(response_server["message"])
                
            else:
                dashboard(response_server['data'],type) # -> chamando a função principal do cliente
                break

def dashboard(cpf,type):

    if type == "c": # -> aqui ficará a área do candidato
        data_veri = {
            'protocol_msg': 'VERIFICAR',
            'cpf': cpf
        }
        cliente_socket.send(json.dumps(data_veri).encode('utf-8'))

        response_server = cliente_socket.recv(1024)
        response_server = json.loads(response_server.decode('utf-8'))

        if response_server['status'] == '406 Incomplete':
            print(response_server['message'])

            listSkills = []
            area = input('Área: ')

            while True:
                skill = input('Digite suas competências (digite . para encerrar): ')
                if skill == '.':
                    break
                listSkills.append(skill)

            descricao = input('Descrição (até 140 caracteres): ')
            cidade = input('Cidade: ')
            uf = input('UF: ')

            data = {
                'protocol_msg': 'completarPerfil',
                'cpf': cpf,
                'area': area,
                'descricao':descricao,
                'skills': listSkills,
                'cidade':cidade,
                'uf':uf
            }

            cliente_socket.send(json.dumps(data).encode('utf-8'))

            response_serverP = cliente_socket.recv(1024)
            response_serverP = json.loads(response_serverP.decode('utf-8')) 
            
            print(response_serverP['message'])

        while True:
            while True:
                try:
                    print()
                    entrada = input('Digite o que deseja fazer:\n\n1-Ver vagas\n2-Candidatar a vaga\n3-Cancelar candidatura\n4-Ver perfil\n5-Ver candidaturas\n\n')
                    print()
                    assert entrada in ['1','2','3','4','5'], 'Escolha uma das opções acima.'
                    break
                except AssertionError as ae:
                    print(ae)

            content_dash = {}
            idVaga = ''
            
            if entrada == '1':
                protocol_msg = 'verVagas'

            elif entrada == '2':
                protocol_msg = 'candidatar'
                while True:
                    try:
                        idVaga = int(input('Digite o id da vaga: '))
                        content_dash['idVaga'] = idVaga
                        break
                    except ValueError:
                        print('Digite um número inteiro referente a vaga em questão.')

            elif entrada == '3':
                protocol_msg = 'cancelarCandidatura'
                
                while True:
                    try:
                        idVaga = int(input('Digite o id da vaga: '))
                        content_dash['idVaga'] = idVaga
                        break
                    except ValueError:
                        print('Digite um número inteiro referente a vaga em questão.')                

            elif entrada == '4':
                protocol_msg = 'verPerfil'
 
            elif entrada == '5':
                protocol_msg = 'verCandidaturas'

            content_dash['protocol_msg'] = protocol_msg
            content_dash['cpf'] = cpf

            cliente_socket.send(json.dumps(content_dash).encode('utf-8'))

            response_server = cliente_socket.recv(1024)
            response_server = json.loads(response_server.decode('utf-8'))

            if protocol_msg == 'verVagas':

                if response_server["status"] == "404 Not Found":
                    print(response_server["message"])
                else:
                    listaVagas = response_server['data']
                    for vaga in listaVagas:
                        print(f"""
                        -------------------------                              

                        Nome: {vaga["nome"]}
                        ID: {vaga['id']}
                        Area: {vaga["area"]}
                        Descricao: {vaga["descricao"]}
                        Quantidade de vagas: {vaga['quantidade']}
                        Empresa: {vaga['nome_empresa']}
                        Salario: {vaga['salario']}
                        Requisitos: {vaga['requisitos']}

                        -------------------------

                        """)

            elif protocol_msg == 'candidatar' or protocol_msg == "cancelarCandidatura":

                if response_server['status'] == "200 OK":
                    logger.info(response_server['message'])
                else:
                    logger.error(response_server['message'])
                
            elif protocol_msg == 'verCandidaturas':

                if response_server['status']  == '200 OK':
                    candidato_candidaturas = response_server['data']
                    print('\nEstas são as vagas que você se candidatou:\n')
                    for vaga in candidato_candidaturas:
                        print(f"""
                        -------------------------                              

                        Nome: {vaga["nome"]}
                        ID: {vaga['id']}
                        Area: {vaga["area"]}
                        Descricao: {vaga["descricao"]}
                        Quantidade de vagas: {vaga['quantidade']}
                        Empresa: {vaga['nome_empresa']}
                        Salario: {vaga['salario']}
                        Requisitos: {vaga['requisitos']}

                        -------------------------

                        """)

                elif response_server['status'] == '404 Not Found':
                    print(response_server['message'])


            elif protocol_msg == 'verPerfil':
                perfil = response_server['data']
                print(f"""
                      
        Nome: {perfil['nome']}                         
        CPF: {perfil['cpf']}
        Email: {perfil['email']}
        Skills: {perfil['skills']}
        Area: {perfil['area']}
        Descricao: {perfil['descricao']}
        Cidade: {perfil['cidade']}
        Uf: {perfil['uf']} 

""")


    elif type == 'r':
        while True:
            print()
            print('Bem-vindo ao ContratAe!')
            print("----------------------")
            protocol_msg = "criar_vaga"
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

            
            data_cliente = {'protocol_msg': protocol_msg, 'type': 'r', 'cpf': cpf, 'vaga_info': dict_vaga}
            
            cliente_socket.send(json.dumps(data_cliente).encode('utf-8'))
            
            response_server = cliente_socket.recv(1024)
            response_server = json.loads(response_server.decode('utf-8'))
            
            logger.info(response_server["message"])

            # cliente_socket.close()

run_cliente()
