"""Shared test fixtures and configuration."""
import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test."""
    # Store original state
    original_activities = deepcopy(activities)
    
    yield
    
    # Restore original state after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_activity():
    """Provide sample activity data for tests."""
    return {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
    }


@pytest.fixture
def sample_email():
    """Provide a sample student email."""
    return "test@mergington.edu"
