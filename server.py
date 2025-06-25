import socket
import threading
from typing import Optional

HOST = '0.0.0.0'
PORT = 5555

clients = []

def broadcast(message: bytes, exclude_sock: Optional[socket.socket] = None):
    for client_sock, _ in clients:
        if client_sock is not exclude_sock:
            try:
                client_sock.sendall(message)
            except:
                pass

def handle_client(client_sock: socket.socket, addr):
    
    try:
        name = client_sock.recv(1024).strip().decode('utf-8')
        print(f"Nova conexão de {addr} como {name}")
        clients.append((client_sock, name))

        while True:
            data = client_sock.recv(4096)
            if not data:
                break  
            msg = f"{name}: ".encode('utf-8') + data
            broadcast(msg, exclude_sock=client_sock)
    except ConnectionResetError:
        pass
    finally:
        print(f"Cliente {addr} ({name}) desconectou")
        clients.remove((client_sock, name))
        client_sock.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen()
        print(f"Servidor rodando em {HOST}:{PORT}")

        try:
            while True:
                client_sock, addr = server_sock.accept()
                t = threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\nServidor encerrado pelo usuário.")
            for client_sock, _ in clients:
                client_sock.close()

if __name__ == '__main__':
    main()
