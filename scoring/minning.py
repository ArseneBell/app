import csv
import json
import re

def readfile():
    liste = []
    try:
        with open ('Foodapp.csv','r', newline='') as csvfile:
        
            reader = csv.reader(csvfile, delimiter=';')
            for ligne in reader:
                liste.append(ligne)
    except:
        print('Erreur')
    return liste[1:]

def readTxt(nom_fichier):

    contenu = "Indisponible :("
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as file:
            contenu = file.read()
            return contenu
    except FileNotFoundError:
        print(f"Fichier {nom_fichier} pas trouvé")
    except Exception as e:
        print(f"Une erreur a ete produite : {e}")

    return contenu



Data = readfile()

def Cleanning(Data):
    Ingredients = [Data[i][5]  for i in range(len(Data))]

    Ingredient = []
    for liste in Ingredients:
        l = liste.split(',')
        for li in l:
            Ingredient.append(li.lower())

    liste = []
    for ingre in Ingredient:
        if ingre not in liste:
            liste.append(ingre)
    


    with open('Ingredients.csv', 'w', newline='') as file :
        writter = csv.writer(file, delimiter=';')
        writter.writerow(['Ingredients'])
        for i in range(len(liste)):
            writter.writerow([liste[i]])
           

def csv_Json(Data):

    delimiteurs = r"[,.\n]"

    for ligne in Data:
        for i in range(len(ligne)):
            if i == 4:
                ligne[i] = readTxt(f"recette/{ligne[i]}")
                ligne[i] = re.split(delimiteurs, ligne[i])

                ligne[i] = [mot.strip() for mot in ligne[i] if mot.strip()]

                dico = {}
                for j in range(len(ligne[i])):
                    dico[f"{j+1}"] = ligne[i][j]
                ligne[i] = dico

            if i == 2:
                ligne[i] = ligne[i].split('\n')

            if i == 5:
                ligne[i] = ligne[i].split(',')


    t_format = []
    for ligne in Data:
        a = {"Titre": ligne[0],
             "Cooking time": 0,
             "lien_video": ligne[3],
             "Images": ligne[2],
             "Ingredients": ligne[5],
             "Instructions": ligne[4],
             "Type": ligne[1]}
        
        t_format.append(a)

    

    with open('app.json', "w", encoding='UTF-8') as file:
        json.dump(t_format, file, indent=4)

Cleanning(Data)
csv_Json(Data)