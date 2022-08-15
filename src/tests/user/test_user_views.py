import pytest
from decimal import Decimal

from src.database.models import ClientCompany, CompanyBankAccount


@pytest.fixture
def bank_account():
    bank_account = CompanyBankAccount(
        agency='123245',
        account_number='92834-9',
        bank_code='044'
    )
    bank_account.save()
    return bank_account


@pytest.fixture
def company_with_bank(bank_account):
    company = ClientCompany(
        company_name='my company',
        phone='(11) 95874-4568',
        declared_billing=Decimal(1235.69),
        bank_accounts=[bank_account],
    )
    company.save()

    return company


def test_get_company(http_client, company_with_bank, fake_now):
    # Given

    path = f'company/{company_with_bank.id}'
    expected_response = {
        'bank_accounts': [
            {
                'account_number': '92834-9',
                'agency': '123245',
                'bank': {
                    'code': '044', 'name': 'Banco BVA'
                },
                'id': 1
            }
        ],
        'company_name': 'my company',
        'created': '2022-08-08T12:00:00',
        'declared_billing': '1235.69',
        'id': 1,
        'phone': '(11) 95874-4568'
    }

    # When
    response = http_client.get(path)

    # Then
    assert response.json == expected_response


def test_create_company(http_client, fake_now):
    # Given

    path = '/company/'
    request_body = {
        'company_name': 'My Company',
        'phone': '(11) 97823-5674',
        'declared_billing': 123.02
    }

    # When
    response = http_client.post(path, json=request_body)

    # Then
    queryset = ClientCompany.query.filter_by(company_name='My Company')
    company = queryset.first()

    assert queryset.count() == 1
    assert company.phone == '(11) 97823-5674'
    assert company.declared_billing == Decimal('123.02')


def test_create_company_with_bank_account(http_client, fake_now):
    # Given

    path = '/company/'
    request_body = {
        'company_name': 'Company with bank account',
        'phone': '(11) 97823-5674',
        'declared_billing': 999.20,
        'bank_accounts': [
            {
                'account_number': '1243',
                'agency': '1290-0',
                'bank_code': '336',
            }
        ]
    }

    # When
    response = http_client.post(path, json=request_body)

    # Then
    queryset = ClientCompany.query.filter_by(company_name='Company with bank account')
    company = queryset.first()

    # Company assertions
    assert queryset.count() == 1
    assert company.phone == '(11) 97823-5674'
    assert company.declared_billing == Decimal('999.20')

    # Account assertions
    assert len(company.bank_accounts) == 1
    assert company.bank_accounts[0].account_number == '1243'
    assert company.bank_accounts[0].agency == '1290-0'
    assert company.bank_accounts[0].bank_code == '336'

    # Bank assertions
    assert company.bank_accounts[0].bank.name == 'C6 Bank'


def test_delete_company(http_client, fake_now, company_with_bank):
    # Given
    path = f'/company/{company_with_bank.id}'

    # When
    http_client.delete(path)

    # Then
    assert ClientCompany.query.get(company_with_bank.id) is None


def test_update_company(http_client, fake_now, company_with_bank):
    # Given
    _id = company_with_bank.id
    path = f'/company/{_id}'
    update_body = {
        'company_name': 'New name for company',
        'bank_accounts': [
            {
                'account_number': '1949',
                'agency': '4440-10',
                'bank_code': '237',
            }
        ]
    }
    expected_serialization = {
        'company_name': 'New name for company',  # updated name
        'phone': '(11) 95874-4568',
        'created': '2022-08-08T12:00:00',
        'declared_billing': Decimal('1235.69'),
        'bank_accounts': [
            {
                'agency': '123245',
                'account_number': '92834-9',
                'bank': {'code': '044', 'name': 'Banco BVA'}
            },
            {
                'agency': '4440-10',  # New bank account being added
                'account_number': '1949',
                'bank': {'code': '237', 'name': 'Banco Bradesco'}
            }
        ]
    }

    # When
    http_client.put(path, json=update_body)

    # Then
    refreshed_company = ClientCompany.query.get(_id)

    assert refreshed_company.serialize(include_id=False) == expected_serialization


def test_update_account(http_client, bank_account):
    # Given
    _id = bank_account.id
    path = f'/company/account/{_id}'
    update_body = {
        'agency': '54321'
    }
    expected_serialization = {
        'agency': '54321',
        'account_number': '92834-9',
        'bank': {'code': '044', 'name': 'Banco BVA'}
    }

    # When
    http_client.put(path, json=update_body)

    # Then
    account = CompanyBankAccount.query.get(_id)
    assert account.serialize(include_id=False) == expected_serialization


def test_delete_account(http_client, bank_account):
    # Given
    _id = bank_account.id
    path = f'/company/account/{_id}'

    # When
    http_client.delete(path)

    # Then
    assert CompanyBankAccount.query.get(_id) is None


def test_add_bank_account(http_client, company_with_bank):
    # Given
    _id = company_with_bank.id
    path = f'/company/{_id}/bank_account'
    request_body = {
        'agency': '55879',
        'account_number': '4679-9',
        'bank_code': '044',
    }

    # When
    http_client.post(path, json=request_body)

    # Then
    refreshed_company = ClientCompany.query.get(_id)
    assert len(refreshed_company.bank_accounts) == 2


def test_add_same_bank_account(http_client, company_with_bank):
    # Given
    _id = company_with_bank.id
    path = f'/company/{_id}/bank_account'
    request_body = {
        'agency': '123245',
        'account_number': '92834-9',
        'bank_code': '044',
    }

    # When
    response = http_client.post(path, json=request_body)

    # Then
    refreshed_company = ClientCompany.query.get(_id)
    assert len(refreshed_company.bank_accounts) == 1
    assert response.status_code == 400
