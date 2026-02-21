from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models import db
from models.user import User, NotificationSettings
from utils.helpers import token_required, validate_password
from werkzeug.utils import secure_filename
import os
import re

profile_bp = Blueprint('profile', __name__)

# Allowed avatar extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get user profile with notification settings"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Ensure notification settings exist
        if not user.notification_settings:
            settings = NotificationSettings(user_id=user.id)
            db.session.add(settings)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error creating notification settings: {e}")
        
        # Refresh user to get the relationship
        db.session.refresh(user)
        
        return jsonify({
            'profile': user.to_profile_dict()
        }), 200
    
    except Exception as e:
        print(f"Profile fetch error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to fetch profile', 'message': str(e)}), 500

@profile_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile information"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            user.name = data['name'].strip()
        
        if 'phone' in data:
            user.phone = data['phone'].strip() if data['phone'] else None
        
        if 'mobile' in data:
            user.mobile = data['mobile'].strip()
        
        if 'department' in data:
            user.department = data['department'].strip() if data['department'] else None
        
        if 'timezone' in data:
            user.timezone = data['timezone'].strip()
        
        if 'company' in data:
            user.company = data['company'].strip() if data['company'] else None
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': user.to_profile_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile', 'message': str(e)}), 500

@profile_bp.route('/profile/avatar', methods=['POST'])
@token_required
def upload_avatar():
    """Upload user avatar"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if file is present
        if 'avatar' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['avatar']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif'}), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large. Maximum size: 5MB'}), 400
        
        # Create uploads directory if it doesn't exist
        upload_folder = os.path.join('uploads', 'avatars')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Generate secure filename
        filename = secure_filename(f"{user_id}_{file.filename}")
        filepath = os.path.join(upload_folder, filename)
        
        # Save file
        file.save(filepath)
        
        # Update user avatar URL
        user.avatar_url = f"/uploads/avatars/{filename}"
        db.session.commit()
        
        return jsonify({
            'message': 'Avatar uploaded successfully',
            'avatar_url': user.avatar_url
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to upload avatar', 'message': str(e)}), 500

@profile_bp.route('/profile/password', methods=['PUT'])
@token_required
def change_password():
    """Change user password"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not all([current_password, new_password]):
            return jsonify({'error': 'Current password and new password are required'}), 400
        
        # Verify current password
        if not user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Validate new password strength
        if not validate_password(new_password):
            return jsonify({'error': 'New password must be at least 6 characters long'}), 400
        
        # Check if new password is different from current
        if current_password == new_password:
            return jsonify({'error': 'New password must be different from current password'}), 400
        
        # Additional password strength validation
        if len(new_password) < 8:
            return jsonify({'error': 'Password should be at least 8 characters for better security'}), 400
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to change password', 'message': str(e)}), 500

@profile_bp.route('/profile/notifications', methods=['PUT'])
@token_required
def update_notifications():
    """Update notification preferences"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get or create notification settings
        settings = user.notification_settings
        if not settings:
            settings = NotificationSettings(user_id=user.id)
            db.session.add(settings)
        
        data = request.get_json()
        
        # Update notification preferences
        if 'email_notifications' in data:
            settings.email_notifications = bool(data['email_notifications'])
        
        if 'ticket_status_updates' in data:
            settings.ticket_status_updates = bool(data['ticket_status_updates'])
        
        if 'critical_alerts' in data:
            settings.critical_alerts = bool(data['critical_alerts'])
        
        if 'weekly_summary' in data:
            settings.weekly_summary = bool(data['weekly_summary'])
        
        if 'ai_insight_updates' in data:
            settings.ai_insight_updates = bool(data['ai_insight_updates'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Notification preferences updated successfully',
            'notification_settings': settings.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update notifications', 'message': str(e)}), 500

@profile_bp.route('/profile/deactivate', methods=['POST'])
@token_required
def deactivate_account():
    """Deactivate user account"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Prevent admin from deactivating their own account
        if user.role == 'admin':
            return jsonify({'error': 'Admin accounts cannot be deactivated'}), 403
        
        user.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Account deactivated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to deactivate account', 'message': str(e)}), 500

@profile_bp.route('/profile', methods=['DELETE'])
@token_required
def delete_account():
    """Delete user account (soft delete by deactivating)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Prevent admin from deleting their own account
        if user.role == 'admin':
            return jsonify({'error': 'Admin accounts cannot be deleted'}), 403
        
        data = request.get_json()
        password = data.get('password')
        
        if not password:
            return jsonify({'error': 'Password confirmation required'}), 400
        
        # Verify password
        if not user.check_password(password):
            return jsonify({'error': 'Incorrect password'}), 401
        
        # Soft delete - deactivate account
        user.is_active = False
        db.session.commit()
        
        # For hard delete, uncomment:
        # db.session.delete(user)
        # db.session.commit()
        
        return jsonify({'message': 'Account deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete account', 'message': str(e)}), 500

@profile_bp.route('/profile/stats', methods=['GET'])
@token_required
def get_profile_stats():
    """Get user activity statistics"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get ticket statistics
        from models.ticket import Ticket
        
        total_tickets = Ticket.query.filter_by(user_id=user.id).count()
        open_tickets = Ticket.query.filter_by(user_id=user.id, status='open').count()
        closed_tickets = Ticket.query.filter_by(user_id=user.id, status='closed').count()
        high_priority = Ticket.query.filter_by(user_id=user.id, priority='high').count()
        
        return jsonify({
            'stats': {
                'total_tickets': total_tickets,
                'open_tickets': open_tickets,
                'closed_tickets': closed_tickets,
                'high_priority': high_priority
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch stats', 'message': str(e)}), 500
