#!/usr/bin/env python3
"""
Seed script for The Solution Desk database
This script generates SQL statements for seeding the database with sample data from seed-data.json.
The statements can be piped to sqlite3 command-line tool.
"""

import os
import sys
import json
import argparse
import base64
from datetime import datetime
import logging
import hashlib
import subprocess
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)


def load_seed_data():
    """Load seed data from JSON file"""
    try:
        seed_path = os.path.join(os.path.dirname(__file__), 'seed-data.json')
        with open(seed_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load seed data: {e}")
        sys.exit(1)


def get_db_path():
    """Get database path from config or use default"""
    try:
        # Try to import config if it exists
        from config import config
        config_name = os.getenv('FLASK_ENV', 'development')
        uri = config[config_name].SQLALCHEMY_DATABASE_URI
        if uri.startswith('sqlite:///'):
            return uri[10:]
    except (ImportError, KeyError, AttributeError) as e:
        logger.warning(f"Could not determine database path from config: {e}")
    
    # Default to instance/app.db if config can't be loaded
    instance_path = os.path.join(parent_dir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    return os.path.join(instance_path, 'app.db')


def escape_sql_string(value):
    """Escape string values for SQL statements"""
    if value is None:
        return "NULL"
    return f"'{str(value).replace("'", "''")}'"


def format_value(value):
    """Format a value for SQL insertion"""
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    return escape_sql_string(value)


def generate_password_hash(password):
    """Generate a simple password hash similar to werkzeug's"""
    # This is a simplified version and not secure for production
    # In real app, we would use werkzeug.security.generate_password_hash
    salt = os.urandom(8).hex()
    h = hashlib.sha256(f"{salt}{password}".encode()).digest()
    hash_b64 = base64.b64encode(h).decode('utf-8')
    return f"sha256${salt}${hash_b64}"


def parse_date(date_str):
    """Parse date string to datetime object"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        logger.warning(f"Invalid date format: {date_str}, using None")
        return None


def format_datetime(dt):
    """Format datetime object for SQL or return NULL if None"""
    if dt is None:
        return "NULL"
    return escape_sql_string(dt.isoformat())


def generate_create_tables_sql():
    """Generate SQL to create all necessary tables"""
    return '''
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS projects;
    DROP TABLE IF EXISTS ideas;
    DROP TABLE IF EXISTS sops;
    DROP TABLE IF EXISTS kpis;
    
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'Viewer',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        slug TEXT NOT NULL UNIQUE,
        description TEXT,
        long_description TEXT,
        image_url TEXT,
        demo_url TEXT,
        github_url TEXT,
        download_url TEXT,
        is_featured INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE ideas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'new',
        priority INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE sops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        content TEXT,
        version TEXT DEFAULT '1.0',
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE kpis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        target_value REAL,
        current_value REAL DEFAULT 0,
        unit TEXT,
        category TEXT,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
'''


def generate_users_sql(users_data, incremental=False):
    """Generate SQL to insert users"""
    logger.info("Generating SQL for users...")
    sql_statements = []
    
    for user_data in users_data:
        email = user_data['email']
        
        if incremental:
            # Add a check to skip if user exists in incremental mode
            sql_statements.append(f"-- Check if user {email} exists")
            sql_statements.append(f"INSERT OR IGNORE INTO users (email, password_hash, role) ")
        else:
            sql_statements.append(f"INSERT INTO users (email, password_hash, role) ")
            
        # Generate password hash
        password_hash = generate_password_hash(user_data['password'])
        
        sql_statements.append(f"VALUES ({escape_sql_string(email)}, {escape_sql_string(password_hash)}, {escape_sql_string(user_data['role'])});")
    
    return "\n".join(sql_statements)


def generate_projects_sql(projects_data, incremental=False):
    """Generate SQL to insert projects"""
    logger.info("Generating SQL for projects...")
    sql_statements = []
    
    for project_data in projects_data:
        slug = project_data['slug']
        
        if incremental:
            sql_statements.append(f"-- Check if project with slug '{slug}' exists")
            sql_statements.append("INSERT OR IGNORE INTO projects ")
        else:
            sql_statements.append("INSERT INTO projects ")
        
        sql_statements.append("(title, slug, description, long_description, image_url, ")
        sql_statements.append("demo_url, github_url, download_url, is_featured) ")
        sql_statements.append("VALUES (")
        sql_statements.append(f"{escape_sql_string(project_data['title'])}, ")
        sql_statements.append(f"{escape_sql_string(project_data['slug'])}, ")
        sql_statements.append(f"{escape_sql_string(project_data['description'])}, ")
        sql_statements.append(f"{escape_sql_string(project_data['long_description'])}, ")
        sql_statements.append(f"{escape_sql_string(project_data['image_url'])}, ")
        sql_statements.append(f"{escape_sql_string(project_data['demo_url'])}, ")
        sql_statements.append(f"{escape_sql_string(project_data['github_url'])}, ")
        sql_statements.append(f"{escape_sql_string(project_data['download_url'])}, ")
        sql_statements.append(f"{1 if project_data['is_featured'] else 0}")
        sql_statements.append(");")
    
    return "\n".join(sql_statements)


def generate_ideas_sql(ideas_data, incremental=False):
    """Generate SQL to insert ideas"""
    logger.info("Generating SQL for ideas...")
    sql_statements = []
    
    for idea_data in ideas_data:
        title = idea_data['title']
        
        if incremental:
            sql_statements.append(f"-- Check if idea '{title}' exists")
            sql_statements.append("INSERT OR IGNORE INTO ideas ")
        else:
            sql_statements.append("INSERT INTO ideas ")
        
        sql_statements.append("(title, description, status, priority) ")
        sql_statements.append("VALUES (")
        sql_statements.append(f"{escape_sql_string(title)}, ")
        sql_statements.append(f"{escape_sql_string(idea_data['description'])}, ")
        sql_statements.append(f"{escape_sql_string(idea_data['status'])}, ")
        sql_statements.append(f"{idea_data['priority']}")
        sql_statements.append(");")
    
    return "\n".join(sql_statements)


def generate_sops_sql(sops_data, incremental=False):
    """Generate SQL to insert SOPs"""
    logger.info("Generating SQL for SOPs...")
    sql_statements = []
    
    for sop_data in sops_data:
        title = sop_data['title']
        
        if incremental:
            sql_statements.append(f"-- Check if SOP '{title}' exists")
            sql_statements.append("INSERT OR IGNORE INTO sops ")
        else:
            sql_statements.append("INSERT INTO sops ")
        
        sql_statements.append("(title, description, content, version, category) ")
        sql_statements.append("VALUES (")
        sql_statements.append(f"{escape_sql_string(title)}, ")
        sql_statements.append(f"{escape_sql_string(sop_data['description'])}, ")
        sql_statements.append(f"{escape_sql_string(sop_data['content'])}, ")
        sql_statements.append(f"{escape_sql_string(sop_data['version'])}, ")
        sql_statements.append(f"{escape_sql_string(sop_data['category'])}")
        sql_statements.append(");")
    
    return "\n".join(sql_statements)


def generate_kpis_sql(kpis_data, incremental=False):
    """Generate SQL to insert KPIs"""
    logger.info("Generating SQL for KPIs...")
    sql_statements = []
    
    for kpi_data in kpis_data:
        title = kpi_data['title']
        
        if incremental:
            sql_statements.append(f"-- Check if KPI '{title}' exists")
            sql_statements.append("INSERT OR IGNORE INTO kpis ")
        else:
            sql_statements.append("INSERT INTO kpis ")
        
        # Parse date strings to datetime objects
        start_date = parse_date(kpi_data['start_date'])
        end_date = parse_date(kpi_data['end_date'])
        
        sql_statements.append("(title, description, target_value, current_value, unit, ")
        sql_statements.append("category, start_date, end_date) ")
        sql_statements.append("VALUES (")
        sql_statements.append(f"{escape_sql_string(title)}, ")
        sql_statements.append(f"{escape_sql_string(kpi_data['description'])}, ")
        sql_statements.append(f"{kpi_data['target_value']}, ")
        sql_statements.append(f"{kpi_data['current_value']}, ")
        sql_statements.append(f"{escape_sql_string(kpi_data['unit'])}, ")
        sql_statements.append(f"{escape_sql_string(kpi_data['category'])}, ")
        sql_statements.append(f"{format_datetime(start_date)}, ")
        sql_statements.append(f"{format_datetime(end_date)}")
        sql_statements.append(");")
    
    return "\n".join(sql_statements)


def run_seed(mode='standard'):
    """Generate SQL statements for seeding the database"""
    logger.info(f"Starting SQL generation in {mode} mode")
    
    # Load seed data
    seed_data = load_seed_data()
    
    # Store all SQL statements
    all_sql = []
    all_sql.append("-- Generated SQL for database seeding")
    all_sql.append(f"-- Mode: {mode}")
    all_sql.append(f"-- Generated at: {datetime.now().isoformat()}")
    all_sql.append("")
    
    # Begin transaction
    all_sql.append("BEGIN TRANSACTION;")
    all_sql.append("")
    
    # Reset database if in reset mode
    if mode == 'reset':
        all_sql.append("-- Reset database")
        all_sql.append(generate_create_tables_sql())
        all_sql.append("")
    
    # Determine if we're running in incremental mode
    incremental = (mode == 'incremental')
    
    # Generate SQL for each model
    all_sql.append("-- Seed users")
    all_sql.append(generate_users_sql(seed_data['users'], incremental))
    all_sql.append("")
    
    all_sql.append("-- Seed projects")
    all_sql.append(generate_projects_sql(seed_data['projects'], incremental))
    all_sql.append("")
    
    all_sql.append("-- Seed ideas")
    all_sql.append(generate_ideas_sql(seed_data['ideas'], incremental))
    all_sql.append("")
    
    all_sql.append("-- Seed SOPs")
    all_sql.append(generate_sops_sql(seed_data['sops'], incremental))
    all_sql.append("")
    
    all_sql.append("-- Seed KPIs")
    all_sql.append(generate_kpis_sql(seed_data['kpis'], incremental))
    all_sql.append("")
    
    # Commit transaction
    all_sql.append("COMMIT;")
    
    # Join all SQL statements with newlines
    sql_content = "\n".join(all_sql)
    
    # Get the database path
    db_path = get_db_path()
    
    # Create SQL file
    output_path = os.path.join(os.path.dirname(__file__), 'seed.sql')
    with open(output_path, 'w') as f:
        f.write(sql_content)
    
    logger.info(f"SQL statements written to {output_path}")
    
    # Execute the SQL if sqlite3 is available
    try:
        logger.info(f"Executing SQL on database at {db_path}")
        result = subprocess.run(
            ['sqlite3', db_path],
            input=sql_content.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if result.returncode == 0:
            logger.info("SQL execution successful")
        else:
            logger.error(f"SQL execution failed: {result.stderr.decode()}")
            logger.info("You can manually run the SQL with:")
            logger.info(f"sqlite3 {db_path} < {output_path}")
    except FileNotFoundError:
        logger.warning("sqlite3 command not found - SQL file generated but not executed")
        logger.info("You can manually run the SQL with:")
        logger.info(f"sqlite3 {db_path} < {output_path}")
    
    logger.info("🌱 Seed complete!")
    return "Database seeding completed successfully."


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Seed the database with sample data.')
    parser.add_argument('--mode', 
                      choices=['standard', 'reset', 'incremental'], 
                      default='standard', 
                      help='Seeding mode: standard (default), reset (wipe first), or incremental (only missing)')
    args = parser.parse_args()
    
    # Run seed process
    try:
        run_seed(args.mode)
    except Exception as e:
        logger.error(f"Seed process failed: {e}")
        sys.exit(1)
