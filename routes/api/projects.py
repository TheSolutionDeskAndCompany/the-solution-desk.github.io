from flask_restful import Resource, reqparse
from flask import jsonify
from models.project import Project
from app import db

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='Title is required')
parser.add_argument('slug', type=str, required=True, help='Slug is required')
parser.add_argument('description', type=str)
parser.add_argument('long_description', type=str)
parser.add_argument('image_url', type=str)
parser.add_argument('demo_url', type=str)
parser.add_argument('github_url', type=str)
parser.add_argument('download_url', type=str)
parser.add_argument('is_featured', type=bool)

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
        args = parser.parse_args()
        proj = Project(
            title=args['title'],
            slug=args['slug'],
            description=args.get('description'),
            long_description=args.get('long_description'),
            image_url=args.get('image_url'),
            demo_url=args.get('demo_url'),
            github_url=args.get('github_url'),
            download_url=args.get('download_url'),
            is_featured=args.get('is_featured', False)
        )
        db.session.add(proj)
        db.session.commit()
        return jsonify(proj.serialize()), 201

    def put(self, id):
        """Update an existing project"""
        proj = Project.query.get_or_404(id)
        args = parser.parse_args()
        
        proj.title = args['title']
        proj.slug = args['slug']
        proj.description = args.get('description', proj.description)
        proj.long_description = args.get('long_description', proj.long_description)
        proj.image_url = args.get('image_url', proj.image_url)
        proj.demo_url = args.get('demo_url', proj.demo_url)
        proj.github_url = args.get('github_url', proj.github_url)
        proj.download_url = args.get('download_url', proj.download_url)
        proj.is_featured = args.get('is_featured', proj.is_featured)
        
        db.session.commit()
        return jsonify(proj.serialize())

    def delete(self, id):
        """Delete a project"""
        proj = Project.query.get_or_404(id)
        db.session.delete(proj)
        db.session.commit()
        return '', 204
