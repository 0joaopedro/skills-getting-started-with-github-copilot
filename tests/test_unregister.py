"""Integration and unit tests for DELETE /activities/{activity_name}/unregister endpoint."""
import pytest


def test_unregister_success(client, reset_activities):
    """Test successful removal of participant from activity.
    
    AAA Pattern:
    - Arrange: Activity with existing participant
    - Act: DELETE request to remove participant
    - Assert: Participant removed and response confirms deletion
    """
    email = "michael@mergington.edu"  # Already in Chess Club
    activity_name = "Chess Club"
    
    # Verify participant exists first
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_activity_not_found(client, reset_activities):
    """Test unregister fails when activity doesn't exist.
    
    AAA Pattern:
    - Arrange: Valid email but invalid activity
    - Act: DELETE from non-existent activity
    - Assert: Receive 404 error
    """
    # Act
    response = client.delete(
        "/activities/Nonexistent Activity/unregister",
        params={"email": "test@mergington.edu"}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_registered(client, reset_activities, sample_email):
    """Test unregister fails when student is not registered.
    
    AAA Pattern:
    - Arrange: Student not registered for activity
    - Act: Attempt to unregister non-member
    - Assert: Receive 400 error
    """
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_allows_reregistration(client, reset_activities, sample_email):
    """Test student can re-register after unregistering.
    
    AAA Pattern:
    - Arrange: Student registered for activity
    - Act: Unregister, then register again
    - Assert: Both operations succeed, student appears in list again
    """
    activity_name = "Chess Club"
    
    # Act - First signup
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": sample_email}
    )
    assert response1.status_code == 200
    
    # Act - Unregister
    response2 = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": sample_email}
    )
    assert response2.status_code == 200
    
    # Act - Re-register
    response3 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": sample_email}
    )
    
    # Assert
    assert response3.status_code == 200
    activities_response = client.get("/activities")
    assert sample_email in activities_response.json()[activity_name]["participants"]
