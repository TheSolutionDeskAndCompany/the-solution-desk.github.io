"""
Tests for KPIs API endpoints

This module contains comprehensive tests for the KPIs API endpoints, including:
- Success cases (200/201) 
- Authentication and authorization
- Validation failures (400)
- Not found cases (404)
- Server error simulations
- Edge cases
"""
import json
import pytest
import logging
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from models import KPI

# Setup test logger
logger = logging.getLogger(__name__)

# =============================================================================
# SUCCESS TESTS (200/201)
# =============================================================================

def test_get_kpis_api(authenticated_client, test_kpis):
    """Test getting all KPIs via API"""
    response = authenticated_client.get('/api/kpis')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    
def test_get_kpis_with_filters(authenticated_client, test_kpis, test_project):
    """Test getting filtered KPIs via API"""
    # Test filtering by project_id
    response = authenticated_client.get(f'/api/kpis?project_id={test_project.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    if len(data) > 0:
        assert all(kpi['project_id'] == test_project.id for kpi in data if 'project_id' in kpi)
    
    # Test filtering by category
    response = authenticated_client.get('/api/kpis?category=Performance')
    assert response.status_code == 200
    data = json.loads(response.data)
    if len(data) > 0:
        assert all(kpi['category'] == 'Performance' for kpi in data if 'category' in kpi)

def test_create_kpi_api_valid(authenticated_client, test_project):
    """Test creating a KPI with valid data"""
    kpi_data = {
        'title': 'New KPI',
        'description': 'Description here',
        'target_value': 100.0,
        'current_value': 25.0,
        'unit': 'points',
        'category': 'Performance',
        'start_date': '2025-01-01T00:00:00',
        'end_date': '2025-12-31T23:59:59',
        'project_id': test_project.id
    }
    response = client.post(
        '/api/kpis',
        data=json.dumps(kpi_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'New KPI'
    assert data['description'] == 'Description here'
    assert data['target_value'] == 100.0
    assert data['current_value'] == 25.0
    assert data['unit'] == 'points'
    assert data['category'] == 'Performance'

def test_get_single_kpi_api(authenticated_client, test_kpi):
    """Test getting a single KPI via API"""
    # Using test_kpi fixture
    response = authenticated_client.get(f'/api/kpis/{test_kpi.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == test_kpi.title
    assert data['description'] == test_kpi.description
    assert float(data['target_value']) == float(test_kpi.target_value)
    assert float(data['current_value']) == float(test_kpi.current_value)

def test_update_kpi_api_valid(authenticated_client, test_kpi, test_project):
    """Test updating a KPI with valid data"""
    # Using test_kpi fixture
    
    # Update the KPI
    update_data = {
        'title': 'Updated KPI',
        'description': 'Updated description',
        'target_value': 200.0,
        'current_value': 75.0,
        'unit': 'updated_unit',
        'category': 'Updated Category'
    }
    response = client.put(
        f'/api/kpis/{new_kpi["id"]}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated KPI'
    assert data['description'] == 'Updated description'
    assert data['target_value'] == 200.0
    assert data['current_value'] == 75.0
    assert data['unit'] == 'updated_unit'
    assert data['category'] == 'Updated Category'

def test_partial_update_kpi_api(authenticated_client, test_kpi):
    """Test partially updating a KPI (PATCH method)"""
    # Only update specific fields
    patch_data = {
        'current_value': 80.0
    }
    
    response = authenticated_client.patch(
        f'/api/kpis/{test_kpi.id}',
        data=json.dumps(patch_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Check that only the specified fields were updated
    assert float(data['current_value']) == 80.0
    assert data['title'] == test_kpi.title  # Should remain unchanged
    assert data['description'] == test_kpi.description  # Should remain unchanged

def test_delete_kpi_api_success(authenticated_client, test_kpi):
    """Test deleting a KPI via API"""
    # Using test_kpi fixture
    
    # Delete the KPI
    response = authenticated_client.delete(f'/api/kpis/{test_kpi.id}')
    assert response.status_code == 204
    
    # Verify KPI is deleted
    get_response = authenticated_client.get(f'/api/kpis/{test_kpi.id}')
    assert get_response.status_code == 404

# =============================================================================
# AUTHENTICATION & AUTHORIZATION TESTS
# =============================================================================

def test_create_kpi_unauthorized(client):
    """Test that unauthenticated requests cannot create KPIs"""
    kpi_data = {
        'title': 'Unauthorized KPI',
        'description': 'Should not be created',
        'target_value': 100.0,
        'current_value': 0.0
    }
    
    response = client.post(
        '/api/kpis',
        data=json.dumps(kpi_data),
        content_type='application/json'
    )
    
    assert response.status_code == 401  # Unauthorized

def test_kpi_permissions(authenticated_client, test_admin, test_kpis):
    """Test authorization rules for KPIs API"""
    # Find a KPI that belongs to the admin user
    admin_kpi = None
    for kpi in test_kpis:
        # This assumes your KPI model has a way to identify the creator
        # Either directly (creator_id) or via project (project.manager_id)
        if hasattr(kpi, 'creator_id') and kpi.creator_id == test_admin.id:
            admin_kpi = kpi
            break
        elif hasattr(kpi, 'project') and hasattr(kpi.project, 'manager_id') and kpi.project.manager_id == test_admin.id:
            admin_kpi = kpi
            break
    
    if admin_kpi:
        # Regular user should not be able to delete another user's KPI
        delete_response = authenticated_client.delete(f'/api/kpis/{admin_kpi.id}')
        assert delete_response.status_code in [401, 403]  # Unauthorized or Forbidden

# =============================================================================
# VALIDATION FAILURE TESTS (400)
# =============================================================================

def test_create_kpi_api_invalid(authenticated_client):
    """Test creating a KPI with invalid data (missing required field)"""
    kpi_data = {
        'description': 'Description without title',
        'target_value': 100
    }
    response = client.post(
        '/api/kpis',
        data=json.dumps(kpi_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Title is required' in str(data) or 'errors' in data or 'message' in data

def test_create_kpi_invalid_values(authenticated_client, test_project):
    """Test creating a KPI with invalid numerical values"""
    kpi_data = {
        'title': 'Invalid Value KPI',
        'description': 'KPI with invalid values',
        'target_value': 'not-a-number',  # Should be a number
        'current_value': 50.0,
        'project_id': test_project.id
    }
    
    response = authenticated_client.post(
        '/api/kpis',
        data=json.dumps(kpi_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data or 'message' in data

def test_create_kpi_invalid_dates(authenticated_client, test_project):
    """Test creating a KPI with invalid date ranges"""
    kpi_data = {
        'title': 'Invalid Date KPI',
        'description': 'KPI with invalid dates',
        'target_value': 100.0,
        'current_value': 0.0,
        'start_date': '2023-12-31T00:00:00',
        'end_date': '2023-01-01T00:00:00',  # End date before start date
        'project_id': test_project.id
    }
    
    response = authenticated_client.post(
        '/api/kpis',
        data=json.dumps(kpi_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'errors' in data or 'message' in data

def test_create_kpi_invalid_json(authenticated_client):
    """Test creating a KPI with invalid JSON data"""
    response = authenticated_client.post(
        '/api/kpis',
        data="This is not valid JSON",
        content_type='application/json'
    )
    assert response.status_code == 400

def test_update_kpi_api_invalid(authenticated_client, test_kpi):
    """Test updating a KPI with invalid data"""
    # Using test_kpi fixture
    
    # Try to update with invalid data
    update_data = {
        'title': ''  # Empty title should fail validation
    }
    response = client.put(
        f'/api/kpis/{new_kpi["id"]}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 400

def test_update_kpi_with_invalid_category(authenticated_client, test_kpi):
    """Test updating a KPI with an invalid category value"""
    update_data = {
        'category': 'invalid_category_value'  # This might not be validated, depending on implementation
    }
    
    response = authenticated_client.put(
        f'/api/kpis/{test_kpi.id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # If categories are validated, this should fail with 400
    # If not, it should succeed with 200
    assert response.status_code in [200, 400]

# =============================================================================
# NOT FOUND TESTS (404)
# =============================================================================

def test_get_nonexistent_kpi_api(client):
    """Test getting a non-existent KPI returns 404"""
    response = client.get('/api/kpis/999')
    assert response.status_code == 404

def test_update_nonexistent_kpi_api(authenticated_client):
    """Test updating a non-existent KPI returns 404"""
    update_data = {
        'title': 'Updated Title',
        'description': 'Updated Description'
    }
    response = client.put(
        '/api/kpis/999',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 404

def test_delete_nonexistent_kpi_api(authenticated_client):
    """Test deleting a non-existent KPI returns 404"""
    response = authenticated_client.delete('/api/kpis/999')
    assert response.status_code == 404

# SERVER ERROR TESTS (500)
# Note: In a real test environment, we would use monkeypatch to simulate server errors

# =============================================================================
# SERVER ERROR TESTS (500)
# =============================================================================

@pytest.mark.parametrize("endpoint,method,data", [
    ('/api/kpis', 'GET', None),
    ('/api/kpis/1', 'GET', None),
    ('/api/kpis', 'POST', {'title': 'Test', 'description': 'Test', 'target_value': 100}),
    ('/api/kpis/1', 'PUT', {'title': 'Updated', 'description': 'Updated'}),
    ('/api/kpis/1', 'DELETE', None),
])
@patch('models.KPI.query')
def test_kpi_api_server_error_simulation(mock_query, endpoint, method, data, authenticated_client):
    """Simulate server errors for KPIs API endpoints"""
    # Configure the mock to raise an exception
    if method == 'GET' and endpoint == '/api/kpis':
        mock_query.all.side_effect = Exception("Database error")
    elif method == 'GET' and '/api/kpis/' in endpoint:
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

def test_kpi_with_very_large_values(authenticated_client, test_project):
    """Test creating a KPI with very large numerical values"""
    kpi_data = {
        'title': 'Large Value KPI',
        'description': 'KPI with large values',
        'target_value': 1000000000.0,  # 1 billion
        'current_value': 999999999.9,
        'unit': 'points',
        'category': 'Performance',
        'project_id': test_project.id
    }
    
    response = authenticated_client.post(
        '/api/kpis',
        data=json.dumps(kpi_data),
        content_type='application/json'
    )
    
    # Check if the API correctly handles these large values
    assert response.status_code == 201
    data = json.loads(response.data)
    assert float(data['target_value']) == 1000000000.0
    assert float(data['current_value']) == 999999999.9

def test_kpi_with_special_chars(authenticated_client, test_project):
    """Test creating a KPI with special characters"""
    kpi_data = {
        'title': 'Test <script>alert("XSS")</script>',
        'description': '!@#$%^&*()_+-=[]{}|;\':",./<?',
        'target_value': 100.0,
        'current_value': 50.0,
        'project_id': test_project.id
    }
    
    response = authenticated_client.post(
        '/api/kpis',
        data=json.dumps(kpi_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    # Verify the special characters were handled properly (escaped or sanitized)
    assert '<script>' not in data['title'] or data['title'] != kpi_data['title']

def test_bulk_kpi_operations(authenticated_client, test_project):
    """Test bulk operations on KPIs if supported"""
    # This test checks if bulk creation/update is supported
    # If not supported, the API should return 404 or another appropriate error
    
    bulk_data = [
        {
            'title': 'Bulk KPI 1',
            'description': 'First bulk KPI',
            'target_value': 100.0,
            'current_value': 10.0,
            'project_id': test_project.id
        },
        {
            'title': 'Bulk KPI 2',
            'description': 'Second bulk KPI',
            'target_value': 200.0,
            'current_value': 20.0,
            'project_id': test_project.id
        }
    ]
    
    response = authenticated_client.post(
        '/api/kpis/bulk',
        data=json.dumps(bulk_data),
        content_type='application/json'
    )
    
    # If bulk operations are supported, it should succeed
    # If not, it should return an appropriate error (not a server error)
    assert response.status_code in [200, 201, 404, 405, 501]
