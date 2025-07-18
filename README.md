# The Solution Desk

A modern web application for The Solution Desk, featuring an interactive Kanban board, project management tools, and more.

**Live here:** https://the-solution-desk.github.io

[![E2E Tests](https://github.com/TheSolutionDeskAndCompany/the-solution-desk.github.io/actions/workflows/cypress.yml/badge.svg)](https://github.com/TheSolutionDeskAndCompany/the-solution-desk.github.io/actions/workflows/cypress.yml)

## Features

- Interactive Kanban board with drag-and-drop functionality
- Project management tools
- Real-time updates
- Responsive design
- Comprehensive testing suite
- CI/CD pipeline with GitHub Actions

## Development

### Prerequisites

- Node.js 18+
- npm 9+

### Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
4. Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

### Testing

Run the test suite:

```bash
# Run all tests
npm test

# Run E2E tests with Cypress
npm run cy:open  # Interactive mode
npm run cy:run   # Headless mode
```

### CI/CD

This project uses GitHub Actions for continuous integration and deployment. The following workflows are configured:

- **E2E Tests**: Runs on every push and pull request to main branches
  - Installs dependencies
  - Starts the development server
  - Runs Cypress end-to-end tests
  - Generates test artifacts and videos

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

### Local Deployment

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

### 🚀 Deploying the Backend to Render

#### Prerequisites

1. **Bash**
2. **cURL**
3. **Render API key** (from your Render dashboard)
4. A `.env` file (optional) containing:

   ```
   DATABASE_URL=your_database_url
   JWT_SECRET=your_jwt_secret
   ```

#### 1. Export Your Render API Key

```bash
export RENDER_API_KEY="your_actual_render_api_key"
```

#### 2. Export (or Provide) App Secrets

If you don't want to use a `.env` file, export directly:

```bash
export DATABASE_URL="your_database_url"
export JWT_SECRET="your_jwt_secret"
```

*Note:* If `DATABASE_URL` or `JWT_SECRET` aren't in your environment, the script will fall back to reading them from `.env` in the current directory.

#### 3. Run the Deployment Script

```bash
chmod +x deploy_to_render.sh
./deploy_to_render.sh
```

* **What it does under the hood:**

  1. Creates (or updates) a Web Service on Render linked to your GitHub repo's `main` branch.
  2. Injects your `DATABASE_URL` and `JWT_SECRET` as env vars.
  3. Sets `buildCommand` and `startCommand` for your Python backend.
  4. Triggers the first deploy automatically.

#### 4. Track Your Deploy

* After the script runs, you'll see:

  ```
  Service ID: srv-abc123xyz
  Deployment triggered at: https://dashboard.render.com/services/ow-backend/deploys
  ```
* **Optional:** Copy that URL into your browser or run:

  ```bash
  curl -s https://dashboard.render.com/services/ow-backend/deploys
  ```

#### 5. Verify Health

Either:

```bash
curl -sSf https://ow-backend.onrender.com/health && echo "✅ Backend is healthy!"
```

Or let the built-in wait loop run automatically:

```bash
# (This is printed for you at the end of deploy_to_render.sh)
until curl -sSf https://ow-backend.onrender.com/health; do
  echo "⏳ Waiting for backend…"
  sleep 5
done
echo "🚀 Backend is live!"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
