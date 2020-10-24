from models import Worker, Company
from base import session
from sqlalchemy.exc import IntegrityError
from random import randint
import names
from datetime import datetime, timedelta


def randomize_numbers(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1

    return randint(range_start, range_end)


def populate():
    random_pib = randomize_numbers(9)

    try:
        new_company = Company(name='Test1', pib=str(random_pib))
        session.add(new_company)
        session.flush()
        print('Company added!')
    except IntegrityError:
        session.rollback()
        print('Firma sa ovim PIB-om vec postoji!')
    else:
        session.commit()

    for i in range(int(input('How many workers should I populate the "Test" company with?'))):
        now = datetime.now().date()
        term = now + timedelta(days=randint(1, 365))

        try:
            new_worker = Worker(jmbg=str(randomize_numbers(13)), company_pib=str(random_pib),
                                full_name=names.get_full_name(),
                                contract_start_date=datetime.now().date(), contract_termination_date=term)
            session.add(new_worker)
            session.flush()
            print('Worker added!')
        except IntegrityError:
            session.rollback()
            print('Radnik sa ovim JMBG-om vec postoji!')
        else:
            session.commit()


populate()
