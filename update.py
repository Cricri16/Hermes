import urllib.request
import os
from tkinter import messagebox
import requests
local = 'v14.6.3'
def chekupdate():
    url = "https://raw.githubusercontent.com/Cricri16/Hermes/main/version.txt"
    with urllib.request.urlopen(url) as f:
        fich = f.readlines()
        version = fich[0][:-1].decode('utf-8')[:-1]
    if version != local:
        print(version+']')
        exit()
        messagebox.showinfo('mise a jou','la messagerie Hermes va etre mise a jour')
        nombre_de_fichier = int(fich[1][:-1].decode('utf-8')) # on recupere le nombre de fichier a telecharger
        liste_a_telecharger = [] # on creer une liste qui va contenir les fichier a telecharger
        for i in range(nombre_de_fichier): # on fait une boucle pour recuperer les fichier a telecharger
            liste_a_telecharger.append(fich[i+2][:-1].decode('utf-8')) # on ajoute les fichier a telecharger a la liste
        for i in liste_a_telecharger:
            url = f"https://raw.githubusercontent.com/Cricri16/Hermes/main/{i}"
            print(url)
            with urllib.request.urlopen(url) as f:
                with open(i[:-1],'wb') as file:
                    file.write(f.read())
        messagebox.showinfo('mise a jour','mise a jour effectuer')
