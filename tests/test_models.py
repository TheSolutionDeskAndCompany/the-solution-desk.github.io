import pytest
from models.project import Project

def test_new_project(app):
    """Test creating a new project"""
    with app.app_context():
        project = Project(
            title='New Project',
            slug='new-project',
            description='A new test project',
            long_description='This is a longer description',
            github_url='https://github.com/test/new-project',
            is_featured=True
        )
        assert project.title == 'New Project'
        assert project.slug == 'new-project'
        assert not project.download_url  # Should be None by default

def test_project_creation(app):
    """Test adding a project to the database"""
    with app.app_context():
        # Count initial projects
        initial_count = Project.query.count()
        
        # Create new project
        project = Project(
            title='Another Project',
            slug='another-project',
            description='Another test project'
        )
        db.session.add(project)
        db.session.commit()
        
        # Should be one more project now
        assert Project.query.count() == initial_count + 1
        assert Project.query.filter_by(slug='another-project').first() is not None

def test_project_representation(app):
    """Test the string representation of a project"""
    with app.app_context():
        project = Project.query.filter_by(slug='test-project').first()
        assert str(project) == '<Project Test Project>'

def test_get_featured_projects(app):
    """Test getting featured projects"""
    with app.app_context():
        featured = Project.get_all(featured_only=True)
        assert len(featured) > 0
        assert all(p.is_featured for p in featured)
