# The Solution Desk

A Flask-based web application for The Solution Desk, featuring project showcases, tools, and contact information.

**Live here:** https://the-solution-desk.github.io

## Features

- Project showcase with detailed views
- Tools and utilities section
- Contact form
- Responsive design
- Database integration
- Testing framework

## Project Structure

```
the-solution-desk/
├── app.py                 # Main application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── instance/              # Instance-specific config
├── models/                # Database models
│   └── project.py         # Project model
├── routes/                # Application routes
│   ├── __init__.py
│   ├── main.py           # Main routes (home, about, contact)
│   ├── projects.py       # Project-related routes
│   └── tools.py          # Tools-related routes
├── static/               # Static files (CSS, JS, images)
├── templates/            # Jinja2 templates
└── tests/                # Test files
    ├── conftest.py      # Test configuration
    ├── test_models.py   # Model tests
    └── test_routes.py   # Route tests
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TheSolutionDeskAndCompany/the-solution-desk.github.io.git
   cd the-solution-desk
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Running the Application

1. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

2. Run the development server:
   ```bash
   python app.py
   ```
   Then visit http://localhost:5000

### Running Tests

```bash
pytest
```

## Deployment

1. For production, set up a WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 'app:create_app()'
   ```

2. Set the following environment variables in production:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   DATABASE_URL=your-database-url
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
