from flask import Blueprint, render_template,request, redirect, url_for, session as sess, jsonify
from app.Entities.user import User

auth = Blueprint('auth', __name__)

@auth.route('/inscription', methods=["POST", "GET"])
def inscription():

    if request.method == "POST":
        donnees = request.form
        nom = donnees['nom']
        sex = request.form.get('sex')
        email = donnees['email']
        password = donnees['password']

        user = User(nom, sexe = sex, email = email, password=password)
        user.Add_user()
        if 'nom_user' not in sess:
            sess.permanent = True
            sess['nom_user'] = nom
            sess['id'] = user.Get_id()

        return redirect(url_for('auth.next'))
    return render_template('inscription.html')

@auth.route('/inscription-suite', methods=["POST", "GET"])
def next():

    if request.method == "POST":
        donnees = request.form
        tel = donnees['tel']
        anneeNaiss = donnees['anneeNaiss']
        user = User(tel = tel, anneeNaiss= anneeNaiss)
        user.Update(sess['id'])

        message = "Incription Terminée"

        return redirect(url_for('index'))
    return render_template('next.html')


@auth.route('/connexion', methods=["POST", "GET"])
def connexion():

    if request.method == "POST":
        donnees = request.form
        nom = donnees['nom']
        password = donnees['password']

        user = User(nom, password = password)

        message = f"Connecté avec Succes"

        if user.Connexion():
            sess.permanent = True
            sess['nom_user'] = nom
            sess['id_user'] = user.Get_id()
            return redirect(url_for('sucess', message = message, route = 'index'))
        else:
            return redirect(request.url)
        
    else:
        
        return render_template('connection.html')
    

@auth.route('/logout')
def logout():
    sess.pop('nom_user', None)
    return redirect(url_for('index'))
    