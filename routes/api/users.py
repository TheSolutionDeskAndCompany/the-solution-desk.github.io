from flask_restful import Resource, reqparse
from flask import jsonify, abort
from flask_login import current_user
from models.user import User
from app import db

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True, help='Email is required')
parser.add_argument('password', type=str)
parser.add_argument('is_admin', type=bool)

class UsersAPI(Resource):
    def get(self, id=None):
        """Get a specific user or all users"""
        # Check if requester is admin
        if not current_user.is_authenticated or not current_user.is_admin:
            return {'message': 'Unauthorized access'}, 403
            
        if id:
            user = User.query.get_or_404(id)
            return jsonify(user.serialize())
            
        all_users = User.query.all()
        return jsonify([u.serialize() for u in all_users])

    def post(self):
        """Create a new user"""
        # Only admins can create users via API
        if not current_user.is_authenticated or not current_user.is_admin:
            return {'message': 'Unauthorized access'}, 403
            
        args = parser.parse_args()
        
        # Check if user already exists
        if User.get_by_email(args['email']):
            return {'message': 'User already exists'}, 409
            
        user = User(
            email=args['email'],
            is_admin=args.get('is_admin', False)
        )
        
        if args.get('password'):
            user.set_password(args['password'])
        else:
            return {'message': 'Password is required'}, 400
            
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 201

    def put(self, id):
        """Update an existing user"""
        # Only admins can update users via API
        if not current_user.is_authenticated or not current_user.is_admin:
            return {'message': 'Unauthorized access'}, 403
            
        user = User.query.get_or_404(id)
        args = parser.parse_args()
        
        # Update email if changed and not already taken
        if args['email'] != user.email:
            existing_user = User.get_by_email(args['email'])
            if existing_user and existing_user.id != id:
                return {'message': 'Email already in use'}, 409
            user.email = args['email']
            
        # Update password if provided
        if args.get('password'):
            user.set_password(args['password'])
            
        # Update admin status if provided
        if 'is_admin' in args:
            user.is_admin = args.get('is_admin')
            
        db.session.commit()
        return jsonify(user.serialize())

    def delete(self, id):
        """Delete a user"""
        # Only admins can delete users via API
        if not current_user.is_authenticated or not current_user.is_admin:
            return {'message': 'Unauthorized access'}, 403
            
        user = User.query.get_or_404(id)
        
        # Prevent deletion of the currently logged-in user
        if current_user.id == user.id:
            return {'message': 'Cannot delete yourself'}, 400
            
        db.session.delete(user)
        db.session.commit()
        return '', 204
