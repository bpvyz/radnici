import datetime
import re
from datetime import datetime

from flask import render_template, request, redirect, session as flask_session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError

import utils
from base import session
from models import Worker, Company

radnici = Blueprint('radnici', __name__)


@radnici.route('/', methods=['GET'])
def index():
    companies = session.query(Company).all()
    flags = utils.get_company_flags(companies)
    return render_template('index.html', list=[[n.name, n.pib, flag] for (n, flag) in zip(companies, flags)])


@radnici.route('/', methods=['POST'])
def company():
    if request.method == 'POST':
        if request.form['submit_button'] == 'company':
            company_name = request.form.get('company_name')
            company_pib = request.form.get('company_pib')
            if company_name != company_pib != '' and re.match(r"\d{9}", company_pib):
                try:
                    new_company = Company(name=company_name, pib=company_pib)
                    session.add(new_company)
                    session.flush()
                except IntegrityError:
                    session.rollback()
                    rroute = '/'
                    err_code = 'Firma sa ovim PIB-om vec postoji!'
                    return render_template('greska.html', error_code=err_code, redirect_route=rroute)

                session.commit()
                companies = session.query(Company).all()
                flags = utils.get_company_flags(companies)
                return render_template('index.html',
                                       list=[[n.name, n.pib, flag] for (n, flag) in zip(companies, flags)])
            else:
                rroute = '/'
                err_code = 'Neispravni podaci firme!'
                return render_template('greska.html', error_code=err_code, redirect_route=rroute)


@radnici.route('/radnici/<pib>', methods=['POST', 'GET'])
def open(pib=None):
    if request.method == 'GET' or request.form['submit_button'] == 'open':
        flask_session['pib'] = pib
        workers = session.query(Worker).filter(Worker.company_pib == pib).all()
        company = session.query(Company).filter(Company.pib == pib).one()
        flags = utils.get_worker_flags(workers)
        return render_template('spisak.html', workers=[[worker, flag] for (worker, flag) in zip(workers,flags)], company=company.name)

    elif request.form['submit_button'] == 'delete':

        session.query(Company).filter(Company.pib == pib).delete()

        session.commit()

        return redirect(url_for('radnici.index'))


@radnici.route('/radnik_dodat', methods=['POST'])
def new_worker():
    pib = flask_session.get('pib')
    if request.method == 'POST':
        if request.form['new_worker'] == 'new_worker':
            worker_jmbg = request.form.get('jmbg')
            worker_full_name = request.form.get('full_name')
            start_date = request.form.get('start_date')
            termination_date = request.form.get('termination_date')

            if start_date:
                try:
                    start_date_object = datetime.strptime(start_date, '%d/%m/%Y')
                    worker_start_date = start_date_object.strftime('%Y-%m-%d')
                except ValueError:
                    session.rollback()
                    rroute = '/radnici'
                    err_code = 'Neispravan datum prijave!'
                    return render_template('greska.html', error_code=err_code, redirect_route=rroute)
                if termination_date:
                    try:
                        termination_date_object = datetime.strptime(termination_date, '%d/%m/%Y')
                        worker_termination_date = termination_date_object.strftime('%Y-%m-%d')
                    except ValueError:
                        session.rollback()
                        rroute = '/radnici'
                        err_code = 'Neispravan datum odjave!'
                        return render_template('greska.html', error_code=err_code, redirect_route=rroute)
                else:
                    worker_termination_date = None

            if worker_full_name and worker_start_date and \
                    re.match(r'\d{13}', worker_jmbg):
                try:
                    new_worker = Worker(jmbg=worker_jmbg,
                                        full_name=worker_full_name,
                                        contract_termination_date=worker_termination_date,
                                        contract_start_date=worker_start_date,
                                        company_pib=pib)
                    session.add(new_worker)
                    session.flush()
                except IntegrityError as e:
                    print(e._message())
                    session.rollback()
                    rroute = '/radnici'
                    err_code = 'Radnik sa ovim JMBG-om vec postoji!'
                    return render_template('greska.html', error_code=err_code, redirect_route=rroute)

                session.commit()
                company = session.query(Company).filter(Company.pib == pib).one()
                workers = session.query(Worker).filter(Worker.company_pib == pib).all()
                flags = utils.get_worker_flags(workers)
                return render_template('spisak.html',
                                       workers=[[worker, flag] for (worker, flag) in zip(workers, flags)],
                                       company=company.name)
            else:
                rroute = '/radnici'
                err_code = 'Neispravni podaci radnika!'
                return render_template('greska.html', error_code=err_code, redirect_route=rroute)


