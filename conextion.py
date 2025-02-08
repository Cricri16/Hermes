import sql
import customhtml
import tkinter
import palette
import stockage
class ident:
    def __init__(self,data:stockage.BigData) -> None:
        data.create('rname')
        data.update('rname',customhtml.bvn())
        self.get_pseudo(data)
    def get_pseudo(self,data:stockage.BigData):
        ret = sql.Where('anuaire_user',
                        colone=['rname'],
                        objet=[data.get('rname')])
        if ret == [] :
            a = self.inscription(data)
        else :
            data.create('pseudo')
            data.update('pseudo',ret[0][2])

    def inscription(self,data:stockage.BigData):
        Var = data.get('rname')

        from tkinter import messagebox
        import sql
        import time
        def register_name(*elem):
            pseudo = ent.get()
            li = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890._-"
            for i in pseudo:
                if i not in li :
                    messagebox.showinfo('nop','Votre pseudo ne doit pas contenir de caractères spéciaux.')
                    return False
            if len(pseudo) > 4 and len(pseudo) < 15:
                inbdd = sql.Where('anuaire_user',
                                colone=['pname'],
                                objet=[pseudo])
                if inbdd :
                    messagebox.showinfo('nop','pseudo deja utiliser')
                else :
                    messagebox.showinfo('nop','Inscription réussie')
                    main.destroy()
                    temp =  sql.Write('anuaire_user',
                                    colone=['rname','pname','date'],
                                    objet=[Var,pseudo,time.time()]
                    )
                    b = sql.Where('anuaire_user',
                        colone=['id'],
                        objet=[temp])
                    data.create('pseudo')
                    data.update('pseudo',pseudo)
                    exit()
            else:
                if len(pseudo) < 4 :
                    messagebox.showinfo('nop','Le pseudo doit avoir au moins 5 caractères.')
                if len(pseudo) >= 15 :
                    messagebox.showinfo('nop','Le pseudo doit avoir moins de 15 caractères.')

        main = tkinter.Tk()
        main.config(background=palette.custom(0))
        main.title('Hermes')
        label = tkinter.Label(main,text="Bienvenue sur Hermes",bg=palette.custom(1),fg='white')
        label.pack(padx = 10,pady = 10)

        f = tkinter.Frame(master=main,bg=palette.custom(1))

        l = "Bonjour " + Var + " . \n \n Vous n'êtes pas inscrit, \n veuillez choisir un pseudo :"
        label = tkinter.Label(f,text=l,bg=palette.custom(2),fg='white')
        label.pack(padx = 10,pady = 10)

        ent = tkinter.Entry(f)
        ent.pack(padx = 10,pady = 10)
        ent.bind("<Return>", register_name)

        but = tkinter.Button(f,text="s'inscrire",command=register_name,bg=palette.custom(1),fg='white')
        but.pack(padx = 10,pady = 10)

        f.pack(padx = 10,pady = 10)

        main.mainloop()

