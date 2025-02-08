clee = '6P~bUTIs2f%6O^3(m-eFrV203yrEXRf0gYj$[j/75#n756E?Z.=!Mu1P5{;v'
liste_chifrement = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!:/.;?,[]"
def letrechang(let):
    let = liste_chifrement.find(let)
    chang = liste_chifrement[let:] + liste_chifrement[:let]
    return chang
def lettr(lettrcle,loclett):
    bla =""
    var = letrechang(lettrcle)
    bla = var[loclett]
    return bla
def chifr(lettre,lettrcle):
    loclett = int(liste_chifrement.find(lettre))
    bla = lettr(lettrcle,loclett)
    return bla
def chifrement(mot): # utiliser 
    if isinstance(mot,str) :
        global clee
        result = ""
        depla = 0
        while len(clee) <= len(mot):
            clee = clee + clee

        for corect in mot :
            if liste_chifrement.find(corect) == -1:
                result = result + corect
            else:
                result = result + str(chifr(corect,str(clee[depla])))
                depla = depla +1
    else:
        return mot
    return result
def lettra(lettrcle,loclett):
    bla =""
    var =letrechang(lettrcle)
    bla = liste_chifrement[var.find(loclett)]
    return bla
def dechifrement(mot): # utiliser 
    global clee
    result = ""
    depla = 0
    while len(str(clee)) <= len(str(mot)):
        clee = clee + clee
    if isinstance(mot,str) :
        for (corect) in mot :
            if isinstance(corect,(int)) == False:
                if liste_chifrement.find(corect) == -1:
                    result = result + corect
                else:
                    result = result + str(lettra(str(clee[depla]),corect))
                    depla = depla +1
            else:
                return corect
    else:
        return mot
    return result
def chirement_list(li):# utiliser
    liste_chifrement=[]
    for i in li:
        liste_chifrement.append(chifrement(i))
    return liste_chifrement
def dechifrement_list(li):# utiliser
    liste_chifrement=[]
    if li:
        for i in li:
            if type(i) is str:
                liste_chifrement.append(dechifrement(i))
            else :
                liste_chifrement.append(i)
        return liste_chifrement
    else:
        return ''