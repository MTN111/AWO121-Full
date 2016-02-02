import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
'''

USER_NAME = 'nikita'
USER_PASSWORD = 'p@ssword'
HOST = '52.28.72.197'
PORT = 8060

engine = create_engine("postgresql+psycopg2://{0}:{1}@{2}:{3}/social_data".format(
							USER_NAME, USER_PASSWORD, HOST, PORT), echo=False)
'''
# config contstraints for postgresql connection
host = 'localhost'
user = 'roman'
password = '12345'
db_name = 'social_data'

# estabilishing connections
engine = create_engine("postgresql+psycopg2://{0}:{1}@{2}/{3}".format(user, password, host, db_name), echo=False)

Base = declarative_base()


session = sessionmaker(bind=engine)()

Base.metadata.create_all(engine)
