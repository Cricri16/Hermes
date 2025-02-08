import time

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
