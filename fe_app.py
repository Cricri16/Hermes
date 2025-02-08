import tkinter
import palette
import tklist
import sql
import msg_fonct
import stockage
import conextion
import be_app
import user_conected
import sendmess
import affichage
import update
class MainInterface(tkinter.Tk):
    def __init__(self,data:stockage.BigData) -> None:
        super().__init__()
        self.title('hermes : '+ data.get('pseudo'))
        self.configure(bg=palette.custom(0))
        self.grid_rowconfigure(1,weight=1)

        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=20)
        self.grid_columnconfigure(3, weight=3)
        # self.grid_columnconfigure(4, weight=5)

        # on definit les 3 frame principale



        # frame de droite

        self.fleft = tkinter.Frame(self,bg=palette.custom(0))
        self.fleft.grid(row=1,column=1,sticky='nsew')
        
        # frame du milieux

        self.fmid = tkinter.Frame(self,bg=palette.custom(0))
        self.fmid.grid(row=1,column=2,sticky='nsew')

        self.fmid.columnconfigure(1,weight=20)
        self.fmid.columnconfigure(2,weight=5)

        self.fmid.rowconfigure(1,weight=1)
        self.fmid.rowconfigure(2,weight=50)
        self.fmid.rowconfigure(3,weight=50)
        self.fmid.rowconfigure(4,weight=1)

        # frame de gauche

        self.fright = tkinter.Frame(self,bg=palette.custom(0))
        self.fright.grid(row=1,column=3,sticky='nsew')

        self.fright.columnconfigure(1,weight=1)

        self.fright.rowconfigure(1,weight=1)
        self.fright.rowconfigure(2,weight=50)
        self.fright.rowconfigure(3,weight=50)
        self.fright.rowconfigure(4,weight=1)





        # frame de droite
        # button public en bas

        self.bpublic = tkinter.Button(self.fleft,bg=palette.custom(1),fg='white',text='public',font=("Courier",12))
        self.bpublic.pack(side='top',fill='x',padx = 5 , pady = 5)
        
        # frame pour listbox 

        self.fgroupe = tkinter.Frame(self.fleft,bg=palette.custom(0))
        self.fgroupe.pack(expand=1,fill='both')

        # listbox groupe
        # bind AF
        #self.lgroupe = tklist.Listbox(master=self.fgroupe,label='groupe',hide=True,font=("Courier",12))
        #self.lgroupe.pack(side='top',fill='both',padx = 5 , pady = 5)

        # listbbox msg
        # bind AF
        self.lbmsg = tklist.Listbox(master=self.fgroupe,label='msg',hide=True,font=("Courier",12))
        self.lbmsg.pack(side='top',fill='both',padx = 5 , pady = 5,expand=1)


        # fmid
        # label emplacement


        self.lemplacement = tkinter.Label(self.fmid, bg=palette.custom(1),fg='white',text='None',font=("Courier",12))
        self.lemplacement.grid(row=1,column=1,columnspan=2,sticky='nsew',padx=5,pady=5)


        self.lbmessage = tklist.Listbox(master=self.fmid,font=("Courier",24))
        self.lbmessage.frame.grid(row=2,rowspan=2,column=1,columnspan=2,sticky='nsew',padx=5,pady=5)

        def tp(*ele,**elem):
            sendmess.message(data,self.emessage,emplacement)
            self.emessage.delete(0,tkinter.END)
        
        self.emessage = tkinter.Entry(self.fmid,bg=palette.custom(1),fg='white',font=("Courier",12))
        self.emessage.bind("<Return>",tp)
        self.emessage.grid(row=4,column=1,sticky='nsew',padx=5,pady=5)

        self.bsend = tkinter.Button(self.fmid,bg=palette.custom(1),fg = 'white',text='envoie',command=tp,font=("Courier",12))
        self.bsend.grid(row=4,column=2,sticky='nsew',padx=5,pady=5)


        # right

        self.econected = tkinter.Entry(self.fright,bg=palette.custom(1),font=("Courier",12),fg='white')
        self.econected.grid(row=1,column=1,sticky='nsew',padx=5,pady=5)

        self.lbconected = tkinter.Listbox(self.fright,activestyle='none',selectbackground=self.fright.cget("background"),bg=palette.custom(1),fg='white',borderwidth=0, highlightthickness=0,font=("Courier",12))
        self.lbconected.grid(row=2,rowspan=3,column=1,sticky='nsew',padx=5,pady=5)
        
        
        emplacement = be_app.Emplacement(frame=self.fmid,label=self.lemplacement)

        self.lbconected.bind('<Button-1>',lambda test : user_conected.move(self.lbconected,emplacement,data))
        self.lbmsg.list.bind('<Button-1>',lambda event : msg_fonct.click(self.lbmsg,emplacement))

        self.bpublic.configure(command=emplacement.public)
        user_conected.Tab(self.fright,self.lbconected,self.econected,data)
        user_conected.Ping(frame=self,data=data)
        # on lie la listbox lbconect a la fonction qui permet de changer le chanel
        # on lie le bouton et la touche retour a send
        def tp(*ele,**elem):
            sendmess.message(data,self.emessage,emplacement)
            self.emessage.delete(0,tkinter.END)
        self.emessage.bind("<Return>",tp)
        affichage.main(data,self.lbmessage,emplacement,self)
        msg_fonct.main(data,self,self.lbmsg,emplacement)

update.chekupdate()
sql.init()# si les base de donnée n'existe pas on les crée

data = stockage.BigData()
data.recup()

conextion.ident(data)


app = MainInterface(data)
app.mainloop()

# on se deconece
empl = sql.Where('log_conect',colone=['pname'],objet=[data.get('pseudo')]) # on se trouve dans la bdd
import time
sql.Update('log_conect',['sortie'],objet=[time.time()],id = empl[0][0])

