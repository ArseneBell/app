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
    for lst in liste[1:]:
        lst[5] = lst[5].split(',')
    return liste[1:]

Data = readfile()
data = [d[5] for d in Data]
datas = [elt.lower() for sous_liste in data for elt in sous_liste]





def Ingredients_Poids(datas):
    Ingredient = datas
    

    Ingredient_occurrence = {}
    for i in Ingredient:
        if i not in Ingredient_occurrence:
            Ingredient_occurrence[i] = 1
        else:
            Ingredient_occurrence[i] += 1

    ingredien_trie = dict(sorted(Ingredient_occurrence.items(), key=lambda x: x[1]))
    occ_min = next(iter(ingredien_trie.values()))
    occ_max = next(iter(reversed(ingredien_trie.values())))

    ingredient_poid = {}
    ingredient_poid = dict(sorted(ingredient_poid.items()))
    for cle in ingredien_trie:
        ingredient_poid[cle] = 5 - (4*(ingredien_trie[cle] - occ_min)/(occ_max - occ_min))


    t_format = {}
    for cle in ingredient_poid:
        t_format[cle] = ingredient_poid[cle]

    with open('ingredient.json', "w", encoding='UTF-8') as file:
        json.dump(t_format, file, indent=4)

Ingredients_Poids(datas)

types = {}
for lst in Data:
    if lst[1] not in types:
        types[lst[1]] = lst[5]
    else:
        for i in lst[5]:
            if i not in types[lst[1]]:
                types[lst[1]].append(i.lower())

with open('types.json', "w", encoding='UTF-8') as file:
    json.dump(types, file, indent=4)