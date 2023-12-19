import json
import socket
import sys
from hashlib import sha256

from loguru import logger

HOST = '127.0.0.1'
PORT = 5000

servidor = (HOST, PORT)

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente_socket.connect(servidor)
except ConnectionRefusedError:
    print('Não foi possível estabelecer conexão com o servidor.')
    sys.exit(1)


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
                assert type_user in ['c','r'], 'Por favor, escolha entre (c) candidato ou (r) recrutador: '
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
            while True:
                cpf = input('CPF: ')
                if all(cpf.isdigit() for cpf in cpf):
                    break
                else:
                    print('O CPF é inválido')

            # hasheando a senha para sha256
            hash_passwd = sha256(input("Digite sua senha: ").encode('utf-8'))
            # convertendo a senha de bytes para hexadecimal
            senha = hash_passwd.hexdigest()

            empresa = ''
            if type == "r":
                empresa = input("Digite o nome da empresa para a qual você está recrutando: ")

            data_cliente = {
                'protocol_msg': protocol_msg,
                'nome': nome,
                'email': email,
                'cpf': cpf,
                'type': type,
                'senha': senha,
                'empresa': empresa
            }

            data_send = json.dumps(data_cliente).encode('utf-8')
            cliente_socket.send(data_send)  # -> enviando via sockets

            response_server = cliente_socket.recv(1024)
            response_server = json.loads(response_server.decode('utf-8'))  # -> resposta do servidor

            if response_server["status"] == "400 Bad Request":
                print(response_server["message"])
                
            else:
                dashboard(response_server['data'], type)  # -> chamando a função principal do cliente
                break

def mostrarVagas(vaga):
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

