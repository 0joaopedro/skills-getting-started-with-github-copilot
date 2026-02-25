"""Integration and unit tests for POST /activities/{activity_name}/signup endpoint."""
import pytest


def test_signup_success(client, reset_activities, sample_email):
    """Test successful registration for an activity.
    
    AAA Pattern:
    - Arrange: Fresh database with available activity
    - Act: POST signup request with valid email and activity
    - Assert: Response confirms signup and activity has new participant
    """
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert sample_email in response.json()["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert sample_email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client, reset_activities, sample_email):
    """Test signup fails when activity doesn't exist.
    
    AAA Pattern:
    - Arrange: Sample email and non-existent activity name
    - Act: POST signup to invalid activity
    - Assert: Receive 404 error
    """
    # Act
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_registration(client, reset_activities):
    """Test signup fails when student already registered.
    
    AAA Pattern:
    - Arrange: Student already registered for activity
    - Act: Attempt to register same student again
    - Assert: Receive 400 error about duplicate registration
    """
    email = "michael@mergington.edu"  # Already in Chess Club
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_multiple_activities(client, reset_activities, sample_email):
    """Test student can register for multiple different activities.
    
    AAA Pattern:
    - Arrange: Sample email and multiple activities
    - Act: Register same student for different activities
    - Assert: Student appears in multiple activity lists
    """
    # Act
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": sample_email}
    )
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": sample_email}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert sample_email in activities["Chess Club"]["participants"]
    assert sample_email in activities["Programming Class"]["participants"]
