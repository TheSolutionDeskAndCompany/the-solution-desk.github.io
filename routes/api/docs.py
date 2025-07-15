"""
API Documentation using Flask-RESTX for Swagger UI
"""
from flask import Blueprint
from flask_restx import Api, Resource, fields

# Create a blueprint for API documentation
api_docs_bp = Blueprint('api_docs', __name__)

# Create API with documentation configuration
api = Api(
    api_docs_bp,
    title='The Solution Desk API',
    version='1.0',
    description='API Documentation for The Solution Desk',
    doc='/docs',
    authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    security='apikey'
)

# Define namespaces for different resource types
ns_projects = api.namespace('projects', description='Project operations')
ns_ideas = api.namespace('ideas', description='Ideas operations')
ns_sops = api.namespace('sops', description='Standard Operating Procedures operations')
ns_kpis = api.namespace('kpis', description='KPI operations')
ns_users = api.namespace('users', description='User operations')

# Define models for documentation
project_model = api.model('Project', {
    'id': fields.Integer(readOnly=True, description='The project unique identifier'),
    'title': fields.String(required=True, description='Project title'),
    'slug': fields.String(required=True, description='URL slug'),
    'description': fields.String(description='Short description'),
    'long_description': fields.String(description='Detailed description'),
    'image_url': fields.String(description='Project image URL'),
    'github_url': fields.String(description='GitHub repository URL'),
    'download_url': fields.String(description='Download URL'),
    'demo_url': fields.String(description='Demo URL'),
    'is_featured': fields.Boolean(description='Featured project status')
})

idea_model = api.model('Idea', {
    'id': fields.Integer(readOnly=True, description='The idea unique identifier'),
    'title': fields.String(required=True, description='Idea title'),
    'description': fields.String(description='Idea description'),
    'status': fields.String(description='Idea status'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

sop_model = api.model('SOP', {
    'id': fields.Integer(readOnly=True, description='The SOP unique identifier'),
    'title': fields.String(required=True, description='SOP title'),
    'content': fields.String(required=True, description='SOP content'),
    'category': fields.String(description='SOP category'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

kpi_model = api.model('KPI', {
    'id': fields.Integer(readOnly=True, description='The KPI unique identifier'),
    'name': fields.String(required=True, description='KPI name'),
    'target': fields.Float(description='Target value'),
    'current': fields.Float(description='Current value'),
    'unit': fields.String(description='Measurement unit'),
    'period': fields.String(description='Time period'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

user_model = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The user unique identifier'),
    'email': fields.String(required=True, description='User email'),
    'role': fields.String(required=True, description='User role (Admin, Contributor, Viewer)'),
    'created_at': fields.DateTime(description='Account creation timestamp')
})

# API Resource documentation
@ns_projects.route('/')
class ProjectList(Resource):
    @api.doc('list_projects')
    @api.marshal_list_with(project_model)
    def get(self):
        """List all projects"""
        pass
        
    @api.doc('create_project')
    @api.expect(project_model)
    @api.marshal_with(project_model, code=201)
    def post(self):
        """Create a new project"""
        pass

@ns_projects.route('/<int:id>')
@api.param('id', 'The project identifier')
class Project(Resource):
    @api.doc('get_project')
    @api.marshal_with(project_model)
    def get(self, id):
        """Fetch a project given its identifier"""
        pass
        
    @api.doc('update_project')
    @api.expect(project_model)
    @api.marshal_with(project_model)
    def put(self, id):
        """Update a project given its identifier"""
        pass
        
    @api.doc('delete_project')
    @api.response(204, 'Project deleted')
    def delete(self, id):
        """Delete a project given its identifier"""
        pass

# Similar patterns for other resources...
@ns_ideas.route('/')
class IdeaList(Resource):
    @api.doc('list_ideas')
    @api.marshal_list_with(idea_model)
    def get(self):
        """List all ideas"""
        pass
        
    @api.doc('create_idea')
    @api.expect(idea_model)
    @api.marshal_with(idea_model, code=201)
    def post(self):
        """Create a new idea"""
        pass

@ns_ideas.route('/<int:id>')
@api.param('id', 'The idea identifier')
class Idea(Resource):
    @api.doc('get_idea')
    @api.marshal_with(idea_model)
    def get(self, id):
        """Fetch an idea given its identifier"""
        pass
