import os
from app import create_app

# Create application instance
app = create_app(os.getenv('FLASK_ENV') or 'production')

# This is needed for Gunicorn to find the app
application = app

if __name__ == "__main__":
    # This block is only used when running locally
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
