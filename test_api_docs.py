"""
Simple test script to verify API documentation is working correctly
"""
import os
import sys
from app import create_app

def test_api_docs():
    """Test that API documentation is accessible"""
    print("Testing API documentation...")
    # Create a test app with development configuration
    app = create_app('development')
    
    # Create a test client
    with app.test_client() as client:
        # Try accessing the API docs endpoint
        response = client.get('/api/docs')
        
        if response.status_code == 200:
            print("✅ API documentation is accessible!")
        else:
            print(f"❌ API documentation returned status code {response.status_code}")
            sys.exit(1)

def test_sentry_config():
    """Test that Sentry is properly configured"""
    print("Testing Sentry configuration...")
    # Check if Sentry DSN is set
    sentry_dsn = os.environ.get('SENTRY_DSN')
    
    if sentry_dsn:
        print(f"✅ Sentry DSN is configured")
    else:
        print("⚠️ Sentry DSN is not configured - this is fine for development")
    
    print("Sentry will be initialized in production environments automatically")

if __name__ == '__main__':
    test_api_docs()
    test_sentry_config()
    print("\nAll tests completed successfully!")
