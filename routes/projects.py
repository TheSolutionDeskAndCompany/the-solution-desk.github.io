from flask import Blueprint, render_template, send_from_directory, current_app, abort, request, redirect, url_for, flash
import os
from models.project import Project
from models.user import RoleEnum
from flask_login import login_required, current_user
from utils.rbac import roles_required
from app import db

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

@projects_bp.route('/create', methods=['GET', 'POST'])
@login_required
@roles_required(RoleEnum.ADMIN.value, RoleEnum.CONTRIBUTOR.value)
def create_project():
    """Create a new project (Admin and Contributor only)"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        github_url = request.form.get('github_url', '')
        demo_url = request.form.get('demo_url', '')
        download_url = request.form.get('download_url', '')
        
        if not title or not description:
            flash('Title and description are required', 'danger')
            return render_template('projects/create.html')
            
        project = Project(title=title, description=description, github_url=github_url,
                         demo_url=demo_url, download_url=download_url)
        db.session.add(project)
        db.session.commit()
        
        flash('Project created successfully', 'success')
        return redirect(url_for('projects.project_detail', slug=project.slug))
        
    return render_template('projects/create.html')

@projects_bp.route('/edit/<slug>', methods=['GET', 'POST'])
@login_required
@roles_required(RoleEnum.ADMIN.value, RoleEnum.CONTRIBUTOR.value)
def edit_project(slug):
    """Edit an existing project (Admin and Contributor only)"""
    project = Project.get_by_slug(slug)
    if not project:
        abort(404)
        
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.github_url = request.form.get('github_url', '')
        project.demo_url = request.form.get('demo_url', '')
        project.download_url = request.form.get('download_url', '')
        
        if not project.title or not project.description:
            flash('Title and description are required', 'danger')
            return render_template('projects/edit.html', project=project)
            
        db.session.commit()
        flash('Project updated successfully', 'success')
        return redirect(url_for('projects.project_detail', slug=project.slug))
        
    return render_template('projects/edit.html', project=project)

@projects_bp.route('/delete/<slug>', methods=['POST'])
@login_required
@roles_required(RoleEnum.ADMIN.value)
def delete_project(slug):
    """Delete a project (Admin only)"""
    project = Project.get_by_slug(slug)
    if not project:
        abort(404)
        
    db.session.delete(project)
    db.session.commit()
    
    flash('Project deleted successfully', 'success')
    return redirect(url_for('projects.list_projects'))
