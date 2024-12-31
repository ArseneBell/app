from flask import Blueprint, redirect, render_template
from dash import Dash, dcc, html,State
#import dash_core_components as dcc
#import dash_html_components as html
from dash.dependencies import Input, Output
from app.Entities.connexion import engine  # Connexion à la BD
import pandas as pd
import plotly.express as px

# Créer un Blueprint pour le tableau de bord
dashboard = Blueprint('dashboard', __name__)

# Intégrer Dash dans Flask
def create_dashboard(server):
    # Création d'une instance Dash liée au serveur Flask
    app = Dash(__name__, server=server, url_base_pathname='/dashboard/')

    # Fonction pour récupérer les données à partir de la base de données
    def get_favorite_data(age):
        try:
            print(f"Exécution de la requête SQL pour l'âge : {age}")  # Log de l'âge
            query = """
            SELECT 
                u.anneeNaiss AS age,
                u.sexe,
                r.type AS type_repas,
                COUNT(r.id) AS nombre_favoris
            FROM 
                favoris f
            JOIN 
                Users u ON f.id_user = u.id
            JOIN 
                recettes r ON f.id_recette = r.id
            WHERE 
                YEAR(CURDATE()) - u.anneeNaiss = %s
            GROUP BY 
                u.sexe, r.type
            ORDER BY 
                nombre_favoris DESC;
            """
            # Exécuter la requête avec l'âge converti en entier
            data = pd.read_sql(query, engine, params=(int(age),))
            print(f"Données récupérées :\n{data}")  # Log des données
            return data
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête SQL : {e}")
            return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur

    # Mise en page du tableau de bord
    app.layout = html.Div([
        html.H1("Dashboard des repas favoris par âge", style={'text-align': 'center'}),
        html.Div([
            dcc.Input(
                id='input-age',
                type='number',
                placeholder='Entrez un âge',
                style={'margin-right': '10px'}
            ),
            html.Button("Entrer", id='submit-button', n_clicks=0)
        ], style={'text-align': 'center', 'margin-bottom': '20px'}),
        dcc.Graph(id='graph-repas-favoris')
    ])

    # Callback pour mettre à jour le graphique après soumission
    @app.callback(
        Output('graph-repas-favoris', 'figure'),
        Input('submit-button', 'n_clicks'),
        State('input-age', 'value')
    )
    def update_graph(n_clicks, age):
        print(f"Callback déclenché : n_clicks={n_clicks}, age={age}")  # Log pour débogage

        if n_clicks == 0 or age is None:
            # Affiche un graphique vide avant que l'utilisateur n'entre un âge
            return px.bar(title="Veuillez entrer un âge pour voir les résultats.")

        # Récupération des données depuis la base
        data = get_favorite_data(age)

        if data.empty:
            print(f"Aucun résultat trouvé pour l'âge {age}.")  # Log pour débogage
            return px.bar(title=f"Aucun résultat trouvé pour l'âge {age}.")

        # Création du graphique avec les données récupérées
        fig = px.bar(
            data,
            x='type_repas',
            y='nombre_favoris',
            color='sexe',
            title=f"Types de repas favoris pour l'âge {age}",
            labels={'type_repas': 'Type de repas', 'nombre_favoris': 'Nombre de favoris'}
        )
        return fig

    return app

# Route Flask pour rediriger vers le tableau de bord Dash
@dashboard.route('/dashboard/')
def redirect_dashboard():
    return redirect('/dashboard/')