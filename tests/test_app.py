import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange - No specific setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_successful():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]

    # Verify the student was added to participants
    response_check = client.get("/activities")
    activities = response_check.json()
    assert email in activities[activity]["participants"]


def test_signup_already_signed():
    # Arrange
    activity = "Programming Class"
    email = "duplicate@mergington.edu"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act - Try to signup again
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_activity_not_found():
    # Arrange
    activity = "NonExistentActivity"
    email = "test@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_successful():
    # Arrange
    activity = "Gym Class"
    email = "unregister@mergington.edu"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]
    assert email in data["message"]
    assert activity in data["message"]

    # Verify the student was removed from participants
    response_check = client.get("/activities")
    activities = response_check.json()
    assert email not in activities[activity]["participants"]


def test_unregister_not_signed():
    # Arrange
    activity = "Soccer Team"
    email = "notsigned@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]


def test_unregister_activity_not_found():
    # Arrange
    activity = "NonExistentActivity"
    email = "test@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]