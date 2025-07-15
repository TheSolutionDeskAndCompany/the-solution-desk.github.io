"""
Load testing configuration for The Solution Desk application
Run with: locust -f tests/performance/locustfile.py
"""

import time
import json
import random
from locust import HttpUser, task, between


class APIUser(HttpUser):
    """
    Simulates users accessing the API endpoints with typical usage patterns.
    Includes authentication and CRUD operations on ideas, projects, and KPIs.
    """
    wait_time = between(1, 5)  # Wait between 1 and 5 seconds between tasks
    
    def on_start(self):
        """
        Authenticate user at the start of simulation
        """
        self.login()
        self.api_token = None
    
    def login(self):
        """
        Simulate user login to get authentication token
        """
        credentials = {
            "email": "admin@example.com", 
            "password": "password123"
        }
        
        with self.client.post(
            "/auth/login", 
            json=credentials,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                # For a real implementation, you might extract a token here
                # self.api_token = response.json()["token"]
                self.api_token = "simulated_token"
                return True
            else:
                response.failure(f"Failed to login: {response.status_code}")
                return False

    @task(10)  # Weight: most common operation
    def view_ideas(self):
        """
        GET /api/ideas - List all ideas
        High frequency task - users often browse ideas
        """
        with self.client.get(
            "/api/ideas",
            name="/api/ideas - List all ideas",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get ideas: {response.status_code}")
    
    @task(5)
    def view_specific_idea(self):
        """
        GET /api/ideas/{id} - View a specific idea
        Medium frequency task
        """
        # In a real scenario, we'd pick a random ID from existing ideas
        idea_id = random.randint(1, 10)
        
        with self.client.get(
            f"/api/ideas/{idea_id}",
            name="/api/ideas/{id} - Get specific idea",
            catch_response=True
        ) as response:
            if response.status_code == 404:
                # We're using random IDs, so 404s are expected sometimes
                pass
            elif response.status_code != 200:
                response.failure(f"Failed to get idea {idea_id}: {response.status_code}")
    
    @task(2)
    def create_idea(self):
        """
        POST /api/ideas - Create a new idea
        Lower frequency task
        """
        idea_data = {
            "title": f"Load Test Idea {time.time()}",
            "description": "This idea was created during load testing",
            "status": random.choice(["new", "in_progress", "completed"]),
            "priority": random.randint(1, 5)
        }
        
        with self.client.post(
            "/api/ideas",
            json=idea_data,
            name="/api/ideas - Create new idea",
            catch_response=True
        ) as response:
            if response.status_code != 201:
                response.failure(f"Failed to create idea: {response.status_code}")
    
    @task(8)
    def view_projects(self):
        """
        GET /api/projects - List all projects
        High frequency task
        """
        with self.client.get(
            "/api/projects",
            name="/api/projects - List all projects",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get projects: {response.status_code}")
    
    @task(4)
    def view_specific_project(self):
        """
        GET /api/projects/{id} - View a specific project
        Medium frequency task
        """
        # In a real scenario, we'd pick a random ID from existing projects
        project_id = random.randint(1, 5)
        
        with self.client.get(
            f"/api/projects/{project_id}",
            name="/api/projects/{id} - Get specific project",
            catch_response=True
        ) as response:
            if response.status_code == 404:
                # We're using random IDs, so 404s are expected sometimes
                pass
            elif response.status_code != 200:
                response.failure(f"Failed to get project {project_id}: {response.status_code}")
    
    @task(6)
    def view_kpis(self):
        """
        GET /api/kpis - List all KPIs
        Medium frequency task
        """
        with self.client.get(
            "/api/kpis",
            name="/api/kpis - List all KPIs",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get KPIs: {response.status_code}")
    
    @task(1)
    def update_kpi(self):
        """
        PUT /api/kpis/{id} - Update a KPI's values
        Low frequency task
        """
        # In a real scenario, we'd pick a random ID from existing KPIs
        kpi_id = random.randint(1, 5)
        
        update_data = {
            "current_value": random.uniform(10.0, 100.0),
            "updated_at": time.strftime("%Y-%m-%d")
        }
        
        with self.client.put(
            f"/api/kpis/{kpi_id}",
            json=update_data,
            name="/api/kpis/{id} - Update KPI",
            catch_response=True
        ) as response:
            if response.status_code == 404:
                # We're using random IDs, so 404s are expected sometimes
                pass
            elif response.status_code != 200:
                response.failure(f"Failed to update KPI {kpi_id}: {response.status_code}")


class WebsiteUser(HttpUser):
    """
    Simulates users browsing the web interface
    """
    wait_time = between(3, 8)  # Web users typically take longer between actions
    
    def on_start(self):
        """
        Simulate user visiting the site and logging in
        """
        self.client.get("/")
        self.login()
    
    def login(self):
        """
        Simulate web login
        """
        # First get the login page to capture any CSRF token
        response = self.client.get("/auth/login")
        
        # Then submit login form
        # In a real implementation, you'd extract the CSRF token from the response
        self.client.post(
            "/auth/login",
            data={
                "email": "user@example.com",
                "password": "password123",
                # "csrf_token": extracted_token
            }
        )
    
    @task(10)
    def view_homepage(self):
        """
        GET / - View homepage
        Most common task for web users
        """
        self.client.get("/", name="Homepage")
    
    @task(5)
    def view_projects_page(self):
        """
        GET /projects - View projects listing page
        Common task for web users
        """
        self.client.get("/projects", name="Projects Page")
    
    @task(4)
    def view_ideas_page(self):
        """
        GET /ideas - View ideas listing page
        Fairly common task for web users
        """
        self.client.get("/ideas", name="Ideas Page")
    
    @task(2)
    def view_kpi_dashboard(self):
        """
        GET /dashboard - View KPI dashboard
        Less common task for regular users
        """
        self.client.get("/dashboard", name="KPI Dashboard")


# Execute with:
# locust -f tests/performance/locustfile.py --host=http://localhost:5000
# Then open http://localhost:8089 in a browser to start the test
