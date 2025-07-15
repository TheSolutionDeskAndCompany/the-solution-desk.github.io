from app import app, db
from models.user import User
from models.project import Project
from models.idea import Idea
from models.sop import SOP
from models.kpi import KPI
import os

with app.app_context():
    db.create_all()
    
    # Create admin user if none exists
    if User.query.filter_by(is_admin=True).first() is None:
        admin = User(email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created with email: admin@example.com and password: admin123")
    
    # Create sample data if needed
    if Project.query.first() is None:
        sample_project = Project(
            title="Sample Project",
            slug="sample-project",
            description="This is a sample project for testing the API.",
            is_featured=True
        )
        db.session.add(sample_project)
    
    if Idea.query.first() is None:
        sample_idea = Idea(
            title="Sample Idea",
            description="This is a sample idea for testing the API.",
            status="new",
            priority=1
        )
        db.session.add(sample_idea)
    
    if SOP.query.first() is None:
        sample_sop = SOP(
            title="Sample SOP",
            description="This is a sample SOP for testing the API.",
            content="# Sample SOP\n\nFollow these steps to complete the process...",
            category="General"
        )
        db.session.add(sample_sop)
    
    if KPI.query.first() is None:
        sample_kpi = KPI(
            title="Sample KPI",
            description="This is a sample KPI for testing the API.",
            target_value=100,
            current_value=75,
            unit="percent",
            category="Performance"
        )
        db.session.add(sample_kpi)
    
    db.session.commit()
    print("Database tables created and sample data added successfully!")