@radnici.route('/radnici', methods=['GET'])
def update():
    pib = flask_session.get('pib')
    company = session.query(Company).filter(Company.pib == pib).one()
    workers = session.query(Worker).filter(Worker.company_pib == pib).all()
    flags = utils.get_worker_flags(workers)
    return render_template('spisak.html',
                           workers=[[worker, flag] for (worker, flag) in zip(workers, flags)],
                           company=company.name)


@radnici.route('/radnici/delete/<worker_jmbg>', methods=['POST'])
def delete(worker_jmbg=None):
    if request.method == "POST":
        worker_row_to_delete = session.query(Worker).filter(Worker.jmbg == worker_jmbg).one()
        session.delete(worker_row_to_delete)
        session.commit()
        return redirect(url_for('radnici.update'))


@radnici.route('/radnici/edit_company/<pib>', methods=['POST'])
def edit_company(pib=None):
    print('edit company')
    company = session.query(Company).filter(Company.pib == pib).one()
    return render_template('edit_company.html', pib1=company.pib, name=company.name)

@radnici.route('/radnici/save_company/<pib>', methods=['POST', 'GET'])
def company_save(pib=None):
    print(f'change {pib}')

    new_name = request.form.get('new_name')
    new_pib = request.form.get('new_pib')

    company_row_to_change = session.query(Company).filter(Company.pib == pib).one()
    workers = session.query(Worker).filter(Worker.company_pib == pib).all()
    for worker in workers:
        print(worker.company_pib, new_pib)
        print(worker.company_pib)

    if new_name:
        company_row_to_change.name = new_name

    if new_pib:
        company_row_to_change.pib = new_pib

    try:

        session.add(company_row_to_change, workers)
        session.flush()

    except IntegrityError as e:
        print(e.__cause__)
        session.rollback()
        rroute = '/'
        err_code = 'Firma sa ovim PIB-om vec postoji!'

        return render_template('greska.html', error_code=err_code, redirect_route=rroute)

    session.commit()

    return redirect(url_for('radnici.index'))

@radnici.route('/radnici/edit/<worker_jmbg>', methods=['POST'])
def edit(worker_jmbg=None):
    worker = session.query(Worker).filter(Worker.jmbg == worker_jmbg).one()
    return render_template('edit.html', worker_jmbg=worker_jmbg, worker=worker, pib=flask_session['pib'])


@radnici.route('/radnici/save/<worker_jmbg>', methods=['POST', 'GET'])
def save(worker_jmbg=None):

    new_jmbg = request.form.get('new_jmbg')
    new_name = request.form.get('new_name')
    subm_date = request.form.get('subm_date')
    term_date = request.form.get('term_date')

    worker_row_to_change = session.query(Worker).filter(Worker.jmbg == worker_jmbg).one()

    if new_jmbg:
        worker_row_to_change.jmbg = new_jmbg

    if new_name:
        worker_row_to_change.full_name = new_name

    if subm_date:
        start_date_object = datetime.strptime(subm_date, '%d/%m/%Y')
        worker_start_date = start_date_object.strftime('%Y-%m-%d')
        worker_row_to_change.contract_start_date = worker_start_date

    if term_date == '' or term_date == "Neodređeno":
        term_date = None

    if term_date:
        term_date = datetime.strptime(term_date, '%d/%m/%Y')

    worker_row_to_change.contract_termination_date = term_date

    try:
        session.add(worker_row_to_change)
        session.flush()

    except IntegrityError:
        session.rollback()
        rroute = '/radnici'
        err_code = 'Radnik sa ovim JMBG-om vec postoji!'

        return render_template('greska.html', error_code=err_code, redirect_route=rroute)

    session.commit()

    return redirect(url_for('radnici.update'))