import pytest
from app import create_app
from app.models.category import Category
from app import db


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_category(app):
    new_category = Category(title="Python Learning", description="A category devoted to Python learning resources")
    db.session.add(new_category)
    db.session.commit()
