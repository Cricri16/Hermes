
import sql
import tkinter
import time
"""
organisation de la bdd :
3 colone : id , 1 nom et 1 contenue
"""

def printal(*elem):
    a = False
    if a :
        print(elem[0])

class BigData:
    def __init__(self) -> None:
        self.name = []
        self.contenue = []
        self.date = []
        # si la bdd local existe on charge les variable

    # fonction intern
    def indox(self,name):
        return self.name.index(name)
    def time(self,index):
        self.date[index] = time.time()
    def save(self,name):
        exist = sql.Where('Var',
                          colone=['nom'],
                          objet=[name],bdd='local.db')
        cont = self.contenue[self.name.index(name)]
        if type(cont) == list:
            cont = str(cont)
        if len(exist) == 0 :
                sql.Write('Var',
                          ['nom','cont'],
                          [name,cont],bdd='local.db')
                printal("BigData INFO : CREATED VAR : {"+name+'}')
                self.time(self.name.index(name))
        elif len(exist) > 1 :
            printal("BigData ERROR : CONFLIT VAR : {"+name+"}")
        else :
            sql.Update('Var',
                       colone=['cont'],
                       objet=[cont],
                       id=exist[0][0],
                       bdd='local.db')
            printal("BigData INFO : UPDATE VAR : {"+name+'}')
            self.time(self.name.index(name))
            
    # fonction externe
    def get(self,name):
        index = self.indox(name)
        if index >= 0 :
            
            cont = self.contenue[index]
            self.time(index)
            return cont
        else :
            self.getlocal(name)
            cont = self.contenue[index]
            self.time(index)
            return cont
    def update(self,name,contenu):
        index = self.indox(name)
        self.contenue[index] = contenu
        self.time(index)
    def create(self,name,cont=''):
        try  :
            self.name.index(name)
            printal("BigData ERROR : variable aleready charged : {"+name+'}')
            return False
        except :
            self.name.append(name)
            self.contenue.append(cont)
            self.date.append(time.time())
            printal("BigData INFO : Var CREATED : {"+name+'}')
            return True
    def exist(self,name):
        if name in self.name :
            return True
        else :
            return False

    # fonction de recuperation
    def getlocal(self,name):
        recup = sql.Where('Var',
                          colone=['nom'],
                          objet=[name],
                          bdd='local.db')
        if not recup :
            printal("BigData ERROR : variable not found : {"+name+'} : ACTION ( CREATION )')
        elif len(recup) > 1 :
            printal("BigData ERROR : multiple variable : {"+name+"} : {"+len(recup)+'}')
        else :
            if self.create(name) :
                self.update(name,recup[2])
            else :
                printal("BigData INFO : exit")
                exit()
    def save_all(self):
        for i in self.name :
            self.save(i)
    def recup(self):
        get = sql.All('Var',bdd='local.db')
        for i in get :
            printal("BigData INFO (Recup) : Var import : ")
            self.create(i[1])
            self.update(i[1],i[2])
            printal("BigData INFO (Recup) : FIN import !")
    # other
    def exista(self,nom,contenu):
        """
        si la variable n'existe pas on la crée
        """
        if not self.exist(nom) :
            self.create(nom,contenu)
        else :
            self.update(nom,contenu)