import socket
import threading

clients = []

def handle_client(client_socket, client_address):
    print(f"{client_address} has connected")
    clients.append(client_socket)
    
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"{client_address}: {message.decode()}")
                broadcast(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            continue

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                remove_client(client)

def remove_client(client_socket):
    print(f"{client_address} disconnected")
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1000)
    print("Server is listening...")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

if __name__ == "__main__":
    start_server()
