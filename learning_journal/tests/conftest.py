# coding=utf-8
import pytest
from learning_journal.models import DBSession, Base, Entry
from sqlalchemy import create_engine
import transaction
import os


TEST_DATABASE_URL = 'postgres://macuser:@localhost:5432/testdb'


@pytest.fixture(scope='session')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)
    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)

    return connection


@pytest.fixture()
def one_entry(session):
    test_entry = Entry(title=u"Test Entry", text=u"Here is my test entry")
    with transaction.manager:
        session.add(test_entry)
    return session.query(Entry).filter(Entry.title == u"Test Entry").first()


@pytest.fixture()
def session(dbtransaction):
    from learning_journal.models import DBSession
    return DBSession


@pytest.fixture()
def app(dbtransaction):
    from learning_journal import main
    # from pyramid.paster import get_appsettings
    from webtest import TestApp
    fake_settings = {'sqlalchemy.url': TEST_DATABASE_URL}
    app = main({}, **fake_settings)
    return TestApp(app)


@pytest.fixture()
def auth_env():
    from .security import pwd_context
    os.environ['AUTH_PASSWORD'] = pwd_context.encrypt('secret')
    os.environ['AUTH_USERNAME'] = 'admin'


@pytest.fixture()
def authenticated_app(app, auth_env):
    data = {'username': 'admin', 'password': 'secret'}
    app.post('/login', data)
    return app
