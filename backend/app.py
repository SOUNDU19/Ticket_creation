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
    app = Flask(__name__)

    # Load config (DB URL already resolved in config.py)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # CORS — allow all origins (frontend on Vercel + local dev)
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })

    JWTManager(app)
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(tickets_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(admin_enhanced_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')

    # Initialize database
    with app.app_context():
        _init_database(app)

    # Static file serving
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory('uploads', filename)

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'NexoraAI API is running'}), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

    return app


def _init_database(app):
    """Create tables, run migrations, seed default data."""
    try:
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # Ensure SQLite directory exists (config.py already creates it, but double-check)
        if 'sqlite' in db_uri:
            raw = db_uri.replace('sqlite:///', '', 1).replace('sqlite:////', '/', 1)
            db_dir = os.path.dirname(raw)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)

        db.create_all()
        print("✓ Database tables created")

        # SQLite migration: ensure users.mobile is nullable
        if 'sqlite' in db_uri:
            _migrate_sqlite(db_uri)

        # Upload directories
        upload_dir = app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(os.path.join(upload_dir, 'avatars'), exist_ok=True)
        print("✓ Upload directories ready")

        # Seed default admin
        if not User.query.filter_by(email='admin@nexora.ai').first():
            admin = User(
                name='Admin',
                email='admin@nexora.ai',
                mobile='+1234567890',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.flush()
            db.session.add(NotificationSettings(user_id=admin.id))
            db.session.commit()
            print("✓ Default admin created: admin@nexora.ai / admin123")

        # Seed default system settings
        if not SystemSettings.query.first():
            db.session.add(SystemSettings())
            db.session.commit()
            print("✓ Default system settings created")

    except Exception as e:
        print(f"⚠ Database init warning: {e}")


def _migrate_sqlite(db_uri):
    """Make users.mobile nullable on existing SQLite databases."""
    try:
        import sqlite3
        raw = db_uri[len('sqlite:///'):]
        db_path = ('/' + raw.lstrip('/')) if raw.startswith('/') else raw
        if not db_path or not os.path.exists(db_path):
            return

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        cols = cursor.fetchall()
        mobile_col = next((c for c in cols if c[1] == 'mobile'), None)

        if mobile_col and mobile_col[3] == 1:  # notnull == 1 means NOT NULL
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
    except Exception as e:
        print(f"⚠ SQLite migration note: {e}")


# Gunicorn entry point
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    print("\n" + "=" * 60)
    print("NEXORAAI — Backend Server")
    print("=" * 60)
    print("URL:   http://localhost:5000")
    print("API:   http://localhost:5000/api")
    print("Admin: admin@nexora.ai / admin123")
    print("=" * 60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
