import base64 as b64

clee = b64.b64decode('NlB+YlVUSXMyZiU2T15mLWVGclYyMDN5ckVYUmYwZ1lqJFtqLzc1I243NTZFPlouPSFNdTFQNTt7dnY=').decode()
liste_chifrement = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!:/.;?,[]"

def a(x):
    y = liste_chifrement.find(x)
    z = liste_chifrement[y:] + liste_chifrement[:y]
    return z

def b(x, y):
    z = a(x)
    return z[y]

def c(x, y):
    z = int(liste_chifrement.find(x))
    return b(y, z)

def d(x):
    if isinstance(x, str):
        global clee
        r = ""
        p = 0
        while len(clee) <= len(x):
            clee = clee + clee

        for q in x:
            if liste_chifrement.find(q) == -1:
                r = r + q
            else:
                r = r + str(c(q, str(clee[p])))
                p = p + 1
    else:
        return x
    return r

def e(x, y):
    z = a(x)
    return liste_chifrement[z.find(y)]

def f(x):
    global clee
    r = ""
    p = 0
    while len(str(clee)) <= len(str(x)):
        clee = clee + clee
    if isinstance(x, str):
        for q in x:
            if isinstance(q, int) == False:
                if liste_chifrement.find(q) == -1:
                    r = r + q
                else:
                    r = r + str(e(str(clee[p]), q))
                    p = p + 1
            else:
                return q
    else:
        return x
    return r

def chifrement(mot): # utiliser 
    if isinstance(mot, str):
        global clee
        result = ""
        depla = 0
        while len(clee) <= len(mot):
            clee = clee + clee

        for corect in mot:
            if liste_chifrement.find(corect) == -1:
                result = result + corect
            else:
                result = result + str(c(corect, str(clee[depla])))
                depla = depla + 1
    else:
        return mot
    return result

def dechifrement(mot): # utiliser 
    global clee
    result = ""
    depla = 0
    while len(str(clee)) <= len(str(mot)):
        clee = clee + clee
    if isinstance(mot, str):
        for corect in mot:
            if isinstance(corect, int) == False:
                if liste_chifrement.find(corect) == -1:
                    result = result + corect
                else:
                    result = result + str(e(str(clee[depla]), corect))
                    depla = depla + 1
            else:
                return corect
    else:
        return mot
    return result

def chirement_list(li): # utiliser
    liste_chifrement = []
    for i in li:
        liste_chifrement.append(chifrement(i))
    return liste_chifrement

def dechifrement_list(li): # utiliser
    liste_chifrement = []
    if li:
        for i in li:
            if type(i) is str:
                liste_chifrement.append(dechifrement(i))
            else:
                liste_chifrement.append(i)
        return liste_chifrement
    else:
        return ''
    
