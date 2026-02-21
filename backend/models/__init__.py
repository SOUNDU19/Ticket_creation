from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models to register them
from .user import User, NotificationSettings
from .ticket import Ticket, InternalNote
from .admin import AuditLog, SystemSettings, AdminNotification
