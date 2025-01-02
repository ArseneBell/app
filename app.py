from flask import Flask, render_template,request, redirect, url_for, session as sess, flash, jsonify
from app.Entities.recette import *
from app.Entities.ingredient import *
from app.Entities.historique import *
from app.fonctions.fonctions import *
from dash import Dash
import requests
from app import create_app
import json


app = create_app()


@app.route('/')
def index():
    url = "http://127.0.0.1:5000/api/recettes"
    recette = requests.get(url)
    recette = recette.json()
    tpe = types_sort(recette)

    url = "http://127.0.0.1:5000/api/favoris"
    fav = requests.get(url)
    fav = fav.json()

    url = "http://127.0.0.1:5000/recommandation"
    rec = requests.get(url)
    rec = rec.json()


    favoris = []
    if 'id' in sess:
        for f in fav:
            if f['id_user'] == sess['id']:
                favoris.append(f['id_recette'])

    recommandation = []   
    for r in rec:
        print(r)
        rc = Recettes()
        recommandation.append(rc.Search_recette(r))
    for r in recommandation:
        print(r.nom)

    return render_template('index.html', types = tpe, url_convert = Url_convert, favoris = favoris, recommandation = recommandation)


@app.route('/repas', methods=["POST", "GET"])
def repas():
    url = "http://127.0.0.1:5000/api/recettes"
    recette = requests.get(url)
    recette = recette.json()
    url = "http://127.0.0.1:5000/api/ingredients"
    ingredient = requests.get(url)
    ingredient = ingredient.json()
    url = "http://127.0.0.1:5000/api/recette_ingredient"
    r_ingre = requests.get(url)
    r_ingre = r_ingre.json()
    url = "http://127.0.0.1:5000/api/vues"
    v = requests.get(url)
    v = v.json()

    with open('vues.json', 'w', encoding='utf-8') as file:
        json.dump(v, file, indent=4, ensure_ascii=False) 

    if request.method == "POST":
        donnees = request.form
        if 'id' in donnees:
            id = donnees['id']
            r = Search_recette(int(id), recette)



        if 'name_repas' in donnees:
            if donnees['name_repas'] == '':
                return redirect(url_for('index'))
            l = Liste_recette(recette)
            name = donnees['name_repas']
            name = closest_string(name, l)
            r = Search_recette(name, recette)
 
        
        nb_vue = int(r['temp_de_cuisson']) +1
        rc = Recettes(temps_de_cuisson = nb_vue)
        rc.Update_vues(r['id'])

        if 'id' in sess:
            h = Historique(recette_id = r['id'], user_id = sess['id'])
            h.Add_Historique()

        r_i = Search_recette_ingre(r['id'], r_ingre)

        ingredients = []
        for identifiant in r_i:
            ingredients.append(Search_nom_ingre(identifiant, ingredient))
        print(ingredients)

    return render_template('repas.html', r = r, convert = convert_instructions, url_convert = Url_convert,youtube = Url_convert_youtube, ingredients = ingredients)


@app.route('/Scoring', methods=["POST", "GET"])
def Scoring():
    if 'nom_user' in sess:
        if request.method == "POST":
            checkboxes = request.form.getlist('ingredients')
            sess['liste_ingredients'] = checkboxes
            return redirect(url_for('scoring.score'))
    else:
        message = "Veuillez vous connecter avant d'avoir acces a cette fonctionalité"
        return redirect(url_for('sucess', message = message, route = 'auth.connexion'))
    return render_template('select.html', current_route = request.path)


    

@app.route('/succes/<string:message>/<string:route>')
def sucess(message, route):
    flash(f"{message}", 'success')
    return redirect(url_for(f'{route}'))

@app.route('/erreur/<string:message>/<string:route>')
def erreur(message, route):
    flash(f"{message}", 'danger')
    return redirect(url_for(f'{route}'))

@app.route('/favoris', methods=["POST", "GET"])
def favoris():
    if request.method == "POST":
        data = request.get_json()
        repas = data.get('repas')
        user = data.get('user')
        print(f"user = {user}")
        f = Favoris(int(repas), int(user))
        if not f.Search_favoris():
            f.Add_favoris()
            m = 'favoris ajouté'
        else:
            f.Del_favoris()
            m = 'favoris supprimé'
    return jsonify({"success": True, "message": m})    


if __name__ == '__main__':
    app.run(debug=True)