from flask import Blueprint, session as sess, request, redirect, url_for, render_template
import requests
import json
import statistics
import csv
import math
from app.Entities.recette import Recettes
from app.fonctions.fonctions import Url_convert

scoring = Blueprint('scoring', __name__)

def score_repas(liste, repas, ingredients):

    repas = [i.lower() for i in repas]
    liste = [i.lower() for i in liste]

    score = 0
    poids_total = 0
    for ingre in liste:
        if ingre in ingredients:
            poids_total += float(ingredients[ingre])
            if ingre in repas:
                score += float(ingredients[ingre])
    if poids_total != 0:
        score = score/(poids_total)
    else:
        score = 0

    return score

def Scoring(liste = ['sel'], types={}, r_i = {}, ingredients = {}):

    #Scoring sur les types
    types_score = {}

    for cle in types:
        types_score[cle] = score_repas(liste, types[cle], ingredients)
    
    
    types_score = dict(sorted(types_score.items(), key=lambda x: x[1], reverse=True))
    cle_scores = [[cle,types_score[cle]] for cle in types_score]
    scores = [types_score[cle] for cle in types_score]
    if len(scores) == 1:
        ecart = 100
    else:
        ecart = statistics.stdev(scores)/(len(scores)-1)
    pertinents = [cle_scores[0][0]]
    for i in range(1, len(cle_scores)):
        if cle_scores[i-1][1] - ecart < cle_scores[i][1]:
            pertinents.append(cle_scores[i][0])
        else:
            break


    #Scoring sur les repas

    repas_scores = []

    for r in r_i:
        if r_i[r][0] in pertinents:
            repas_scores.append([r, score_repas(liste, r_i[r][0:], ingredients)])

    repas_scores = sorted(repas_scores, key=lambda x: x[1], reverse=True)

    scores = [rps[1] for rps in repas_scores]
    if len(scores) == 1:
        ecart = 100
    else:
        ecart = statistics.stdev(scores)/(len(scores)-1)
    repas_pertinents = [repas_scores[0][0]]
    for i in range(1, len(repas_scores)):
        if repas_scores[i-1][1] - ecart < repas_scores[i][1]:
            repas_pertinents.append(repas_scores[i][0])
        else:
            break
    return repas_pertinents


    

#Scoring(['tomate','oignon','sel'])

@scoring.route('/score', methods=["POST", "GET"])
def score():
    url = "http://127.0.0.1:5000/api/types"
    types = requests.get(url)
    types = types.json()
    url = "http://127.0.0.1:5000/api/ingredient_poids"
    ingredient = requests.get(url)
    ingredient = ingredient.json()
    url = "http://127.0.0.1:5000/api/recette_noms_ingredients"
    r_ingre = requests.get(url)
    r_ingre = r_ingre.json()

    if request.method == "POST":
        checkboxes = request.form.getlist('ingredients')
        repas = Scoring(checkboxes, types, r_ingre, ingredient)
        print(repas)
        if repas == None:
            repas = []
        r = Recettes()
        rep = []
        for rp in repas:
            rp = r.Search_recette_nom(rp)
            rep.append(rp)
    return render_template('select.html', current_route = request.path, Repas = rep, url_convert = Url_convert)

    
