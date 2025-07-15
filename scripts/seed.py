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
    """Load seed data from JSON file and sanitize edge cases"""
    try:
        seed_path = os.path.join(os.path.dirname(__file__), 'seed-data.json')
        with open(seed_path, 'r') as file:
            data = json.load(file)
        
        # Sanitize and validate the data
        return sanitize_seed_data(data)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load seed data: {e}")
        sys.exit(1)


def sanitize_seed_data(data):
    """Sanitize and validate seed data, handling edge cases"""
    # Process users
    for user in data['users']:
        # Validate email - truncate if too long
        if len(user['email']) > 120:
            logger.warning(f"User email too long ({len(user['email'])} chars): {user['email'][:30]}...")
            user['email'] = user['email'][:120]
        
        # Ensure password exists
        if not user.get('password'):
            logger.warning(f"User {user['email']} missing password, setting default")
            user['password'] = 'defaultPassword123'
        
        # Ensure role exists with a valid value
        valid_roles = ['Admin', 'Contributor', 'Viewer']
        if not user.get('role') or user['role'] not in valid_roles:
            logger.warning(f"User {user['email']} has invalid role: {user.get('role')}, defaulting to Viewer")
            user['role'] = 'Viewer'
    
    # Process projects
    for project in data['projects']:
        # Truncate title if too long (100 chars max in schema)
        if len(project['title']) > 100:
            logger.warning(f"Project title too long ({len(project['title'])} chars): {project['title'][:30]}...")
            project['title'] = project['title'][:100]
        
        # Ensure slug exists and is unique
        if not project.get('slug'):
            logger.warning(f"Project missing slug: {project['title']}")
            # Generate slug from title
            project['slug'] = project['title'].lower().replace(' ', '-')[:50]
        
        # Handle missing descriptions
        if not project.get('description'):
            logger.warning(f"Project missing description: {project['title']}")
            project['description'] = f"Description for {project['title']}"
    
    # Process ideas
    for idea in data['ideas']:
        # Truncate title if too long
        if len(idea['title']) > 100:
            logger.warning(f"Idea title too long ({len(idea['title'])} chars): {idea['title'][:30]}...")
            idea['title'] = idea['title'][:100]
        
        # Set default status if missing
        if not idea.get('status'):
            logger.warning(f"Idea missing status: {idea['title']}, defaulting to 'new'")
            idea['status'] = 'new'
        
        # Set default priority if missing or invalid
        if not isinstance(idea.get('priority'), int):
            logger.warning(f"Idea has invalid priority: {idea.get('priority')}, defaulting to 0")
            idea['priority'] = 0
    
    # Process SOPs
    for sop in data['sops']:
        # Truncate title if too long
        if len(sop['title']) > 100:
            logger.warning(f"SOP title too long ({len(sop['title'])} chars): {sop['title'][:30]}...")
            sop['title'] = sop['title'][:100]
        
        # Set default version if missing
        if not sop.get('version'):
            logger.warning(f"SOP missing version: {sop['title']}, defaulting to '1.0'")
            sop['version'] = '1.0'
        
        # Handle missing content
        if not sop.get('content'):
            logger.warning(f"SOP missing content: {sop['title']}, adding placeholder")
            sop['content'] = f"# {sop['title']}\n\nPlaceholder content."
    
    # Process KPIs
    for kpi in data['kpis']:
        # Truncate title if too long
        if len(kpi['title']) > 100:
            logger.warning(f"KPI title too long ({len(kpi['title'])} chars): {kpi['title'][:30]}...")
            kpi['title'] = kpi['title'][:100]
        
        # Escape special characters in title and category
        if kpi.get('category') and any(char in kpi['category'] for char in '<>&\'"'):
            logger.warning(f"KPI category contains special characters: {kpi['category']}")
            kpi['category'] = kpi['category'].replace('<', '&lt;').replace('>', '&gt;')
        
        # Ensure date fields exist
        current_year = datetime.now().year
        if not kpi.get('start_date'):
            logger.warning(f"KPI missing start_date: {kpi['title']}, using current date")
            kpi['start_date'] = datetime.now().isoformat()
        
        if not kpi.get('end_date'):
            logger.warning(f"KPI missing end_date: {kpi['title']}, setting to year end")
            kpi['end_date'] = f"{current_year}-12-31T23:59:59"
        
        # Handle very old dates by setting a reasonable minimum
        try:
            start_date = datetime.fromisoformat(kpi['start_date'].replace('Z', '+00:00'))
            if start_date.year < 2010:
                logger.warning(f"KPI has very old start date ({start_date.year}): {kpi['title']}, adjusting to 2010")
                kpi['start_date'] = f"2010-01-01T00:00:00"
        except (ValueError, AttributeError):
            logger.warning(f"KPI has invalid start_date format: {kpi['title']}, using current date")
            kpi['start_date'] = datetime.now().isoformat()
    
    return data


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
    """Generate SQL statements for users with proper escaping"""
    logger.info("Generating SQL for users...")
    sql_statements = []
    
    for user in users_data:
        email = user['email'].replace("'", "''")
        password = user['password']
        role = user.get('role', 'Viewer').replace("'", "''")
        password_hash = generate_password_hash(password)
        
        if incremental:
            sql_statements.append(f"-- Check if user {email} exists")
            sql_statements.append("INSERT OR IGNORE INTO users ")
        else:
            sql_statements.append("INSERT INTO users ")
            
        sql_statements.append("(email, password_hash, role) ")
        sql_statements.append("VALUES (")
        sql_statements.append(f"{escape_sql_string(email)}, ")
        sql_statements.append(f"{escape_sql_string(password_hash)}, ")
        sql_statements.append(f"{escape_sql_string(role)}")
        sql_statements.append(");")
    
    return "\n".join(sql_statements)


