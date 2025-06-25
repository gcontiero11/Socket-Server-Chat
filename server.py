# server.py

import socket
import threading
import os
from typing import Optional

HOST = '0.0.0.0'
PORT = 5555

clients = []  # lista de (socket, nome)

def broadcast(message: bytes, exclude_sock: Optional[socket.socket] = None):
    """Envia a mensagem para todos os clientes, exceto exclude_sock."""
    for client_sock, _ in clients:
        if client_sock is not exclude_sock:
            try:
                client_sock.sendall(message)
            except:
                pass  # ignora erros de envio

def handle_client(client_sock: socket.socket, addr):
    """Thread responsável por receber mensagens de um cliente e retransmiti-las."""
    try:
        # Recebe o nome do cliente (bastante simples: até newline)
        name = client_sock.recv(1024).strip().decode('utf-8')
        print(f"Nova conexão de {addr} como {name}")
        # Armazena na lista
        clients.append((client_sock, name))

        # Laço de recebimento contínuo
        while True:
            data = client_sock.recv(4096)
            if not data:
                break  # cliente desconectou
            # Formata: "Nome: mensagem"
            msg = f"{name}: ".encode('utf-8') + data
            broadcast(msg, exclude_sock=client_sock)
    except ConnectionResetError:
        pass
    finally:
        # Remove cliente e fecha socket
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
                # dispara thread para tratar esse cliente
                t = threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\nServidor encerrado pelo usuário.")

if __name__ == '__main__':
    main()
