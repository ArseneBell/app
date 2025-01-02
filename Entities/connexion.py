from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,text, Table, DateTime,func,select,PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, relationship
import sqlalchemy.exc


user ='arsene'
password = 'Aomine477%'
host = 'localhost'
port ='3306'
database = 'App'
dbUrl = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine( dbUrl,
                        pool_size=1000,             # Nombre maximum de connexions simultanées
                        max_overflow=2000,          # Connexions supplémentaires au-delà de `pool_size`
                        pool_timeout=30 )

try:
    connection = engine.connect()
    print("Connected to the database")
except sqlalchemy.exc.OperationalError as e:
    print(f"Error connecting to the database: {e}")


Session = sessionmaker(bind = engine)
session = Session()


Base = declarative_base()