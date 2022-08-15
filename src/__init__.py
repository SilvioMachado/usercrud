from flask import Flask

from src.database.db import init_from_app
from src.exceptions import InvalidException, handle_invalid_exception

app = Flask(__name__)
app.config.from_pyfile('/app/config/local.py')

# Database related
init_from_app(app)

# Error handling related
app.register_error_handler(400, handle_invalid_exception)

# Blueprints related
from src.user import blueprint as user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/company')


# Shell related
@app.cli.command('shell_plus')
def shell_plus():
    from IPython import embed
    from src.database.models import (
        Bank, CompanyBankAccount, ClientCompany
    )
    from src.database.db import db

    embed(
        user_ns={
            'app': app,
            'Bank': Bank,
            'CompanyBankAccount': CompanyBankAccount,
            'ClientCompany': ClientCompany,
            'db': db
        })
