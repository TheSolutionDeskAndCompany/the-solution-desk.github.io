"""
Schema initialization and common utilities
"""
from flask_marshmallow import Marshmallow

ma = Marshmallow()

def init_ma(app):
    """Initialize Marshmallow with the Flask app"""
    ma.init_app(app)
