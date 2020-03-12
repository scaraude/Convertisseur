"""
1. chosit le fichier (boucle tant que le fichier est invalide
2. boucle sur la lecture du fichier (tant qu'il y a une ligne à lire)
    2.1 récupère la balise
    2.2 aiguillage en fct de la balise
    2.3 traite les infos à récup de la ligne
3. ecrit le fichier convertie
"""

import os

dicoNote = {"C2": 1, "D2": 5, "E2": 9, "F2": 11, "G2": 15, "A2": 19, "B2": 22,
            "C3": 25, "D3": 29, "E3": 32, "F3": 34, "G3": 38, "A3": 42, "B3": 46,
            "C4": 48, "D4": 52, "E4": 56, "F4": 58, "G4": 62, "A4": 66, "B4": 69,
            "C5": 71, "D5": 75, "E5": 79, "F5": 81, "G5": 85, "A5": 89, "B5": 93,
            "C6": 95, "D6": 98, "E6": 102, "F6": 105, "G6": 108, "A6": 112, "B6": 116,
            "C7": 119}
dicoSpe = { "!r" : 251, "!t" : 253, "!m" : 254, "erreur" : 255, "separateur" : 250} #252 pris pour le tempo

# choppe le fichier a convertir
def FileChoice():
    chemin = "C:/Users/412877/Documents/Partition/"
    dossierDeSave = "Embedded/"      #parce qu'on enregistre pas dans le meme dossier
    fichierInput = str()
    suffixeXml = ".musicxml"
    suffixeFile = ".txt"

    print("fichier à convertir ?", "\n")
    fichierInput = input()

    fileRead = chemin + fichierInput + suffixeXml
    fileWrite = chemin + dossierDeSave + fichierInput + suffixeFile

    return fileRead, fileWrite


def GetBalise(ligne):
    if ligne.find("tempo") != -1:  # !!! CHECKER i ya d'autre balise qui contiennent "tempo"
        return "tempo"
    elif ligne.find("<alter>") != -1:
        return "alter"
    elif ligne.find("<note") != -1:
        return "note"
    elif ligne.find("<octave>") != -1:
        return "octave"
    elif ligne.find("<step>") != -1:
        return "step"
    elif ligne.find("<staff>") != -1:
        return "staff"
    elif ligne.find("<duration>") != -1:
        return "duration"
    elif ligne.find("</note>") != -1:
        return "/note"
    elif ligne.find("<backup>") != -1:
        return "backup"
    elif ligne.find("<forward>") != -1:
        return "forward"
    elif ligne.find("<rest/>") != -1 or ligne.find("<rest>") != -1:
        return "rest"
    elif ligne.find("tied") != -1:  # !!! CHECKER i ya d'autre balise qui contiennent "tied"
        return "tied"
    elif ligne.find("<measure number") != -1:  # !!! CHECKER i ya d'autre balise qui contiennent "measure"
        return "mesure"
    elif ligne.find("<chord/>") != -1:
        return "chord"
    elif ligne.find("<notations>") != -1:
        return "notation"
    elif ligne.find("</notations>") != -1:
        return "/notation"
    else:
        return "none"


def ExploitBalise(ligne, balise):  # EXTRAIT LES DONNEES DE LA BALISE
    if balise == "step":
        lNote = ligne[ligne.find(">") + 1: ligne.find("<", ligne.find(">"))]  # extrait la lettre entre > et <
        return lNote

    if balise == "octave":
        cNote = ligne[ligne.find(">") + 1: ligne.find("<", ligne.find(">"))]  # extrait le chiffre entre > et <
        return cNote

    if balise == "alter":
        alter = int(ligne[ligne.find(">") + 1: ligne.find("<", ligne.find(">"))])  # extrait l'alteration entre > et <
        return alter

    if balise == "duration":
        duration = int(ligne[ligne.find(">") + 1: ligne.find("<", ligne.find(">"))])  # extrait la durée entre > et <
        return duration

    if balise == "tempo":
        tempo = int(
            ligne[ligne.find("\"") + 1: ligne.find("\"", ligne.find("\"") + 1)])  # extrait la lettre entre " et "
        return tempo

    if balise == "staff":
        staff = int(ligne[ligne.find(">") + 1: ligne.find("<", ligne.find(">"))])  # extrait la lettre entre > et <
        return staff

    if balise == "mesure":
        try :
            mesure = int(ligne[ligne.find("\"") + 1: ligne.find("\"", ligne.find("\"") + 1)])
        except:
            mesure = dicoSpe["erreur"]
        return mesure

    if balise == "tied":
        tiedType = ligne[ligne.find("\"") + 1: ligne.find("\"", ligne.find("\"") + 1)]
        return tiedType


