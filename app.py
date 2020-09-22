from flask import Flask, render_template, request, redirect, make_response, session, url_for
import os
import re
import ast
from datetime import datetime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, MetaData, Table, create_engine

connection_string = 'postgresql://paunzz:PwnOrange1@aa14ovik0da3nng.cfeumv6xw9cy.eu-central-1.rds.amazonaws.com:5432/baza'


eng = create_engine(connection_string)
Base = declarative_base()

metadata = MetaData()
Session = sessionmaker(bind=eng)
sess = Session()

class Company(Base):
    __tablename__ = 'companies'

    pib = Column(String(9), primary_key=True)
    name = Column(String(50), nullable=False)


class Worker(Base):
    __tablename__ = 'workers'

    jmbg = Column(String(13), primary_key=True)
    full_name = Column(String(50), nullable=False)
    contract_start_date = Column(Date)
    contract_termination_date = Column(Date)
    company_pib = Column(String(9), ForeignKey('companies.pib'), nullable=False)
    email_sent = Column(Boolean)
    company = relationship('Company', foreign_keys=[company_pib])

app = Flask(__name__)
data_path = './static/'

@app.route('/', methods=['GET'])
def index():
    companies = sess.query(Company).all()
    return render_template('index.html', dropdown_list=[[n.name, n.pib] for n in companies])


@app.route('/', methods=['POST'])
def company():

    if request.method == 'POST':
        if request.form['submit_button'] == 'company':
            company_name = request.form.get('company_name')
            company_pib = request.form.get('company_pib')
            if company_name != company_pib != '' and re.match(r"\d{9}", company_pib):
                # add to db
                new_company = Company(name=company_name, pib=company_pib)
                sess.add(new_company)
                sess.commit()
                companies = sess.query(Company).all()
                return render_template('index.html', dropdown_list=[[n.name, n.pib] for n in companies])
            else:
                rroute = '/'
                err_code = 'Neispravni podaci firme!'
                return render_template('greska.html', error_code=err_code, redirect_route=rroute)

@app.route('/radnici/<pib>/<company_name>', methods=['POST'])
def open(pib=None, company_name=None):
    print('open')
    if request.form['submit_button'] == 'open':
        print(pib, company_name)
        session['company_name'] = company_name
        session['pib'] = pib

        workers = sess.query(Worker).filter(Worker.company_pib == pib).all()

        return render_template('spisak.html', company=company_name, workers=[worker for worker in workers])

@app.route('/radnik_dodat', methods=['POST'])
def new_worker():
    print('new worker')
    company_name = session.get('company_name')
    pib = session.get('pib')
    if request.method == 'POST':
        if request.form['new_worker'] == 'new_worker':

            worker_jmbg = request.form.get('jmbg')
            worker_full_name = request.form.get('full_name')
            start_date = request.form.get('start_date')
            termination_date = request.form.get('termination_date')

            if start_date and termination_date:
                start_date_object = datetime.strptime(start_date, '%d/%m/%Y')
                termination_date_object = datetime.strptime(termination_date, '%d/%m/%Y')
                worker_start_date = start_date_object.strftime('%Y-%m-%d')
                worker_termination_date = termination_date_object.strftime('%Y-%m-%d')

            if worker_full_name and worker_termination_date and worker_start_date and \
                    re.match(r'\d{13}', worker_jmbg):
                new_worker = Worker(jmbg=worker_jmbg, full_name=worker_full_name,
                                    contract_termination_date=worker_termination_date, contract_start_date=worker_start_date, company_pib=pib)
                sess.add(new_worker)
                sess.commit()
                return render_template('dodat.html')
            else:
                rroute = '/radnici'
                err_code = 'Neispravni podaci radnika!'
                return render_template('greska.html', error_code=err_code, redirect_route=rroute)

@app.route('/radnici', methods=['GET'])
def update():
    print('update')
    company_name = session.get('company_name')
    pib = session.get('pib')
    workers = sess.query(Worker).filter(Worker.company_pib == pib).all()
    return render_template('spisak.html', company=company_name, workers=[worker for worker in workers])

@app.route('/radnici/actions/<action>/<worker_jmbg>', methods=['GET', 'POST'])
def actions(action=None, worker_jmbg=None):
    print('actions')

    def delete_entry(entry):
        sess.delete(entry)
        sess.commit()

    if request.method == "POST":
        if action == 'delete':
            print('delete')
            worker_row_to_delete = sess.query(Worker).filter(Worker.jmbg == worker_jmbg).one()
            delete_entry(worker_row_to_delete)
            return redirect(url_for('update'))

        elif action == 'change':
            return redirect(url_for('update'))
        # elif action == 'renew':
        #     return redirect(url_for('update'))

    elif request.method == "GET":


        return redirect(url_for('update'))

if __name__ == '__main__':
    app.secret_key = '123'
    app.run(port=8081)