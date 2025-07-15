from flask import Blueprint, render_template, jsonify, request
from app import db

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not Found'}), 404
    return render_template('404.html'), 404

@errors.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal Server Error'}), 500
    return render_template('500.html'), 500

@errors.app_errorhandler(403)
def forbidden(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Forbidden'}), 403
    return render_template('403.html'), 403

@errors.app_errorhandler(400)
def bad_request(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Bad Request'}), 400
    return render_template('400.html'), 400
