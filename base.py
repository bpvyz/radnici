from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

DATABASE_URL = os.environ['DATABASE_URL']

eng = create_engine(DATABASE_URL)
Session = sessionmaker(bind=eng)
session = Session()
