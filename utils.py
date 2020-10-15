from datetime import datetime
from models import Worker
import base

sess = base.create_session()
now = datetime.now().date()


def get_flags(companies):

    flags = []

    for company in companies:

        workers = sess.query(Worker).filter(Worker.company_pib == company.pib).all()

        minimum_delta = None

        for worker in workers:
            if worker.contract_termination_date is not None:
                delta = abs((worker.contract_termination_date - now).days)
                if minimum_delta is None or delta < minimum_delta:
                    minimum_delta = delta

        if minimum_delta is None:
            flags.append(['gray', ''])
        elif minimum_delta < 10:
            flags.append(['red', minimum_delta])
        elif minimum_delta < 31:
            flags.append(['yellow', minimum_delta])
        else:
            flags.append(['green', minimum_delta])

    return flags