def GetNote(curseur, NumeroLigne):
    infoNote = []

    alter = 0
    chord = False
    note = ""
    tieded = False

    ligne = f.readline()
    balise = GetBalise(ligne)
    NumeroLigne += 1

    infoNote.insert(1, curseur)

    # print("ligne : ", NumeroLigne - 1)

    while balise != "/note":
        if balise == "rest":
            infoNote.insert(0, dicoSpe["!r"])

        if balise == "chord":
            chord = True

        if balise == "step":
            note += ExploitBalise(ligne, balise)

        if balise == "octave":
            note += ExploitBalise(ligne, balise)

        if balise == "duration":
            duree = ExploitBalise(ligne, balise)
            infoNote.insert(2, duree)
            if not chord:
                curseur += duree

        if balise == "alter":
            alter = ExploitBalise(ligne, balise)

        if balise == "staff":
            infoNote.insert(3, ExploitBalise(ligne, balise))

        if balise == "tied":
            if ExploitBalise(ligne, balise) == "stop":
                i = len(stock) - 1
                while stock[i][0] != dicoNote[note]:
                    i -= 1
                stock[i][2] += duree
                tieded = True

        ligne = f.readline()
        balise = GetBalise(ligne)
        NumeroLigne += 1

    if note != "":
        infoNote.insert(0, dicoNote[note])

    if chord:
        infoNote[1] = stock[len(stock) - 1][1]

    if tieded:
        infoNote = []

    return curseur, NumeroLigne, infoNote


if __name__ == "__main__":

    while True:
        try:
            fileRead, fileWrite = FileChoice()
            f = open(fileRead, "r")
            break
        except :
            print("this file is not available...")


    stock = []
    curseur = 0
    mesure = 0

    NumberOfLine = 0

    for line in f:
        NumberOfLine += 1
        balise = GetBalise(line)

        if balise == "note":
            curseur, NumberOfLine, infoNote = GetNote(curseur, NumberOfLine)
            if infoNote != []:
                stock.append(infoNote)
            if len(infoNote) != 4: # sort les erreurs
                print(NumberOfLine)
                print(infoNote)

        if balise == "mesure":
            curseur = 0
            mesure = ExploitBalise(line, balise)
            stock.append([dicoSpe["!m"], mesure])
            print(mesure)
            print()

        if balise == "tempo":
            stock.append([dicoSpe["!t"], ExploitBalise(line, balise)])

        if balise == "backup":
            line = f.readline()
            NumberOfLine += 1
            balise = GetBalise(line)
            curseur -= ExploitBalise(line, balise)

        if balise == "forward":
            line = f.readline()
            NumberOfLine += 1
            balise = GetBalise(line)
            curseur += ExploitBalise(line, balise)

    f.close()

    print(stock)

    nbItem = 0
    sizeItem = 0
    nbBytes = 0

    with open(fileWrite, "wb") as f:
        i = 0
        while i < len(stock):
            j = 0
            while (j < len(stock[i])):
                #print(stock[i][j])
                try:
                    f.write(bytes([stock[i][j]]))
                    nbBytes += 1
                except:
                    #f.write(stock[i][j])
                    print("le stock[" + str(i) + "][" + str(j) + "] n'est pas convertible en byte")
                sizeItem += stock[i][j].__sizeof__()
                j += 1
            nbItem += j
            f.write(bytes(dicoSpe["separateur"])) #Séparateur de note (byte 250 pour délimiter chaque note)
            nbBytes+=1
            i += 1

    print()
    print("taille du stock : " + str(len(stock)))  # colonne dans le tableau
    print("nombre d'item : " + str(nbItem))  # élément dans le tableau
    print()
    print("nombre de bytes : " + str(nbBytes))
    print("taille du stock : " + str(stock.__sizeof__())) # en bytes
    print("taille de tous les elements : " + str(sizeItem)) # en bytes

    f.close()