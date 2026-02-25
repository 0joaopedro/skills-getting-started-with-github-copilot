"""Integration tests for GET /activities endpoint."""
import pytest


def test_get_all_activities(client, reset_activities):
    """Test retrieving all activities successfully.
    
    AAA Pattern:
    - Arrange: Activities are pre-loaded in the system
    - Act: Send GET request to /activities
    - Assert: Verify response contains all activities with correct structure
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    
    # Verify activities exist
    assert len(activities) > 0
    assert "Chess Club" in activities
    assert "Programming Class" in activities


def test_activity_structure(client, reset_activities):
    """Test that activities have correct structure.
    
    AAA Pattern:
    - Arrange: Request activities endpoint
    - Act: Parse response JSON
    - Assert: Verify each activity has required fields
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    activity = activities["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_participants_included(client, reset_activities):
    """Test that existing participants are included in response.
    
    AAA Pattern:
    - Arrange: Activities with existing participants
    - Act: Fetch activities
    - Assert: Verify participants are listed
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    chess_club = activities["Chess Club"]
    assert len(chess_club["participants"]) > 0
    assert "michael@mergington.edu" in chess_club["participants"]
