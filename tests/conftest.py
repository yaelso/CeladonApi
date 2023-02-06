import pytest
from app import create_app
from app.models.category import Category
from app.models.checklist import Checklist
from app.models.task import Task
from app.models.habit import Habit
from app.models.pokemon import Pokemon
from app.models.user_pokemon import UserPokemon
from app.models.user import User
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
def one_user(app):
    new_user = User(firebase_id="")
    db.session.add(new_user)
    db.session.commit()

@pytest.fixture
def three_users(app):
    db.session.add_all([
        User(firebase_id=""),
        User(firebase_id=""),
        User(firebase_id=""),
    ])
    db.session.commit()

@pytest.fixture
def three_pokemon(app):
    pass

@pytest.fixture
def two_pokemon_belong_to_one_user(app, three_pokemon):
    pass

@pytest.fixture
def active_pokemon(app, two_pokemon_belong_to_one_user):
    pass

@pytest.fixture
def one_category(app, one_user):
    new_category = Category(user_id=1, title="Python Learning", description="A category devoted to Python learning resources")
    db.session.add(new_category)
    db.session.commit()

@pytest.fixture
def one_checklist_belongs_to_one_category(app, one_category):
    new_checklist = Checklist(title="Automate the Boring Stuff", description="A foundational Python text", category_id=1)
    db.session.add(new_checklist)
    db.session.commit()

@pytest.fixture
def archived_checklist(app, one_checklist_belongs_to_one_category):
    new_checklist = Checklist(title="Real Python - DevOps With Python", description="A Real Python learning path", category_id=1)
    db.session.add(new_checklist)
    new_checklist.is_archived = True
    db.session.commit()

@pytest.fixture
def favorited_checklist(app, one_checklist_belongs_to_one_category):
    new_checklist = Checklist(title="Real Python - DevOps With Python", description="A Real Python learning path", category_id=1)
    db.session.add(new_checklist)
    new_checklist.is_favorited = True
    db.session.commit()

@pytest.fixture
def one_task_belong_to_one_checklist(app, one_checklist_belongs_to_one_category):
    db.session.add(Task(title="Chapter 1", checklist_id=1))
    db.session.commit()

@pytest.fixture
def three_tasks_belong_to_one_checklist(app, one_checklist_belongs_to_one_category):
    db.session.add_all([
        Task(title="Chapter 1", checklist_id=1),
        Task(title="Chapter 2", checklist_id=1),
        Task(title="Chapter 3", checklist_id=1),
    ])
    db.session.commit()

@pytest.fixture
def three_habits_belong_to_one_user(app, one_user):
    pass
