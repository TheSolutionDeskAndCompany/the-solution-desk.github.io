"""
Test Configuration Settings

This module contains configuration settings specifically for test environments.
It ensures tests use an isolated database and appropriate settings.
"""

import os
import tempfile

# Use in-memory SQLite for faster tests
TEST_DATABASE_URI = "sqlite:///:memory:"

# Alternatively, use a file-based SQLite database
# db_fd, db_path = tempfile.mkstemp()
# TEST_DATABASE_URI = f"sqlite:///{db_path}"

# Test config class
class TestConfig:
    """Flask test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test_secret_key"
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # JWT settings for testing
    JWT_SECRET_KEY = "test_jwt_secret"
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # Disable mail for testing
    MAIL_SUPPRESS_SEND = True
    
    # Test user credentials
    TEST_USER_EMAIL = "test@example.com"
    TEST_USER_PASSWORD = "password"
    TEST_ADMIN_EMAIL = "admin@example.com"
    TEST_ADMIN_PASSWORD = "admin_password"
    
    # Configure logging for tests
    LOG_LEVEL = "ERROR"
    LOG_TO_STDOUT = False
    LOG_TO_FILE = False

    # Enable debug mode for tests
    DEBUG = True
    
    # Rate limiting settings for tests (disable rate limiting)
    RATELIMIT_ENABLED = False


def get_test_config():
    """Return a config dictionary for testing"""
    return {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "test_secret_key",
        "WTF_CSRF_ENABLED": False,
        "JWT_SECRET_KEY": "test_jwt_secret",
        "JWT_ACCESS_TOKEN_EXPIRES": 3600,
        "MAIL_SUPPRESS_SEND": True,
        "LOG_LEVEL": "ERROR",
        "LOG_TO_STDOUT": False,
        "LOG_TO_FILE": False,
        "DEBUG": True,
        "RATELIMIT_ENABLED": False,
    }
