import os
import tempfile
import pytest
from datetime import datetime
from app import create_app, db
from models.project import Project
from models.user import User, RoleEnum
from models.idea import Idea
from models.kpi import KPI
from flask_login import login_user

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
        
        # Add test ideas
        test_idea_1 = Idea(
            title='Test Idea 1',
            description='A test idea with high priority',
            status='new',
            priority=1
        )
        
        test_idea_2 = Idea(
            title='Test Idea 2',
            description='A test idea in progress',
        )
        
        viewer_user = User(
            email="viewer@example.com",
            password="password",
            role="Viewer"
        )
        
        db.session.add_all([admin_user, regular_user, viewer_user])
        db.session.commit()
        logger.info("Test users created successfully")

    yield app

    # Clean up / reset resources
    with app.app_context():
        logger.info("Tearing down test database")
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Create a test client for the app"""
    return app.test_client()


@pytest.fixture()
def authenticated_client(app, test_user):
    """Create a test client that is already authenticated"""
    client = app.test_client()
    # Configure the client with authentication headers
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {test_user.token}'
    return client


@pytest.fixture()
def test_user(app):
    """Create and return a test user with a valid token"""
    with app.app_context():
        user = User.query.filter_by(email="test@example.com").first()
        token = create_access_token(identity=user.id)
        user.token = token
        return user


@pytest.fixture()
def test_admin(app):
    """Create and return a test admin user with a valid token"""
    with app.app_context():
        admin = User.query.filter_by(email="admin@example.com").first()
        token = create_access_token(identity=admin.id)
        admin.token = token
        return admin


@pytest.fixture()
def test_project(app):
    """Create and return a test project"""
    with app.app_context():
        user = User.query.filter_by(email="admin@example.com").first()
        
        # Create a test project
        project = Project(
            name="Test Project",
            description="A test project for automated testing",
            status="active",
            manager_id=user.id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        db.session.add(project)
        db.session.commit()
        
        return project


@pytest.fixture()
def test_ideas(app, test_user, test_admin):
    """Create and return multiple test ideas"""
    with app.app_context():
        # Create test ideas with various states
        ideas = [
            Idea(
                title="Test Idea 1",
                description="A test idea for automated testing",
                status="new",
                priority=3,
                creator_id=test_user.id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            Idea(
                title="Test Idea 2",
                description="Another test idea for status testing",
                status="in_progress",
                priority=5,
                creator_id=test_user.id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            Idea(
                title="Test Idea 3",
                description="A completed test idea",
                status="completed",
                priority=2,
                creator_id=test_admin.id,
                created_at=datetime.now(timezone.utc) - timedelta(days=5),
                updated_at=datetime.now(timezone.utc)
            ),
            Idea(
                title="Test Idea 4",
                description="An archived test idea",
                status="archived",
                priority=1,
                creator_id=test_admin.id,
                created_at=datetime.now(timezone.utc) - timedelta(days=30),
                updated_at=datetime.now(timezone.utc) - timedelta(days=10)
            ),
        ]
        
        db.session.add_all(ideas)
        db.session.commit()
        
        return ideas


@pytest.fixture()
def test_idea(app, test_ideas):
    """Return a single test idea for simpler tests"""
    return test_ideas[0] if test_ideas else None


@pytest.fixture()
def test_projects(app, test_user, test_admin):
    """Create and return multiple test projects"""
    with app.app_context():
        # Create test projects with various states
        projects = [
            Project(
                name="Active Project",
                description="An active test project",
                status="active",
                manager_id=test_admin.id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            Project(
                name="Planning Project",
                description="A project in planning phase",
                status="planning",
                manager_id=test_user.id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            Project(
                name="Completed Project",
                description="A completed test project",
                status="completed",
                manager_id=test_admin.id,
                created_at=datetime.now(timezone.utc) - timedelta(days=60),
                updated_at=datetime.now(timezone.utc) - timedelta(days=2)
            ),
            Project(
                name="On Hold Project",
                description="A project currently on hold",
                status="on_hold",
                manager_id=test_user.id,
                created_at=datetime.now(timezone.utc) - timedelta(days=15),
                updated_at=datetime.now(timezone.utc) - timedelta(days=5)
            ),
        ]
        
        db.session.add_all(projects)
        db.session.commit()
        
        return projects


@pytest.fixture()
def test_kpis(app, test_projects):
    """Create and return multiple test KPIs"""
    with app.app_context():
        projects = test_projects or [Project.query.first()]
        
        # Create test KPIs for different projects
        kpis = [
            KPI(
                name="Revenue Growth",
                description="Monthly revenue growth percentage",
                target_value=15.0,
                current_value=12.5,
                unit="percent",
                project_id=projects[0].id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            KPI(
                name="Customer Satisfaction",
                description="Customer satisfaction score",
                target_value=4.5,
                current_value=4.2,
                unit="score",
                project_id=projects[0].id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            KPI(
                name="On-time Delivery",
                description="Percentage of on-time deliveries",
                target_value=95.0,
                current_value=92.0,
                unit="percent",
                project_id=projects[1].id if len(projects) > 1 else projects[0].id,
                created_at=datetime.now(timezone.utc) - timedelta(days=10),
                updated_at=datetime.now(timezone.utc)
            ),
        ]
        
        db.session.add_all(kpis)
        db.session.commit()
        
        return kpis


@pytest.fixture()
def test_kpi(app, test_kpis):
    """Return a single test KPI for simpler tests"""
    return test_kpis[0] if test_kpis else None
