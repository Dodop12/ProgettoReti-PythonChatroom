#!/usr/bin/env python3
"""Script Python per la realizzazione di un Server multithread
per connessioni CHAT asincrone.
Corso di Programmazione di Reti - Università di Bologna"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_connections():
    """Accetta connessioni dai client."""
    while True:
        try:
            client, client_address = SERVER.accept()
            print("%s:%s si è collegato." % client_address)
            addresses[client] = client_address
            Thread(target=manage_client, args=(client,)).start()
        except Exception as e:
            print(f"Errore nell'accettare una nuova connessione: {e}")


def manage_client(client):
    """Gestisce la comunicazione con il client."""
    try:
        name = client.recv(BUFFER_SIZE).decode("utf8")
        join_msg = "Benvenuto nella chat, %s!." % name
        client.send(bytes(join_msg, "utf8"))
        msg = "%s si è unito alla chat!" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name

        while True:
            msg = client.recv(BUFFER_SIZE)
            if msg == bytes("{quit}", "utf8"):
                client.close()
                del clients[client]
                broadcast(bytes("%s ha abbandonato la chat." % name, "utf8"))
                break
            else:
                broadcast(msg, name + ": ")
    except Exception as e:
        print(f"Errore di comunicazione con il client: {e}")
        client.close()
        if client in clients:
            del clients[client]
            broadcast(bytes("%s si e' disconnesso dalla chat a causa di un errore." % name, "utf8"))


def broadcast(msg, tag=""):
    """Trasmette messaggi ai client connessi alla chat."""
    for user in clients:
        try:
            user.send(bytes(tag, "utf8") + msg)
        except Exception as e:
            print(f"Errore durante l'invio del messaggio: {e}")


# Dizionari per memorizzare client connessi e relativi indirizzi
clients = {}
addresses = {}

HOST = ""
PORT = 53000
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

if __name__ == "__main__":
    try:
        SERVER.listen(5)
        print("In attesa di connessioni...")
        ACCEPT_THREAD = Thread(target=accept_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except Exception as e:
        print(f"Errore durante l'esecuzione del server: {e}")
    finally:
        SERVER.close()
