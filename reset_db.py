#!/usr/bin/env python3
"""
Database reset script for CI/CD pipeline.
Drops all tables and recreates them to ensure clean test environment.
"""
import os
import sys
from app import create_app, db

def reset_database():
    """Reset the database by dropping and recreating all tables."""
    try:
        # Create app instance for testing environment
        app = create_app('testing')
        
        with app.app_context():
            print("🔄 Resetting database...")
            
            # Drop all tables
            print("📦 Dropping all tables...")
            db.drop_all()
            
            # Recreate all tables
            print("🏗️  Creating all tables...")
            db.create_all()
            
            print("✅ Database reset complete.")
            return True
            
    except Exception as e:
        print(f"❌ Database reset failed: {str(e)}")
        return False

def main():
    """Main function to run database reset."""
    success = reset_database()
    
    if not success:
        sys.exit(1)
    
    print("🎉 Ready for testing!")

if __name__ == '__main__':
    main()
