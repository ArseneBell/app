from flask import Blueprint, redirect
from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import json

# Créer un Blueprint pour le tableau de bord
dashboard = Blueprint('dashboard', __name__)

def create_dashboard(server):
    app = Dash(__name__, server=server, url_base_pathname='/dashboard/')

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


    def load_data():
        """Lire et charger les données depuis le fichier JSON."""
        with open('vues.json', 'r', encoding='utf-8') as file:
            vues = json.load(file)
        nb_vues = []
        types = []
        for v in vues:
            types.append(v)
            nb_vues.append(vues[v])

        data_pie = pd.DataFrame({
            "Catégorie": types,
            "Valeur": nb_vues
        })

        return data_pie
    
    data_curve = pd.DataFrame({
        "Jour": [1, 2, 3, 4, 5, 6, 7],
        "Valeur A": [10, 7, 3, 9, 15, 12, 17],
        "Valeur B": [20, 25, 21, 20, 27, 31, 29]
    })

    data_scatter = pd.DataFrame({
        "X": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        "Y": [15, 25, 35, 45, 55, 65, 75, 85, 95, 105],
        "Catégorie": ["A", "A", "B", "B", "C", "C", "D", "D", "E", "E"]
    })

    app.layout = html.Div([
        html.H1("Dashboard Interactif", className='text-center my-4'),

        # Ligne 1 : Graphique en barres + Diagramme camembert
        html.Div([
            html.Div([
                html.H3("Graphique des repas favoris", className="mb-3"),
                dcc.Input(
                    id='input-age',
                    type='number',
                    placeholder='Entrez un âge',
                    className='form-control mb-3'
                ),
                html.Button("Entrer", id='submit-button', n_clicks=0, className='btn btn-primary mb-3'),
                dcc.Graph(id='graph-repas-favoris', style={'height': '400px'}),
            ], className="col-md-6 col-sm-12 mb-4"),

            html.Div([
                html.H3("Vues en fonction des Types", className="mb-3"),
                dcc.Dropdown(
                    id='category-dropdown',
                    multi=True,
                    className='form-select'
                ),
                dcc.Graph(id='pie-chart', style={'height': '400px'}),
            ], className="col-md-6 col-sm-12 mb-4")
        ], className="row"),

        # Ligne 2 : Nuage de points + Diagramme de courbe
        html.Div([

            html.Div([
                html.H3("Diagramme de Courbe", className="mb-3"),
                dcc.Dropdown(
                    id='curve-metric-dropdown',
                    options=[
                        {"label": "Valeur A", "value": "Valeur A"},
                        {"label": "Valeur B", "value": "Valeur B"}
                    ],
                    value="Valeur A",
                    className='form-select'
                ),
                dcc.Graph(id='curve-chart', style={'height': '400px'}),
            ], className="col-12 col-md-6  mb-4")
        ], className="row")
    ], className="container")

    @app.callback(
        [Output('category-dropdown', 'options'),
         Output('pie-chart', 'figure')],
        Input('category-dropdown', 'value')
    )
    def update_pie_chart(selected_categories):
        # Charger les données depuis le fichier JSON
        data_pie = load_data()
        options = [{"label": cat, "value": cat} for cat in data_pie["Catégorie"]]

        if not selected_categories:
            selected_categories = data_pie["Catégorie"].tolist()

        filtered_data = data_pie[data_pie["Catégorie"].isin(selected_categories)]
        fig = px.pie(
            filtered_data,
            names='Catégorie',
            values='Valeur',
            title="Répartition des Vues par Types"
        )
        return options, fig

    @app.callback(
        Output('graph-repas-favoris', 'figure'),
        Input('submit-button', 'n_clicks'),
        State('input-age', 'value')
    )
    def update_bar_chart(n_clicks, age):
        if n_clicks == 0 or age is None:
            return px.bar(title="Veuillez entrer un âge pour voir les résultats.")

        data = pd.DataFrame({})  # Remplacez avec une requête pour vos données
        if data.empty:
            return px.bar(title=f"Aucun résultat trouvé pour l'âge {age}.")

        fig = px.bar(
            data,
            x='type_repas',
            y='nombre_favoris',
            color='sexe',
            title=f"Types de repas favoris pour l'âge {age}",
            labels={'type_repas': 'Type de repas', 'nombre_favoris': 'Nombre de favoris'}
        )
        return fig
    
    @app.callback(
        Output('scatter-chart', 'figure'),
        Input('scatter-category-dropdown', 'value')
    )
    def update_scatter(selected_category):
        if not selected_category:
            return px.scatter(title="Aucune catégorie sélectionnée")

        filtered_data = data_scatter[data_scatter["Catégorie"] == selected_category]
        fig = px.scatter(
            filtered_data,
            x='X',
            y='Y',
            title=f"Nuage de points pour la catégorie {selected_category}",
            labels={'X': 'Variable X', 'Y': 'Variable Y'},
            color_discrete_sequence=['blue']
        )
        return fig
    

    @app.callback(
        Output('curve-chart', 'figure'),
        Input('curve-metric-dropdown', 'value')
    )
    def update_curve(selected_metric):
        if not selected_metric:
            return px.line(title="Aucune métrique sélectionnée")

        fig = px.line(
            data_curve,
            x='Jour',
            y=selected_metric,
            title=f"Évolution de {selected_metric} au fil des jours",
            labels={'Jour': 'Jour', selected_metric: 'Valeur'}
        )
        return fig

    return app

@dashboard.route('/dashboard/')
def redirect_dashboard():
    return redirect('/dashboard/')
