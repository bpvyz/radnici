from flask import render_template, request, redirect, session, url_for, Blueprint
import datetime, re
from datetime import datetime
import base
import utils
from models import Worker, Company
from sqlalchemy.exc import IntegrityError


radnici = Blueprint('radnici', __name__)
sess = base.create_session()


@radnici.route('/', methods=['GET'])
def index():
    companies = sess.query(Company).all()
    flags = utils.get_flags(companies)
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
                    sess.add(new_company)
                    sess.flush()
                except IntegrityError:
                    sess.rollback()
                    rroute = '/'
                    err_code = 'Firma sa ovim PIB-om vec postoji!'
                    return render_template('greska.html', error_code=err_code, redirect_route=rroute)
                else:
                    sess.commit()
                    companies = sess.query(Company).all()
                    flags = utils.get_flags(companies)
                    return render_template('index.html', list=[[n.name, n.pib, flag] for (n, flag) in zip(companies, flags)])
            else:
                rroute = '/'
                err_code = 'Neispravni podaci firme!'
                return render_template('greska.html', error_code=err_code, redirect_route=rroute)

@radnici.route('/radnici/<pib>/<company_name>', methods=['POST', 'GET'])
def open(pib=None, company_name=None):
    print('open')
    if request.method == 'GET' or request.form['submit_button'] == 'open':
        session['company_name'] = company_name
        session['pib'] = pib
        workers = sess.query(Worker).filter(Worker.company_pib == pib).all()
        return render_template('spisak.html', company=company_name, workers=[worker for worker in workers])

    elif request.form['submit_button'] == 'delete':

        sess.query(Worker).filter(Worker.company_pib == pib).delete()
        sess.query(Company).filter(Company.pib == pib).delete()

        sess.commit()

        return redirect(url_for('radnici.index'))


@radnici.route('/radnik_dodat', methods=['POST'])
def new_worker():
    print('new worker')
    pib = session.get('pib')
    if request.method == 'POST':
        if request.form['new_worker'] == 'new_worker':

            worker_jmbg = request.form.get('jmbg')
            worker_full_name = request.form.get('full_name')
            start_date = request.form.get('start_date')
            termination_date = request.form.get('termination_date')

            if start_date:
                start_date_object = datetime.strptime(start_date, '%d/%m/%Y')
                worker_start_date = start_date_object.strftime('%Y-%m-%d')
                if termination_date:
                    termination_date_object = datetime.strptime(termination_date, '%d/%m/%Y')
                    worker_termination_date = termination_date_object.strftime('%Y-%m-%d')
                else:
                    worker_termination_date = None

            if worker_full_name and worker_start_date and \
                    re.match(r'\d{13}', worker_jmbg):
                try:
                    new_worker = Worker(jmbg=worker_jmbg, full_name=worker_full_name,
                                    contract_termination_date=worker_termination_date, contract_start_date=worker_start_date, company_pib=pib)
                    sess.add(new_worker)
                    sess.flush()
                except IntegrityError:
                    sess.rollback()
                    rroute = '/radnici'
                    err_code = 'Radnik sa ovim JMBG-om vec postoji!'
                    return render_template('greska.html', error_code=err_code, redirect_route=rroute)
                else:
                    sess.commit()
                    return render_template('dodat.html')
            else:
                rroute = '/radnici'
                err_code = 'Neispravni podaci radnika!'
                return render_template('greska.html', error_code=err_code, redirect_route=rroute)

@radnici.route('/radnici', methods=['GET'])
def update():
    print('update')
    company_name = session.get('company_name')
    pib = session.get('pib')
    workers = sess.query(Worker).filter(Worker.company_pib == pib).all()

    return render_template('spisak.html', company=company_name, workers=[worker for worker in workers])

@radnici.route('/radnici/actions/<action>/<worker_jmbg>', methods=['GET', 'POST'])
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
            return redirect(url_for('radnici.update'))

        # elif action == 'change':
        #     return redirect(url_for('radnici.update'))
        # elif action == 'accept':
        #     return redirect(url_for('radnici.update'))

    elif request.method == "GET":
        return redirect(url_for('radnici.update'))