from flask_restful import Resource, reqparse
from flask import jsonify
from models.idea import Idea
from app import db

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='Title is required')
parser.add_argument('description', type=str)
parser.add_argument('status', type=str)
parser.add_argument('priority', type=int)

class IdeasAPI(Resource):
    def get(self, id=None):
        """Get a specific idea or all ideas"""
        if id:
            idea = Idea.query.get_or_404(id)
            return jsonify(idea.serialize())
        all_ideas = Idea.query.all()
        return jsonify([i.serialize() for i in all_ideas])

    def post(self):
        """Create a new idea"""
        args = parser.parse_args()
        idea = Idea(
            title=args['title'],
            description=args.get('description'),
            status=args.get('status', 'new'),
            priority=args.get('priority', 0)
        )
        db.session.add(idea)
        db.session.commit()
        return jsonify(idea.serialize()), 201

    def put(self, id):
        """Update an existing idea"""
        idea = Idea.query.get_or_404(id)
        args = parser.parse_args()
        
        idea.title = args['title']
        idea.description = args.get('description', idea.description)
        idea.status = args.get('status', idea.status)
        idea.priority = args.get('priority', idea.priority)
        
        db.session.commit()
        return jsonify(idea.serialize())

    def delete(self, id):
        """Delete an idea"""
        idea = Idea.query.get_or_404(id)
        db.session.delete(idea)
        db.session.commit()
        return '', 204
