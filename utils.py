from datetime import datetime
from models import Worker
import base
import requests

sess = base.create_session()
d1 = datetime.now().date()


def get_flags(companies):
    flags = []
    for company in companies:
        workers = sess.query(Worker).filter(Worker.company_pib == company.pib).all()
        if workers:
            delta = []
            for worker in workers:
                if worker.contract_termination_date is not None:
                    d2 = worker.contract_termination_date
                    delta.append(abs((d2 - d1).days))
            m = min(delta)
            if m < 10:
                flags.append(['red', m])
            elif m < 31:
                flags.append(['yellow', m])
            else:
                flags.append(['green', m])
        else:
            flags.append(['gray', ''])
    return flags

api_base_url = "https://api.mailgun.net/v3/sandboxe94e5d92baf94b42a378e412c3b5e8df.mailgun.org"
api_key = "key-f0ae9a300f4090e6826868072e1cf7a3"

def send_email(vreme, ime_firme, radnici, url):
    return requests.post(
        f"{api_base_url}/messages",
        auth=("api", api_key),
        data={"from": "obavestenje@mojradnik.com",
              "to": ["bogdanbokipaunovic@gmail.com"],
              "subject": f"",
              "text": f"{url}"})

send_email(7, 'AUTO SHOP', 'Nemanja Dojcinovic', 'http://127.0.0.1:8081/radnici/712712831/AUTO%20SHOP')