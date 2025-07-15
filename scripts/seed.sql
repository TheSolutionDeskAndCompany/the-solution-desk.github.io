-- Generated SQL for database seeding
-- Mode: reset
-- Generated at: 2025-07-15T06:45:41.025913

BEGIN TRANSACTION;

-- Reset database

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


-- Seed users
INSERT INTO users 
(email, password_hash, role) 
VALUES (
'admin@solutiondesk.com', 
'sha256$99ef9943ade34284$zx0dvAyRZF27znmy/5IYnTygVYORmd351zUSaoyMk3E=', 
'Admin'
);
INSERT INTO users 
(email, password_hash, role) 
VALUES (
'contributor@solutiondesk.com', 
'sha256$e2b4af37a176f85a$SEtEO3+lfYbgQIdA4ztkBsNQAPBgjDhlkMPWua/W7WE=', 
'Contributor'
);
INSERT INTO users 
(email, password_hash, role) 
VALUES (
'viewer@solutiondesk.com', 
'sha256$ea1de6dd25b24227$A1XL7J5HDKsQWGSHWS1d+crfc5rHgxInEU1c4moPOwk=', 
'Viewer'
);
INSERT INTO users 
(email, password_hash, role) 
VALUES (
'test@example.com', 
'sha256$32926453bcbf3307$vIX7YSCIXqD35XewU3/WBLF2PFZ87P6TGuSVckXYHYU=', 
'Viewer'
);
INSERT INTO users 
(email, password_hash, role) 
VALUES (
'longemailtestingthemaximumlengthpossibleforemailaddress@verylongdomainnamethatmightcauseuiissues.co.uk', 
'sha256$43de01f0780a94fc$GXMyjcjEsQC8nd575dLFPwj2rt1h+VSk0u6WbZQzjjo=', 
'Viewer'
);

-- Seed projects
INSERT INTO projects 
(title, slug, description, long_description, image_url, 
demo_url, github_url, download_url, is_featured) 
VALUES (
'Portfolio Website', 
'portfolio-website', 
'A responsive portfolio website showcasing projects and skills', 
'A comprehensive portfolio website built using React and Flask, featuring dynamic content loading, responsive design, and a contact form that integrates with email services. The site is optimized for performance and SEO.', 
'/static/images/projects/portfolio.jpg', 
'https://portfolio.solutiondesk.com', 
'https://github.com/solutiondesk/portfolio', 
NULL, 
1
);
INSERT INTO projects 
(title, slug, description, long_description, image_url, 
demo_url, github_url, download_url, is_featured) 
VALUES (
'Task Management System', 
'task-management', 
'A Kanban-style task management application', 
'A comprehensive task management system with drag-and-drop functionality, task priorities, deadlines, and team collaboration features. Built with React for the frontend and Flask for the backend API.', 
'/static/images/projects/task-manager.jpg', 
'https://tasks.solutiondesk.com', 
'https://github.com/solutiondesk/task-manager', 
'/downloads/task-manager-v1.0.zip', 
1
);
INSERT INTO projects 
(title, slug, description, long_description, image_url, 
demo_url, github_url, download_url, is_featured) 
VALUES (
'E-commerce Platform', 
'ecommerce-platform', 
'A full-featured e-commerce solution', 
'An end-to-end e-commerce platform with product catalog, shopping cart, payment processing, and order management. Integrates with various payment gateways and shipping services.', 
'/static/images/projects/ecommerce.jpg', 
'https://shop.solutiondesk.com', 
'https://github.com/solutiondesk/ecommerce', 
NULL, 
0
);
INSERT INTO projects 
(title, slug, description, long_description, image_url, 
demo_url, github_url, download_url, is_featured) 
VALUES (
'This is an extremely long project title that might cause UI issues in some views and should be handl', 
'very-long-title-project', 
'Testing extremely long titles', 
'This project exists solely to test how the UI handles extremely long titles and descriptions. It''s important that our application can handle edge cases like this gracefully without breaking layouts or truncating text inappropriately.', 
NULL, 
NULL, 
NULL, 
NULL, 
0
);
INSERT INTO projects 
(title, slug, description, long_description, image_url, 
demo_url, github_url, download_url, is_featured) 
VALUES (
'Empty Project', 
'empty-project', 
'Description for Empty Project', 
NULL, 
NULL, 
NULL, 
NULL, 
NULL, 
0
);

-- Seed ideas
INSERT INTO ideas 
(title, description, status, priority) 
VALUES (
'AI-powered Content Recommender', 
'Create a content recommendation system using machine learning algorithms to suggest personalized content based on user behavior and preferences.', 
'new', 
3
);
INSERT INTO ideas 
(title, description, status, priority) 
VALUES (
'Mobile App Version', 
'Develop a mobile application version of our platform for iOS and Android devices with offline capabilities.', 
'in_progress', 
5
);
INSERT INTO ideas 
(title, description, status, priority) 
VALUES (
'This is an extremely long idea title that exceeds normal length and will test the handling of excess', 
'A normal description for an idea with an extremely long title.', 
'new', 
2
);
INSERT INTO ideas 
(title, description, status, priority) 
VALUES (
'Idea with Missing Status', 
'This idea has a missing status field which should be handled by defaulting to ''new''', 
'new', 
3
);
INSERT INTO ideas 
(title, description, status, priority) 
VALUES (
'Interactive Dashboard', 
'Build an interactive analytics dashboard with real-time data visualization and filtering capabilities.', 
'completed', 
2
);
INSERT INTO ideas 
(title, description, status, priority) 
VALUES (
'Social Media Integration', 
'Add social media integration to allow users to share content directly from our platform to various social networks.', 
'new', 
1
);
INSERT INTO ideas 
(title, description, status, priority) 
VALUES (
'Dark Mode Theme', 
'Implement a dark mode theme option for better user experience in low-light environments and to reduce eye strain.', 
'in_progress', 
4
);
INSERT INTO ideas 
(title, description, status, priority) 
VALUES (
'Legacy Feature Migration', 
NULL, 
'archived', 
0
);

