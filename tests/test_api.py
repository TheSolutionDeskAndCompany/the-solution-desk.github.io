"""
Tests for API endpoints with Marshmallow validation
"""
import json
import pytest
from flask import url_for

def test_get_projects_api(client):
    """Test getting all projects via API"""
    response = client.get('/api/projects')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'title' in data[0]
    assert 'slug' in data[0]

def test_get_single_project_api(client):
    """Test getting a single project via API"""
    response = client.get('/api/projects/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Test Project'
    assert data['slug'] == 'test-project'

def test_get_nonexistent_project_api(client):
    """Test getting a non-existent project returns 404"""
    response = client.get('/api/projects/999')
    assert response.status_code == 404

def test_create_project_api_valid(admin_client):
    """Test creating a project with valid data"""
    project_data = {
        'title': 'API Created Project',
        'slug': 'api-created-project',
        'description': 'Created via API',
        'is_featured': True
    }
    response = admin_client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == project_data['title']
    assert data['slug'] == project_data['slug']

def test_create_project_api_invalid(admin_client):
    """Test creating a project with invalid data (missing required field)"""
    project_data = {
        # Missing required 'title'
        'slug': 'invalid-project',
        'description': 'This should fail validation'
    }
    response = admin_client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data

def test_create_project_api_duplicate_title(admin_client):
    """Test creating a project with duplicate title fails validation"""
    project_data = {
        'title': 'Test Project',  # Already exists from fixture
        'slug': 'another-test-project',
        'description': 'Should fail due to duplicate title'
    }
    response = admin_client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data
    assert 'title' in data['errors']

def test_update_project_api_valid(admin_client):
    """Test updating a project with valid data"""
    project_data = {
        'title': 'Updated API Project',
        'description': 'Updated via API test'
    }
    response = admin_client.put(
        '/api/projects/1',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated API Project'
    assert data['description'] == 'Updated via API test'

def test_update_project_api_invalid(admin_client):
    """Test updating a project with invalid data"""
    project_data = {
        'title': '',  # Empty title should fail validation
        'description': 'Invalid update'
    }
    response = admin_client.put(
        '/api/projects/1',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data

def test_delete_project_api(admin_client):
    """Test deleting a project via API"""
    # First create a project to delete
    project_data = {
        'title': 'Project To Delete via API',
        'slug': 'api-delete-project',
        'description': 'Will be deleted in test'
    }
    create_response = admin_client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    created_id = json.loads(create_response.data)['id']
    
    # Now delete it
    response = admin_client.delete(f'/api/projects/{created_id}')
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = admin_client.get(f'/api/projects/{created_id}')
    assert get_response.status_code == 404

def test_api_error_handling(client):
    """Test API error responses are properly formatted as JSON"""
    response = client.get('/api/nonexistent-endpoint')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert 'message' in data
