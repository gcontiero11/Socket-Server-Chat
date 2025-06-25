import socket
import threading
import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555

def receive_messages(sock: socket.socket):
    """Recebe e exibe mensagens do servidor."""
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("Conexão encerrada pelo servidor.")
                break
            # exibe a mensagem recebida
            print(data.decode('utf-8'))
    except ConnectionResetError:
        print("Conexão perdida.")
    finally:
        sys.exit(0)

def send_messages(sock: socket.socket):
    """Lê do stdin e envia mensagens ao servidor."""
    try:
        while True:
            msg = input()
            if msg.strip() == '':
                continue
            sock.sendall(msg.encode('utf-8'))
    except (BrokenPipeError, OSError):
        pass

def main():
    name = input("Digite seu nome: ").strip()
    if not name:
        print("Nome não pode ser vazio.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((SERVER_HOST, SERVER_PORT))
        except ConnectionRefusedError:
            print("Não foi possível conectar ao servidor.")
            return

        # envia o nome ao servidor
        sock.sendall((name + '\n').encode('utf-8'))

        # inicia thread de recebimento
        threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
        # loop de envio
        send_messages(sock)

if __name__ == '__main__':
    main()