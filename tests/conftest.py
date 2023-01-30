import pytest
from app import create_app
from app.models.category import Category
from app.models.checklist import Checklist
from app.models.task import Task
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

@pytest.fixture
def one_checklist_belongs_to_one_category(app, one_category):
    new_checklist = Checklist(title="Automate the Boring Stuff", description="A foundational Python text", category_id=1)
    db.session.add(new_checklist)
    db.session.commit()

@pytest.fixture
def one_task_belong_to_one_checklist(app, one_checklist_belongs_to_one_category):
    db.session.add_all([
        Task(title="Chapter 1", checklist_id=1),
    ])
    db.session.commit()

@pytest.fixture
def three_tasks_belong_to_one_checklist(app, one_checklist_belongs_to_one_category):
    db.session.add_all([
        Task(title="Chapter 1", checklist_id=1),
        Task(title="Chapter 2", checklist_id=1),
        Task(title="Chapter 3", checklist_id=1),
    ])
    db.session.commit()
