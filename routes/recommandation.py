import pandas as pd
import numpy as np
from scipy.linalg import svd
from sqlalchemy import create_engine
from flask import Blueprint, request, jsonify, session as sess, redirect,url_for

recommandation = Blueprint('recommandation', __name__)

# Connexion à la base de données
def connecter_bd():
    moteur = create_engine("mysql+pymysql://arsene:Aomine477%@localhost/App")
    return moteur

def charger_toutes_les_recettes():
    moteur = connecter_bd()
    requete_recettes = "SELECT DISTINCT id FROM recettes;"
    toutes_les_recettes = pd.read_sql(requete_recettes, moteur)['id'].values
    return toutes_les_recettes


# Charger les données de l'historique et des favoris d'un utilisateur
def charger_donnees_utilisateur(utilisateur_id):
    moteur = connecter_bd()
    
    # Requête pour extraire l'historique des recherches
    requete_historique = f"""
        SELECT utilisateur_id, recette_id 
        FROM Historique 
        WHERE utilisateur_id = {utilisateur_id};
    """
    historique_recherche = pd.read_sql(requete_historique, moteur)
    
    # Requête pour extraire les favoris
    requete_favoris = f"""
        SELECT id_user AS utilisateur_id, id_recette AS recette_id 
        FROM favoris 
        WHERE id_user = {utilisateur_id};
    """
    favoris = pd.read_sql(requete_favoris, moteur)
    
    # Vérification des données
    if historique_recherche.empty:
        raise ValueError("L'historique de recherche est vide pour cet utilisateur.")
    if favoris.empty:
        raise ValueError("Les favoris sont vides pour cet utilisateur.")
    
    return historique_recherche, favoris

def creer_matrice_interaction(historique_recherche, favoris, toutes_les_recettes):
    # Récupérer tous les utilisateurs
    utilisateurs = historique_recherche['utilisateur_id'].unique()
    
    # Initialiser la matrice d'interaction avec tous les utilisateurs et toutes les recettes
    R = pd.DataFrame(0, index=utilisateurs, columns=toutes_les_recettes)
    
    # Ajouter les interactions (1 pour les vues ou favoris)
    for _, row in historique_recherche.iterrows():
        R.at[row['utilisateur_id'], row['recette_id']] = 1
    for _, row in favoris.iterrows():
        R.at[row['utilisateur_id'], row['recette_id']] = 1
    
    # Vérification : Afficher la matrice construite
    print("Matrice d'interaction R après construction avec toutes les recettes :")
    print(R)
    
    return R



def bi_diagonalisation(R):
    R_np = R.values
    U, S, Vt = svd(R_np, full_matrices=False)
    W = np.dot(U, np.diag(S))  # Matrice utilisateur
    Z = np.dot(np.diag(S), Vt)  # Matrice plats
    return W, Z

import random

def recommander_menus(W, Z, utilisateur_id, R, top_n=6):
    predictions = np.dot(W, Z)
    predictions_df = pd.DataFrame(predictions, index=R.index, columns=R.columns)
    
    # Identifier les recettes non vues
    recettes_non_vues = R.columns[R.loc[utilisateur_id] == 0]  # Colonnes avec 0 pour cet utilisateur
    print("Recettes non vues :", recettes_non_vues)
    
    if len(recettes_non_vues) == 0:
        print(f"Aucune recette non vue pour l'utilisateur {utilisateur_id}.")
        return []
    
    # Mélanger les recettes non vues de manière aléatoire
    recettes_non_vues = list(recettes_non_vues)
    random.shuffle(recettes_non_vues)
    
    # Limiter au top_n pour retourner un sous-ensemble aléatoire
    recommandations = recettes_non_vues[:top_n]
    print(f"Recommandations aléatoires pour l'utilisateur {utilisateur_id} :", recommandations)
    
    return recommandations






# API pour obtenir les recommandations de menus pour un utilisateur
@recommandation.route('/', methods=['GET','POST'])
def index(utilisateur_id=1):
    if 'id' in sess:
        utilisateur_id=int(sess['id'])
    historique_recherche, favoris = charger_donnees_utilisateur(utilisateur_id)
    toutes_les_recettes = charger_toutes_les_recettes()
    R = creer_matrice_interaction(historique_recherche, favoris, toutes_les_recettes)
    W, Z = bi_diagonalisation(R)
    
    # Récupérer plusieurs menus recommandés
    repas_recommandes = recommander_menus(W, Z, utilisateur_id, R, top_n=5)  # Top 5 menus
    return jsonify(repas_recommandes)






