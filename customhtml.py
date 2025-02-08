class html:
    def __init__(self,fichier) -> None:
        self.fichier = open(fichier,'r')
    def close(self):
        self.fichier.close()
    def get_div(self,clas,fichier = ''):
        if fichier == '' :
            self.text = self.fichier.readlines()
        ret = []
        a = False
        ent = ''
        for i in self.text :
            if i.find(f'<div class="{clas}">') >= 0 :
                ret.append(i)
                a = True
                ent = i[:i.find('<')]
            if i.find(f'{ent}</div>') >= 0 and a == True :
                ret.append(i)
                return ret
            if a == True :
                ret.append(i)
        return False
    def get_balise(self,balise,lists = '') :
        if list == '' :
            self.text = self.fichier.readlines()
        else :
            self.text = lists
        for i in self.text :
            if i.find(f'<{balise}>') >= 0 :
                return i[i.find(balise)+len(balise)+1:i.find(f'</{balise}>')]
def bvn():
    bvn = html('P:\\Bienvenue.htm')
    b = bvn.get_div('top')
    name = bvn.get_balise('b',b)
    name = name[3:]
    bvn.close()
    return name
