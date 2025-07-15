from flask import Blueprint, render_template, send_from_directory, current_app
import os

# Create main blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@main.route('/contact')
def contact():
    """Render the contact page"""
    return render_template('contact.html')

@main.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')

@main.route('/downloads/<path:filename>')
def download_file(filename):
    """Serve files from the downloads directory"""
    return send_from_directory(
        os.path.join(current_app.root_path, 'downloads'),
        filename,
        as_attachment=True
    )

@main.route('/.well-known/security.txt')
def security_txt():
    """Serve security.txt for security policy"""
    return send_from_directory(
        os.path.join(current_app.root_path, 'static', '.well-known'),
        'security.txt',
        mimetype='text/plain'
    )
