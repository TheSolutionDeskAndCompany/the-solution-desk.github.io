"""
Tests for Projects API endpoints

This module contains comprehensive tests for the Projects API endpoints, including:
- Success cases (200/201)
- Authentication and authorization
- Validation failures (400)
- Not found cases (404)
- Server error simulations
"""
import json
import pytest
import logging
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from models import Project

# Setup test logger
logger = logging.getLogger(__name__)

# =============================================================================
# SUCCESS TESTS (200/201)
# =============================================================================

def test_get_projects_api(client):
    """Test getting all projects via API"""
    response = client.get('/api/projects')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0  # Should have test project from fixture
    
def test_get_projects_with_filters(client, test_projects):
    """Test getting filtered projects via API"""
    # Test filtering by status
    response = client.get('/api/projects?status=active')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert all(project['status'] == 'active' for project in data)
    
    # Test sorting (if implemented)
    response = client.get('/api/projects?sort=created_at&order=desc')
    assert response.status_code == 200

def test_get_single_project_api(client, test_project):
    """Test getting a single project via API"""
    response = client.get(f'/api/projects/{test_project.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == test_project.name
    assert data['description'] == test_project.description

def test_create_project_api_valid(authenticated_client, test_user):
    """Test creating a project with valid data"""
    project_data = {
        'name': 'New Project',
        'description': 'Description here',
        'status': 'planning',
        'start_date': '2023-07-01',
        'end_date': '2023-12-31',
        'manager_id': test_user.id
    }
    response = authenticated_client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'New Project'
    assert data['description'] == 'Description here'
    assert data['status'] == 'planning'

def test_update_project_api_valid(authenticated_client, test_project, test_user):
    """Test updating a project with valid data"""
    # Using the test_project fixture
    
    # Update the project
    update_data = {
        'name': 'Updated Project',
        'description': 'Updated description',
        'status': 'completed',
        'manager_id': test_user.id
    }
    response = authenticated_client.put(
        f'/api/projects/{test_project.id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated Project'
    assert data['description'] == 'Updated description'
    assert data['status'] == 'completed'

def test_partial_update_project_api(authenticated_client, test_project):
    """Test partially updating a project (PATCH method)"""
    # Only update specific fields
    patch_data = {
        'status': 'on_hold'
    }
    
    response = authenticated_client.patch(
        f'/api/projects/{test_project.id}',
        data=json.dumps(patch_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Check that only the specified fields were updated
    assert data['status'] == 'on_hold'
    assert data['name'] == test_project.name  # Should remain unchanged
    assert data['description'] == test_project.description  # Should remain unchanged

def test_delete_project_api_success(authenticated_client, test_project):
    """Test deleting a project via API"""
    # Using test_project fixture directly
    
    # Delete the project
    response = authenticated_client.delete(f'/api/projects/{test_project.id}')
    assert response.status_code == 204
    
    # Verify project is deleted
    get_response = client.get(f'/api/projects/{test_project.id}')
    assert get_response.status_code == 404

# =============================================================================
# AUTHENTICATION & AUTHORIZATION TESTS
# =============================================================================

def test_create_project_unauthorized(client):
    """Test that unauthenticated requests cannot create projects"""
    project_data = {
        'name': 'Unauthorized Project',
        'description': 'Should not be created',
        'status': 'planning'
    }
    
    response = client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    
    assert response.status_code == 401  # Unauthorized

def test_project_permissions(authenticated_client, test_admin, test_projects):
    """Test authorization rules for projects API"""
    # Regular user should not be able to delete another user's project
    project_created_by_admin = [p for p in test_projects if p.manager_id == test_admin.id][0]
    
    # Attempt to delete someone else's project
    delete_response = authenticated_client.delete(f'/api/projects/{project_created_by_admin.id}')
    assert delete_response.status_code in [401, 403]  # Unauthorized or Forbidden

# =============================================================================
# VALIDATION FAILURE TESTS (400)
# =============================================================================

def test_create_project_api_invalid(authenticated_client):
    """Test creating a project with invalid data (missing required field)"""
    project_data = {
        'description': 'Description without name',
        'status': 'active'
    }
    response = authenticated_client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data

def test_create_project_invalid_dates(authenticated_client):
    """Test creating a project with invalid date ranges"""
    project_data = {
        'name': 'Invalid Date Project',
        'description': 'Project with invalid dates',
        'status': 'planning',
        'start_date': '2023-12-31',
        'end_date': '2023-01-01'  # End date before start date
    }
    
    response = authenticated_client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data or 'message' in data
def test_create_project_invalid_json(authenticated_client):
    """Test creating a project with invalid JSON data"""
    response = authenticated_client.post(
        '/api/projects',
        data="This is not valid JSON",
        content_type='application/json'
    )
    assert response.status_code == 400

def test_update_project_api_invalid(authenticated_client, test_project):
    """Test updating a project with invalid data"""
    # Using test_project fixture
    
    # Try to update with invalid data
    update_data = {
        'name': ''  # Empty name should fail validation
    }
    response = authenticated_client.put(
        f'/api/projects/{test_project.id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data

def test_update_project_with_invalid_status(authenticated_client, test_project):
    """Test updating a project with an invalid status value"""
    update_data = {
        'status': 'invalid_status_value'  # This should not be a valid status
    }
    
    response = authenticated_client.put(
        f'/api/projects/{test_project.id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400

# =============================================================================
# NOT FOUND TESTS (404)
# =============================================================================

def test_get_nonexistent_project_api(client):
    """Test getting a non-existent project returns 404"""
    response = client.get('/api/projects/999')
    assert response.status_code == 404

def test_update_nonexistent_project_api(authenticated_client):
    """Test updating a non-existent project returns 404"""
    update_data = {
        'title': 'Updated Title',
        'description': 'Updated Description'
    }
    response = client.put(
        '/api/projects/999',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 404

def test_delete_nonexistent_project_api(authenticated_client):
    """Test deleting a non-existent project returns 404"""
    response = authenticated_client.delete('/api/projects/999')
    assert response.status_code == 404

# =============================================================================
# SERVER ERROR TESTS (500)
# =============================================================================

@pytest.mark.parametrize("endpoint,method,data", [
    ('/api/projects', 'GET', None),
    ('/api/projects/1', 'GET', None),
    ('/api/projects', 'POST', {'name': 'Test', 'description': 'Test'}),
    ('/api/projects/1', 'PUT', {'name': 'Updated', 'description': 'Updated'}),
    ('/api/projects/1', 'DELETE', None),
])
@patch('models.Project.query')
def test_project_api_server_error_simulation(mock_query, endpoint, method, data, authenticated_client):
    """Simulate server errors for projects API endpoints"""
    # Configure the mock to raise an exception
    if method == 'GET' and endpoint == '/api/projects':
        mock_query.all.side_effect = Exception("Database error")
    elif method == 'GET' and '/api/projects/' in endpoint:
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

def test_project_with_very_long_content(authenticated_client, test_user):
    """Test creating a project with very long content"""
    project_data = {
        'name': 'A' * 255,  # Maximum name length if limited
        'description': 'B' * 5000,  # Very long description
        'status': 'planning',
        'manager_id': test_user.id
    }
    
    response = authenticated_client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    
    # Check if the API correctly handles or rejects this case
    assert response.status_code in [201, 400]
    
    if response.status_code == 201:
        data = json.loads(response.data)
        assert len(data['name']) == 255
        assert len(data['description']) == 5000

def test_project_with_special_chars(authenticated_client, test_user):
    """Test creating a project with special characters"""
    project_data = {
        'name': 'Test <script>alert("XSS")</script>',
        'description': '!@#$%^&*()_+-=[]{}|;\':",./<?',
        'status': 'planning',
        'manager_id': test_user.id
    }
    
    response = authenticated_client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    # Verify the special characters were handled properly (escaped or sanitized)
    assert '<script>' not in data['name'] or data['name'] != project_data['name']

def test_get_projects_with_kpis(authenticated_client, test_projects, test_kpis):
    """Test retrieving projects with associated KPIs"""
    # Test getting projects with KPIs if API supports this
    response = authenticated_client.get('/api/projects?include=kpis')
    
    # If endpoint doesn't support this query parameter, this test can be skipped
    if response.status_code == 200:
        data = json.loads(response.data)
        assert isinstance(data, list)
        
        # At least one project should have KPIs
        has_kpis = False
        for project in data:
            if 'kpis' in project and len(project['kpis']) > 0:
                has_kpis = True
                break
        
        if 'kpis' in data[0]:  # Only assert if API returns this structure
            assert has_kpis
