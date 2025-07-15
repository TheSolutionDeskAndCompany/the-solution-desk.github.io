"""
Health check endpoint for monitoring application status
Used by integration tests and monitoring systems
"""

from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint
    Returns 200 OK when application is running
    """
    return jsonify({
        'status': 'ok',
        'message': 'Application is running'
    }), 200