def generate_projects_sql(projects_data, incremental=False):
    """Generate SQL to insert projects with edge case handling"""
    logger.info("Generating SQL for projects...")
    sql_statements = []
    
    for project_data in projects_data:
        # Handle required fields
        title = project_data['title']
        slug = project_data['slug']
        
        # Handle optional fields with defaults
        description = project_data.get('description')
        if description is None:
            logger.warning(f"Project '{title[:30]}...' has no description, using NULL")
        
        long_description = project_data.get('long_description')
        image_url = project_data.get('image_url')
        demo_url = project_data.get('demo_url')
        github_url = project_data.get('github_url')
        download_url = project_data.get('download_url')
        is_featured = 1 if project_data.get('is_featured') else 0
        
        if incremental:
            sql_statements.append(f"-- Check if project with slug '{slug}' exists")
            sql_statements.append("INSERT OR IGNORE INTO projects ")
        else:
            sql_statements.append("INSERT INTO projects ")
        
        sql_statements.append("(title, slug, description, long_description, image_url, ")
        sql_statements.append("demo_url, github_url, download_url, is_featured) ")
        sql_statements.append("VALUES (")
        sql_statements.append(f"{escape_sql_string(title)}, ")
        sql_statements.append(f"{escape_sql_string(slug)}, ")
        sql_statements.append(f"{escape_sql_string(description) if description else 'NULL'}, ")
        sql_statements.append(f"{escape_sql_string(long_description) if long_description else 'NULL'}, ")
        sql_statements.append(f"{escape_sql_string(image_url) if image_url else 'NULL'}, ")
        sql_statements.append(f"{escape_sql_string(demo_url) if demo_url else 'NULL'}, ")
        sql_statements.append(f"{escape_sql_string(github_url) if github_url else 'NULL'}, ")
        sql_statements.append(f"{escape_sql_string(download_url) if download_url else 'NULL'}, ")
        sql_statements.append(f"{is_featured}")
        sql_statements.append(");")
    
    return "\n".join(sql_statements)


def generate_ideas_sql(ideas_data, incremental=False):
    """Generate SQL to insert ideas with proper handling of edge cases"""
    logger.info("Generating SQL for ideas...")
    sql_statements = []
    
    for idea_data in ideas_data:
        title = idea_data['title']
        
        # Safely handle potentially missing fields
        description = idea_data.get('description')
        if description is None:
            logger.warning(f"Idea '{title[:30]}...' has no description, using NULL")
            description = None
        
        status = idea_data.get('status', 'new')
        priority = idea_data.get('priority', 0)
        
        if incremental:
            sql_statements.append(f"-- Check if idea '{title}' exists")
            sql_statements.append("INSERT OR IGNORE INTO ideas ")
        else:
            sql_statements.append("INSERT INTO ideas ")
        
        sql_statements.append("(title, description, status, priority) ")
        sql_statements.append("VALUES (")
        sql_statements.append(f"{escape_sql_string(title)}, ")
        sql_statements.append(f"{escape_sql_string(description) if description else 'NULL'}, ")
        sql_statements.append(f"{escape_sql_string(status)}, ")
        sql_statements.append(f"{priority}")
        sql_statements.append(");")
    
    return "\n".join(sql_statements)


def generate_sops_sql(sops_data, incremental=False):
    """Generate SQL to insert SOPs with edge case handling"""
    logger.info("Generating SQL for SOPs...")
    sql_statements = []
    
    for sop_data in sops_data:
        title = sop_data['title']
        
        # Handle optional fields with defaults
        description = sop_data.get('description')
        if description is None:
            logger.warning(f"SOP '{title[:30]}...' has no description, using NULL")
            
        content = sop_data.get('content')
        if content is None:
            logger.warning(f"SOP '{title[:30]}...' has no content, using placeholder")
            content = f"# {title}\n\nPlaceholder content for {title}"
        
        version = sop_data.get('version', '1.0')
        category = sop_data.get('category', 'General')
        
        if incremental:
            sql_statements.append(f"-- Check if SOP '{title}' exists")
            sql_statements.append("INSERT OR IGNORE INTO sops ")
        else:
            sql_statements.append("INSERT INTO sops ")
        
        sql_statements.append("(title, description, content, version, category) ")
        sql_statements.append("VALUES (")
        sql_statements.append(f"{escape_sql_string(title)}, ")
        sql_statements.append(f"{escape_sql_string(description) if description else 'NULL'}, ")
        sql_statements.append(f"{escape_sql_string(content)}, ")
        sql_statements.append(f"{escape_sql_string(version)}, ")
        sql_statements.append(f"{escape_sql_string(category)}")
        sql_statements.append(");")
    
    return "\n".join(sql_statements)


