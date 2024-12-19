import json
import statistics
import csv
from Entities.ingredient import *


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

def score(liste, repas):

    repas = [i.lower() for i in repas]
    liste = [i.lower() for i in liste]

    ingredient = Ingredients()
    score = 0.0
    poids_total = 0.0
    for ingre in liste:
        poids_total += float(ingredient.Search_poids(ingre))
        if ingre in repas:
            score += float(ingredient.Search_poids(ingre))

    print(score)
    score = score/(poids_total)

    return score

def Scoring(liste = ['sel']):

    #Scoring sur les types


    with open('types.json', 'r', encoding='utf-8') as f:
        types = json.load(f)

    types_score = {}

    for cle in types:
        types_score[cle] = score(liste,types[cle])
    
    
    types_score = dict(sorted(types_score.items(), key=lambda x: x[1], reverse=True))
    cle_scores = [[cle,types_score[cle]] for cle in types_score]
    scores = [types_score[cle] for cle in types_score]
    ecart = statistics.stdev(scores)/(len(scores)-1)
    pertinents = [cle_scores[0][0]]
    for i in range(1, len(cle_scores)):
        if cle_scores[i-1][1] - ecart < cle_scores[i][1]:
            pertinents.append(cle_scores[i][0])
        else:
            break


    #Scoring sur les repas

    recette = Recettes()
    recettes = recette.Readrecettes()
    recette_ingredient = Recette_ingredients()
    ingredient = Ingredients()

    ingredients_id = {}
    for r in recettes:
        ingredients_id[r.nom] = recette_ingredient.Search_ingredients(r.id)

    recette_ingredients = {}
    for cle in ingredients_id:
        if cle not in recette_ingredients:
            liste = []
            for ingre in ingredients_id[cle]:
                liste.append(ingredient.Search_nom(ingre))
            recette_ingredients[cle] = liste

    repas_scores = []

    for r in recettes:
        if r.type in pertinents:
            print(r.nom)
            repas_scores.append([r.nom,score(liste, recette_ingredients[r.nom])])

    print(repas_scores)
    

    repas_scores = sorted(repas_scores, key=lambda x: x[1], reverse=True)

    scores = [rps[1] for rps in repas_scores]
    ecart = statistics.stdev(scores)/(len(scores)-1)
    repas_pertinents = [repas_scores[0][0]]
    for i in range(1, len(repas_scores)):
        if repas_scores[i-1][1] - ecart < repas_scores[i][1]:
            repas_pertinents.append(repas_scores[i][0])
        else:
            break

    print(repas_pertinents)



    

Scoring(['sel','persil'])