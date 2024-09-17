import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

# Create UDP socket for client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)

client_name = None  # Username after login
main_window = None  # To keep a reference to the main window
text_messages = None  # To keep a reference to the ScrolledText widget
send_window = None  # To keep a reference to the send message window

# Register account
def register():
    global client_name
    client_name = entry_username.get()
    
    if client_name:
        client_socket.sendto(f"register:{client_name}".encode(), server_address)
        data, _ = client_socket.recvfrom(1024)
        response = data.decode()
        messagebox.showinfo("Notification", response)
    else:
        messagebox.showwarning("Warning", "Registration name cannot be empty!")

# Login
def login():
    global client_name
    client_name = entry_username.get()
    
    if client_name:
        client_socket.sendto(f"login:{client_name}".encode(), server_address)
        data, _ = client_socket.recvfrom(1024)
        response = data.decode()
        
        if "Username does not exist" in response:
            messagebox.showerror("Error", "Username does not exist!")
        else:
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            show_messages(response)
    else:
        messagebox.showwarning("Warning", "Username cannot be empty!")

# Display received messages after login
def show_messages(messages):
    global text_messages, main_window
    main_window = tk.Tk()
    main_window.title("Message List")
    
    tk.Label(main_window, text=f"Messages for {client_name}:").pack(pady=10)
    
    text_messages = scrolledtext.ScrolledText(main_window, height=10, width=50)
    text_messages.pack(padx=10, pady=5)
    text_messages.insert(tk.END, messages)
    text_messages.config(state=tk.DISABLED)

    # Button to open the send message window
    btn_send_message = tk.Button(main_window, text="Send Message", command=open_send_message_window)
    btn_send_message.pack(pady=10)

    # Refresh button to update the message list
    btn_refresh = tk.Button(main_window, text="Refresh", command=refresh_messages)
    btn_refresh.pack(pady=5)

    main_window.mainloop()

# Refresh message list without closing the window
def refresh_messages():
    thread = threading.Thread(target=receive_email)
    thread.start()

# Receive email and update the message list
def receive_email():
    try:
        client_socket.sendto(f"receive:{client_name}".encode(), server_address)
        data, _ = client_socket.recvfrom(1024)
        emails = data.decode()

        if emails == "No new mail.":
            emails = "No new mail."

        # Update the text_messages content
        def update_text_messages():
            text_messages.config(state=tk.NORMAL)
            text_messages.delete(1.0, tk.END)  # Clear old content
            text_messages.insert(tk.END, emails)  # Insert new content
            text_messages.config(state=tk.DISABLED)

        main_window.after(0, update_text_messages)  # Use after to update GUI

    except Exception as e:
        messagebox.showerror("Error", f"Error receiving mail: {e}")

# Send email
def send_email():
    if send_window:
        receiver = entry_receiver.get()
        email_content = text_email_content.get("1.0", tk.END).strip()

        if receiver and email_content:
            client_socket.sendto(f"send:{client_name}:{receiver}:{email_content}".encode(), server_address)
            data, _ = client_socket.recvfrom(1024)
            response = data.decode()
            messagebox.showinfo("Notification", response)
        else:
            messagebox.showwarning("Warning", "Please enter all required information.")

# Open the send message window in a new top-level window
# Open the send message window in a new top-level window
def open_send_message_window():
    global send_window, entry_receiver, text_email_content

    # Check if the window already exists and is open
    if send_window and tk.Toplevel.winfo_exists(send_window):
        send_window.lift()  # Bring the existing window to the front
        return

    # Create a new window if the previous one was closed
    send_window = tk.Toplevel(main_window)
    send_window.title("Send Message")

    frame_send = tk.Frame(send_window)
    frame_send.pack(pady=10)

    tk.Label(frame_send, text="Recipient:").grid(row=0, column=0, padx=5, pady=5)
    entry_receiver = tk.Entry(frame_send, width=30)
    entry_receiver.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_send, text="Message Content:").grid(row=1, column=0, padx=5, pady=5)
    text_email_content = scrolledtext.ScrolledText(frame_send, height=10, width=40)
    text_email_content.grid(row=1, column=1, padx=5, pady=5)

    btn_send = tk.Button(frame_send, text="Send Email", command=send_email)
    btn_send.grid(row=2, column=1, padx=5, pady=5)


# Login/register interface
def open_login_window():
    global entry_username, login_window
    login_window = tk.Tk()
    login_window.title("Mail Client - Login/Register")

    tk.Label(login_window, text="Username:").pack(pady=10)
    entry_username = tk.Entry(login_window)
    entry_username.pack(pady=5)

    btn_register = tk.Button(login_window, text="Register", command=register)
    btn_register.pack(pady=5)

    btn_login = tk.Button(login_window, text="Login", command=login)
    btn_login.pack(pady=5)

    login_window.mainloop()

# Launch the login interface
open_login_window()

client_socket.close()
