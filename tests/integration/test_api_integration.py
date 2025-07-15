"""
Integration tests for The Solution Desk API
These tests make real HTTP requests to a running test server.
"""

import os
import pytest
import requests
import subprocess
import time
import signal
import json
from datetime import datetime

# Test server configuration
TEST_HOST = "127.0.0.1"
TEST_PORT = 5001  # Using a different port than development
BASE_URL = f"http://{TEST_HOST}:{TEST_PORT}"
SERVER_PROCESS = None

def setup_module():
    """Start the Flask server for integration testing"""
    global SERVER_PROCESS
    env = os.environ.copy()
    env["FLASK_ENV"] = "testing"
    env["DATABASE_URL"] = "sqlite:///test_integration.db"
    
    # Start server as a background process
    SERVER_PROCESS = subprocess.Popen(
        ["flask", "run", "--host", TEST_HOST, "--port", str(TEST_PORT)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Give the server time to start
    time.sleep(2)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            raise Exception("Server did not start correctly")
    except Exception as e:
        if SERVER_PROCESS:
            SERVER_PROCESS.terminate()
        raise Exception(f"Failed to start test server: {str(e)}")

def teardown_module():
    """Shutdown the Flask server after testing"""
    if SERVER_PROCESS:
        SERVER_PROCESS.terminate()
        SERVER_PROCESS.wait()

class TestIdeasAPIIntegration:
    """Integration tests for the Ideas API endpoints"""
    
    def test_get_all_ideas(self):
        """Test retrieving all ideas"""
        response = requests.get(f"{BASE_URL}/api/ideas")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_and_get_idea(self):
        """Test creating a new idea and retrieving it"""
        # Create a new idea
        idea_data = {
            "title": "Integration Test Idea",
            "description": "This idea was created during integration testing",
            "status": "new",
            "priority": 3
        }
        
        create_response = requests.post(
            f"{BASE_URL}/api/ideas",
            json=idea_data,
            headers={"Content-Type": "application/json"}
        )
        assert create_response.status_code == 201
        
        created_idea = create_response.json()
        idea_id = created_idea["id"]
        
        # Retrieve the created idea
        get_response = requests.get(f"{BASE_URL}/api/ideas/{idea_id}")
        assert get_response.status_code == 200
        retrieved_idea = get_response.json()
        
        # Verify the idea was created correctly
        assert retrieved_idea["title"] == idea_data["title"]
        assert retrieved_idea["description"] == idea_data["description"]
        assert retrieved_idea["status"] == idea_data["status"]
        assert retrieved_idea["priority"] == idea_data["priority"]
    
    def test_update_idea(self):
        """Test updating an existing idea"""
        # Create a new idea first
        idea_data = {
            "title": "Idea to Update",
            "description": "This idea will be updated",
            "status": "new",
            "priority": 2
        }
        
        create_response = requests.post(
            f"{BASE_URL}/api/ideas",
            json=idea_data,
            headers={"Content-Type": "application/json"}
        )
        assert create_response.status_code == 201
        
        created_idea = create_response.json()
        idea_id = created_idea["id"]
        
        # Update the idea
        update_data = {
            "title": "Updated Idea Title",
            "description": "This idea has been updated",
            "status": "in_progress",
            "priority": 1
        }
        
        update_response = requests.put(
            f"{BASE_URL}/api/ideas/{idea_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        assert update_response.status_code == 200
        
        updated_idea = update_response.json()
        assert updated_idea["title"] == update_data["title"]
        assert updated_idea["status"] == update_data["status"]
    
    def test_delete_idea(self):
        """Test deleting an idea"""
        # Create a new idea first
        idea_data = {
            "title": "Idea to Delete",
            "description": "This idea will be deleted",
            "status": "new",
            "priority": 4
        }
        
        create_response = requests.post(
            f"{BASE_URL}/api/ideas",
            json=idea_data,
            headers={"Content-Type": "application/json"}
        )
        assert create_response.status_code == 201
        
        created_idea = create_response.json()
        idea_id = created_idea["id"]
        
        # Delete the idea
        delete_response = requests.delete(f"{BASE_URL}/api/ideas/{idea_id}")
        assert delete_response.status_code == 204
        
        # Verify the idea no longer exists
        get_response = requests.get(f"{BASE_URL}/api/ideas/{idea_id}")
        assert get_response.status_code == 404


class TestProjectsAPIIntegration:
    """Integration tests for the Projects API endpoints"""
    
    def test_get_all_projects(self):
        """Test retrieving all projects"""
        response = requests.get(f"{BASE_URL}/api/projects")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_and_get_project(self):
        """Test creating a new project and retrieving it"""
        # Create a new project
        project_data = {
            "title": "Integration Test Project",
            "description": "This project was created during integration testing",
            "long_description": "This is a detailed description for integration testing",
            "slug": "integration-test-project",
            "github_url": "https://github.com/test/integration-project",
            "download_url": "/downloads/integration-test-project.zip",
            "is_featured": True
        }
        
        create_response = requests.post(
            f"{BASE_URL}/api/projects",
            json=project_data,
            headers={"Content-Type": "application/json"}
        )
        assert create_response.status_code == 201
        
        created_project = create_response.json()
        project_id = created_project["id"]
        
        # Retrieve the created project
        get_response = requests.get(f"{BASE_URL}/api/projects/{project_id}")
        assert get_response.status_code == 200
        retrieved_project = get_response.json()
        
        # Verify the project was created correctly
        assert retrieved_project["title"] == project_data["title"]
        assert retrieved_project["slug"] == project_data["slug"]
    
    def test_update_project(self):
        """Test updating an existing project"""
        # Create a new project first
        project_data = {
            "title": "Project to Update",
            "description": "This project will be updated",
            "long_description": "This is a detailed description",
            "slug": "project-to-update",
            "github_url": "https://github.com/test/update-project",
            "download_url": "/downloads/update-project.zip",
            "is_featured": False
        }
        
        create_response = requests.post(
            f"{BASE_URL}/api/projects",
            json=project_data,
            headers={"Content-Type": "application/json"}
        )
        assert create_response.status_code == 201
        
        created_project = create_response.json()
        project_id = created_project["id"]
        
        # Update the project
        update_data = {
            "title": "Updated Project Title",
            "description": "This project has been updated",
            "is_featured": True
        }
        
        update_response = requests.put(
            f"{BASE_URL}/api/projects/{project_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        assert update_response.status_code == 200
        
        updated_project = update_response.json()
        assert updated_project["title"] == update_data["title"]
        assert updated_project["is_featured"] == update_data["is_featured"]


class TestKPIsAPIIntegration:
    """Integration tests for the KPIs API endpoints"""
    
    def test_get_all_kpis(self):
        """Test retrieving all KPIs"""
        response = requests.get(f"{BASE_URL}/api/kpis")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_and_get_kpi(self):
        """Test creating a new KPI and retrieving it"""
        # Create a new KPI
        today = datetime.now().strftime("%Y-%m-%d")
        end_date = "2025-12-31"
        
        kpi_data = {
            "title": "Integration Test KPI",
            "description": "This KPI was created during integration testing",
            "target_value": 100.0,
            "current_value": 50.0,
            "unit": "percent",
            "category": "Performance",
            "start_date": today,
            "end_date": end_date
        }
        
        create_response = requests.post(
            f"{BASE_URL}/api/kpis",
            json=kpi_data,
            headers={"Content-Type": "application/json"}
        )
        assert create_response.status_code == 201
        
        created_kpi = create_response.json()
        kpi_id = created_kpi["id"]
        
        # Retrieve the created KPI
        get_response = requests.get(f"{BASE_URL}/api/kpis/{kpi_id}")
        assert get_response.status_code == 200
        retrieved_kpi = get_response.json()
        
        # Verify the KPI was created correctly
        assert retrieved_kpi["title"] == kpi_data["title"]
        assert retrieved_kpi["description"] == kpi_data["description"]
        assert float(retrieved_kpi["target_value"]) == kpi_data["target_value"]
    
    def test_update_kpi(self):
        """Test updating an existing KPI"""
        # Create a new KPI first
        today = datetime.now().strftime("%Y-%m-%d")
        end_date = "2025-12-31"
        
        kpi_data = {
            "title": "KPI to Update",
            "description": "This KPI will be updated",
            "target_value": 200.0,
            "current_value": 75.0,
            "unit": "count",
            "category": "Engagement",
            "start_date": today,
            "end_date": end_date
        }
        
        create_response = requests.post(
            f"{BASE_URL}/api/kpis",
            json=kpi_data,
            headers={"Content-Type": "application/json"}
        )
        assert create_response.status_code == 201
        
        created_kpi = create_response.json()
        kpi_id = created_kpi["id"]
        
        # Update the KPI
        update_data = {
            "title": "Updated KPI Title",
            "current_value": 100.0,
            "category": "Updated Category"
        }
        
        update_response = requests.put(
            f"{BASE_URL}/api/kpis/{kpi_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        assert update_response.status_code == 200
        
        updated_kpi = update_response.json()
        assert updated_kpi["title"] == update_data["title"]
        assert float(updated_kpi["current_value"]) == update_data["current_value"]
