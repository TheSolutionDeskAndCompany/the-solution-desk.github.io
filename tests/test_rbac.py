"""
Tests for Role-Based Access Control functionality
"""
import pytest
from flask import url_for
from models.user import RoleEnum

def test_admin_access_control_panel(admin_client):
    """Test admin can access admin panel"""
    response = admin_client.get('/admin/')
    assert response.status_code == 200
    assert b'Home - The Solution Desk Admin' in response.data

def test_contributor_no_admin_access(contributor_client):
    """Test contributor cannot access admin panel"""
    response = contributor_client.get('/admin/')
    assert response.status_code == 403

def test_viewer_no_admin_access(viewer_client):
    """Test viewer cannot access admin panel"""
    response = viewer_client.get('/admin/')
    assert response.status_code == 403

def test_project_creation_admin(admin_client):
    """Test admin can create projects"""
    response = admin_client.post('/projects/create', data={
        'title': 'New Admin Project',
        'slug': 'new-admin-project',
        'description': 'Test admin creating project'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Project created successfully' in response.data

def test_project_creation_contributor(contributor_client):
    """Test contributor can create projects"""
    response = contributor_client.post('/projects/create', data={
        'title': 'New Contributor Project',
        'slug': 'new-contributor-project',
        'description': 'Test contributor creating project'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Project created successfully' in response.data

def test_project_creation_viewer(viewer_client):
    """Test viewer cannot create projects"""
    response = viewer_client.post('/projects/create', data={
        'title': 'New Viewer Project',
        'slug': 'new-viewer-project',
        'description': 'Test viewer creating project'
    }, follow_redirects=True)
    assert response.status_code == 403

def test_project_edit_admin(admin_client, app):
    """Test admin can edit projects"""
    with app.app_context():
        response = admin_client.post('/projects/test-project/edit', data={
            'title': 'Updated Test Project',
            'slug': 'test-project',
            'description': 'Updated description'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Project updated successfully' in response.data

def test_project_edit_contributor(contributor_client, app):
    """Test contributor can edit projects"""
    with app.app_context():
        response = contributor_client.post('/projects/test-project/edit', data={
            'title': 'Contributor Updated Project',
            'slug': 'test-project',
            'description': 'Contributor updated description'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Project updated successfully' in response.data

def test_project_edit_viewer(viewer_client, app):
    """Test viewer cannot edit projects"""
    with app.app_context():
        response = viewer_client.post('/projects/test-project/edit', data={
            'title': 'Viewer Updated Project',
            'slug': 'test-project',
            'description': 'Viewer updated description'
        }, follow_redirects=True)
        assert response.status_code == 403

def test_project_delete_admin(admin_client, app):
    """Test admin can delete projects"""
    with app.app_context():
        # First create a project to delete
        admin_client.post('/projects/create', data={
            'title': 'Project To Delete',
            'slug': 'project-to-delete',
            'description': 'This project will be deleted'
        })
        
        # Now try to delete it
        response = admin_client.post('/projects/project-to-delete/delete', follow_redirects=True)
        assert response.status_code == 200
        assert b'Project deleted successfully' in response.data

def test_project_delete_contributor(contributor_client, app):
    """Test contributor cannot delete projects"""
    with app.app_context():
        # First create a project as admin
        response = contributor_client.post('/projects/create', data={
            'title': 'Project Contributor Cant Delete',
            'slug': 'project-contributor-cant-delete',
            'description': 'Testing deletion permissions'
        })
        
        # Now try to delete it
        response = contributor_client.post('/projects/project-contributor-cant-delete/delete', follow_redirects=True)
        assert response.status_code == 403

def test_project_delete_viewer(viewer_client, app):
    """Test viewer cannot delete projects"""
    with app.app_context():
        response = viewer_client.post('/projects/test-project/delete', follow_redirects=True)
        assert response.status_code == 403
