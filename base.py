from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = 'postgresql://postgres:123@localhost/'

eng = create_engine(DATABASE_URL)
Session = sessionmaker(bind=eng)
session = Session()
