from flask import Blueprint, redirect, render_template
from dash import Dash, dcc, html
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
    app = Dash(__name__, server=server, url_base_pathname='/dashboard/')
    
    # Chargement des données (fonction)
    def get_favorite_data(age):
        query = """
        SELECT 
            u.anneeNaiss AS age,
            u.sexe,
            r.type AS type_repas,
            COUNT(r.id) AS nombre_favoris
        FROM 
            favoris f
        JOIN 
            Users u ON f.user_id = u.id
        JOIN 
            recettes r ON f.recette_id = r.id
        WHERE 
            YEAR(CURDATE()) - u.anneeNaiss = %s
        GROUP BY 
            u.sexe, r.type
        ORDER BY 
            nombre_favoris DESC;
        """
        return pd.read_sql(query, engine, params=(age,))

    # Mise en page du tableau de bord
    app.layout = html.Div([
        dcc.Input(id='input-age', type='number', placeholder='Entrez un âge'),
        dcc.Graph(id='graph-repas-favoris')
    ])

    # Callback pour mettre à jour le graphique
    @app.callback(
        Output('graph-repas-favoris', 'figure'),
        Input('input-age', 'value')
    )
    def update_graph(age):
        if age is None:
            return px.bar(title="Veuillez entrer un âge pour voir les résultats.")
        
        data = get_favorite_data(age)
        fig = px.bar(data, x='type_repas', y='nombre_favoris', color='sexe',
                     title=f"Types de repas favoris pour l'âge {age}")
        return fig

    return app

# Route pour rediriger vers Dash (optionnelle)
@dashboard.route('/dashboard/')
def redirect_dashboard():
    return redirect('/dashboard/')