-- Seed SOPs
INSERT INTO sops 
(title, description, content, version, category) 
VALUES (
'New Client Onboarding', 
'Standard procedure for onboarding new clients to our platform', 
'# New Client Onboarding Procedure

## Step 1: Initial Consultation
- Schedule a 30-minute call to understand client needs
- Document requirements and expectations

## Step 2: Account Setup
- Create client account in the system
- Send welcome email with login credentials

## Step 3: Training Session
- Schedule a 1-hour training session
- Cover basic platform features and use cases

## Step 4: Follow-up
- Check in after 7 days to address any questions
- Request feedback on onboarding experience', 
'1.2', 
'Customer Service'
);
INSERT INTO sops 
(title, description, content, version, category) 
VALUES (
'Software Deployment Process', 
'Step-by-step procedure for deploying new code to production', 
'# Software Deployment Process

## Pre-Deployment
1. Complete all code reviews
2. Run automated test suite
3. Verify staging environment deployment

## Deployment
1. Create deployment branch
2. Deploy to production server
3. Run smoke tests

## Post-Deployment
1. Monitor application performance
2. Check error logs
3. Update documentation', 
'2.0', 
'Development'
);
INSERT INTO sops 
(title, description, content, version, category) 
VALUES (
'Emergency Response Protocol', 
'Protocol for handling critical system outages and emergencies', 
'# Emergency Response Protocol

## Detection
- Automated monitoring alerts
- Customer reported issues

## Assessment
- Determine severity level (1-4)
- Identify affected systems

## Response
- Level 1: Immediate all-hands response
- Level 2: Team lead coordinates response
- Level 3: On-call engineer handles
- Level 4: Scheduled fix

## Communication
- Update status page
- Send customer notifications
- Internal incident report', 
'1.5', 
'Operations'
);

-- Seed KPIs
INSERT INTO kpis 
(title, description, target_value, current_value, unit, 
category, start_date, end_date) 
VALUES (
'Monthly Active Users', 
'Number of unique users who engage with the platform each month', 
10000.0, 
7500.0, 
'users', 
'Engagement', 
'2025-01-01T00:00:00', 
'2025-12-31T23:59:59'
);
INSERT INTO kpis 
(title, description, target_value, current_value, unit, 
category, start_date, end_date) 
VALUES (
'KPI with Very Old Start Date', 
'This KPI has a start date from many years ago to test date handling', 
100.0, 
80.0, 
'points', 
'Testing', 
'2010-01-01T00:00:00', 
'2030-12-31T23:59:59'
);
INSERT INTO kpis 
(title, description, target_value, current_value, unit, 
category, start_date, end_date) 
VALUES (
'KPI with Missing Dates', 
'This KPI is missing date fields which should be handled gracefully', 
50.0, 
25.0, 
'%', 
'Testing', 
'2025-07-15T06:45:41.025833', 
'2025-12-31T23:59:59'
);
INSERT INTO kpis 
(title, description, target_value, current_value, unit, 
category, start_date, end_date) 
VALUES (
'KPI with Special Characters: #$%^&*()!@', 
'Testing how special characters are handled in titles and descriptions', 
100.0, 
50.0, 
'units', 
'Testing &lt;script&gt;alert(''XSS Test'')&lt;/script&gt;', 
'2025-01-01T00:00:00', 
'2025-12-31T23:59:59'
);
INSERT INTO kpis 
(title, description, target_value, current_value, unit, 
category, start_date, end_date) 
VALUES (
'Customer Satisfaction', 
'Average satisfaction score from customer feedback surveys', 
4.8, 
4.5, 
'stars', 
'Customer Service', 
'2025-01-01T00:00:00', 
'2025-12-31T23:59:59'
);
INSERT INTO kpis 
(title, description, target_value, current_value, unit, 
category, start_date, end_date) 
VALUES (
'Conversion Rate', 
'Percentage of visitors who complete a desired action', 
5.0, 
3.2, 
'%', 
'Sales', 
'2025-01-01T00:00:00', 
'2025-12-31T23:59:59'
);
INSERT INTO kpis 
(title, description, target_value, current_value, unit, 
category, start_date, end_date) 
VALUES (
'Bug Resolution Time', 
'Average time to resolve reported bugs', 
48.0, 
72.0, 
'hours', 
'Development', 
'2025-01-01T00:00:00', 
'2025-12-31T23:59:59'
);

COMMIT;