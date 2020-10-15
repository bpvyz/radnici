from models import Worker, Company
from base import create_session
from sqlalchemy.exc import IntegrityError
from random import randint
import names
from datetime import datetime, timedelta


def randomize_numbers(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1

    return randint(range_start, range_end)


sess = create_session()


def populate():
    random_pib = randomize_numbers(9)

    try:
        new_company = Company(name='Test', pib=str(random_pib))
        sess.add(new_company)
        sess.flush()
        print('Company added!')
    except IntegrityError:
        sess.rollback()
        print('Firma sa ovim PIB-om vec postoji!')
    else:
        sess.commit()

    for i in range(int(input('How many workers should I populate the "Test" company with?'))):
        now = datetime.now().date()
        term = now + timedelta(days=randint(1, 365))

        try:
            new_worker = Worker(jmbg=str(randomize_numbers(13)), company_pib=str(random_pib),
                                full_name=names.get_full_name(),
                                contract_start_date=datetime.now().date(), contract_termination_date=term)
            sess.add(new_worker)
            sess.flush()
            print('Worker added!')
        except IntegrityError:
            sess.rollback()
            print('Radnik sa ovim JMBG-om vec postoji!')
        else:
            sess.commit()


populate()
