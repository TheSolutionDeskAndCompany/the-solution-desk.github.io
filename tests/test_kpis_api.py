"""
Tests for KPIs API endpoints
"""
import json
import pytest
from datetime import datetime

# SUCCESS TESTS (200/201)

def test_get_kpis_api(client):
    """Test getting all KPIs via API"""
    response = client.get('/api/kpis')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    
def test_create_kpi_api_valid(client):
    """Test creating a KPI with valid data"""
    kpi_data = {
        'title': 'New KPI',
        'description': 'Description here',
        'target_value': 100.0,
        'current_value': 25.0,
        'unit': 'points',
        'category': 'Performance',
        'start_date': '2025-01-01T00:00:00',
        'end_date': '2025-12-31T23:59:59'
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

def test_get_single_kpi_api(client):
    """Test getting a single KPI via API"""
    # First create a KPI
    kpi_data = {
        'title': 'Test KPI', 
        'description': 'Test Description',
        'target_value': 100.0,
        'current_value': 50.0,
        'unit': 'percent',
        'category': 'Test Category'
    }
    create_response = client.post(
        '/api/kpis',
        data=json.dumps(kpi_data),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    new_kpi = json.loads(create_response.data)
    
    # Now get the KPI
    response = client.get(f'/api/kpis/{new_kpi["id"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Test KPI'
    assert data['description'] == 'Test Description'
    assert data['target_value'] == 100.0
    assert data['current_value'] == 50.0

def test_update_kpi_api_valid(client):
    """Test updating a KPI with valid data"""
    # First create a KPI
    kpi_data = {
        'title': 'Original KPI', 
        'description': 'Original description',
        'target_value': 100.0,
        'current_value': 0.0
    }
    create_response = client.post(
        '/api/kpis',
        data=json.dumps(kpi_data),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    new_kpi = json.loads(create_response.data)
    
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

def test_delete_kpi_api_success(client):
    """Test deleting a KPI via API"""
    # First create a KPI to delete
    kpi_data = {
        'title': 'KPI to Delete',
        'description': 'Will be deleted'
    }
    create_response = client.post(
        '/api/kpis',
        data=json.dumps(kpi_data),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    new_kpi = json.loads(create_response.data)
    
    # Delete the KPI
    response = client.delete(f'/api/kpis/{new_kpi["id"]}')
    assert response.status_code == 204
    
    # Verify KPI is deleted
    get_response = client.get(f'/api/kpis/{new_kpi["id"]}')
    assert get_response.status_code == 404

# VALIDATION FAILURE TESTS (400)

def test_create_kpi_api_invalid(client):
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

def test_update_kpi_api_invalid(client):
    """Test updating a KPI with invalid data"""
    # First create a KPI
    kpi_data = {
        'title': 'Original KPI',
        'description': 'Original description'
    }
    create_response = client.post(
        '/api/kpis',
        data=json.dumps(kpi_data),
        content_type='application/json'
    )
    assert create_response.status_code == 201
    new_kpi = json.loads(create_response.data)
    
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

# NOT FOUND TESTS (404)

def test_get_nonexistent_kpi_api(client):
    """Test getting a non-existent KPI returns 404"""
    response = client.get('/api/kpis/999')
    assert response.status_code == 404

def test_update_nonexistent_kpi_api(client):
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

def test_delete_nonexistent_kpi_api(client):
    """Test deleting a non-existent KPI returns 404"""
    response = client.delete('/api/kpis/999')
    assert response.status_code == 404

# SERVER ERROR TESTS (500)
# Note: In a real test environment, we would use monkeypatch to simulate server errors

def test_kpi_api_server_error_simulation(client):
    """
    Simulate a server error (this is a placeholder)
    In a real test environment, we would use monkeypatch to force an exception
    """
    # This test is a placeholder for the server error test case
    # The actual implementation would depend on how server errors are handled
    # in the application and the testing framework
    pass
