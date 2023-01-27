from werkzeug.exceptions import HTTPException
from app.models.category import Category
import pytest

@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_categories_no_saved_categories(client):
    response = client.get("/categories")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_all_categories(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_post_category_must_contain_title(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_post_category_must_contain_description(client):
    pass

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_category(client, one_category):
    response = client.delete("/categories/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Category #1 "Python Learning" successfully deleted'
    }
    assert Category.query.get(1) == None

@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_category_not_found(client):
    pass
