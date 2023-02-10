from werkzeug.exceptions import HTTPException
from app.models.habit import Habit
import pytest


@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_habit(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_habit_must_contain_title(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_habits_no_saved_habits(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_habits_three_saved_habits(client, three_habits_belong_to_one_user):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_update_habit_reps(client, three_habits_belong_to_one_user):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_reset_habit_reps(client, three_habits_belong_to_one_user):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_habit(client, three_habits_belong_to_one_user):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_habit_not_found(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_habit_invalid_id(client):
    pass
