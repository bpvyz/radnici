from sqlalchemy import Column, String, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    pib = Column(String(9), primary_key=True)
    name = Column(Text, nullable=False)


class Worker(Base):
    __tablename__ = 'workers'

    jmbg = Column(String(13), primary_key=True)
    full_name = Column(String(50), nullable=False)
    contract_start_date = Column(Date)
    contract_termination_date = Column(Date, nullable=True)
    company_pib = Column(String(9), ForeignKey('companies.pib'), nullable=False)
    email_sent = Column(Boolean)
    company = relationship('Company', foreign_keys=[company_pib])