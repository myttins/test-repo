import pytest
from src.app import app as _app
from src.db import db as _db


@pytest.fixture
def app():
    _app.config.update({
        "TESTING": True,
    })
    with _app.app_context():
        _db.create_all()
    yield _app
    with _app.app_context():
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db():
    return _db
