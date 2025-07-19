import pytest
import json
from app import create_app, db
from models.user import User, RoleEnum


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    with app.app_context():
        user = User(email='test@example.com')
        user.set_password('testpassword123')
        user.role = RoleEnum.VIEWER.value
        db.session.add(user)
        db.session.commit()
        return user


class TestUserRegistration:
    """Test user registration endpoint."""
    
    def test_successful_registration(self, client):
        """Test successful user registration."""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        
        response = client.post('/api/auth/register', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert 'token' in response_data
        assert 'user' in response_data
        assert response_data['user']['email'] == 'newuser@example.com'
        assert response_data['message'] == 'User registered successfully'
    
    def test_registration_duplicate_email(self, client, sample_user):
        """Test registration with duplicate email."""
        data = {
            'email': 'test@example.com',  # Same as sample_user
            'password': 'newpassword123'
        }
        
        response = client.post('/api/auth/register',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 409
        response_data = json.loads(response.data)
        assert response_data['error'] == 'Email already registered'
    
    def test_registration_missing_data(self, client):
        """Test registration with missing data."""
        data = {'email': 'test@example.com'}  # Missing password
        
        response = client.post('/api/auth/register',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'Email and password are required' in response_data['error']
    
    def test_registration_invalid_email(self, client):
        """Test registration with invalid email format."""
        data = {
            'email': 'invalid-email',
            'password': 'testpassword123'
        }
        
        response = client.post('/api/auth/register',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'Invalid email format' in response_data['error']
    
    def test_registration_weak_password(self, client):
        """Test registration with weak password."""
        data = {
            'email': 'test@example.com',
            'password': 'weak'  # Too short
        }
        
        response = client.post('/api/auth/register',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'Password must be at least 8 characters long' in response_data['error']


class TestUserLogin:
    """Test user login endpoint."""
    
    def test_successful_login(self, client, sample_user):
        """Test successful user login."""
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'token' in response_data
        assert 'user' in response_data
        assert response_data['user']['email'] == 'test@example.com'
        assert response_data['message'] == 'Login successful'
    
    def test_login_invalid_credentials(self, client, sample_user):
        """Test login with invalid credentials."""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 401
        response_data = json.loads(response.data)
        assert response_data['error'] == 'Invalid email or password'
    
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user."""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'testpassword123'
        }
        
        response = client.post('/api/auth/login',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 401
        response_data = json.loads(response.data)
        assert response_data['error'] == 'Invalid email or password'
    
    def test_login_missing_data(self, client):
        """Test login with missing data."""
        data = {'email': 'test@example.com'}  # Missing password
        
        response = client.post('/api/auth/login',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'Email and password are required' in response_data['error']


class TestProtectedEndpoints:
    """Test JWT-protected endpoints."""
    
    def get_auth_token(self, client, email='test@example.com', password='testpassword123'):
        """Helper method to get authentication token."""
        data = {'email': email, 'password': password}
        response = client.post('/api/auth/login',
                             data=json.dumps(data),
                             content_type='application/json')
        return json.loads(response.data)['token']
    
    def test_get_current_user_with_token(self, client, sample_user):
        """Test getting current user with valid token."""
        token = self.get_auth_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.get('/api/auth/me', headers=headers)
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'user' in response_data
        assert response_data['user']['email'] == 'test@example.com'
    
    def test_get_current_user_without_token(self, client):
        """Test getting current user without token."""
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401
        response_data = json.loads(response.data)
        assert response_data['error'] == 'Token is missing'
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token."""
        headers = {'Authorization': 'Bearer invalid-token'}
        
        response = client.get('/api/auth/me', headers=headers)
        
        assert response.status_code == 401
        response_data = json.loads(response.data)
        assert response_data['error'] == 'Invalid token'
    
    def test_verify_token_valid(self, client, sample_user):
        """Test token verification with valid token."""
        token = self.get_auth_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.post('/api/auth/verify', headers=headers)
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['valid'] is True
        assert 'user' in response_data
    
    def test_refresh_token(self, client, sample_user):
        """Test token refresh."""
        token = self.get_auth_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.post('/api/auth/refresh', headers=headers)
        
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert 'token' in response_data
        assert response_data['message'] == 'Token refreshed successfully'
        
        # New token should be different from the old one
        assert response_data['token'] != token
