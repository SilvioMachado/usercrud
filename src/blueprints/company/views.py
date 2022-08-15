from flask import request

from src.user.blueprint import blueprint
from src.database.models import ClientCompany, CompanyBankAccount


@blueprint.get('/<int:company_id>')
def company_get(company_id):
    return ClientCompany.query.get_or_404(
        company_id, description='Invalid Company'
    ).serialize()


@blueprint.post('/')
def company_post():
    ClientCompany.create_from_dict(request.json)
    return ''


@blueprint.delete('/<int:company_id>')
def company_delete(company_id):
    ClientCompany.delete_by_id(company_id)
    return ''


@blueprint.post('/<int:company_id>/bank_account')
def add_bank_account(company_id):
    client_company = ClientCompany.query.get_or_404(company_id)
    bank_account = CompanyBankAccount.create_from_dict(request.json)

    client_company.add_bank_account(bank_account)

    return ''


@blueprint.put('/<int:company_id>')
def company_update(company_id):
    client_company = ClientCompany.query.get_or_404(company_id)
    client_company.update_from_dict(request.json)
    return ''


@blueprint.put('/account/<int:account_id>')
def update_bank_account(account_id):
    bank_account = CompanyBankAccount.query.get(account_id)
    bank_account.update_from_dict(request.json)
    return ''


@blueprint.delete('/account/<int:account_id>')
def delete_bank_account(account_id):
    CompanyBankAccount.delete_by_id(account_id)
    return ''
