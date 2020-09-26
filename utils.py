from datetime import datetime
from models import Company, Worker
import base

sess = base.create_session()
d1 = datetime.now().date()

def get_flags(companies):
    flags = []
    for company in companies:
        workers = sess.query(Worker).filter(Worker.company_pib == company.pib).all()
        if workers:
            delta = []
            for worker in workers:
                d2 = worker.contract_termination_date
                delta.append(abs((d2 - d1).days))
            m = min(delta)
            if m<10:
                flags.append(['red', m])
            elif m<31:
                flags.append(['yellow', m])
            else:
                flags.append(['green', m])
        else:
            flags.append(['gray', ''])
    return(flags)