import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import Config
from models.user import db as user_db, User
# Remove the duplicate db import from task model
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.analytics import analytics_bp

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    user_db.init_app(app)
    # Remove the duplicate initialization
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    
    # Create tables
    with app.app_context():
        user_db.create_all()
        # Remove the duplicate creation
        
        # Create default admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', role='admin')
            admin.set_password('admin123')
            user_db.session.add(admin)
            user_db.session.commit()
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Task Management API is running'}), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'Welcome to the Task Management API',
            'endpoints': {
                'auth': '/api/auth',
                'tasks': '/api/tasks',
                'analytics': '/api/analytics',
                'health': '/health'
            }
        }), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('DEBUG', 'True').lower() == 'true'
    )