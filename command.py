import stockage
import tkinter
import be_app
import sql
from tkinter import messagebox
import partage
import requests
from requests.exceptions import ConnectionError
from tkinter import filedialog
import customhtml
import time
import os
dev = True
def ouvrir_explorateur_fichier():
    root = tkinter.Tk()
    root.withdraw()  # Masquer la fenêtre principale
    chemin_fichier = filedialog.askopenfilename()  # Ouvrir l'explorateur de fichiers
    root.destroy()
    return chemin_fichier

def analyse_commande(entrer:str,data:stockage.BigData,emplacement:be_app.Emplacement):
    if entrer[:5] == "/file" :
        file(entrer,data,emplacement)
    elif entrer[:10] == "/file_get " :
        file_get(entrer,data,emplacement)
    elif entrer[:5] == "/msg " :
        msg(entrer,data,emplacement)
    elif entrer[:6] == "/link ":
        link(entrer,data,emplacement)
    elif entrer[:12] == "/new_pseudo ":
        new_pseudo(entrer,data,emplacement)
    elif entrer[:12] == "/log_pseudo ":
        log_pseudo(entrer,data,emplacement)
    else :
        messagebox.showinfo("command incorect","cette commande n'existe pas")

def file(entrer:str,data:stockage.BigData,emplacement:be_app.Emplacement):
    if entrer[5:] == '' :
        entrer += ouvrir_explorateur_fichier()
    if entrer[5:]:
        try:
            file_size = os.path.getsize(entrer[5:])
            if file_size > 0.5 * 1024 * 1024 * 1024:  # 0.5 GB in bytes
                messagebox.showinfo("Fichier trop volumineux", "La taille du fichier dépasse 0.5 Go")
                return False
        except OSError as e:
            messagebox.showinfo("Erreur de fichier", f"Erreur lors de l'accès au fichier: {e}")
            return False
    if not entrer[6:] :
        return False
    empl = partage.send(data.get('pseudo'),entrer[5:].replace('/','\\'))
    if empl == False :
        return False
    col = emplacement.sqlcolone()
    col.append("hiden_data")
    def justname(entrer,sys):
        num = entrer.count(sys)
        for i in range(num):
            entrer = entrer[entrer.find(sys)+1:]
        return entrer
    entrer = justname(entrer,'\\')
    entrer = justname(entrer,'/')
    obj=emplacement.complet((data.get('pseudo') + " a partagé : " + entrer ),data.get('pseudo'),False)
    obj.append("file_hiden_data : "+ str(empl))
    sql.Write(emplacement.emplacement['table'],
            colone=col,
            objet=obj)

def file_get(entrer:str,data:stockage.BigData,emplacement:be_app.Emplacement):
    emp = entrer[10:]
    print(emp)
    partage.recept(emp)

def msg(entrer:str,data:stockage.BigData,emplacement:be_app.Emplacement):
    recept = entrer[5:]# on extrait le pseudo
    in_bdd = sql.Where('log_conect',
              colone=['pname','sortie'],
              objet=[recept,0]) # on regarde si il existe une perssone comme ca dans la bdd
    if in_bdd :
        emplacement.msg(recept)
    else :
        messagebox.showinfo('non conecter',"la perssone rechercher n'est pas conecter")

def link(entrer:str,data:stockage.BigData,emplacement:be_app.Emplacement):
    url = entrer[6:]
    def isurl(url) :
        if url[:4] != 'http' and url[:3] != 'www' and url[:4] != 'ftp' and url[:5] != 'https':
            return messagebox.showinfo('lien non valide',"le lien ne commence pas corectement")
        try:
            r = requests.get(url)
            r.raise_for_status()
        except ConnectionError:
            return messagebox.showinfo('lien non valide',"le site ne repond pas ou n'existe pas")
        else:
            return True
    if isurl(url) :
        print("url valide")
        # on envoi le lien et on l'ecrit dans la bdd avec le lien dans hiden_data
        col = emplacement.sqlcolone()
        col.append("hiden_data")
        obj=emplacement.complet((data.get('pseudo') + " a partagé le lien : " + url),data.get('pseudo'),False)
        obj.append("link_hiden_data : "+ str(url))
        sql.Write(emplacement.emplacement['table'],
                colone=col,
                objet=obj)
        
def new_pseudo(entrer:str,data:stockage.BigData,emplacement:be_app.Emplacement):
    def check(enter:str):
        li = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890._-" # on verifie que le pseudo ne contient pas de caractere speciaux
        for i in enter[12]:
            if i not in li :
                print(i)
                messagebox.showinfo('erreur modification','Votre pseudo ne doit pas contenir de caractères spéciaux.')
                return False
        if not (4<len(enter[12:])<15) : # on verifie que le pseudo a la bonne taille
            messagebox.showinfo('erreur modification','Le pseudo doit avoir entre 5 et 14 caractères.')
            return False
        exist = sql.Where('anuaire_user',
                                colone=['pname'],
                                objet=[enter[12:]]) # on verifie que le pseudo n'existe pas deja
        if exist :
            messagebox.showinfo('erreur modification','pseudo deja utiliser')
            return False
        return True
        
    real_name = customhtml.bvn() # on recupere le nom de la personne
    ligne = sql.Where('anuaire_user',colone=['rname'],objet=[real_name]) # on regarde si il existe
    if ligne[-1][-1] + (7*24*60*60) >= time.time() and dev == False:
        messagebox.showinfo('changement de pseudo',"vous avez deja changer de pseudo il y a moins de 7 jours")
        return False
    elif check(entrer) == False and dev == False :
        return False
    else :
        sql.Update('anuaire_user',colone=['pname'],objet=[entrer[12:]],id=ligne[0][0]) # on met a jour la bdd dans l'anuaire
        sql.Write('new_pseudo',colone=['rname','last','new','date'],objet=[real_name,data.get('pseudo'),entrer[12:],time.time()]) # on ecrit dans la bdd
        data.update('pseudo',entrer[12:]) # on met a jour le pseudo
        messagebox.showinfo('changement de pseudo',"le pseudo a bien ete changer")

def log_pseudo(entrer:str,data:stockage.BigData,emplacement:be_app.Emplacement):
    pseudo = entrer[12:]
    ligne = sql.Where('anuaire_user',colone=['pname'],objet=[pseudo])
    real_pseudo = ligne[0][1]
    recherche = sql.Where('new_pseudo',colone=['rname'],objet=[real_pseudo])
    liste = ""
    if recherche :
        for i in recherche :
            liste +=  "\n \t - " + i[3]
        messagebox.showinfo('log changement de pseudo',"Voici les pseudo que la personne a eu : " + liste)
    else :
        messagebox.showinfo('log changement de pseudo',"la personne n'a jamais changer de pseudo")
