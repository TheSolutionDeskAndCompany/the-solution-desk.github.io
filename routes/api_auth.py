from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import BadRequest
import jwt
from datetime import datetime, timedelta
from functools import wraps
from app import db
from models.user import User, RoleEnum
import re

api_auth_bp = Blueprint('api_auth', __name__, url_prefix='/api/auth')

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def generate_token(user_id):
    """Generate JWT token for user"""
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(
                seconds=int(current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
            ),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        return token
    except Exception as e:
        current_app.logger.error(f"Token generation error: {str(e)}")
        return None

def jwt_required(f):
    """Decorator to require JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid authorization header format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            current_user_id = payload['user_id']
            current_user = User.query.get(current_user_id)
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
                
            # Make current_user available in the request context
            request.current_user = current_user
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            current_app.logger.error(f"JWT validation error: {str(e)}")
            return jsonify({'error': 'Token validation failed'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

@api_auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user via API"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validation
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        is_valid, password_message = validate_password(password)
        if not is_valid:
            return jsonify({'error': password_message}), 400
        
        # Check if user already exists
        existing_user = User.get_by_email(email)
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        user = User(email=email)
        user.set_password(password)
        
        # Make first user an admin, others are viewers by default
        if User.query.count() == 0:
            user.role = RoleEnum.ADMIN.value
        else:
            user.role = RoleEnum.VIEWER.value
        
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = generate_token(user.id)
        if not token:
            return jsonify({'error': 'Failed to generate token'}), 500
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': user.serialize()
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@api_auth_bp.route('/login', methods=['POST'])
def login():
    """Login user via API"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user
        user = User.get_by_email(email)
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate token
        token = generate_token(user.id)
        if not token:
            return jsonify({'error': 'Failed to generate token'}), 500
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.serialize()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@api_auth_bp.route('/me', methods=['GET'])
@jwt_required
def get_current_user():
    """Get current user information"""
    try:
        user = request.current_user
        return jsonify({
            'user': user.serialize()
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get current user error: {str(e)}")
        return jsonify({'error': 'Failed to get user information'}), 500

@api_auth_bp.route('/verify', methods=['POST'])
@jwt_required
def verify_token():
    """Verify if token is valid"""
    try:
        user = request.current_user
        return jsonify({
            'valid': True,
            'user': user.serialize()
        }), 200
    except Exception as e:
        current_app.logger.error(f"Token verification error: {str(e)}")
        return jsonify({'error': 'Token verification failed'}), 500

@api_auth_bp.route('/refresh', methods=['POST'])
@jwt_required
def refresh_token():
    """Refresh JWT token"""
    try:
        user = request.current_user
        new_token = generate_token(user.id)
        
        if not new_token:
            return jsonify({'error': 'Failed to generate new token'}), 500
        
        return jsonify({
            'message': 'Token refreshed successfully',
            'token': new_token,
            'user': user.serialize()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Token refresh error: {str(e)}")
        return jsonify({'error': 'Token refresh failed'}), 500
