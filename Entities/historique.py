from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,text, Table, DateTime,func, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, relationship
import sqlalchemy.exc
from app.Entities.connexion import *
from datetime import datetime


class Historique(Base):

    __tablename__ = 'Historique'
    recette_id = Column('recette_id',Integer, ForeignKey('recettes.id'), nullable = False)
    user_id = Column('utilisateur_id',Integer, ForeignKey('Users.id'), nullable = False)
    date = Column('date',DateTime, nullable = False)
    id = Column('id', Integer, primary_key = True, nullable = False, autoincrement = True)


    def __init__(self, recette_id = 0, user_id = 0):
        self.recette_id = recette_id
        self.user_id = user_id
        self.date = datetime.now()
        self.Session = sessionmaker(bind = engine)

    def Add_Historique(self):
        session = self.Session()
        session.add(self)
        session.commit()
        session.refresh(self)

    def Read_Historique_User(self):
        session = self.Session()
        result = session.query(Historique).filter(Historique.recette_id == self.recette_id and Historique.user_id == self.user_id)
        return result
    
    def Read_Historique(self):
        session = self.Session()
        result = session.query(Historique)
        return result
    
    def Search_Historique(self):
        session = self.Session()
        result = session.query(Historique).filter(Historique.recette_id == self.recette_id and Historique.user_id == self.user_id).first()
        if result == None:
            return False
        return True

