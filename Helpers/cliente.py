# import socket
# from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
# import json
# import pickle
# import time

# HOST = '127.0.0.1'
# PORT = 5000

# servidor = (HOST, PORT)
# # cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # cliente_socket.connect(servidor)
# class Http_class(SimpleHTTPRequestHandler):
#     def end_headers(self):g
#         self.send_header('Access-Control-Allow-Origin', '*')
#         super().end_headers()
    
#     def _set_headers(self, status=200, content_type='application/json'):
#         self.send_response(status)
#         self.send_header('Content-type', content_type)
#         self.send_header('Access-Control-Allow-Origin', '*') 
#         self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
#         self.send_header('Access-Control-Allow-Headers', 'Content-Type')
#         self.end_headers()
        
#     def do_OPTIONS(self):
#         self._set_headers()

#     def do_POST(self):
#         content_length = int(self.headers['Content-Length'])
#         payload = self.rfile.read(content_length) #-> Recebendo o dado via HTTP    
#         time.sleep(1)
        
#         protocol_msg = "POST" # -> definindo a flag do protocolo.
            
#         cliente_socket.send(protocol_msg.encode('utf-8'))
            
#         data_cliente = json.loads(payload.decode('utf-8')) # -> usando a lib JSON para tranformar em dicionario python
#         data_cliente = pickle.dumps(data_cliente) # -> usando o pickle para tranformar em binario 
#         cliente_socket.send(data_cliente) # -> enviando via sockets
            
#         # protocol_response = cliente_socket.recv(1024) # -> Receber resposta do servidor (Protocolo)
#         # print(protocol_response.decode('utf-8'))
        
#         # Enviar resposta
#         response_data = {'mensagem': '"Candidato cadastrado com sucesso !'}
#         self._set_headers()
#         self.wfile.write(json.dumps(response_data).encode('utf-8'))
        
# class CustomHTTPServer(ThreadingHTTPServer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.client_socket.connect((HOST, PORT))

# def run(server_class=CustomHTTPServer, handler_class=Http_class, porta=8000):
#     server_address = ('0.0.0.0', porta)
#     httpd = server_class(server_address, handler_class)
#     print(f'Servidor rodando na porta {porta}')
#     httpd.serve_forever()
# run()


import socket
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
import pickle

HOST = '127.0.0.1'
PORT_HTTP = 8000
PORT_TCP = 5000

class Http_class(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        payload = self.rfile.read(content_length)  # Recebendo o dado via HTTP    

        # Tratamento do protocolo no servidor
        protocol_msg = "POST"
        response_data = self.server.protocol_handler(protocol_msg, payload)

        # Enviar resposta
        self._set_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
    
    def do_GET(self):
        # Tratamento do protocolo no servidor para o método GET
        # protocol_msg = "GET"
        # response_data = self.server.protocol_handler(protocol_msg, None)

        # Transforma os dados em JSON
        response_data = {"teste": "Deu bom"}
        response_json = json.dumps(response_data)
        
        # Configura os cabeçalhos da resposta
        self._set_headers(content_type='application/json')

        # Envia os dados para o navegador
        self.wfile.write(response_json.encode('utf-8'))
        print('Resposta enviada no método GET')

class CustomHTTPServer(ThreadingHTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT_TCP))

    def protocol_handler(self, msg, data):
        self.client_socket.send(msg.encode('utf-8'))
        data_cliente = json.loads(data.decode('utf-8'))
        data_cliente = pickle.dumps(data_cliente)
        self.client_socket.send(data_cliente)

        # Aguarde e receba a resposta do servidor TCP
        protocol_response = self.client_socket.recv(1024)
        protocol_response = protocol_response.decode('utf-8')
        return {'mensagem': f'Resposta do servidor TCP: {protocol_response}'}

def run(server_class=CustomHTTPServer, handler_class=Http_class, porta_http=8000, porta_tcp=5000):
    server_address = ('0.0.0.0', porta_http)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor HTTP rodando na porta {porta_http}')
    print(f'Servidor TCP conectado à porta {porta_tcp}')
    httpd.serve_forever()
