#!/usr/bin/env python3
"""Script relativa alla chat del client utilizzato per lanciare la GUI Tkinter."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import messagebox


def receive():
    """Riceve e decodifica messaggi dal server."""
    while True:
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            msg_list.insert(tk.END, msg)
        except OSError:
            break


def send_message(event=None):
    """Invia messaggi al server. Se riceve il comando Quit, il client viene chiuso."""
    msg = my_msg.get()
    my_msg.set("")
    try:
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            chat_window.quit()
            client_socket.close()
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante l'invio del messaggio: {e}")


def quit(event=None):
    """Chiude la chat inviando il comando di Quit."""
    my_msg.set("{quit}")
    send_message()


def start_chat():
    """Avvia la chat creando la GUI ed effettuando la connessione."""
    global client_socket, chat_window, my_msg, msg_list, NICKNAME
    HOST = host_entry.get()
    PORT = port_entry.get()

    if not PORT:
        PORT = 53000
    else:
        try:
            PORT = int(PORT)
        except ValueError:
            messagebox.showerror(
                "Porta non valida", "La porta deve essere un valore numerico intero."
            )
            return

    NICKNAME = nickname_entry.get()
    
    if not NICKNAME:
        messagebox.showerror("Errore", "Nickname non inserito.")
        return

    ADDRESS = (HOST, PORT)

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(ADDRESS)
        client_socket.send(bytes(NICKNAME, "utf8"))
    except Exception as e:
        messagebox.showerror(
            "Errore di connessione", f"Impossibile connettersi al server: {e}"
        )
        return

    # Chiude la finestra di login
    login_window.withdraw()

    # Crea la GUI della chat
    chat_window = tk.Toplevel()
    chat_window.title(f"Chat - {NICKNAME}")

    messages_frame = tk.Frame(chat_window)
    my_msg = tk.StringVar()
    scrollbar = tk.Scrollbar(messages_frame)

    msg_list = tk.Listbox(
        messages_frame, height=15, width=50, yscrollcommand=scrollbar.set
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tk.Entry(chat_window, textvariable=my_msg)
    entry_field.bind("<Return>", send_message)
    entry_field.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

    send_button = tk.Button(chat_window, text="Invio", command=send_message, width=6)
    send_button.pack(side=tk.LEFT, padx=5, pady=5)

    quit_button = tk.Button(chat_window, text="Quit", command=quit, width=6)
    quit_button.pack(side=tk.LEFT, padx=5, pady=5)

    chat_window.protocol("WM_DELETE_WINDOW", quit)

    receive_thread = Thread(target=receive)
    receive_thread.start()


BUFFER_SIZE = 1024

# Schermata di login
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("200x160")

tk.Label(login_window, text="Server host:").pack()
host_entry = tk.Entry(login_window)
host_entry.pack()

tk.Label(login_window, text="Porta del server host:").pack()
port_entry = tk.Entry(login_window)
port_entry.pack()

tk.Label(login_window, text="Nickname:").pack()
nickname_entry = tk.Entry(login_window)
nickname_entry.pack()

tk.Button(login_window, text="Connetti", command=start_chat).pack()

login_window.mainloop()
