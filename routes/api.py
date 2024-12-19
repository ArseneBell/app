from flask import Blueprint
from app.Entities.recette import *
from app.Entities.ingredient import *
from app.fonctions.fonctions import *
import requests

api = Blueprint('api', __name__)

#API-----------------------------------------

#routes des recettes tels que dans la bd
@api.route('/recettes', methods=['GET'])
def readrecettes():
    r = Recettes()
    session = r.Session()
    query = select(Recettes)
    session.execute(query)
    results = session.execute(query).scalars().all()
    dico_recette = dict_recette(results)
    
    return dico_recette

# route des id rectte et id ingredients
@api.route('/recette_ingredient', methods = ['GET'])
def read_recette_ingredient():
    ri = Recette_ingredients()
    session = ri.Session()
    query = select(Recette_ingredients)
    session.execute(query)
    results = session.execute(query).scalars().all()
    return dict_recette_ingre(results)


#routes des noms recettes et liste d'ingredients
@api.route('/recette_noms_ingredients', methods = ['GET'])
def read_recette_noms_ingredients():

    url = "http://127.0.0.1:5000/api/recettes"
    recette = requests.get(url)
    recette = recette.json()

    url = "http://127.0.0.1:5000/api/recette_ingredient"
    r_i = requests.get(url)
    r_i = r_i.json()

    i = Ingredients()

    rec = {}
    for r in recette:
        for ri in r_i:
            if ri['id_recette'] == r['id']:
                if r['nom'] not in rec:
                    rec[r['nom']] = [r['type']]
                    rec[r['nom']].append(i.Search_nom(ri['id_ingredient']))
                else:
                    if i.Search_nom(ri['id_ingredient']) in rec[r['nom']]:
                        pass
                    else:
                        rec[r['nom']].append(i.Search_nom(ri['id_ingredient']))
    return rec



#routes des types et des ingredients
@api.route('/types', methods = ['GET'])
def read_types():

    url = "http://127.0.0.1:5000/api/recettes"
    recette = requests.get(url)
    recette = recette.json()

    url = "http://127.0.0.1:5000/api/recette_ingredient"
    r_i = requests.get(url)
    r_i = r_i.json()

    i = Ingredients()

    types = {}
    for r in recette:
        for ri in r_i:
            if ri['id_recette'] == r['id']:
                if r['type'] not in types:
                    types[r['type']] = []
                    types[r['type']].append(i.Search_nom(ri['id_ingredient']))
                else:
                    if i.Search_nom(ri['id_ingredient']) in types[r['type']]:
                        pass
                    else:
                        types[r['type']].append(i.Search_nom(ri['id_ingredient']))
    return types


#routes des ingredients tels que dans la bd
@api.route('/ingredients', methods = ['GET'])
def readingredients():
    i = Ingredients()
    session = i.Session()
    query = select(Ingredients)
    session.execute(query)
    results = session.execute(query).scalars().all()
    return dict_ingredient(results)


#route des ingredients et poids
@api.route('/ingredient_poids', methods = ['GET'])
def readingredients_poids():
    i = Ingredients()
    session = i.Session()
    query = select(Ingredients)
    session.execute(query)
    results = session.execute(query).scalars().all()
    return dict_ingredient_poids(results)


#route des favoris
@api.route('/favoris', methods = ['GET'])
def ReadFavoris():
    f = Favoris()
    session = f.Session()
    query = select(Favoris)
    session.execute(query)
    results = session.execute(query).scalars().all()
    return dict_favoris(results)

