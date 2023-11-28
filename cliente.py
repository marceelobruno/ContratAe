import socket
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
import pickle

HOST = '127.0.0.1'
PORT = 5000

servidor = (HOST, PORT)

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(servidor)

servidor = (HOST, PORT)
class Http_class(SimpleHTTPRequestHandler):
    
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
    def do_OPTIONS(self):
        self._set_headers()
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        
        content_length = int(self.headers['Content-Length'])
        payload = self.rfile.read(content_length) #-> Recebendo o dado via HTTP
            
        protocol_msg = "POST" # -> definindo a flag do protocolo.
            
        cliente_socket.send(protocol_msg.encode('utf-8'))
            
        data_cliente = json.loads(payload.decode('utf-8')) # -> usando a lib JSON para tranformar em dicionario python
        data_cliente = pickle.dumps(data_cliente) # -> usando o pickle para tranformar em binario 
        cliente_socket.send(data_cliente) # -> enviando via sockets
            
            
        # protocol_response = cliente_socket.recv(1024) # -> Receber resposta do servidor (Protocolo)
        # print(protocol_response.decode('utf-8'))
        
        # Enviar resposta
        response_data = {'mensagem': '"Candidato cadastrado com sucesso !'}
        self._set_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        

def run(server_class=ThreadingHTTPServer, handler_class=Http_class, porta=8000):
    server_address = ('0.0.0.0', porta)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor rodando na porta {porta}')
    httpd.serve_forever()

run()
