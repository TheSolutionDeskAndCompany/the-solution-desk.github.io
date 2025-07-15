def test_home_page(client):
    """Test the home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'The Solution Desk' in response.data

def test_projects_list(client):
    """Test the projects listing page"""
    response = client.get('/projects/')
    assert response.status_code == 200
    assert b'Projects' in response.data

def test_project_detail(client):
    """Test viewing a single project"""
    response = client.get('/projects/test-project')
    assert response.status_code == 200
    assert b'Test Project' in response.data

def test_nonexistent_project(client):
    """Test viewing a non-existent project returns 404"""
    response = client.get('/projects/nonexistent')
    assert response.status_code == 404

def test_contact_page(client):
    """Test the contact page loads"""
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'Contact' in response.data

def test_tools_page(client):
    """Test the tools page loads"""
    response = client.get('/tools/')
    assert response.status_code == 200
    assert b'Tools' in response.data
