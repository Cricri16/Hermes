import stockage
import tklist
import sql
import tkinter
import be_app
import palette
class main:
    def __init__(self,data:stockage.BigData,frame:tkinter.Frame,listbox:tklist.Listbox,emplacement:be_app.Emplacement) -> None:
        # on va voir si il existe deja une var dans data qui contient les utilisateur afficher
        if not data.exist('seen_user') :
            data.create('seen_user',[])
        self.pseudo = data.get('pseudo')
        self.frame= frame
        self.frame.after(0,self.notif,data,listbox,emplacement)
        self.frame.after(500,self.new_msg,data,listbox)
        pass
    def notif(self,data:stockage.BigData,listbox:tklist.Listbox,emplacement:be_app.Emplacement):
        user = data.get('seen_user')# on recupére les perssone avec qui on discute
        for i in user:
            if i != emplacement.emplacement['specificite'] : # on verifie que ce n'est pas la perssone avec qui on parle
                nombre = data.get(i)# on recupére le nombre  de message avec cette perssone
                rnumber = sql.special_recherche(
                    comand="SELECT * FROM private_message WHERE (( sender = ? and recept = ?) or ( sender = ? and recept = ?)) AND id > ?",
                    objet=[self.pseudo,i,i,self.pseudo,nombre]
                )# on recpére tout les message supérieur a nombre
                cont = len(rnumber)# on les conte
                if rnumber and rnumber[-1][1] != data.get('pseudo'):# si il y en a on affiche en notif
                    ids = listbox.content.index(i) # on trouve l'id du perso
                    listbox.config(ids,{'bg':'#697565'})# on change le text et la couleur
                    data.update(i,rnumber[-1][0])# on lui actualise le dernier message
                    data.save(i)
        self.frame.after(500,self.notif,data,listbox,emplacement)# on rapelle la fonction
    def new_msg(self,data:stockage.BigData,listbox:tklist.Listbox): # on voit si y'a des nouveaux msg
        msg = data.get('seen_user')# on recup la list des perssone que on conait
        msg_in_bdd = sql.special_recherche("SELECT sender,recept FROM private_message WHERE sender = ? OR recept = ?",[self.pseudo,self.pseudo])
        for i in msg_in_bdd :
            i:list # on precise que i est une list
            i.pop(i.index(self.pseudo)) # on retire notre pseudo
            if i[0] not in (msg) and i[0] != data.get('pseudo'):# si la perssone n'est pas dans msg
                # on l'ajoute a la listbox et a la list seen user
                data.create(i[0],0)# on lui crée une variable
                listbox.insert(i[0])
                tp = data.get('seen_user')
                tp: list
                tp.append(i[0])
                data.update('seen_user',tp)# on le rajoute a la liste des perssone aficher
        self.frame.after(500,self.new_msg,data,listbox)

def click(listbox:tklist.Listbox,emplacement:be_app.Emplacement):
    how,hiden = listbox.get() # on recupére le nom
    listbox.list.selection_clear(0,tkinter.END)
    if how != False:
        emplacement.msg(how)# on change l'emplacement
        listbox.config(listbox.content.index(how),{'bg':palette.custom(1)})# on reset le text et la couleur
