from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, create_engine


def create_session():

    connection_string = 'postgresql://USER:PASS@aa14ovik0da3nng.cfeumv6xw9cy.eu-central-1.rds.amazonaws.com:5432/baza'
    eng = create_engine(connection_string)
    Session = sessionmaker(bind=eng)
    sess = Session()

    return(sess)