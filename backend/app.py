from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models import db
from models.user import User, NotificationSettings
from models.ticket import Ticket
from models.admin import AuditLog, SystemSettings, AdminNotification
from routes.auth import auth_bp
from routes.tickets import tickets_bp
from routes.admin import admin_bp
from routes.admin_enhanced import admin_enhanced_bp
from routes.profile import profile_bp
from routes.analytics import analytics_bp
import os

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })
    JWTManager(app)

    # Try PostgreSQL, fall back to SQLite if connection fails
    try:
        db.init_app(app)
        with app.app_context():
            db.engine.connect()
    except Exception as db_err:
        print(f"⚠ Primary DB failed ({db_err}), falling back to SQLite")
        if os.getenv('RENDER'):
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////opt/render/project/src/nexora.db'
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/nexora.db'
        db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(tickets_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(admin_enhanced_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')
    
    # Create tables and default admin
    with app.app_context():
        try:
            # Ensure database directory exists
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            
            db.create_all()
            print("✓ Database tables created")

            # Migration: make mobile column nullable if it isn't already
            try:
                import sqlite3
                raw_db_path = db_path if db_path else 'nexora.db'
                conn = sqlite3.connect(raw_db_path)
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(users)")
                cols = cursor.fetchall()
                mobile_col = next((c for c in cols if c[1] == 'mobile'), None)
                if mobile_col and mobile_col[3] == 1:  # notnull == 1
                    # Recreate users table without NOT NULL on mobile
                    cursor.executescript("""
                        PRAGMA foreign_keys=off;
                        BEGIN TRANSACTION;
                        ALTER TABLE users RENAME TO _users_old;
                        CREATE TABLE users (
                            id VARCHAR(36) PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            email VARCHAR(120) UNIQUE NOT NULL,
                            mobile VARCHAR(20),
                            company VARCHAR(100),
                            password_hash VARCHAR(255) NOT NULL,
                            role VARCHAR(20) DEFAULT 'user',
                            avatar_url VARCHAR(255),
                            phone VARCHAR(20),
                            department VARCHAR(100),
                            timezone VARCHAR(50) DEFAULT 'UTC',
                            is_active BOOLEAN DEFAULT 1,
                            created_at TIMESTAMP,
                            updated_at TIMESTAMP,
                            last_login TIMESTAMP
                        );
                        INSERT INTO users SELECT * FROM _users_old;
                        DROP TABLE _users_old;
                        COMMIT;
                        PRAGMA foreign_keys=on;
                    """)
                    conn.commit()
                    print("✓ Migrated users.mobile to nullable")
                conn.close()
            except Exception as migration_err:
                print(f"⚠ Migration note: {migration_err}")
            
            # Create uploads directory
            upload_dir = app.config.get('UPLOAD_FOLDER', 'uploads')
            os.makedirs(os.path.join(upload_dir, 'avatars'), exist_ok=True)
            print("✓ Upload directories created")
            
            # Create default admin if not exists
            admin = User.query.filter_by(email='admin@nexora.ai').first()
            if not admin:
                admin = User(
                    name='Admin',
                    email='admin@nexora.ai',
                    mobile='+1234567890',
                    role='admin'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.flush()  # Get admin ID
                
                # Create notification settings for admin
                admin_settings = NotificationSettings(user_id=admin.id)
                db.session.add(admin_settings)
                
                db.session.commit()
                print("✓ Default admin created: admin@nexora.ai / admin123")
            
            # Create default system settings if not exists
            settings = SystemSettings.query.first()
            if not settings:
                settings = SystemSettings()
                db.session.add(settings)
                db.session.commit()
                print("✓ Default system settings created")
        except Exception as e:
            print(f"⚠ Database initialization warning: {str(e)}")
            # Don't fail the app startup, just log the error
    
    # Serve uploaded files
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory('uploads', filename)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'NexoraAI API is running'}), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

# Create app instance for gunicorn
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    print("\n" + "="*60)
    print("NEXORAAI SUPPORT SUITE - BACKEND SERVER")
    print("="*60)
    print("Server running on: http://localhost:5000")
    print("API Base URL: http://localhost:5000/api")
    print("Default Admin: admin@nexora.ai / admin123")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
