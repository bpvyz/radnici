from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

user = os.environ['dbuser']
password = os.environ['dbpass']


def create_session():
    connection_string = f'postgresql://{user}:{password}@aa14ovik0da3nng.cfeumv6xw9cy.eu-central-1.rds.amazonaws.com:5432/baza'
    eng = create_engine(connection_string)
    Session = sessionmaker(bind=eng)
    sess = Session()

    return sess
