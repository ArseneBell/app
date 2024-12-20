from app.Entities.connexion import *

class Recettes(Base):

    __tablename__ = 'recettes'
    id = Column('id', String(255), primary_key = True, nullable = False, autoincrement = True)
    nom = Column('nom', String(255))
    instructions = Column('instructions', String(255))
    image_url = Column('image_url', String(255))
    lien_youtube = Column('lien_youtube', String(255))
    temps_de_cuisson = Column('temps_de_cuisson', String(255))
    type = Column('type', String(255))


    def __init__(self, nom = '', instructions = '', image_url = '', lien_youtube = '', temps_de_cuisson = '', type = ''):
        self.nom = nom
        self.type = type
        self.instructions = instructions
        self.image_url = image_url
        self.lien_youtube = lien_youtube
        self.temps_de_cuisson = temps_de_cuisson
        self.Session = sessionmaker(bind = engine)

    def Readrecettes(self):
        session = self.Session()
        query = select(Recettes)
        session.execute(query)
        results = session.execute(query).scalars().all()
        return results
    
    def Search_recette(self, id):
        session = self.Session()
        result = session.query(Recettes).filter(Recettes.id == id).first()
        return result
    

    def Search_recette_nom(self, nom):
        session = self.Session()
        result = session.query(Recettes).filter(Recettes.nom == nom).first()
        return result
    

    

class Favoris(Base):

    __tablename__ = 'favoris'
    recette_id = Column('id_recette',Integer, ForeignKey('recettes.id'), nullable = False)
    user_id = Column('id_user',Integer, ForeignKey('Users.id'), nullable = False)

    __table_args__ = (
        PrimaryKeyConstraint('id_user','id_recette'),
    )

    def __init__(self, recette_id = 0, user_id = 0):
        self.recette_id = recette_id
        self.user_id = user_id
        self.Session = sessionmaker(bind = engine)

    def Add_favoris(self):
        if not self.Search_favoris():
            session = self.Session()
            session.add(self)
            session.commit()
            session.refresh(self)

    def ReadFavoris(self):
        session = self.Session()
        query = select(Favoris)
        session.execute(query)
        results = session.execute(query).scalars().all()
        return results
    
    def Search_favoris(self):
        session = self.Session()
        result = session.query(Favoris).filter(Favoris.recette_id == self.recette_id and Favoris.user_id == self.user_id).first()
        if result == None:
            return False
        return True