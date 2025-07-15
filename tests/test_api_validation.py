"""
API Validation Tests
This module contains tests that validate API responses against schemas,
check for common security issues, and ensure proper error handling.
"""

import json
import pytest
from flask import url_for
import jsonschema
from app import create_app
from models import db, User, Project, Idea, KPI
from tests.conftest import app, client, test_user, test_project, test_idea, test_kpi

# Define JSON schemas for validation
idea_schema = {
    "type": "object",
    "required": ["id", "title", "description", "status", "created_at", "updated_at"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "status": {"type": "string", "enum": ["new", "in_progress", "completed", "archived"]},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
        "priority": {"type": ["integer", "null"]},
        "creator_id": {"type": ["integer", "null"]},
    },
    "additionalProperties": False
}

project_schema = {
    "type": "object",
    "required": ["id", "name", "description", "status", "created_at", "updated_at"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "status": {"type": "string", "enum": ["planning", "active", "completed", "on_hold"]},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
        "manager_id": {"type": ["integer", "null"]}
    },
    "additionalProperties": False
}

kpi_schema = {
    "type": "object",
    "required": ["id", "name", "description", "target_value", "created_at", "updated_at"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "target_value": {"type": "number"},
        "current_value": {"type": ["number", "null"]},
        "unit": {"type": ["string", "null"]},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
        "project_id": {"type": ["integer", "null"]}
    },
    "additionalProperties": False
}


class TestAPIValidation:
    """Test API endpoints for proper response structure and security"""

    def test_ideas_endpoint_schema_validation(self, client, test_user, test_idea):
        """Test that the ideas endpoint returns valid schema"""
        # Login user first
        login_response = client.post('/auth/login',
                                    json={'email': 'test@example.com', 'password': 'password'})
        token = json.loads(login_response.data).get('token')

        # Get ideas with token
        response = client.get('/api/ideas',
                            headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify the response is a list
        assert isinstance(data, list)
        
        # Validate each idea against our schema
        for idea in data:
            try:
                jsonschema.validate(instance=idea, schema=idea_schema)
            except jsonschema.exceptions.ValidationError as e:
                pytest.fail(f"Response does not match schema: {e}")

    def test_projects_endpoint_schema_validation(self, client, test_user, test_project):
        """Test that the projects endpoint returns valid schema"""
        # Login user first
        login_response = client.post('/auth/login',
                                    json={'email': 'test@example.com', 'password': 'password'})
        token = json.loads(login_response.data).get('token')

        # Get projects with token
        response = client.get('/api/projects',
                            headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify the response is a list
        assert isinstance(data, list)
        
        # Validate each project against our schema
        for project in data:
            try:
                jsonschema.validate(instance=project, schema=project_schema)
            except jsonschema.exceptions.ValidationError as e:
                pytest.fail(f"Response does not match schema: {e}")

    def test_kpis_endpoint_schema_validation(self, client, test_user, test_kpi):
        """Test that the KPIs endpoint returns valid schema"""
        # Login user first
        login_response = client.post('/auth/login',
                                    json={'email': 'test@example.com', 'password': 'password'})
        token = json.loads(login_response.data).get('token')

        # Get KPIs with token
        response = client.get('/api/kpis',
                            headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify the response is a list
        assert isinstance(data, list)
        
        # Validate each KPI against our schema
        for kpi in data:
            try:
                jsonschema.validate(instance=kpi, schema=kpi_schema)
            except jsonschema.exceptions.ValidationError as e:
                pytest.fail(f"Response does not match schema: {e}")

    def test_api_security_headers(self, client):
        """Test that the API returns proper security headers"""
        response = client.get('/health')
        
        # Check for security headers
        headers = response.headers
        
        # Check for typical security headers (these may vary based on your app's configuration)
        # These tests may need adjustment based on your actual security header setup
        assert 'Content-Type' in headers
        assert 'X-Content-Type-Options' in headers or 'Content-Security-Policy' in headers
        
        # Check that sensitive headers are not exposed
        assert 'Server' not in headers or headers['Server'] == 'Flask'
        assert 'X-Powered-By' not in headers

    def test_unauthorized_access_rejection(self, client):
        """Test that unauthorized access is properly rejected"""
        # Try accessing protected endpoint without authentication
        response = client.get('/api/projects')
        
        # Should get 401 Unauthorized
        assert response.status_code == 401
        
        data = json.loads(response.data)
        # Check for proper error structure
        assert 'error' in data
        assert isinstance(data['error'], str)

    def test_invalid_input_handling(self, client, test_user):
        """Test that API properly handles invalid input"""
        # Login user first
        login_response = client.post('/auth/login',
                                    json={'email': 'test@example.com', 'password': 'password'})
        token = json.loads(login_response.data).get('token')
        
        # Try creating a project with invalid data
        invalid_project = {
            "name": "",  # Empty name should be rejected
            "description": "Test description",
            "status": "invalid_status"  # Invalid status should be rejected
        }
        
        response = client.post('/api/projects',
                              json=invalid_project,
                              headers={'Authorization': f'Bearer {token}'})
        
        # Should get 400 Bad Request
        assert response.status_code == 400
        
        data = json.loads(response.data)
        # Check for proper error structure
        assert 'error' in data
        assert isinstance(data['error'], str)

    def test_sql_injection_protection(self, client, test_user):
        """Test basic protection against SQL injection"""
        # Login user first
        login_response = client.post('/auth/login',
                                    json={'email': 'test@example.com', 'password': 'password'})
        token = json.loads(login_response.data).get('token')
        
        # Try a basic SQL injection in a query parameter
        response = client.get('/api/ideas?title=test\' OR \'1\'=\'1',
                            headers={'Authorization': f'Bearer {token}'})
        
        # Should still get 200 OK but not expose all records
        assert response.status_code == 200
        
        # Parse response
        data = json.loads(response.data)
        
        # If SQL injection worked, we'd get all ideas back regardless of title
        # Since we're using SQLAlchemy with parameterized queries, this should be safe
        # This is a simple verification that not all records are returned
        assert len(data) <= 1
