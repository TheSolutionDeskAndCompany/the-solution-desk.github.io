"""
Initialize Flask-Migrate for database migrations
"""
from app import create_app, db
from flask_migrate import init, migrate, upgrade

def initialize_migrations():
    """
    Initializes the migrations directory structure
    and creates the first migration for PostgreSQL
    """
    app = create_app()
    with app.app_context():
        # Initialize the migration repository
        init()
        
        # Create the first migration
        migrate(message="Init Postgres schema")
        
        # Apply the migration
        upgrade()
        
        print("Migrations initialized successfully!")

if __name__ == "__main__":
    initialize_migrations()
