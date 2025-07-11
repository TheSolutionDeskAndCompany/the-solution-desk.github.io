from flask import Flask, render_template, send_from_directory, abort
import os

# Initialize Flask app, serve static at root to expose .well-known
app = Flask(__name__, static_folder='static', static_url_path='')

# Project definitions
projects = {
    'autohired': {
        'name': 'AutoHired',
        'tagline': 'AI-powered resume + job application bot',
        'category': 'Automation Tool',
        'tech_stack': 'Python, Flask, OpenAI API',
        'description': 'Automatically generate and submit tailored job applications based on your resume and job listings.',
        'download_link': '/downloads/autohired.zip',
        'repo_link': 'https://github.com/TheSolutionDeskAndCompany/AutoHired'
    },
    'organiserpro': {
        'name': 'OrganiserPro',
        'tagline': 'CLI-based file management tool',
        'category': 'CLI Utility',
        'tech_stack': 'Python, argparse',
        'description': 'Sort, clean, and deduplicate files across massive directories using the command line.',
        'download_link': '/downloads/organiserpro.zip',
        'repo_link': 'https://github.com/TheSolutionDeskAndCompany/OrganiserPro'
    },
    'process-optimization-app': {
        'name': 'Process Optimization App',
        'tagline': 'Smart automation assistant for daily ops',
        'category': 'Automation Assistant',
        'tech_stack': 'Python, Flask',
        'description': 'Smart automation assistant for daily ops',
        'download_link': None,
        'repo_link': 'https://github.com/TheSolutionDeskAndCompany/Process-Optimization-App'
    },
    'shelltasker': {
        'name': 'ShellTasker',
        'tagline': 'Custom script automation via reusable CLI commands',
        'category': 'CLI Utility',
        'tech_stack': 'Python',
        'description': 'Custom script automation via reusable CLI commands',
        'download_link': None,
        'repo_link': 'https://github.com/TheSolutionDeskAndCompany/ShellTasker'
    },
    'quickdeploy-cli': {
        'name': 'QuickDeploy CLI',
        'tagline': 'One-command full-stack deploy to Vercel/Netlify',
        'category': 'CLI Utility',
        'tech_stack': 'Node.js',
        'description': 'One-command full-stack deploy to Vercel/Netlify',
        'download_link': None,
        'repo_link': 'https://github.com/TheSolutionDeskAndCompany/QuickDeploy-CLI'
    }
}

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

@app.route('/projects/<project_id>')
def project_detail(project_id):
    project = projects.get(project_id)
    if not project:
        abort(404)
    return render_template('project_detail.html', project=project)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
