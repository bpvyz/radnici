from datetime import datetime

from base import session
from models import Worker

now = datetime.now().date()


def get_flags(companies):
    flags = []

    for company in companies:

        workers = session.query(Worker).filter(Worker.company_pib == company.pib).all()

        minimum_delta = None

        for worker in workers:
            if worker.contract_termination_date is not None:
                delta = abs((worker.contract_termination_date - now).days)
                if minimum_delta is None or delta < minimum_delta:
                    minimum_delta = delta

        if minimum_delta is None:
            flags.append(['gray', ''])
        elif minimum_delta < 10:
            flags.append(['#FF1744', minimum_delta])
        elif minimum_delta < 31:
            flags.append(['#FFEA00', minimum_delta])
        else:
            flags.append(['#66BB6A', minimum_delta])

    return flags
