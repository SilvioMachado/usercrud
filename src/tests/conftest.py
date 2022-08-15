from datetime import datetime

import pytest


TEST_DATABASE = 'usercrud_test'
FAKE_NOW = datetime(2022, 8, 8, 12, 0, 0)


@pytest.fixture(autouse=True)
def fake_now(freezer):
    return freezer.move_to(FAKE_NOW)


@pytest.fixture(scope='session')
def app():
    from src import app
    from src.database.db import db, init_from_app

    app.config.from_pyfile('/app/config/local.py')

    init_from_app(app)

    db.drop_all()
    db.create_all()

    # Stop this function to execute test session
    yield app

    # After tests are done, this function should resume
    db.session.close()
    db.drop_all()


@pytest.fixture(
    scope='session', autouse=True
)
def banks(app):
    from src.database.db import db
    from src.database.models import Bank
    from src.tests.data.banks import bank_list

    obj_list = [Bank(**bank) for bank in bank_list]
    db.session.add_all(obj_list)
    db.session.commit()


@pytest.fixture
def http_client(app):
    return app.test_client()
