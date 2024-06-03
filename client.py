import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_msg():
    codename = input("Enter your codename: ")
    send(codename)
    while True:
        msg = input()
        send(msg)
        if msg == DISCONNECT_MESSAGE:
            break

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive_msg():
    while True:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length.strip())
                msg = client.recv(msg_length).decode(FORMAT)
                print(msg)
        except:
            print("An error occurred!")
            break

thread_send = threading.Thread(target=send_msg)
thread_receive = threading.Thread(target=receive_msg)
thread_send.start()
thread_receive.start()
