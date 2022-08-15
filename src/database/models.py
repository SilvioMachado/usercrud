from typing import Dict

from src.exceptions import InvalidException
from src.database.db import db
from src.database.mixin import SaveMixin


def default_now():
    from datetime import datetime
    return datetime.utcnow()


class ClientCompany(db.Model, SaveMixin):
    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(80), nullable=False)

    phone = db.Column(db.String(15), nullable=False)
    """
    Should contain only numbers. Country code, region code and phone number. 
    E.g.: 5511954879564. The Integer type serves as constraint here.
    """

    created = db.Column(db.DateTime, default=default_now)
    """
    Python datetime, should be set only by the system.
    """

    declared_billing = db.Column(db.DECIMAL(12, 2), nullable=False)
    """
    How much money a company has made. For this test project, the time frame is unspecified.
    """

    bank_accounts = db.relationship('CompanyBankAccount', backref='company')
    """
    Relation with CompanyBankAccount. Use .add_bank_account()
    """

    def serialize(self, include_id: bool = True) -> Dict:
        _dict = {
            'company_name': self.company_name,
            'phone': self.phone,
            'created': self.created.isoformat(),
            'declared_billing': self.declared_billing,
            'bank_accounts': [
                acc.serialize(include_id=include_id) for acc in self.bank_accounts
            ],
        }
        if include_id:
            _dict['id'] = self.id

        return _dict

    def update_from_dict(self, _dict: Dict):
        if _dict.get('bank_accounts'):
            for bank in _dict.pop('bank_accounts'):
                self.bank_accounts.append(CompanyBankAccount(**bank))

        for key, value in _dict.items():
            setattr(self, key, value)

        db.session.commit()

    def add_bank_account(self, bank_account: 'CompanyBankAccount'):
        for _bank_account in self.bank_accounts:
            if bank_account.is_same(_bank_account):
                raise InvalidException('Account already registered.')

        self.bank_accounts.append(bank_account)
        self.save()

    @classmethod
    def create_from_dict(cls, _dict: Dict) -> 'ClientCompany':
        bank_accounts = []

        if _dict.get('bank_accounts'):
            for bank in _dict.pop('bank_accounts'):
                bank_accounts.append(CompanyBankAccount(**bank))

        client_company = cls(**_dict, bank_accounts=bank_accounts)
        db.session.add(client_company)
        db.session.commit()

        return client_company

    @staticmethod
    def delete_by_id(company_id: int):
        company = ClientCompany.query.get_or_404(company_id)
        db.session.delete(company)
        db.session.commit()


class CompanyBankAccount(db.Model, SaveMixin):
    id = db.Column(db.Integer, primary_key=True)

    agency = db.Column(db.String(10), nullable=False)

    account_number = db.Column(db.String(10), nullable=False)

    bank_code = db.Column(db.String(3), db.ForeignKey('bank.code'), nullable=False)
    """
    The 3 digit code that defines the Bank as a Financial Agent. 
    """

    company_id = db.Column(db.Integer, db.ForeignKey('client_company.id'))

    def update_from_dict(self, _dict: Dict):
        for key, value in _dict.items():
            setattr(self, key, value)

        db.session.commit()

    def serialize(self, include_user: bool = False, include_id: bool = True) -> Dict:
        _dict = {
            'agency': self.agency,
            'account_number': self.account_number,
            'bank': self.bank.serialize,
        }

        if include_user:
            _dict['user'] = self.user.serialize
        if include_id:
            _dict['id'] = self.id
        return _dict

    def is_same(self, account: 'CompanyBankAccount') -> bool:
        fields = ['agency', 'account_number', 'bank_code']
        for field in fields:
            if not getattr(self, field) == getattr(account, field):
                return False

        return True

    @classmethod
    def create_from_dict(cls, _dict: Dict) -> 'CompanyBankAccount':
        account = CompanyBankAccount(**_dict)
        account.save()

        return account

    @staticmethod
    def delete_by_id(_id: int):
        CompanyBankAccount.query.get_or_404(_id).delete()


class Bank(db.Model, SaveMixin):
    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String(3), index=True, unique=True, nullable=False)
    """
    The 3 digit code that defines the Bank as a Financial Agent. 
    """

    name = db.Column(db.String(50), nullable=False)

    user_bank_accounts = db.relationship('CompanyBankAccount', backref='bank')

    @property
    def serialize(self) -> Dict:
        return {
            'code': self.code,
            'name': self.name,
        }

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'{self.code} - {self.name}'
