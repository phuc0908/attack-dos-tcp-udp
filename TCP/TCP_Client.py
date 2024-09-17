import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, message + "\n")
                text_area.yview(tk.END)
                text_area.config(state=tk.DISABLED)
        except:
            break

def send_message(client_socket, message_entry, text_area):
    message = message_entry.get("1.0", tk.END).strip()
    if message:
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, message + "\n", "right")
        text_area.yview(tk.END)
        text_area.config(state=tk.DISABLED)

        try:
            client_socket.send(message.encode())
            message_entry.delete("1.0", tk.END)
        except Exception as e:
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, f"Error sending message: {e}\n", "error")
            text_area.yview(tk.END)
            text_area.config(state=tk.DISABLED)

def on_close(client_socket, window):
    client_socket.send(" has connected".encode())
    client_socket.close()
    print("Connection closed.")
    window.destroy()

def on_shift_enter_pressed(event):
    return "break"

def start_gui(client_socket):
    window = tk.Tk()
    window.title("TCP Chatroom")

    # Set size and background color
    window.geometry("500x400")
    window.configure(bg="#2c3e50")

    main_frame = tk.Frame(window, bg="#2c3e50")
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=0)

    text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state=tk.DISABLED, bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12))
    text_area.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
    text_area.tag_configure("right", justify='right')

    # Entry for typing messages
    message_entry = tk.Text(main_frame, height=2, bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12))
    message_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    # Send button
    send_button = tk.Button(main_frame, text="Send", command=lambda: send_message(client_socket, message_entry, text_area),
                            bg="#e74c3c", fg="white", font=("TimesNewRoman", 12, "bold"))
    send_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    # Bind Shift-Enter and Enter
    message_entry.bind("<Shift-Return>", on_shift_enter_pressed)
    message_entry.bind("<Return>", lambda event: send_message(client_socket, message_entry, text_area))

    window.protocol("WM_DELETE_WINDOW", lambda: on_close(client_socket, window))

    # Start thread
    threading.Thread(target=receive_messages, args=(client_socket, text_area), daemon=True).start()

    window.mainloop()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    start_gui(client_socket)

if __name__ == "__main__":
    start_client()
