import socket
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
import pickle
from hashlib import sha256

HOST = '127.0.0.1'
PORT_HTTP = 8000
PORT_TCP = 5000
class Http_class(SimpleHTTPRequestHandler):
    def end_headers(self):
        super().end_headers()

    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "86400")  # 24 horas
        self.end_headers()
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        json_data = self.rfile.read(content_length)  # -> Recebendo o dado via HTTP    

        data_cliente = json.loads(json_data.decode('utf-8')) # -> Lendo os dados JSON 
        # Tratamento do protocolo no servidor
        protocol_msg = data_cliente["flag_protocol"] # -> Menssagem para o protocolo SPC
        response_server = self.server.protocol_handler(protocol_msg, data_cliente)

        if "data" in response_server:
            response_server["data"] = response_server["data"].dict_user()

        # Enviar resposta
        self._set_headers()
        self.wfile.write(json.dumps(response_server).encode('utf-8'))
    
    def do_GET(self):
        # Tratamento do protocolo no servidor HTTP para o método GET.
        response_data = {"Status": "Online"}
        response_json = json.dumps(response_data)
        self._set_headers(content_type='application/json')

        self.wfile.write(response_json.encode('utf-8'))
        print('Resposta enviada no método GET')

class CustomHTTPServer(ThreadingHTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT_TCP))

    def protocol_handler(self, msg, data_cliente):
        self.client_socket.send(pickle.dumps(msg))

        hash_passwd = sha256(data_cliente["senha"].encode())
        # convertendo a senha de bytes para hexadecimal
        data_cliente["senha"] = hash_passwd.hexdigest()
                
        data_cliente = pickle.dumps(data_cliente) # -> Convertendo em dicionario pyhton
        self.client_socket.send(data_cliente) # -> Enviado para o sevidor SPC

        # Aguarde e receba a resposta do servidor TCP
        protocol_response = self.client_socket.recv(1024)
        protocol_response = pickle.loads(protocol_response)
        return protocol_response

def run(server_class=CustomHTTPServer, handler_class=Http_class, porta_http=8000, porta_tcp=5000):
    server_address = ('0.0.0.0', porta_http)
    httpd = server_class(server_address, handler_class)
    # print(f'Servidor HTTP rodando na porta {porta_http}')
    # print(f'Servidor TCP conectado à porta {porta_tcp}')
    httpd.serve_forever()


run()
