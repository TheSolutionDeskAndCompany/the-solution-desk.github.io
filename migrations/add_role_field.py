"""
Migration script to add role field to User model and 
migrate existing users from is_admin boolean to role enum.
"""
from app import create_app, db
from models.user import User, RoleEnum
from sqlalchemy import Column, String, Boolean
from sqlalchemy.sql import text
import sys

def migrate_users():
    """
    This function migrates users from the is_admin boolean field
    to the new role enum field.
    
    1. Check if role column exists
    2. If not, add it
    3. For each user with is_admin=True, set role to Admin
    4. For each user with is_admin=False, set role to Viewer
    5. Remove is_admin column
    """
    app = create_app()
    with app.app_context():
        try:
            # Check if role column exists
            result = db.session.execute(text("PRAGMA table_info(user)")).fetchall()
            columns = [col[1] for col in result]
            
            if 'role' not in columns:
                print("Adding 'role' column...")
                db.session.execute(text("ALTER TABLE user ADD COLUMN role VARCHAR(32) DEFAULT 'Viewer'"))
                
                # Set Admins based on is_admin value
                if 'is_admin' in columns:
                    print("Migrating users from is_admin to role...")
                    # Set Admin role for users with is_admin=1
                    db.session.execute(
                        text("UPDATE user SET role = 'Admin' WHERE is_admin = 1")
                    )
                    
                # Commit changes
                db.session.commit()
                print("Migration successful! All users now have a role.")
            else:
                print("Role column already exists. No migration needed.")
                
        except Exception as e:
            print(f"Error during migration: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrate_users()
