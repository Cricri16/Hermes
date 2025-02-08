import stockage
import tkinter
import be_app
import sql
from tkinter import messagebox
import partage
import requests
from requests.exceptions import ConnectionError
from tkinter import filedialog
import command

def message(data:stockage.BigData,entry:tkinter.Entry,emplacement:be_app.Emplacement):
    # on recupére l'entrer
    entrer = entry.get()
    # on recupére ou on génére le dernier message envoier pour cancel le spam
    if data.exist('last_message') :
        last = data.get('last_message')
    else :
        data.create('last_message',entrer)
        last = ''
    # si il sont diferent on ecrit dans la bdd
    if last != entrer and entrer != '' or entrer[:11] == "//admin_unk":
        """
        on pouras faire en sorte d'envoyer des lien web et des fichier
        """
        if entrer[:1] != "/" : # on regarde si c'est pas la comande pour envoyer un msg
            sql.Write(emplacement.emplacement['table'],
                    emplacement.sqlcolone(),
                    emplacement.complet(entrer,data.get('pseudo'),False))
            data.update('last_message',entrer)
        else :
            command.analyse_commande(entrer,data,emplacement)