def generate_kpis_sql(kpis_data, incremental=False):
    """Generate SQL to insert KPIs with edge case handling"""
    logger.info("Generating SQL for KPIs...")
    sql_statements = []
    
    if not isinstance(kpis_data, list):
        logger.warning("KPIs data is not a list, converting...")
        if isinstance(kpis_data, dict):
            kpis_data = [kpis_data]
        else:
            logger.error("Invalid KPI data format")
            return "-- No valid KPI data to insert"
    
    for kpi_data in kpis_data:
        # Ensure we're working with a dictionary
        if not isinstance(kpi_data, dict):
            logger.warning(f"Skipping invalid KPI data: {kpi_data}")
            continue
            
        # Handle required title field
        if 'title' not in kpi_data:
            logger.warning("KPI missing title, skipping")
            continue
        
        title = kpi_data['title']
        
        # Handle potentially missing fields or invalid data
        description = kpi_data.get('description')
        if description is None:
            logger.warning(f"KPI '{title[:30]}...' has no description, using NULL")
            description = None
            
        # Handle numeric fields
        try:
            target_value = float(kpi_data.get('target_value', 0))
        except (ValueError, TypeError):
            logger.warning(f"KPI '{title[:30]}...' has invalid target_value, using 0")
            target_value = 0
            
        try:
            current_value = float(kpi_data.get('current_value', 0))
        except (ValueError, TypeError):
            logger.warning(f"KPI '{title[:30]}...' has invalid current_value, using 0")
            current_value = 0
            
        unit = kpi_data.get('unit', '')
        category = kpi_data.get('category', '')
        
        # Handle potential special characters in category
        if category and any(char in category for char in '<>&\'"'):
            logger.warning(f"KPI '{title[:30]}...' has special characters in category, escaping")
            # Already handled in sanitize function, just log the warning
            
        if incremental:
            sql_statements.append(f"-- Check if KPI '{title}' exists")
            sql_statements.append("INSERT OR IGNORE INTO kpis ")
        else:
            sql_statements.append("INSERT INTO kpis ")
            
        # Parse dates if provided
        start_date = None
        if 'start_date' in kpi_data and kpi_data['start_date']:
            try:
                start_date = parse_date(kpi_data['start_date'])
                # Warn about very old dates (already handled in sanitize function)
                if start_date.year < 2010:
                    logger.warning(f"KPI '{title[:30]}...' has very old start_date: {start_date.year}")
            except ValueError:
                logger.warning(f"KPI '{title[:30]}...' has invalid start_date format, using NULL")
                
        end_date = None
        if 'end_date' in kpi_data and kpi_data['end_date']:
            try:
                end_date = parse_date(kpi_data['end_date'])
            except ValueError:
                logger.warning(f"KPI '{title[:30]}...' has invalid end_date format, using NULL")
        
        sql_statements.append("(title, description, target_value, current_value, unit, ")
        sql_statements.append("category, start_date, end_date) ")
        sql_statements.append("VALUES (")
        sql_statements.append(f"{escape_sql_string(title)}, ")
        sql_statements.append(f"{escape_sql_string(description) if description else 'NULL'}, ")
        sql_statements.append(f"{target_value}, ")
        sql_statements.append(f"{current_value}, ")
        sql_statements.append(f"{escape_sql_string(unit)}, ")
        sql_statements.append(f"{escape_sql_string(category)}, ")
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
    try:
        # Add debugging to check the KPIs data structure
        if 'kpis' not in seed_data:
            logger.warning("No KPIs data found in seed data")
            all_sql.append("-- No KPIs data to insert")
        else:
            kpis_data = seed_data['kpis']
            logger.info(f"KPIs data type: {type(kpis_data)}")
            
            # Ensure kpis_data is a list
            if not isinstance(kpis_data, list):
                logger.warning("KPIs data is not a list, converting to list")
                if isinstance(kpis_data, dict):
                    kpis_data = [kpis_data]
                else:
                    logger.error(f"Invalid KPIs data type: {type(kpis_data)}")
                    kpis_data = []
            
            logger.info(f"Number of KPIs: {len(kpis_data)}")
            all_sql.append(generate_kpis_sql(kpis_data, incremental))
    except Exception as e:
        logger.error(f"Error processing KPIs data: {e}")
        all_sql.append("-- Error processing KPIs data")
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
    parser.add_argument('--debug', 
                      action='store_true', 
                      help='Enable debug logging')
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run seeding process
    try:
        run_seed(mode=args.mode)
    except Exception as e:
        logger.error(f"Seed process failed: {e}")
        # Print traceback for better debugging
        import traceback
        logger.error("Error details:")
        logger.error(traceback.format_exc())
        sys.exit(1)
