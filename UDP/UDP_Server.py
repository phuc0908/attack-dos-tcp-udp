import socket
import os
from datetime import datetime

# Initialize UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 12345))

print("Mail server is running...")

# Create client directory if it doesn't exist
def create_client_directory(client_name):
    if not os.path.exists(client_name):
        os.makedirs(client_name)

# Handle requests from clients
while True:
    # Receive data from client
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode()

    # Handle account registration
    if message.startswith("register:"):
        client_name = message.split(":")[1]
        if not os.path.exists(client_name):
            create_client_directory(client_name)
            server_socket.sendto(f"Registration successful for {client_name}".encode(), client_address)
        else:
            server_socket.sendto(f"Account {client_name} already exists.".encode(), client_address)

    # Handle login
    elif message.startswith("login:"):
        client_name = message.split(":")[1]
        if os.path.exists(client_name):
            # Retrieve the client's email messages
            email_files = []
            for file in os.listdir(client_name):
                with open(os.path.join(client_name, file), 'r') as f:
                    email_files.append(f"{file}: {f.read()}")

            if email_files:
                response = "\n".join(email_files)
            else:
                response = "No new mail."

            server_socket.sendto(response.encode(), client_address)
        else:
            server_socket.sendto("Username does not exist.".encode(), client_address)

    # Handle sending mail
    elif message.startswith("send:"):
        _, sender, receiver, email_content = message.split(":", 3)
        if os.path.exists(receiver):
            # Create file name with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{sender}_{timestamp}.txt"
            
            # Save email content to file
            with open(os.path.join(receiver, file_name), 'w') as f:
                f.write(email_content)
            
            server_socket.sendto(f"Mail sent to {receiver}".encode(), client_address)
        else:
            server_socket.sendto(f"Recipient {receiver} does not exist.".encode(), client_address)

    # Handle receiving mail
    elif message.startswith("receive:"):
        client_name = message.split(":")[1]
        if os.path.exists(client_name):
            email_files = []
            for file in os.listdir(client_name):
                with open(os.path.join(client_name, file), 'r') as f:
                    email_files.append(f"{file}: {f.read()}")

            if email_files:
                response = "\n".join(email_files)
            else:
                response = "No new mail."

            server_socket.sendto(response.encode(), client_address)
        else:
            server_socket.sendto("Username does not exist.".encode(), client_address)
