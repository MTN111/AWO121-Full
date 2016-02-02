
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

DB_HOST = 'localhost'
DB_USER = 'roman'
DB_PASSWORD = '12345'
DB_NAME = 'social_data'

engine = create_engine("postgresql+psycopg2://{0}:{1}@{2}/social_data".format(
							DB_USER, DB_PASSWORD, DB_HOST, DB_NAME), echo=False)

Base = declarative_base()

session = sessionmaker(bind=engine)()

