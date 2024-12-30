from app.Entities.recette import *

class Ingredients(Base):

    __tablename__ = 'ingredients'
    id = Column('id', String(255), primary_key = True, nullable = False, autoincrement = True)
    nom = Column('nom', String(255))
    poids = Column('poids', String(255))


    def __init__(self, nom = '', poids = ''):
        self.nom = nom
        self.poids = poids
        self.Session = sessionmaker(bind = engine)

    def Readingredients(self):
        session = self.Session()
        query = select(Ingredients)
        session.execute(query)
        results = session.execute(query).scalars().all()
        return results
    
    def Search_nom(self, ingre_id):
        session = self.Session()
        result = session.query(Ingredients).filter(Ingredients.id == ingre_id).first()
        return result.nom
    
    def Search_poids(self, nom):
        session = self.Session()
        result = session.query(Ingredients).filter(Ingredients.nom == nom).first()
        session.commit()
        if result:
            return result.poids
        return 0
    

class Recette_ingredients(Base):
    __tablename__ = 'recette_ingredients'
    recette_id = Column('recette_id',Integer, ForeignKey('recettes.id'), nullable = False)
    ingredient_id = Column('ingredient_id',Integer, ForeignKey('ingredients.id'), nullable = False)
    quantite = Column('quantite', String(255))


    __table_args__ = (
        PrimaryKeyConstraint('recette_id', 'ingredient_id'),
    )

    def __init__(self, recette_id = 0, ingredient_id = 0, quantite = ''):
        self.recette_id = recette_id
        self.ingredient_id = ingredient_id
        self.quantite = quantite
        self.Session = sessionmaker(bind = engine)


    def Read(self):
        session = self.Session()
        query = select(Recette_ingredients)
        session.execute(query)
        results = session.execute(query).scalars().all()
        return results
    
    def Search_ingredients(self, r_id):
        session = self.Session()
        result = session.query(Recette_ingredients).filter(Recette_ingredients.recette_id == r_id)

        ingredient_id = []
        for r in result:
            ingredient_id.append(r.ingredient_id)

        return ingredient_id
    


