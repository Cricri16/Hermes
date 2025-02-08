import sql
import be_app
import stockage
import tkinter
import tklist
max_ligne_search = 20
max_ligne_search = str(max_ligne_search)
class main:
    def __init__(self,data:stockage.BigData,listbox:tkinter.Listbox,emplacement:be_app.Emplacement,frame=tkinter.Frame) -> None:
        self.pseudo = data.get('pseudo')# on recupére le pseudo
        self.last_emplacement = ''# on def lancien emplaement pour pas que la premiére execution de main crash
        self.fr = frame# on rend acessible la frame a toute les fonction pour que l'on puisse faire des multi thread
        self.main(data,listbox,emplacement)# on lance main
    def main(self,data:stockage.BigData,listbox:tkinter.Listbox,emplacement:be_app.Emplacement):
        if self.last_emplacement == emplacement.label(): # on regarde i on est sur le mem emplacement que l'execution precedente
            self.message(data,listbox,emplacement)# si oui on lance message pour voir si il n'y a pas de nouveaux message
        else :
            self.move(data,listbox,emplacement) # sinon on lance la fonction qui aficche les message du nouvel emplacement
        self.last_emplacement = emplacement.label() # on met a jour lanciene emplacment car si il a changer les fonction move a été lancer
        self.fr.after(100,self.main,data,listbox,emplacement) # on rapelle la fonction 100 ms plus tard
    def message(self,data:stockage.BigData,listbox:tklist.Listbox,emplacement:be_app.Emplacement):
        if not data.exist(emplacement.label()): # on regarde si data a une variable a cet emplacement
            data.create(emplacement.label(),0) # si il n'y en a pas on l'ajoute
        nouveaux_message = self.get_message (emplacement,data.get(emplacement.label()))# on recupére les nouveaux message
        for traitement_message in nouveaux_message :# on examine tout les nouveaux message
            message_dico = emplacement.sql(traitement_message) # on le met sous forme de dico 
            hiden_data = 0 # on set les données cacher a zero
            if message_dico['hiden_data'] : # on regarde si notre message contient des donée cache
                hiden_data = message_dico['hiden_data'] # on met les donnée cacher dans une variable
            if message_dico['id'] > data.get(emplacement.label()) : # on regarde si ce message est un nouveaux
                listbox.insert(('['+message_dico['pname']+' :]'+message_dico['content']),hiden_data=hiden_data) # on l'ajoute a l'interface, c'est l'interface qui gére la couleur via hiden data
                listbox.see() # on dit de cadrer sur le dernier message
                data.update(emplacement.label(),message_dico['id']) # on met a jour le dernier id car si on l'a ajouter c'est que c'etait un nouveaux

    def move(self,data:stockage.BigData,listbox:tklist.Listbox,emplacement:be_app.Emplacement):
        listbox.clean() # on effece la listbox car on change d'emplacement
        if not data.exist(emplacement.label()): # on regarde si on a une vriable pour cette emplacement
            data.create(emplacement.label(),0) # on le crée
        last = data.get(emplacement.label())# on met le dernier dans une varpour pas que l'update a la fin crash
        last_message = False# pour que le dernier if marche
        if emplacement.emplacement['zone'] == 'msg': # on regarde si on s'est deplacer dans le message privé
            last_message = sql.special_recherche(
                    comand="""SELECT * FROM private_message WHERE 
                    ( sender = ? and recept = ?) or 
                    ( sender = ? and recept = ?) 
                    ORDER BY id DESC LIMIT """+max_ligne_search+" ",
                    objet=[self.pseudo,
                           emplacement.emplacement['specificite'],
                           emplacement.emplacement['specificite'],
                           self.pseudo]) # on recupére les dernier message

        elif emplacement.emplacement['zone'] == 'public': # on regarde si on s'est deplacer dans le chanel public
            last_message = sql.special_recherche(comand="SELECT * FROM message ORDER BY id DESC LIMIT "+max_ligne_search,objet=[]) # on recupére le nombre definit par max ligne search des dernier messate

        if last_message :
            last_message.reverse()# on l'inversse pour l'avoie de plus ancien au plus jeune
            for last_message_unit in last_message :#on les traite un pars un
                message_dico = emplacement.sql(last_message_unit) # on les met en dico
                listbox.insert(('['+message_dico['pname']+' :]'+message_dico['content']),hiden_data=message_dico['hiden_data'])# on l'ajoute a l'interface
                last = message_dico['id']
        data.update(emplacement.label(),last) # on fait en sorte de redefinir le dernier id pour ne pas aficher plus et avoir deux fois le meme message a cause de la fonction message

            
    def get_message(self,emplacement:be_app.Emplacement,index=0):
        if emplacement.emplacement['zone'] == 'public': # on regarde si on est dans public
            tp = sql.Where(emplacement.emplacement['table'],
                    colone=['id'],
                    objet=[index],
                    operation='>',) # si oui on recherche tout les message qui on un id supérieur au dernier que l'on posséde

        elif emplacement.emplacement['zone'] == "msg" : # on regarde si on est dans msg
            tp = sql.special_recherche(comand="""SELECT * FROM private_message WHERE 
                                       id > ? and 
                                       (( sender = ? and recept = ?) or 
                                       ( sender = ? and recept = ?))""",
                           objet=[index,
                                  self.pseudo,
                                  emplacement.emplacement['specificite'],
                                  emplacement.emplacement['specificite'],
                                  self.pseudo]) # on recherche tout les message qui sont aparut aprés notre derniére verif
        
        return tp # on renvoie