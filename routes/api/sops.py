from flask_restful import Resource, reqparse
from flask import jsonify
from models.sop import SOP
from app import db

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='Title is required')
parser.add_argument('description', type=str)
parser.add_argument('content', type=str)
parser.add_argument('version', type=str)
parser.add_argument('category', type=str)

class SopsAPI(Resource):
    def get(self, id=None):
        """Get a specific SOP or all SOPs"""
        if id:
            sop = SOP.query.get_or_404(id)
            return jsonify(sop.serialize())
        all_sops = SOP.query.all()
        return jsonify([s.serialize() for s in all_sops])

    def post(self):
        """Create a new SOP"""
        args = parser.parse_args()
        sop = SOP(
            title=args['title'],
            description=args.get('description'),
            content=args.get('content'),
            version=args.get('version', '1.0'),
            category=args.get('category')
        )
        db.session.add(sop)
        db.session.commit()
        return jsonify(sop.serialize()), 201

    def put(self, id):
        """Update an existing SOP"""
        sop = SOP.query.get_or_404(id)
        args = parser.parse_args()
        
        sop.title = args['title']
        sop.description = args.get('description', sop.description)
        sop.content = args.get('content', sop.content)
        sop.version = args.get('version', sop.version)
        sop.category = args.get('category', sop.category)
        
        db.session.commit()
        return jsonify(sop.serialize())

    def delete(self, id):
        """Delete a SOP"""
        sop = SOP.query.get_or_404(id)
        db.session.delete(sop)
        db.session.commit()
        return '', 204
