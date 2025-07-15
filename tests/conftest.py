import os
import tempfile
import pytest
from app import create_app, db
from models.project import Project

@pytest.fixture
def app():
    """Create and configure a new app instance for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False
    })

    # Create the database and load test data
    with app.app_context():
        db.create_all()
        # Add test data
        test_project = Project(
            title='Test Project',
            slug='test-project',
            description='A test project',
            long_description='This is a longer description for the test project',
            github_url='https://github.com/test/project',
            download_url='/downloads/test-project.zip',
            is_featured=True
        )
        db.session.add(test_project)
        db.session.commit()

    yield app

    # Clean up the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def test_project():
    """A test project for use in tests."""
    return {
        'title': 'Test Project',
        'slug': 'test-project',
        'description': 'A test project',
        'long_description': 'This is a longer description for the test project',
        'github_url': 'https://github.com/test/project',
        'download_url': '/downloads/test-project.zip',
        'is_featured': True
    }
