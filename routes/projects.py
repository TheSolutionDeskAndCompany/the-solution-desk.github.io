from flask import Blueprint, render_template, send_from_directory, current_app, abort
import os
from models.project import Project

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/')
def list_projects():
    """List all projects"""
    projects = Project.get_all()
    return render_template('projects/index.html', projects=projects)

@projects_bp.route('/<slug>')
def project_detail(slug):
    """Show project details"""
    project = Project.get_by_slug(slug)
    if not project:
        abort(404)
    return render_template('projects/detail.html', project=project)

@projects_bp.route('/<slug>/download')
def download_project(slug):
    """Download project files"""
    project = Project.get_by_slug(slug)
    if not project or not project.download_url:
        abort(404)
    
    # If it's a local file
    if project.download_url.startswith('/'):
        return send_from_directory(
            os.path.join(current_app.root_path, 'downloads'),
            os.path.basename(project.download_url),
            as_attachment=True
        )
    # If it's a URL, redirect to it
    from flask import redirect
    return redirect(project.download_url)
