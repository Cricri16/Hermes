import sql
import os
import time
import random
from tkinter import messagebox
import shutil
def envoie(file):
    if not os.path.exists(file):
        messagebox.showinfo('fichier introuvable','le fichier demandé est introuvable')
        return False
    file = open(file,'rb')
    content = file.read()
    file.close()
    return content

def write(bin_code,title):
    if not bin_code :
        print('code_binaire inexistant')
        return False
    if not os.path.exists("hermes_download\\"):
        os.mkdir("hermes_download\\")
    file = open('hermes_download\\' + title,'wb+')
    file.write(bin_code)
    file.close()

def send(sender,file:str):
    if file.find('\\') >= 0 :
        if not os.path.exists("hermes_memo\\"):
            os.mkdir("hermes_memo\\")
        shutil.copy(file,"hermes_memo\\")
        num = file.count('\\')
        for i in range(num):
            file = file[file.find('\\')+1:]#"C:\Users\Mr.shen\Downloads"
    content = envoie("hermes_memo\\" + file) # on recupére le code bianire
    if not content :
        return False
    var = file
    ret = sql.Write('partage',['sender','content','recu','time',"file_name"],[sender,content,0,time.time(),var])
    if os.path.exists("hermes_memo\\" + file):
        os.remove("hermes_memo\\" + file)
    return ret # on le met dans la base de donnée

def recept(id):
    cont = sql.Where('partage',['id','recu'],[int(id),0])
    if not cont :
        messagebox.showinfo('fichier introuvable','le fichier demandé est introuvable ou deja telechargé')
        return False
    name_file = cont[0][5]
    contenu = cont[0][2]
    write(contenu,name_file)
    sql.Update('partage',['recu','content'],[1,0],id)
    os.system('start hermes_download\\"' + name_file+'"')

