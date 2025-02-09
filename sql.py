import sqlite3
import time
import chifrement
import os

sql_bdd_emplacement = "Q:\Espace d"+chr(39) +chr(233)+"change\\bdd.db"

def init():
    """
on doit verifier que le fichier bdd existe bien
si non on le crée
comande sql """
    lists = [
"""CREATE TABLE "anuaire_user" (
	"id"	INTEGER UNIQUE,
	"rname"	TEXT,
	"pname"	TEXT,
	"date"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
)""",
"""CREATE TABLE "groupe" (
	"id"	INTEGER UNIQUE,
	"pname"	TEXT,
	"zone"	TEXT,
    "groupe" TEXT,
	"content"	TEXT, `type` TEXT,
	"date"	INTEGER,
    "hiden_data"    TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)""",
"""CREATE TABLE "log_conect" (
	"id"	INTEGER UNIQUE,
	"pname"	TEXT,
	"zone"	TEXT,
	"arivée"	INTEGER,
	"actualisation"	INTEGER,
	"sortie"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
)""",
"""CREATE TABLE "message" (
	"id"	INTEGER UNIQUE,
	"pname"	TEXT,
	"zone"	TEXT,
	"content"	TEXT, `type` TEXT,
	"date"	INTEGER,
    "hiden_data"    TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)""",
"""CREATE TABLE "private_message" (
	"id"	INTEGER UNIQUE,
	"sender"	TEXT,
	"zone"	TEXT,
	"recept"	TEXT,
	"content"	TEXT, `type` TEXT, "date"	INTEGER,
    "hiden_data"    TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)""",
"""CREATE TABLE "partage" (
	"id"	INTEGER UNIQUE,
	"sender"	TEXT,
	"content"	TEXT,
	"recu"	INTEGER,
	"time"	INTEGER,
    "file_name" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)""",
"""CREATE TABLE "new_pseudo" (
	"id"	INTEGER,
    "rname" TEXT,
	"last"	TEXT,
	"new"	TEXT,
	"date"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);"""]
    if not os.path.exists(sql_bdd_emplacement):
        main = sqlite3.connect(sql_bdd_emplacement)
        for i in lists :
            main.execute(i)
        main.close()
        main = sqlite3.connect(sql_bdd_emplacement)
        data = chifrement.chirement_list(['Robin CRIADO','Dev',time.time()])
        cursor = main.cursor()
        cursor.execute("INSERT INTO anuaire_user (rname,pname,date) VALUES (?,?,?)",data)
        main.commit()
        main.close()
    lists = ["""CREATE TABLE "Var" (
	"id"	INTEGER UNIQUE,
	"nom"	TEXT,
	"cont"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)"""]
    if not os.path.exists('local.db'):
        main = sqlite3.connect('local.db')
        for i in lists :
            main.execute(i)
        main.close()
init()

def format(table,colone,objet,condition = False , operation = '=',ty = 'AND'):
    comand = "SELECT * FROM " + table + " where "
    if len(colone) == len(objet) :
        if len(colone) == 1 :
            comand += colone[0] + " " + operation + " ? "
        elif len(colone) == 0 : # erreur posible
            return False
        else :
            for i in colone :
                if colone.index(i) == 0 :
                    comand += i + " " + operation + " ? "
                else :
                    comand += ""+ty+" " + i + " " + operation + " ? "
        if condition :
            comand += " " + condition
    else :
        return "len(colone) != len(objet)"
    return comand

def Where(table:str,colone:list,objet:list,operation='=',condition = False,prin = False,ty ='AND',bdd=sql_bdd_emplacement):
    conn = sqlite3.connect(bdd)
    cursor = conn.cursor()
    comand = format(table,colone,objet,condition,operation,ty=ty)
    if prin:
        print(comand)
    cursor.execute(comand,chifrement.chirement_list(objet))
    ret = []
    for row in cursor.fetchall():
        ret.append(chifrement.dechifrement_list(row))
    conn.close()
    return ret

def special_recherche(comand,objet,bdd=sql_bdd_emplacement,pri=False):
    conn = sqlite3.connect(bdd)
    cursor = conn.cursor()
    cursor.execute(comand,chifrement.chirement_list(objet))
    if pri:
        print(f'{comand} \n {objet}')
    ret = []
    for row in cursor.fetchall():
        ret.append(chifrement.dechifrement_list(row))

    conn.close()
    return ret
def parentformat(colone:list):
    ret1 = "("
    ret2 = "("
    for i in colone:
        if colone.index(i) == 0 :
            ret1 += " " + i
            ret2 += " ?"
        else :
            ret1 += " , " + i
            ret2 += " , ?"
    return ret1 + ") VALUES " + ret2 + " )"


def Write(table,colone:list,objet:list,pri = False,bdd=sql_bdd_emplacement):
    conn = sqlite3.connect(bdd)
    cursor = conn.cursor()
    if len(colone) != len(objet) :
        return"len(colone) != len(objet)"
    comand = "INSERT INTO " + table + " " + parentformat(colone)
    if pri:
        print(comand)
        print(objet)
    cursor.execute(comand,chifrement.chirement_list(objet))
    conn.commit()
    conn.close()
    return Where(table=table,colone=colone,objet=objet,bdd=bdd,prin=pri)[0][0]
def formatupdate(colone:list,objet:list):
    ret = " SET "
    if len(colone) != len(objet) :
        return "len(colone) != len(objet)"
    for i in colone :
        empl = colone.index(i)
        if empl == 0 :
            ret += i + " = ?"
        else :
            ret += " , " + i + " = ?"
    return ret

def Update(table:str,colone:list,objet:list,id:int,prin = False,bdd=sql_bdd_emplacement):
    conn = sqlite3.connect(bdd)
    cursor = conn.cursor()
    comand = "UPDATE " + table + formatupdate(colone,chifrement.chirement_list(objet)) + " WHERE id = " + str(id)
    if prin :
        print(comand)
    cursor.execute(comand,chifrement.chirement_list(objet))
    conn.commit()
    conn.close()
    return True

def All(table,bdd=sql_bdd_emplacement):
    conn = sqlite3.connect(bdd)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM "+ table)
    res = cursor.fetchall()
    ret = []
    for i in res :
        ret.append(chifrement.dechifrement_list(i))
    return ret


