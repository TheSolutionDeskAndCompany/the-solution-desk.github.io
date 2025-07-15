"""
Tests for Ideas API endpoints
"""
import json
import pytest

# SUCCESS TESTS (200/201)

def test_get_ideas_api(client):
    """Test getting all ideas via API"""
    response = client.get('/api/ideas')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    
def test_create_idea_api_valid(client):
    """Test creating an idea with valid data"""
    idea_data = {
        'title': 'New Idea',
        'description': 'Description here',
        'status': 'new',
        'priority': 2
    }
    response = client.post(
        '/api/ideas',
        data=json.dumps(idea_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'New Idea'
    assert data['description'] == 'Description here'
    assert data['status'] == 'new'
    assert data['priority'] == 2

def test_get_single_idea_api(client):
    """Test getting a single idea via API"""
    # First create an idea
    idea_data = {
        'title': 'Test Idea',
        'description': 'Test Description',
        'status': 'new',
        'priority': 1
    }
    create_response = client.post(
        '/api/ideas',
        data=json.dumps(idea_data),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    new_idea = json.loads(create_response.data)
    
    # Now get the idea
    response = client.get(f'/api/ideas/{new_idea["id"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Test Idea'
    assert data['description'] == 'Test Description'
    assert data['status'] == 'new'

def test_update_idea_api_valid(client):
    """Test updating an idea with valid data"""
    # First create an idea
    idea_data = {
        'title': 'Original Idea',
        'description': 'Original description',
        'status': 'new'
    }
    create_response = client.post(
        '/api/ideas',
        data=json.dumps(idea_data),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    original_idea = json.loads(create_response.data)
    
    # Update the idea
    update_data = {
        'title': 'Updated Idea',
        'description': 'Updated description',
        'status': 'in_progress',
        'priority': 3
    }
    response = client.put(
        f'/api/ideas/{original_idea["id"]}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated Idea'
    assert data['description'] == 'Updated description'
    assert data['status'] == 'in_progress'
    assert data['priority'] == 3

def test_delete_idea_api_success(client):
    """Test deleting an idea via API"""
    # First create an idea to delete
    idea_data = {
        'title': 'Idea to Delete',
        'description': 'Will be deleted'
    }
    create_response = client.post(
        '/api/ideas',
        data=json.dumps(idea_data),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    new_idea = json.loads(create_response.data)
    
    # Delete the idea
    response = client.delete(f'/api/ideas/{new_idea["id"]}')
    assert response.status_code == 204
    
    # Verify idea is deleted
    get_response = client.get(f'/api/ideas/{new_idea["id"]}')
    assert get_response.status_code == 404

# VALIDATION FAILURE TESTS (400)

def test_create_idea_api_invalid(client):
    """Test creating an idea with invalid data (missing required field)"""
    idea_data = {
        'description': 'Description without title',
        'status': 'new'
    }
    response = client.post(
        '/api/ideas',
        data=json.dumps(idea_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Title is required' in str(data) or 'errors' in data or 'message' in data

def test_update_idea_api_invalid(client):
    """Test updating an idea with invalid data"""
    # First create an idea
    idea_data = {
        'title': 'Original Idea',
        'description': 'Original description'
    }
    create_response = client.post(
        '/api/ideas',
        data=json.dumps(idea_data),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    original_idea = json.loads(create_response.data)
    
    # Try to update with invalid data
    update_data = {
        'title': ''  # Empty title should fail validation
    }
    response = client.put(
        f'/api/ideas/{original_idea["id"]}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 400

# NOT FOUND TESTS (404)

def test_get_nonexistent_idea_api(client):
    """Test getting a non-existent idea returns 404"""
    response = client.get('/api/ideas/999')
    assert response.status_code == 404

def test_update_nonexistent_idea_api(client):
    """Test updating a non-existent idea returns 404"""
    update_data = {
        'title': 'Updated Title',
        'description': 'Updated Description'
    }
    response = client.put(
        '/api/ideas/999',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 404

def test_delete_nonexistent_idea_api(client):
    """Test deleting a non-existent idea returns 404"""
    response = client.delete('/api/ideas/999')
    assert response.status_code == 404

# SERVER ERROR TESTS (500)
# Note: In a real test environment, we would use monkeypatch to simulate server errors

def test_idea_api_server_error_simulation(client):
    """
    Simulate a server error (this is a placeholder)
    In a real test environment, we would use monkeypatch to force an exception
    """
    # This test is a placeholder for the server error test case
    # The actual implementation would depend on how server errors are handled
    # in the application and the testing framework
    pass
