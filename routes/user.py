from flask import Blueprint, render_template,request, redirect, url_for, session as sess, jsonify
from app.Entities.user import User
from app.Entities.recette import Recettes
from app.fonctions.fonctions import *
import requests

user = Blueprint('user', __name__)

@user.route('/')
def index():
    if 'id' in sess :
        user = SearchUser(int(sess['id']))
        return render_template('user.html', user = user)
    else:
        message = "Veuillez vous connecter avant d'avoir acces a cette fonctionalité"
        return redirect(url_for('sucess', message = message, route = 'auth.connexion'))


@user.route('/update', methods=["POST", "GET"])
def update():
    user = SearchUser(int(sess['id']))
    if request.method == "POST":
        donnees = request.form
        user.nom = donnees['nom']
        user.email = donnees['email']
        user.tel = donnees['tel']
        user.anneeNaiss = donnees['annee']
        users = User(nom = user.nom, anneeNaiss = user.anneeNaiss, sexe = user.sexe, email = user.email, tel = user.tel, password = user.password)
        users.Update(sess['id'])

        message = "Modifié avec success"

        return redirect(url_for('sucess', route='user.index', message=message))
    return redirect(url_for('user.index'))


@user.route('/historique', methods=["POST", "GET"])
def historique():
    url = "http://127.0.0.1:5000/api/historique"
    histo = requests.get(url)
    histo = histo.json()

    his = []
    if 'id' in sess:
        for h in histo:
            if h['id_user'] == sess['id']:
                his.append(h['id_recette'])

    repas = []
    for h in his:
        r = Recettes()
        repas.append(r.Search_recette(int(h)))
    return render_template('historique.html', user = user, repas = repas, url_convert = Url_convert)


@user.route('/favoris', methods=["POST", "GET"])
def favoris():
    url = "http://127.0.0.1:5000/api/favoris"
    fav = requests.get(url)
    fav = fav.json()

    fa = []
    if 'id' in sess:
        for h in fav:
            if h['id_user'] == sess['id']:
                fa.append(h['id_recette'])

    repas = []
    for h in fa:
        r = Recettes()
        repas.append(r.Search_recette(int(h)))
    return render_template('historique.html', user = user, repas = repas, url_convert = Url_convert)