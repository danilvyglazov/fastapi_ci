from fastapi.testclient import TestClient

from main import app


def test_all_get():
    with TestClient(app) as client:
        response = client.get("/recipes/", headers={"X-Token": "coneofsilence"})
        assert response.status_code == 200
        for data in response.json():
            assert list(data.keys()) == ["title", "views", "time_to_cook"]


def test_adding_new_recipe_and_get_it_by_id():
    with TestClient(app) as client:
        response = client.post(
            "/recipes/",
            headers={"X-Token": "coneofsilence", "Content-Type": "application/json"},
            json={
                "title": "Meat",
                "time_to_cook": 30,
                "ingredients": "Meat",
                "description": "Tasty meat",
            },
        )
        result: dict = response.json()
        new_id = result.get("recipe_id")
        del result["recipe_id"]
        new_data = client.get(
            f"/recipes/{new_id}", headers={"X-Token": "coneofsilence"}
        )
        assert result == {
            "title": "Meat",
            "time_to_cook": 30,
            "ingredients": "Meat",
            "description": "Tasty meat",
            "views": 0,
        }
        assert response.status_code == 201
        assert new_data.json() == {
            "title": "Meat",
            "time_to_cook": 30,
            "ingredients": "Meat",
            "description": "Tasty meat",
            "views": 1,
            "recipe_id": new_id,
        }
