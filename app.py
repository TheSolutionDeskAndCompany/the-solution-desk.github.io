from flask import Flask, render_template, send_from_directory
import os

# Initialize Flask app, serve static at root to expose .well-known
app = Flask(__name__, static_folder='static', static_url_path='')

# Project definitions
projects = [
    {'name': 'AutoHired', 'description': 'AI-powered resume + job application bot', 'download': False},
    {'name': 'OrganiserPro', 'description': 'CLI-based file management tool', 'download': True, 'file': 'project.zip'},
    {'name': 'Process Optimization App', 'description': 'Smart automation assistant for daily ops', 'download': False},
    {'name': 'ShellTasker', 'description': 'Custom script automation via reusable CLI commands', 'download': False},
    {'name': 'QuickDeploy CLI', 'description': 'One-command full-stack deploy to Vercel/Netlify', 'download': False},
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
