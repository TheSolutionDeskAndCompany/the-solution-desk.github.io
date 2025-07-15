from flask_restful import Resource
from flask import jsonify, request, current_app
from marshmallow import ValidationError
from models.project import Project
from schemas.project import ProjectSchema
from app import db

class ProjectsAPI(Resource):
    def get(self, id=None):
        """Get a specific project or all projects"""
        if id:
            proj = Project.query.get_or_404(id)
            return jsonify(proj.serialize())
        all_projects = Project.query.all()
        return jsonify([p.serialize() for p in all_projects])

    def post(self):
        """Create a new project"""
        try:
            # Load data through schema with validation
            schema = ProjectSchema()
            schema.context = {'create_mode': True}
            proj = schema.load(request.get_json())
            
            # Add and commit to database
            db.session.add(proj)
            db.session.commit()
            
            # Log successful creation
            current_app.logger.info(f"Project created: {proj.title}")
            
            return jsonify(schema.dump(proj)), 201
            
        except ValidationError as err:
            current_app.logger.warning(f"Project creation validation error: {err.messages}")
            return {"errors": err.messages}, 400
        except Exception as e:
            current_app.logger.error(f"Error creating project: {str(e)}")
            db.session.rollback()
            return {"error": "An error occurred while creating the project"}, 500

    def put(self, id):
        """Update an existing project"""
        try:
            proj = Project.query.get_or_404(id)
            
            # Load and validate data through schema
            schema = ProjectSchema()
            schema.context = {'create_mode': False}
            
            # Partial=True allows for partial updates
            data = request.get_json()
            proj = schema.load(data, instance=proj, partial=True)
            
            db.session.commit()
            current_app.logger.info(f"Project updated: {proj.title} (ID: {id})")
            
            return jsonify(schema.dump(proj))
            
        except ValidationError as err:
            current_app.logger.warning(f"Project update validation error for ID {id}: {err.messages}")
            return {"errors": err.messages}, 400
        except Exception as e:
            current_app.logger.error(f"Error updating project ID {id}: {str(e)}")
            db.session.rollback()
            return {"error": "An error occurred while updating the project"}, 500

    def delete(self, id):
        """Delete a project"""
        try:
            proj = Project.query.get_or_404(id)
            project_title = proj.title  # Store for logging before deletion
            
            db.session.delete(proj)
            db.session.commit()
            
            current_app.logger.info(f"Project deleted: {project_title} (ID: {id})")
            return '', 204
            
        except Exception as e:
            current_app.logger.error(f"Error deleting project ID {id}: {str(e)}")
            db.session.rollback()
            return {"error": "An error occurred while deleting the project"}, 500
