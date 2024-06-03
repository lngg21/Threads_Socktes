import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}  # Dicionário para armazenar clientes e seus codinomes

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    # Receber e armazenar o codinome do cliente
    codename = conn.recv(HEADER).decode(FORMAT)
    codename_length = int(codename.strip())
    codename = conn.recv(codename_length).decode(FORMAT)
    clients[conn] = codename

    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length.strip())
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                else:
                    print(f"[{codename}] {msg}")
                    broadcast(f"{codename}: {msg}", conn)
        except:
            connected = False
    
    conn.close()
    del clients[conn]
    print(f"[DISCONNECTED] {addr} ({codename}) disconnected.")

def broadcast(msg, conn):
    for client in clients:
        if client != conn:
            try:
                message = msg.encode(FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                client.send(send_length)
                client.send(message)
            except:
                client.close()
                del clients[client]

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()
