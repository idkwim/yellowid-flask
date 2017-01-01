import pytest
from .config import *


@pytest.fixture
def app(request):
    main.app.config["TESTING"] = True
    main.app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_URI
    ctx = main.app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return main.app


@pytest.fixture
def db(request):
    def teardown():
        main.db.drop_all()
    main.db.create_all()
    request.addfinalizer(teardown)
    return main.db


@pytest.fixture
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def test_client(app):
    return app.test_client()


def test_hello(test_client, session):
    assert isinstance(test_client, FlaskClient)


def test_add_user(session):
    user = model.User(user_key="test_id")
    assert repr(user) == "<User %r>" % ("test_id")
    session.add(user)
    session.commit()
    assert user.id > 0
    user = search_user("test_id")
    assert user is not None


def test_delete_user(session):
    user = model.User(user_key="test_id")
    session.add(user)
    session.commit()
    user = search_user("test_id")
    session.delete(user)
    session.commit()
    user = search_user("test_id")
    assert user is None


def search_user(user_key):
    user = model.User.query.filter_by(user_key=user_key).first()
    return user
