"""
Tests for Projects API endpoints
"""
import json
import pytest

# SUCCESS TESTS (200/201)

def test_get_projects_api(client):
    """Test getting all projects via API"""
    response = client.get('/api/projects')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0  # Should have test project from fixture
    
def test_get_single_project_api(client):
    """Test getting a single project via API"""
    # First get all projects
    response = client.get('/api/projects')
    assert response.status_code == 200
    projects = json.loads(response.data)
    assert len(projects) > 0
    
    # Get the first project
    project_id = projects[0]['id']
    response = client.get(f'/api/projects/{project_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'title' in data
    assert 'slug' in data

def test_create_project_api_valid(client):
    """Test creating a project with valid data"""
    project_data = {
        'title': 'New Project',
        'slug': 'new-project',
        'description': 'Description here',
        'is_featured': True
    }
    response = client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'New Project'
    assert data['slug'] == 'new-project'
    assert data['description'] == 'Description here'
    assert data['is_featured'] == True

def test_update_project_api_valid(client):
    """Test updating a project with valid data"""
    # First create a project
    project_data = {
        'title': 'Project to Update',
        'slug': 'project-to-update',
        'description': 'Will be updated'
    }
    create_response = client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    new_project = json.loads(create_response.data)
    
    # Update the project
    update_data = {
        'title': 'Updated Project',
        'description': 'Updated description',
        'is_featured': False
    }
    response = client.put(
        f'/api/projects/{new_project["id"]}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated Project'
    assert data['description'] == 'Updated description'
    assert data['is_featured'] == False

def test_delete_project_api_success(client):
    """Test deleting a project via API"""
    # First create a project to delete
    project_data = {
        'title': 'Project to Delete',
        'slug': 'project-to-delete',
        'description': 'Will be deleted'
    }
    create_response = client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    new_project = json.loads(create_response.data)
    
    # Delete the project
    response = client.delete(f'/api/projects/{new_project["id"]}')
    assert response.status_code == 204
    
    # Verify project is deleted
    get_response = client.get(f'/api/projects/{new_project["id"]}')
    assert get_response.status_code == 404

# VALIDATION FAILURE TESTS (400)

def test_create_project_api_invalid(client):
    """Test creating a project with invalid data (missing required field)"""
    project_data = {
        'description': 'Description without title',
        'is_featured': True
    }
    response = client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data

def test_create_project_api_duplicate_slug(client):
    """Test creating a project with duplicate slug fails validation"""
    # First create a project
    project_data = {
        'title': 'First Project',
        'slug': 'unique-slug',
        'description': 'First project'
    }
    create_response = client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    
    # Try to create another project with the same slug
    duplicate_data = {
        'title': 'Duplicate Slug Project',
        'slug': 'unique-slug',
        'description': 'This should fail with a validation error'
    }
    response = client.post(
        '/api/projects',
        data=json.dumps(duplicate_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data

def test_update_project_api_invalid(client):
    """Test updating a project with invalid data"""
    # First create a project
    project_data = {
        'title': 'Project to Update',
        'slug': 'project-for-invalid-update',
        'description': 'Will try invalid update'
    }
    create_response = client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    new_project = json.loads(create_response.data)
    
    # Try to update with invalid data
    update_data = {
        'title': ''  # Empty title should fail validation
    }
    response = client.put(
        f'/api/projects/{new_project["id"]}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data

# NOT FOUND TESTS (404)

def test_get_nonexistent_project_api(client):
    """Test getting a non-existent project returns 404"""
    response = client.get('/api/projects/999')
    assert response.status_code == 404

def test_update_nonexistent_project_api(client):
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

def test_delete_nonexistent_project_api(client):
    """Test deleting a non-existent project returns 404"""
    response = client.delete('/api/projects/999')
    assert response.status_code == 404

# SERVER ERROR TESTS (500)
# Note: In a real test environment, we would use monkeypatch to simulate server errors

def test_project_api_server_error_simulation(client):
    """
    Simulate a server error (this is a placeholder)
    In a real test environment, we would use monkeypatch to force an exception
    """
    # This test is a placeholder for the server error test case
    # The actual implementation would depend on how server errors are handled
    # in the application and the testing framework
    pass
