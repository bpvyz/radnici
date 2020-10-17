import requests
from base import session
from models import Worker, Company
from datetime import datetime
import os

MAILGUN_BASE_URL = os.environ['MAILGUN_BASE_URL']
MAILGUN_KEY = os.environ['MAILGUN_KEY']
d1 = datetime.now().date()


def get_email_list():
    workers = session.query(Worker).all()
    worker_list = []
    for worker in workers:
        if worker.contract_termination_date is not None:
            company_name = session.query(Company).filter(Company.pib == worker.company_pib).one().name

            d2 = worker.contract_termination_date
            time_left = abs((d2 - d1).days)
            if time_left <= 7:
                url = f"{os.environ['SERVER_URL']}/radnici/{worker.company_pib}"
                worker_list.append({'JMBG': worker.jmbg,
                                    'full_name': worker.full_name,
                                    'company_name': company_name,
                                    'time_left': time_left,
                                    'url': url
                                    })
    return worker_list


def send_email(worker_list):
    n = len(worker_list)
    if n > 0:
        return requests.post(
            f"{MAILGUN_BASE_URL}/messages",
            auth=("api", MAILGUN_KEY),
            data={"from": "obavestenje@mojradnik.com",
                  "to": ["agencijapapiri@gmail.com", "bogdanbokipaunovic@gmail.com"],
                  "subject": f"Obavestenje, {n} radnik/a pred istekom ugovora",
                  "text": [f"{worker['JMBG']}, "
                           f"{worker['full_name']}, "
                           f"{worker['company_name']}, "
                           f"{worker['time_left']} dan/a, "
                           f"{worker['url']}" for worker in worker_list]
                  })
    return "Terminating process due to empty mailing list!"


send_email(get_email_list())