def dashboard(cpf, type):

    if type == "c":  # -> aqui ficará a área do candidato
        data_veri = {
            'protocol_msg': 'VERIFICAR',
            'cpf': cpf
        }
        cliente_socket.send(json.dumps(data_veri).encode('utf-8'))

        response_server = cliente_socket.recv(1024)
        response_server = json.loads(response_server.decode('utf-8'))

        if response_server['status'] == '406 Incomplete':
            print(response_server['message'])

            area = input('Área: ')
            habilidades = ''

            while True:
                skill = input('Digite suas competências (digite . para encerrar): ').strip()
                if skill == '.':
                    break
                elif len(skill) == 0:
                    print('Por favor, informe uma competência')
                    continue
                habilidades += "".join(skill + ',')

            listSkills = habilidades[:-1]

            descricao = input('Descrição (até 140 caracteres): ')
            cidade = input('Cidade: ')
            uf = input('UF: ')

            data = {
                'protocol_msg': 'completarPerfil',
                'cpf': cpf,
                'area': area,
                'descricao': descricao,
                'skills': listSkills,
                'cidade': cidade,
                'uf': uf
            }

            cliente_socket.send(json.dumps(data).encode('utf-8'))

            response_serverP = cliente_socket.recv(1024)
            response_serverP = json.loads(response_serverP.decode('utf-8')) 

            print(response_serverP['message'])
        print('\n\n----------------------')
        print('Bem-vindo ao ContratAe!')
        print("----------------------")

        while True:
            while True:
                try:
                    print()
                    entrada = input('Digite o que deseja fazer:\n\n1-Ver vagas\n2-Candidatar a vaga\n3-Cancelar candidatura\n4-Ver perfil\n5-Ver candidaturas\n6-Sair\n\n')
                    print()
                    assert entrada in ['1','2','3','4','5','6'], 'Escolha uma das opções acima.'
                    break
                except AssertionError as ae:
                    print(ae)

            content_dash = {}

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

            elif entrada == '6':
                cliente_socket.close()
                sys.exit(1)

            content_dash['protocol_msg'] = protocol_msg
            content_dash['cpf'] = cpf
            content_dash['type'] = type
            cliente_socket.send(json.dumps(content_dash).encode('utf-8'))

            response_server = cliente_socket.recv(1024)
            response_server = json.loads(response_server.decode('utf-8'))

            if protocol_msg == 'verVagas':
                if response_server["status"] == "404 Not Found":
                    logger.error(response_server["message"])
                else:
                    listaVagas = response_server['data']
                    for vaga in listaVagas:
                        mostrarVagas(vaga)

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
                        mostrarVagas(vaga)

                elif response_server['status'] == '404 Not Found':
                    logger.error(response_server['message'])

            elif protocol_msg == 'verPerfil':
                perfil = response_server['data']
                print(f"""
        Nome: {perfil['nome']}
        CPF: {perfil['cpf']}
        Email: {perfil['email']}
        Skills: {perfil['skills']}
        Área: {perfil['area']}
        Descricao: {perfil['descricao']}
        Cidade: {perfil['cidade']}
        UF: {perfil['uf']}
""")

    elif type == 'r':
        print()
        print('Bem-vindo ao ContratAe!')
        print("----------------------")
        print("Crie sua primeira vaga")
        print("----------------------")

        protocol_msg = "criar_vaga"
        dict_vaga = {}
        dict_vaga["nome_vaga"] = input("Digite o nome da vaga: ")
        dict_vaga["area_vaga"] = input("Digite a área de atuação: ")
        dict_vaga["descricao_vaga"] = input("Digite uma breve descrição: ")

        while True:
            try:
                dict_vaga["quant_candidaturas"] = int(input("Aceita quantas candidaturas? "))
                if dict_vaga["quant_candidaturas"] <= 0:
                    raise ValueError('Digite um número válido maior que 0.')
                break
            except ValueError:
                print('Digite um número válido maior que 0.')

        while True:
            try:
                dict_vaga["salario_vaga"] = float(input("Digite o salário: "))
                assert dict_vaga['salario_vaga'] > 0, "Digite uma quantia maior que 0."
                break
            except AssertionError as ae:
                print(ae)
            except ValueError:
                print('Digite uma quantia utilizando números. (Para os decimais, utilize ( . ) ao invés de ( , ) )')

        dict_vaga["requisitos"] = ''
        while True:
            resquisito_vaga = input('Digite os requisitos da vaga, 1 por vez (Digite "." para encerrar): ').strip()
            if resquisito_vaga == '.':
                break
            elif len(resquisito_vaga) == 0:
                print('Por favor, informe um requisito')
                continue
            dict_vaga["requisitos"] += "".join(resquisito_vaga + ',')
        dict_vaga["requisitos"] = dict_vaga["requisitos"][:-1]

        data_cliente = {'protocol_msg': protocol_msg, 'type': 'r', 'cpf': cpf, 'vaga_info': dict_vaga}

        cliente_socket.send(json.dumps(data_cliente).encode('utf-8'))

        response_server = cliente_socket.recv(1024)
        response_server = json.loads(response_server.decode('utf-8'))

        logger.info(response_server["message"])

        while True:
            while True:
                try:
                    print()
                    entrada = input('Digite o que deseja fazer:\n\n1-Ver candidaturas da vaga\n2-Sair\n\n')
                    print()
                    assert entrada in ['1', '2'], 'Escolha uma das opções acima.'
                    break
                except AssertionError as ae:
                    print(ae)

            content_dash = {}

            if entrada == '1':

                protocol_msg = 'verCandidaturas'
                content_dash['cpf'] = cpf
                content_dash['protocol_msg'] = protocol_msg
                content_dash['type'] = type
                content_dash['idVaga'] = response_server['data']

                cliente_socket.send(json.dumps(content_dash).encode('utf-8'))

                new_response_server = cliente_socket.recv(1024)
                new_response_server = json.loads(new_response_server.decode('utf-8'))

                if new_response_server['status'] == '404 Not Found':
                    print(new_response_server['message'])

                else:
                    for candidato in new_response_server['data']:
                        print(f"""
            =============================================
                    Nome: {candidato['nome']}
                    CPF: {candidato['cpf']}
                    Email: {candidato['email']}
                    Área: {candidato['area']}
                    Competências: {candidato['skills']}
                    Cidade: {candidato['cidade']}
                    UF: {candidato['uf']}

                    Descrição: {candidato['descricao']}
                        """)

            elif entrada == '2':
                cliente_socket.close()
                sys.exit(1)


run_cliente()
