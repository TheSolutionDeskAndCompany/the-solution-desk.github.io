"""
Flask CLI commands for The Solution Desk application
"""
import os
import json
from datetime import datetime
import click
import logging
from flask import current_app
from flask.cli import with_appcontext
from app import db

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_date(date_str):
    """Parse date string to datetime object"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        logger.warning(f"Invalid date format: {date_str}, using None")
        return None

def load_seed_data():
    """Load seed data from JSON file"""
    try:
        seed_path = os.path.join(current_app.root_path, 'scripts', 'seed-data.json')
        with open(seed_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load seed data: {e}")
        return None

@click.command('seed')
@click.option('--mode', type=click.Choice(['standard', 'reset', 'incremental']), default='standard',
              help='Seed mode: standard (default), reset (wipe first), or incremental (only missing)')
@with_appcontext
def seed_command(mode):
    """Seed database with sample data."""
    from models.user import User
    from models.project import Project
    from models.idea import Idea
    from models.sop import SOP
    from models.kpi import KPI
    
    logger.info(f"Starting database seed in {mode} mode")
    
    # Load seed data
    seed_data = load_seed_data()
    if not seed_data:
        logger.error("No seed data found. Exiting.")
        return
    
    # Reset database if in reset mode
    if mode == 'reset':
        logger.info("Resetting database...")
        db.drop_all()
        db.create_all()
        logger.info("Database reset complete.")
    
    # Determine if we're running in incremental mode
    incremental = (mode == 'incremental')
    
    # Seed users
    logger.info("Seeding users...")
    created_users = 0
    
    for user_data in seed_data['users']:
        email = user_data['email']
        
        # Check if user exists in incremental mode
        if incremental and User.get_by_email(email):
            logger.info(f"User {email} already exists, skipping.")
            continue
            
        # Create new user
        user = User(email=email, role=user_data['role'])
        user.set_password(user_data['password'])
        db.session.add(user)
        created_users += 1
    
    db.session.commit()
    logger.info(f"Created {created_users} users.")
    
    # Seed projects
    logger.info("Seeding projects...")
    created_projects = 0
    
    for project_data in seed_data['projects']:
        slug = project_data['slug']
        
        # Check if project exists in incremental mode
        if incremental and Project.get_by_slug(slug):
            logger.info(f"Project with slug '{slug}' already exists, skipping.")
            continue
            
        # Create new project
        project = Project(
            title=project_data['title'],
            slug=project_data['slug'],
            description=project_data['description'],
            long_description=project_data['long_description'],
            image_url=project_data['image_url'],
            demo_url=project_data['demo_url'],
            github_url=project_data['github_url'],
            download_url=project_data['download_url'],
            is_featured=project_data['is_featured']
        )
        db.session.add(project)
        created_projects += 1
    
    db.session.commit()
    logger.info(f"Created {created_projects} projects.")
    
    # Seed ideas
    logger.info("Seeding ideas...")
    created_ideas = 0
    
    for idea_data in seed_data['ideas']:
        # For incremental mode, we'll skip if an idea with the same title exists
        title = idea_data['title']
        
        if incremental:
            existing_idea = Idea.query.filter_by(title=title).first()
            if existing_idea:
                logger.info(f"Idea '{title}' already exists, skipping.")
                continue
        
        # Create new idea
        idea = Idea(
            title=title,
            description=idea_data['description'],
            status=idea_data['status'],
            priority=idea_data['priority']
        )
        db.session.add(idea)
        created_ideas += 1
    
    db.session.commit()
    logger.info(f"Created {created_ideas} ideas.")
    
    # Seed SOPs
    logger.info("Seeding SOPs...")
    created_sops = 0
    
    for sop_data in seed_data['sops']:
        title = sop_data['title']
        
        if incremental:
            existing_sop = SOP.query.filter_by(title=title).first()
            if existing_sop:
                logger.info(f"SOP '{title}' already exists, skipping.")
                continue
        
        # Create new SOP
        sop = SOP(
            title=title,
            description=sop_data['description'],
            content=sop_data['content'],
            version=sop_data['version'],
            category=sop_data['category']
        )
        db.session.add(sop)
        created_sops += 1
    
    db.session.commit()
    logger.info(f"Created {created_sops} SOPs.")
    
    # Seed KPIs
    logger.info("Seeding KPIs...")
    created_kpis = 0
    
    for kpi_data in seed_data['kpis']:
        title = kpi_data['title']
        
        if incremental:
            existing_kpi = KPI.query.filter_by(title=title).first()
            if existing_kpi:
                logger.info(f"KPI '{title}' already exists, skipping.")
                continue
        
        # Create new KPI
        kpi = KPI(
            title=title,
            description=kpi_data['description'],
            target_value=kpi_data['target_value'],
            current_value=kpi_data['current_value'],
            unit=kpi_data['unit'],
            category=kpi_data['category'],
            start_date=parse_date(kpi_data['start_date']),
            end_date=parse_date(kpi_data['end_date'])
        )
        db.session.add(kpi)
        created_kpis += 1
    
    db.session.commit()
    logger.info(f"Created {created_kpis} KPIs.")
    
    logger.info("🌱 Seed complete!")
    return "Database seeding completed successfully."

def register_commands(app):
    """Register Flask CLI commands"""
    app.cli.add_command(seed_command)
