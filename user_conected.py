import sql
import stockage
import tkinter
import time
import be_app
import os
class Tab:
    def __init__(self,frame:tkinter.Frame,
                 listbox:tkinter.Listbox,
                 entry:tkinter.Entry,
                 data:stockage.BigData) -> None:
        self.last =  'de'
        self.last_list = []
        self.last_nb = 99
        frame.after(250,self.generate_list,data,frame,
                      entry,listbox)
    def generate_list(self,data:stockage.BigData,
                      frame:tkinter.Frame,
                      entry:tkinter.Entry,
                      listbox:tkinter.Listbox):
        """
        1) recupére la list des joueur ( en fonction de entry )
        2) la met sur BigData
        3) modifie la list
        """
        def exist(nom,contenu):
            """
            si la variable n'existe pas on la crée
            """
            if not data.exist(nom) :
                data.create(nom,contenu)
            else :
                data.update(nom,contenu)

        entrer = entry.get()
        # stockage de l'entrer utilisateur
        # fin
        nb = len(sql.Where('log_conect',colone=['sortie'],objet=[0]))

        if entrer != self.last or nb != self.last_nb:
            self.last_nb = nb
            exist('entrer_user',entrer)
            self.last = entrer
            # on recupére la list des perssone conecter si entry != self.last
            user_conected = sql.Where('log_conect',
                                    colone=['pname'],
                                    objet=[data.get('entrer_user')+'%'],
                                    operation='LIKE',condition=' AND sortie = 0 Limit 9')
            # on extrait que les nom
            def name(varlist):
                ret=[]
                for i in varlist :
                    ret.append(i[1])
                return ret
            user_conected = name(user_conected)
            exist('user_conected',user_conected)
            # fin
            # si la list n'est pas la meme on change la listbox
            if user_conected != self.last_list :
                self.last_list = user_conected
                listbox.delete(0,tkinter.END)
                for i in user_conected :
                    listbox.insert('end',i)
                    """
                    pour la v 15 on pourais faire en sorte qu'il sait perciser dans la 
                    bdd les caractéristique de la perssone ( deleger prof eleve ect... )
                    """
        # on relance la fonction
        frame.after(250,self.generate_list,data,frame,
                      entry,listbox)
class Ping:
    def __init__(self,frame:tkinter.Frame,
                 data:stockage.BigData) -> None:
        frame.after(500,self.auto,data,frame)
        frame.after(4000,self.chain,frame)
    def auto(self,data:stockage.BigData,frame:tkinter.Frame):
        # on se trouve dans la bdd
        temp = sql.Where('log_conect',
                         colone=['pname'],
                         objet=[data.get('pseudo')])
        # si non nul alors on existe
        if temp != [] :
            if temp[0][5] == -1 :
                exit()
            elif temp[0][5] != 0 and temp[0][5] != -1 :
                # au cas ou on aurais crash et le chain d'un autre programe nous aurais fait depop
                # ou on se conect, bref on modif notre ligne avec notre arivé et on indique que on est la
                sql.Update('log_conect',
                           colone=['arivée','actualisation','sortie'],
                           objet=[time.time(),time.time(),0],
                           id=temp[0][0])
            else :
                # actualisation srttandart nous maintient conecter
                sql.Update('log_conect',
                           colone=['actualisation'],
                           objet=[time.time()],
                           id=temp[0][0])
        else:
            # si on n'est pas dans la base de donnée on se rajoute
            sql.Write('log_conect',
                        colone=['pname','arivée','actualisation','sortie'],
                        objet=[data.get('pseudo'),time.time(),time.time(),0])
        # on rapelle la fonction avec les paramétre
        frame.after(500,self.auto,data,frame)
    def chain(self,frame:tkinter.Frame):
        """
        parcour les perssone conecter pour voir ce qui aurais crash
        pour ca on regarde leur horaire d'actualisation et si il y a plus de 5 s de decalage 
        on le marque en deco
        """
        # on prend les perssone marqués comme conecter
        here = sql.Where('log_conect',
                         colone=['sortie'],
                         objet=[0])
        for i in here:
            if i[4] + 5 <= time.time() and i[5] != -1:
                # si n'a pas actualiser depuis plus de 5 s
                sql.Update('log_conect',
                           colone=['sortie'],
                           objet=[time.time()],
                           id=i[0])
                # on le marque en deconecter
        frame.after(4000,self.chain,frame)

def move(listbox:tkinter.Listbox,emplacement:be_app.Emplacement,data:stockage.BigData):
        empl = str(listbox.curselection())# on recup en str le truc click
        if empl != '()':# si il est pas nul
            empl = empl[1:empl.find(',')]#
            empl = int(empl)# on extrait le vrai nombre
            bdd = sql.Where('log_conect',
                                    colone=['pname'],
                                    objet=[data.get('entrer_user')+'%'],
                                    operation='LIKE',condition=' AND sortie = 0 Limit 9')# on recup les utilisateur qui resemble a ce qu'on a dans le mess
            if data.get('pseudo') != data.get('user_conected')[empl] : # si on n'a pas click sur nous
                emplacement.msg(data.get('user_conected')[empl])# on change d'emplacement