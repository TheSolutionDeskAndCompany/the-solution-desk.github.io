import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils.sentry import init_sentry
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_restful import Api
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
admin = Admin(name='Solution Desk Admin', template_mode='bootstrap3')
api = Api()

def create_app(config_name=None):
    # Initialize Flask app
    app = Flask(__name__, static_folder='static', static_url_path='')
    
    # Default to FLASK_ENV or 'development' if not specified
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Configure logging
    handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=100000, backupCount=5)
    handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s in %(module)s: %(message)s'
    ))
    app.logger.addHandler(handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    app.logger.info('Application startup')
    
    # Load instance config (overrides default config)
    app.config.from_pyfile('config.py', silent=True)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Setup login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Create upload folder if it doesn't exist
    os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)
    
    # Register blueprints with URL prefixes
    from routes.main import main as main_bp
    from routes.auth import auth_bp
    from routes.api_auth import api_auth_bp
    from routes.projects import projects_bp
    from routes.tools import tools_bp
    from errors import errors as errors_bp
    from routes.api.docs import api_docs_bp
    from routes.health import health_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_auth_bp)  # JWT API auth routes
    app.register_blueprint(projects_bp, url_prefix='/projects')
    app.register_blueprint(tools_bp, url_prefix='/tools')
    app.register_blueprint(errors_bp)
    app.register_blueprint(api_docs_bp, url_prefix='/api')
    app.register_blueprint(health_bp)
    
    # Initialize Marshmallow
    from schemas import init_ma
    init_ma(app)
    
    # Initialize Sentry for production error monitoring
    init_sentry(app)
    
    # Initialize Flask-RESTful API
    api.init_app(app)
    
    # Register API resources
    from routes.api.projects import ProjectsAPI
    from routes.api.ideas import IdeasAPI
    from routes.api.sops import SopsAPI
    from routes.api.users import UsersAPI
    from routes.api.kpis import KpisAPI
    
    api.add_resource(ProjectsAPI, '/api/projects', '/api/projects/<int:id>')
    api.add_resource(IdeasAPI, '/api/ideas', '/api/ideas/<int:id>')
    api.add_resource(SopsAPI, '/api/sops', '/api/sops/<int:id>')
    api.add_resource(UsersAPI, '/api/users', '/api/users/<int:id>')
    api.add_resource(KpisAPI, '/api/kpis', '/api/kpis/<int:id>')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(int(user_id))

# Initialize Flask-Admin
def init_admin(app):
    from flask_admin.contrib.sqla import ModelView
    from models.project import Project
    from models.user import User
    from models.idea import Idea
    from models.sop import SOP
    from models.kpi import KPI
    from flask_login import current_user
    from flask import redirect, url_for
    
    class SecureModelView(ModelView):
        def is_accessible(self):
            return current_user.is_authenticated and current_user.role == 'Admin'
        
        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('auth.login'))
    
    admin.init_app(app)
    admin.add_view(SecureModelView(User, db.session))
    admin.add_view(SecureModelView(Project, db.session))
    admin.add_view(SecureModelView(Idea, db.session))
    admin.add_view(SecureModelView(SOP, db.session))
    admin.add_view(SecureModelView(KPI, db.session))

# Create app instance using environment variable or default to development
app = create_app(os.getenv('FLASK_ENV') or 'development')

# Register CLI commands
from commands import register_commands
register_commands(app)

# Initialize admin after app is created
with app.app_context():
    init_admin(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
