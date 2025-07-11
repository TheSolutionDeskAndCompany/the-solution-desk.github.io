from flask import Flask, render_template, send_from_directory, abort
import os

# Initialize Flask app, serve static at root to expose .well-known
app = Flask(__name__, static_folder='static', static_url_path='')

# Project definitions
import json

with open(os.path.join(app.root_path, 'projects.json')) as f:
    projects = json.load(f)


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
