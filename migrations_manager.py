"""
Migrations management script for PostgreSQL setup
"""
import os
import sys
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from models.user import User, RoleEnum
from models.project import Project
from models.idea import Idea
from models.sop import SOP
from models.kpi import KPI

app = create_app()
migrate = Migrate(app, db)

def migrate_is_admin_to_role():
    """
    Migrates users from is_admin boolean field to role enum field
    after the initial database migration is complete
    """
    with app.app_context():
        users = User.query.all()
        for user in users:
            # Check if user has is_admin attribute and role is not set
            if hasattr(user, 'is_admin') and user.is_admin:
                user.role = RoleEnum.ADMIN.value
            else:
                user.role = RoleEnum.VIEWER.value
            
        db.session.commit()
        print(f"Migrated {len(users)} users to new role-based system")

if __name__ == '__main__':
    # This script is used to help with migration tasks
    # but the actual migrations should be run with the Flask CLI
    print("Migration management script")
    print("Usage: python migrations_manager.py [command]")
    print("Available commands:")
    print("  migrate_roles - Migrate users from is_admin to role field")
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'migrate_roles':
            migrate_is_admin_to_role()
        else:
            print(f"Unknown command: {command}")
    else:
        print("No command specified")
