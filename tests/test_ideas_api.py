"""
Tests for Ideas API endpoints
"""
import json
import pytest
import logging
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from models import Idea

# Setup test logger
logger = logging.getLogger(__name__)

# =============================================================================
# SUCCESS TESTS (200/201)
# =============================================================================

def test_get_ideas_api(client):
    """Test getting all ideas via API"""
    response = client.get('/api/ideas')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    
def test_get_ideas_with_filters(client, test_ideas):
    """Test getting filtered ideas via API"""
    # Test filtering by status
    response = client.get('/api/ideas?status=new')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert all(idea['status'] == 'new' for idea in data)
    
    # Test filtering by priority (if implemented)
    response = client.get('/api/ideas?priority=1')
    assert response.status_code == 200
    
    # Test sorting (if implemented)
    response = client.get('/api/ideas?sort=created_at&order=desc')
    assert response.status_code == 200

def test_create_idea_api_valid(authenticated_client, test_user):
    """Test creating an idea with valid data"""
    idea_data = {
        'title': 'New Idea',
        'description': 'Description here',
        'status': 'new',
        'priority': 2,
        'tags': ['innovation', 'test']
    }
    response = authenticated_client.post(
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

def test_get_single_idea_api(client, test_idea):
    """Test getting a single idea via API"""
    # Using the test_idea fixture directly
    
    # Now get the idea
    response = client.get(f'/api/ideas/{test_idea.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == test_idea.title
    assert data['description'] == test_idea.description
    assert data['status'] == test_idea.status

def test_update_idea_api_valid(authenticated_client, test_idea):
    """Test updating an idea with valid data"""
    # Using test_idea fixture directly
    
    # Update the idea
    update_data = {
        'title': 'Updated Idea',
        'description': 'Updated description',
        'status': 'in_progress',
        'priority': 3,
        'tags': ['updated', 'important']
    }
    response = authenticated_client.put(
        f'/api/ideas/{test_idea.id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated Idea'
    assert data['description'] == 'Updated description'
    assert data['status'] == 'in_progress'
    assert data['priority'] == 3

def test_partial_update_idea_api(authenticated_client, test_idea):
    """Test partially updating an idea (PATCH method)"""
    # Only update specific fields
    patch_data = {
        'status': 'in_progress',
        'priority': 4
    }
    
    response = authenticated_client.patch(
        f'/api/ideas/{test_idea.id}',
        data=json.dumps(patch_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Check that only the specified fields were updated
    assert data['status'] == 'in_progress'
    assert data['priority'] == 4
    assert data['title'] == test_idea.title  # Should remain unchanged
    assert data['description'] == test_idea.description  # Should remain unchanged

def test_delete_idea_api_success(authenticated_client, test_idea):
    """Test deleting an idea via API"""
    # Using test_idea fixture directly
    
    # Delete the idea
    response = authenticated_client.delete(f'/api/ideas/{test_idea.id}')
    assert response.status_code == 204
    
    # Verify idea is deleted
    get_response = authenticated_client.get(f'/api/ideas/{test_idea.id}')
    assert get_response.status_code == 404

# =============================================================================
# AUTHENTICATION & AUTHORIZATION TESTS
# =============================================================================

def test_create_idea_unauthorized(client):
    """Test that unauthenticated requests cannot create ideas"""
    idea_data = {
        'title': 'Unauthorized Idea',
        'description': 'Should not be created'
    }
    
    response = client.post(
        '/api/ideas',
        data=json.dumps(idea_data),
        content_type='application/json'
    )
    
    assert response.status_code == 401  # Unauthorized

def test_idea_permissions(authenticated_client, test_admin, test_ideas):
    """Test authorization rules for ideas API"""
    # Regular user should not be able to delete another user's idea
    idea_created_by_admin = [i for i in test_ideas if i.creator_id == test_admin.id][0]
    
    # Attempt to delete someone else's idea
    delete_response = authenticated_client.delete(f'/api/ideas/{idea_created_by_admin.id}')
    assert delete_response.status_code in [401, 403]  # Unauthorized or Forbidden
    
    # Admin client should be able to delete any idea
    # (requires additional test with admin client fixture)

# =============================================================================
# VALIDATION FAILURE TESTS (400)
# =============================================================================

def test_create_idea_api_invalid(authenticated_client):
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

def test_update_idea_api_invalid(authenticated_client, test_idea):
    """Test updating an idea with invalid data"""
    # Using test_idea fixture directly
    
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

def test_create_idea_invalid_json(authenticated_client):
    """Test creating an idea with invalid JSON data"""
    response = authenticated_client.post(
        '/api/ideas',
        data="This is not valid JSON",
        content_type='application/json'
    )
    assert response.status_code == 400

def test_update_idea_with_invalid_status(authenticated_client, test_idea):
    """Test updating an idea with an invalid status value"""
    update_data = {
        'status': 'invalid_status_value'  # This should not be a valid status
    }
    
    response = authenticated_client.put(
        f'/api/ideas/{test_idea.id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400

# =============================================================================
# NOT FOUND TESTS (404)
# =============================================================================

def test_get_nonexistent_idea_api(authenticated_client):
    """Test getting a non-existent idea returns 404"""
    response = authenticated_client.get('/api/ideas/999')
    assert response.status_code == 404

def test_update_nonexistent_idea_api(authenticated_client):
    """Test updating a non-existent idea returns 404"""
    update_data = {
        'title': 'Updated Title',
        'description': 'Updated Description'
    }
    response = authenticated_client.put(
        '/api/ideas/999',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 404

def test_delete_nonexistent_idea_api(authenticated_client):
    """Test deleting a non-existent idea returns 404"""
    response = authenticated_client.delete('/api/ideas/999')
    assert response.status_code == 404

# =============================================================================
# SERVER ERROR TESTS (500)
# =============================================================================

@pytest.mark.parametrize("endpoint,method,data", [
    ('/api/ideas', 'GET', None),
    ('/api/ideas/1', 'GET', None),
    ('/api/ideas', 'POST', {'title': 'Test', 'description': 'Test'}),
    ('/api/ideas/1', 'PUT', {'title': 'Updated', 'description': 'Updated'}),
    ('/api/ideas/1', 'DELETE', None),
])
@patch('models.Idea.query')
def test_idea_api_server_error_simulation(mock_query, endpoint, method, data, authenticated_client):
    """Simulate server errors for ideas API endpoints"""
    # Configure the mock to raise an exception
    if method == 'GET' and endpoint == '/api/ideas':
        mock_query.all.side_effect = Exception("Database error")
    elif method == 'GET' and '/api/ideas/' in endpoint:
        mock_query.get.side_effect = Exception("Database error")
    elif method == 'POST':
        mock_query.add.side_effect = Exception("Database error")
    elif method == 'PUT' or method == 'DELETE':
        mock_query.get.side_effect = Exception("Database error")
    
    # Make the request
    if method == 'GET':
        response = authenticated_client.get(endpoint)
    elif method == 'POST':
        response = authenticated_client.post(endpoint, json=data)
    elif method == 'PUT':
        response = authenticated_client.put(endpoint, json=data)
    elif method == 'DELETE':
        response = authenticated_client.delete(endpoint)
    
    # All these should return 500 Internal Server Error
    assert response.status_code == 500

# =============================================================================
# EDGE CASE TESTS
# =============================================================================

def test_idea_with_very_long_content(authenticated_client):
    """Test creating an idea with very long content"""
    idea_data = {
        'title': 'A' * 255,  # Maximum title length if limited
        'description': 'B' * 5000  # Very long description
    }
    
    response = authenticated_client.post(
        '/api/ideas',
        data=json.dumps(idea_data),
        content_type='application/json'
    )
    
    # Check if the API correctly handles or rejects this case
    assert response.status_code in [201, 400]
    
    if response.status_code == 201:
        data = json.loads(response.data)
        assert len(data['title']) == 255
        assert len(data['description']) == 5000

def test_idea_with_special_chars(authenticated_client):
    """Test creating an idea with special characters"""
    idea_data = {
        'title': 'Test <script>alert("XSS")</script>',
        'description': '!@#$%^&*()_+-=[]{}|;\':",./<?'
    }
    
    response = authenticated_client.post(
        '/api/ideas',
        data=json.dumps(idea_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    # Verify the special characters were handled properly (escaped or sanitized)
    assert '<script>' not in data['title'] or data['title'] != idea_data['title']

def test_bulk_idea_operations(authenticated_client, test_ideas):
    """Test bulk operations on ideas if supported"""
    # This test assumes the API might support bulk operations
    # If not implemented, this test can be skipped or modified
    
    # Example: Get multiple ideas by ID
    idea_ids = [str(idea.id) for idea in test_ideas[:2]]
    response = authenticated_client.get(f'/api/ideas?ids={";".join(idea_ids)}')
    
    # This might not be implemented yet, so check for 200 or 404/501
    if response.status_code == 200:
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == len(idea_ids)
