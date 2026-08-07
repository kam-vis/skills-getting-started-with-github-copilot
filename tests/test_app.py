import copy

from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def setup_function():
    app_module.activities = copy.deepcopy(app_module.ORIGINAL_ACTIVITIES)


def test_unregister_participant_removes_them_from_activity():
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"


def test_unregister_participant_returns_404_when_not_found():
    response = client.delete("/activities/Chess Club/participants/unknown@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
