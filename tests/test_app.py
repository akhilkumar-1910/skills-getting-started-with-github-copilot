from urllib.parse import quote


def test_root_redirects_to_static_index(client):
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_map(client):
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_success_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": email})
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Activity"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_missing_email_returns_422(client):
    # Arrange
    activity_name = "Chess Club"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(path)

    # Assert
    assert response.status_code == 422


def test_signup_url_encoded_activity_name_succeeds(client):
    # Arrange
    activity_name = "Programming Class"
    email = "encoded.student@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.delete(path, params={"email": email})
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Activity"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.delete(path, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-signed-up@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_missing_email_returns_422(client):
    # Arrange
    activity_name = "Chess Club"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.delete(path)

    # Assert
    assert response.status_code == 422
