from Entities.connexion import engine
import pandas as pd

def test_sql(age):
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
    data = pd.read_sql(query, engine, params=(age,))
    print(data)

test_sql(20)  # Remplace 19 par un âge réel
