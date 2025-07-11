from flask import Flask, render_template, send_from_directory, abort
import os

# Initialize Flask app, serve static at root to expose .well-known
app = Flask(__name__, static_folder='static', static_url_path='')

# Project definitions
projects = [
    {
        'name': 'AutoHired',
        'slug': 'autohired',
        'description': 'AI-powered resume + job application bot',
        'download': False,
        'repo_url': 'https://github.com/TheSolutionDeskAndCompany/AutoHired'
    },
    {
        'name': 'OrganiserPro',
        'slug': 'organiserpro',
        'description': 'CLI-based file management tool',
        'download': True,
        'file': 'project.zip',
        'repo_url': 'https://github.com/TheSolutionDeskAndCompany/OrganiserPro'
    },
    {
        'name': 'Process Optimization App',
        'slug': 'process-optimization-app',
        'description': 'Smart automation assistant for daily ops',
        'download': False,
        'repo_url': 'https://github.com/TheSolutionDeskAndCompany/Process-Optimization-App'
    },
    {
        'name': 'ShellTasker',
        'slug': 'shelltasker',
        'description': 'Custom script automation via reusable CLI commands',
        'download': False,
        'repo_url': 'https://github.com/TheSolutionDeskAndCompany/ShellTasker'
    },
    {
        'name': 'QuickDeploy CLI',
        'slug': 'quickdeploy-cli',
        'description': 'One-command full-stack deploy to Vercel/Netlify',
        'download': False,
        'repo_url': 'https://github.com/TheSolutionDeskAndCompany/QuickDeploy-CLI'
    },
]

@app.route('/')
def index():
    return render_template('index.html', projects=projects)

@app.route('/projects')
def projects_page():
    return render_template('index.html', projects=projects)

@app.route('/tools')
def tools_page():
    # Placeholder tools listing
    tools = ['AutoHired', 'OrganiserPro', 'Process Optimization App', 'ShellTasker', 'QuickDeploy CLI']
    return render_template('tools.html', tools=tools)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'downloads'), filename, as_attachment=True)

@app.route('/.well-known/security.txt')
def security_txt():
    return send_from_directory(os.path.join(app.root_path, 'static', '.well-known'), 'security.txt')

# Helper to create URL slugs
def slugify(name):
    return name.lower().replace(' ', '-')

@app.route('/projects/<slug>')
def project_detail(slug):
    project = next((p for p in projects if p['slug'] == slug), None)
    if not project:
        abort(404)
    return render_template('project_detail.html', project=project)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
