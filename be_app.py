import time
import sql
import tkinter
class Emplacement:
    def __init__(self,frame:tkinter.Frame,label:tkinter.Label) -> None:
        self.emplacement = {
            'zone' : 'public',
            'specificite' : '',
            'table' : 'message'
        }
        self.lastempl = ''
        self.frame = frame
        self.actlabel(label)
    def label(self):
        zone = self.emplacement['zone'] 
        spe = self.emplacement['specificite']
        spe = '' if spe == '' else f" : {spe}"
        return zone + spe
    def actlabel(self,label:tkinter.Label):
        if self.lastempl != self.emplacement :
            pr = self.label()
            label.configure(text=pr)
        self.frame.after(200,self.actlabel,label)
    def msg(self,spe):
        self.emplacement['zone'] = 'msg'
        self.emplacement['specificite'] = spe
        self.emplacement['table'] = 'private_message'
    def public(self):
        self.emplacement = {
            'zone' : 'public',
            'specificite' : '',
            'table' : 'message'
        }
        self.lastempl = ''
    def groupe(self,spe):
        self.emplacement['zone'] = 'groupe'
        self.emplacement['specificite'] = spe
        self.emplacement['table'] = 'groupe'
    def sql(self,lis):
        # on lui donne une list et il nous sort un dico
        if self.emplacement['zone'] == 'public':
            return  {
                'id' : lis[0],
                'pname' : lis[1],
                'zone' : lis[2],
                'content' : lis[3],
                'type' : lis[4],
                'date' : lis[5],
                'hiden_data' : lis[6]
            }
        elif self.emplacement['zone'] == 'groupe':
            return  {
                'id' : lis[0],
                'pname' : lis[1],
                'zone' : lis[2],
                'groupe' : lis[3],
                'content' : lis[4],
                'type' : lis[5],
                'date' : lis[6],
                'hiden_data' : lis[6]
            }
        elif self.emplacement['zone'] == 'msg':
            return  {
                'id' : lis[0],
                'pname' : lis[1],
                'zone' : lis[2],
                'recept' : lis[3],
                'content' : lis[4],
                'type' : lis[5],
                'date' : lis[6],
                'hiden_data' : lis[7]
            }
    def sqlcolone(self):
        if self.emplacement['zone'] == 'public':
            return  [
                'pname' ,
                'zone' ,
                'content' ,
                'type' ,
                'date',
            ]
        elif self.emplacement['zone'] == 'groupe':
            return  [
                'pname' ,
                'zone' ,
                'groupe' ,
                'content' ,
                'type' ,
                'date',
            ]
        elif self.emplacement['zone'] == 'msg':
            return  [
                'sender' ,
                'zone' ,
                'recept' ,
                'content' ,
                'type' ,
                'date',
            ]
        else :
            print('zone inconue')
    def complet(self,cont,name,typ):
        if self.emplacement['zone'] == ( 'msg' or 'groupe'):
            return [
                name,
                False,
                self.emplacement['specificite'],
                cont,
                typ,
                time.time()
            ]
        elif self.emplacement['zone'] == 'public':
            return [
                name,
                False,
                cont,
                typ,
                time.time()
            ]

class background:
    def __init__(self,frame:tkinter.Frame) -> None:
        # initialisation des tache qui doivent marcher en arriere plan
        self.bdd = bdd(frame) # on initialise les tache sur la bdd

class bdd :
    def __init__(self,frame:tkinter.Frame) -> None:
        self.frame = frame # on rend la frame accessible a toute les fonction
        self.delete_old_load() # on suprime les fichier qui ont plus de 10 minutes toute les 10 minutes
        self.verification_pseudo() # on verifie que tout les pseudo sont reglementaire
    def delete_old_load(self):
        # on suprime les fichier qui ont plus de 10 minutes toute les 10 minutes
        recup = sql.Where('partage',colone=['time'],objet=[time.time()-600],operation='<')# on recupére les fichier qui ont plus de 10 minutes
        for i in recup: # on les analyse
            sql.Update('partage',colone=['recu','content'],objet=[1,0],id=i[0]) # on les suprime et on les marque comme telechargé
        self.frame.after(60000,self.delete_old_load) # on relance la fonction toute les 10 minutes
    def verification_pseudo(self):
        def check(enter:str):
            li = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890._-" # on verifie que le pseudo ne contient pas de caractere speciaux
            for i in enter: #on les analyse
                if i not in li : # on verifie si il n'est pas dans la liste des caractere autorisé
                    return False # si il est pas dans la liste on renvoi False
            if not (4<len(enter)<15) : # on verifie que le pseudo a la bonne taille
                return False # si il ne fait pas la bonne taille on renvoi False
            exist = sql.Where('anuaire_user',
                                    colone=['pname'],
                                    objet=[enter]) # on verifie que le pseudo n'existe pas deja
            if exist :
                return False
            return True
        # on verifie si tout les pseudo stont reglementaire
        recup = sql.All('anuaire_user') # on recupére tout les pseudo inscrit
        for i in recup: # on les analyse
            if check(i[2]): # on verifie si il est reglementaire
                sql.Update('anuaire_user',colone=['rname','pname'],objet=[False,False],id=i[0]) # on suprime les pseudo qui ne sont pas reglementaire
                print('pseudo suprimer : ',i[2])
                find = sql.Where('log_conect',colone=['pname'],objet=[i[2]]) # on trouve toute ses conextion
                for i in find:
                    sql.Update('log_conect',colone=['sortie'],objet=[-1],id=i[0]) # on le deconecte
        self.frame.after(5*60*1000,self.verification_pseudo) # on relance la fonction toute les 5 minutes