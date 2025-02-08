import tkinter
import palette
from tkinter import ttk
import partage
import webbrowser
from tkinter import font
class Listbox:

    def __init__(self,master:tkinter.Frame,label=False,hide=False,bind=False,cont=[],**element) -> None:
        self.content = cont
        self.master_info = master
        # on def la frame principale

        self.frame = tkinter.Frame(master=master,bg=palette.custom(0))
        self.frame.grid_rowconfigure(1,weight=1)
        self.frame.grid_rowconfigure(2,weight=100)
        self.frame.grid_columnconfigure(1,weight=20)
        self.frame.grid_columnconfigure(2,weight=5)

        # la listbox

        self.content = cont

        
        
        if hide :
            self.bhide = tkinter.Button(self.frame,text='-',command=self.hide)
            self.hide_etat = False
            self.bhide.grid(row=1,column=2,sticky='nsew',padx = 5 , pady = 5)
        if label and hide :
            self.label = tkinter.Label(self.frame,text=label,bg = palette.custom(2),fg='white')
            self.label.grid(row=1,column=1,sticky='nsew')
        elif label and not hide :
            self.label = tkinter.Label(self.frame,text=label,bg = palette.custom(2),fg='white')
            self.label.grid(row=1,column=1,columnspan=2,sticky='nsew')


        self.fr2 = tkinter.Frame(self.frame,bg=palette.custom(2))
        self.fr2.grid(row=2,column=1,columnspan=2,sticky='nsew')
        self.scrollbar = ttk.Scrollbar(self.fr2, orient=tkinter.VERTICAL)
        # Link it to the listbox.
        self.list = tkinter.Listbox(master=self.fr2,selectbackground=palette.custom(1),
                                    listvariable=self.content,
                                    yscrollcommand=self.scrollbar.set,bg=palette.custom(1),
                                    fg='white',
                                    borderwidth=0, 
                                    highlightthickness=0,
                                    font=("Arial",11))
        if bind  :
            self.bind_info = bind
            self.list.bind('<Button-1>',lambda event : bind(element))
        self.scrollbar.config(command=self.list.yview)


        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)


        self.list.pack(side='left',expand=1,fill='both')
        self.list.bind('<Button-1>',lambda event : self.clic())
        self.hiden = []
        self.last_master = master.winfo_width()
        self.verif_data = []
        self.verif_hiden = []
        self.verification()
    def insert(self,element,index=False,hiden_data=0,unique=False):
        if index :
            tp = index
        else :
            index = tkinter.END
            tp = -1
        if hiden_data == None :
            hiden_data = '0'
        if (hiden_data == '0' or hiden_data == 0 ) and element[:7]=='[Dev :]' :
            hiden_data = 'Dev_admin'
        hiden_data = str(hiden_data)
        self.hiden.append(hiden_data)
        self.content.append(element)
        self.list.insert(index,element)
        self.actualisation_taille()
    def hide(self,**elem):
        if self.hide_etat :
            self.fr2.grid(row=2,column=1,columnspan=2,sticky='nsew')
            self.bhide.configure(text='-')
            self.hide_etat = False
        else:
            self.fr2.grid_forget()
            self.bhide.configure(text='+')
            self.hide_etat = True
    def clean(self):
        self.hiden = []
        self.content = []
        self.list.delete(0,tkinter.END)
    def get(self):
        empl = str(self.list.curselection())
        if empl != '()':
            empl = empl[1:empl.find(',')]
            empl = int(empl)
            return self.verif_data[empl],self.verif_hiden[empl]
        return False,False
    def pack(self,**elem): 
        self.frame.pack(**elem)
    def config(self,index,dico):
        self.list.itemconfig(index,dico)
        self.list.update()
    def see(self):
        self.list.see('end')
    def clic(self):
        mess,hide = self.get()
        self.list.selection_clear(0,tkinter.END)
        if mess == False or hide == False :
            return False
        elif hide[:18] == "file_hiden_data : " :
            partage.recept(hide[18:]) # telecharge le fichier
        elif hide[:18] == "link_hiden_data : " :
            webbrowser.open(hide[18:]) # on ouvre le lien dans le navigateur par defauld
    def verification(self):
        if self.last_master != self.master_info.winfo_width() :
            self.actualisation_taille()
            self.last_master = self.master_info.winfo_width()
        self.master_info.after(500,self.verification)
    def actualisation_taille(self):
        all_item = self.content # on recupére tout les item de la listbox
        hiden_item = self.hiden # on recupére leur data
        self.list.delete(0,tkinter.END)
        self.verif_data = []
        self.verif_hiden = []
        taile_interface = self.master_info.winfo_width() # on trouve la taille de l'interfaec
        for item in all_item : # on verifie tout les item un pars un
            hiden = hiden_item[all_item.index(item)]
            size = 0 # on crée la variable taille
            for lettre in item : # on parcours les lettre de l'item
                size += font.Font(family="Arial",size=12).measure(lettre) # on rajoute la taille de la lettre pour avoir la taille total de la phrase a la fin
            if size >= taile_interface : # on compare les deux
                if 1 < size/taile_interface < 2 :
                    taux = 2
                else :
                    taux = size//taile_interface # on fait la divisio pour savoir en combien on doit la diviser
                part = len(item)//taux # on prend la longueyr des troncons
                for i in range(taux) : # on répéte l'operation pour le decouper taux fois
                    self.list.insert(tkinter.END,item[:part])# on ajoute le troncons
                    self.verif_data.append(item[:part])
                    self.verif_hiden.append(hiden)
                    self.color(hiden)
                    
                    self.see()
                    item = item[part:]# on retir le troncons ajouter
                if item : # si il reste un truc dans item
                    self.list.insert(tkinter.END,item)# on le rajoute a la sortie
                    self.verif_data.append(item)
                    self.verif_hiden.append(hiden)
                    self.color(hiden)
                    
                    self.see()
            else :
                self.list.insert(tkinter.END,item)
                self.verif_data.append(item)
                self.verif_hiden.append(hiden)
                self.color(hiden)
                self.see()
    def color(self,hide):
        if hide[:18] == "file_hiden_data : " :
            self.list.itemconfigure(tkinter.END,{'bg':'#8A0012'})
        elif hide[:18] == "link_hiden_data : ":
            self.list.itemconfigure(tkinter.END,{'bg':'#150B8A'})