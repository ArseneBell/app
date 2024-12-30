from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,text, Table, DateTime,func
from sqlalchemy.orm import sessionmaker, relationship
import sqlalchemy.exc
from app.Entities.connexion import *


class User(Base):
    def __init__(self, nom = '', anneeNaiss = 0, sexe = '', email = '', tel = '', password = '', statut = 'user', preferences = 'none'):
        self.nom = nom
        self.anneeNaiss = anneeNaiss
        self.sexe = sexe
        self.email= email
        self.tel = tel
        self.preferences = preferences
        self.password = password
        self.statut = statut
        self.Session = sessionmaker(bind = engine)

    __tablename__ = 'Users'
    id = Column('id', Integer, primary_key = True, autoincrement = True)
    nom = Column('nom', String(255))
    anneeNaiss = Column('anneeNaiss', Integer)
    sexe = Column('sexe', String(255))
    tel = Column('tel', String(255))
    email = Column('email', String(255))
    preferences = Column('preferences', String(255), nullable = True)
    password = Column('mot_de_pass', String(255), nullable = True)
    statut = Column('status', String(255), nullable = True)


    def SearchUser(self):
        session = self.Session()
        result = session.query(User).filter(User.nom == self.nom and User.email == self.email and User.statut == self.statut).first()
        session.commit()

        if result == None:
            return False
        return True
    
    def Get_id(self):
        session = self.Session()
        result = session.query(User).filter(User.nom == self.nom and User.email == self.email and User.password == self.password).first()
        session.commit()
        return result.id
    
    def Update(self, id):
        session = self.Session()
        result = session.query(User).filter(User.id == id).first()
        if result != None:
            if self.nom != '':
                result.nom = self.nom
            if self.anneeNaiss != 0:
                result.anneeNaiss = self.anneeNaiss
            if self.email != '':
                result.email = self.email
            if self.sexe != '':
                result.sexe != self.sexe
            if self.password != '':
                result.password = self.password
            if self.tel != '':
                result.tel = self.tel
            if self.statut != 'user':
                result.statut = self.statut
            if self.preferences != '':
                result.preferences = self.preferences
            session.commit()
            return True
        return False
        

    

    def Connexion(self):
        session = self.Session()
        result = session.query(User).filter(User.nom == self.nom and User.password == self.password).first()
        if result == None:
            return False
        return True

    def Add_user(self):
        if self.SearchUser():
            print('Un utilisateur similaire existe deja')
        else:
            try:
                session = self.Session()
                session.add(self)
                session.commit()
                session.refresh(self)
            except(sqlalchemy.exc.IntegrityError):
                print("Erreur Un tuple avec le meme id existe deja")
        

    def ifAdmin(self):
        if self.statut == 'admin':
            return True
        return False




Base.metadata.create_all(engine)