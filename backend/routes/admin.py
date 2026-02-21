from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import get_jwt_identity
from models import db
from models.ticket import Ticket
from models.user import User
from models.admin import AuditLog, SystemSettings, AdminNotification
from utils.helpers import admin_required
from datetime import datetime, timedelta
from sqlalchemy import func
import csv
import io
import json

admin_bp = Blueprint('admin', __name__)

def log_admin_action(admin_id, action, target_type, target_id=None, details=None):
    """Helper function to log admin actions"""
    try:
        log = AuditLog(
            admin_id=admin_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=json.dumps(details) if details else None,
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Failed to log admin action: {e}")

@admin_bp.route('/admin/dashboard-stats', methods=['GET'])
@admin_required
def get_dashboard_stats():
    """Get comprehensive dashboard statistics"""
    try:
        # Basic counts
        total_tickets = Ticket.query.count()
        total_users = User.query.filter_by(role='user').count()
        open_tickets = Ticket.query.filter_by(status='open').count()
        in_progress_tickets = Ticket.query.filter_by(status='in_progress').count()
        resolved_tickets = Ticket.query.filter_by(status='resolved').count()
        closed_tickets = Ticket.query.filter_by(status='closed').count()
        high_priority = Ticket.query.filter_by(priority='high').count()
        
        # AI metrics
        tickets_with_ai = Ticket.query.filter(Ticket.ai_confidence > 0).all()
        avg_confidence = sum(t.ai_confidence for t in tickets_with_ai) / len(tickets_with_ai) if tickets_with_ai else 0
        low_confidence_count = len([t for t in tickets_with_ai if t.ai_confidence < 0.7])
        
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_tickets = Ticket.query.filter(Ticket.created_at >= week_ago).count()
        recent_users = User.query.filter(User.created_at >= week_ago, User.role == 'user').count()
        
        # Active users (logged in last 30 days)
        month_ago = datetime.utcnow() - timedelta(days=30)
        active_users = User.query.filter(
            User.last_login >= month_ago,
            User.role == 'user',
            User.is_active == True
        ).count()
        
        return jsonify({
            'stats': {
                'total_tickets': total_tickets,
                'total_users': total_users,
                'open_tickets': open_tickets,
                'in_progress_tickets': in_progress_tickets,
                'resolved_tickets': resolved_tickets,
                'closed_tickets': closed_tickets,
                'high_priority': high_priority,
                'avg_ai_confidence': round(avg_confidence * 100, 2),
                'low_confidence_count': low_confidence_count,
                'recent_tickets': recent_tickets,
                'recent_users': recent_users,
                'active_users': active_users
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch dashboard stats', 'message': str(e)}), 500

@admin_bp.route('/admin/tickets', methods=['GET'])
@admin_required
def get_all_tickets():
    """Get all tickets with advanced filtering"""
    try:
        # Get query parameters
        status = request.args.get('status')
        category = request.args.get('category')
        priority = request.args.get('priority')
        search = request.args.get('search')
        user_id = request.args.get('user_id')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Build query
        query = Ticket.query
        
        if status:
            query = query.filter_by(status=status)
        if category:
            query = query.filter_by(category=category)
        if priority:
            query = query.filter_by(priority=priority)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if search:
            query = query.filter(
                (Ticket.title.ilike(f'%{search}%')) | 
                (Ticket.description.ilike(f'%{search}%')) |
                (Ticket.id.ilike(f'%{search}%'))
            )
        if date_from:
            query = query.filter(Ticket.created_at >= datetime.fromisoformat(date_from))
        if date_to:
            query = query.filter(Ticket.created_at <= datetime.fromisoformat(date_to))
        
        # Order by created_at descending
        query = query.order_by(Ticket.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        tickets = [ticket.to_dict() for ticket in pagination.items]
        
        return jsonify({
            'tickets': tickets,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch tickets', 'message': str(e)}), 500

@admin_bp.route('/admin/tickets/<ticket_id>', methods=['PUT'])
@admin_required
def update_ticket(ticket_id):
    """Update ticket (admin)"""
    try:
        admin_id = get_jwt_identity()
        ticket = Ticket.query.get(ticket_id)
        
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        data = request.get_json()
        old_values = ticket.to_dict()
        
        # Update allowed fields
        if 'status' in data:
            ticket.status = data['status']
        if 'priority' in data:
            ticket.priority = data['priority']
        if 'category' in data:
            ticket.category = data['category']
        
        db.session.commit()
        
        # Log action
        log_admin_action(
            admin_id,
            'ticket_updated',
            'ticket',
            ticket_id,
            {'old': old_values, 'new': ticket.to_dict()}
        )
        
        return jsonify({
            'message': 'Ticket updated successfully',
            'ticket': ticket.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update ticket', 'message': str(e)}), 500

@admin_bp.route('/admin/tickets/<ticket_id>', methods=['DELETE'])
@admin_required
def delete_ticket(ticket_id):
    """Delete ticket (soft delete)"""
    try:
        admin_id = get_jwt_identity()
        ticket = Ticket.query.get(ticket_id)
        
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        ticket_data = ticket.to_dict()
        
        # Soft delete - just mark as deleted or actually delete
        db.session.delete(ticket)
        db.session.commit()
        
        # Log action
        log_admin_action(
            admin_id,
            'ticket_deleted',
            'ticket',
            ticket_id,
            ticket_data
        )
        
        return jsonify({'message': 'Ticket deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete ticket', 'message': str(e)}), 500

@admin_bp.route('/admin/tickets/bulk-update', methods=['POST'])
@admin_required
def bulk_update_tickets():
    """Bulk update tickets"""
    try:
        admin_id = get_jwt_identity()
        data = request.get_json()
        
        ticket_ids = data.get('ticket_ids', [])
        updates = data.get('updates', {})
        
        if not ticket_ids or not updates:
            return jsonify({'error': 'Missing ticket_ids or updates'}), 400
        
        updated_count = 0
        for ticket_id in ticket_ids:
            ticket = Ticket.query.get(ticket_id)
            if ticket:
                if 'status' in updates:
                    ticket.status = updates['status']
                if 'priority' in updates:
                    ticket.priority = updates['priority']
                updated_count += 1
        
        db.session.commit()
        
        # Log action
        log_admin_action(
            admin_id,
            'tickets_bulk_updated',
            'ticket',
            None,
            {'count': updated_count, 'updates': updates}
        )
        
        return jsonify({
            'message': f'{updated_count} tickets updated successfully',
            'count': updated_count
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to bulk update tickets', 'message': str(e)}), 500

@admin_bp.route('/admin/analytics', methods=['GET'])
@admin_required
def get_admin_analytics():
    """Get comprehensive analytics"""
    try:
        # Get all tickets
        tickets = Ticket.query.all()
        
        # Category distribution
        categories = {}
        for ticket in tickets:
            categories[ticket.category] = categories.get(ticket.category, 0) + 1
        
        # Priority distribution
        priorities = {
            'high': len([t for t in tickets if t.priority == 'high']),
            'medium': len([t for t in tickets if t.priority == 'medium']),
            'low': len([t for t in tickets if t.priority == 'low'])
        }
        
        # Status distribution
        statuses = {
            'open': len([t for t in tickets if t.status == 'open']),
            'in_progress': len([t for t in tickets if t.status == 'in_progress']),
            'resolved': len([t for t in tickets if t.status == 'resolved']),
            'closed': len([t for t in tickets if t.status == 'closed'])
        }
        
        # Tickets over time (last 30 days)
        tickets_timeline = []
        for i in range(30, -1, -1):
            date = datetime.utcnow() - timedelta(days=i)
            count = Ticket.query.filter(
                func.date(Ticket.created_at) == date.date()
            ).count()
            tickets_timeline.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })
        
        return jsonify({
            'categories': categories,
            'priorities': priorities,
            'statuses': statuses,
            'tickets_timeline': tickets_timeline
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch analytics', 'message': str(e)}), 500

@admin_bp.route('/admin/model-metrics', methods=['GET'])
@admin_required
def get_model_metrics():
    """Get AI model performance metrics"""
    try:
        tickets = Ticket.query.filter(Ticket.ai_confidence > 0).all()
        
        if not tickets:
            return jsonify({
                'avg_confidence': 0,
                'total_predictions': 0,
                'low_confidence_count': 0,
                'category_distribution': {},
                'confidence_distribution': {}
            }), 200
        
        # Calculate metrics
        avg_confidence = sum(t.ai_confidence for t in tickets) / len(tickets)
        low_confidence = [t for t in tickets if t.ai_confidence < 0.7]
        
        # Category distribution
        category_dist = {}
        for ticket in tickets:
            category_dist[ticket.category] = category_dist.get(ticket.category, 0) + 1
        
        # Confidence distribution
        confidence_ranges = {
            '0-50%': 0,
            '50-70%': 0,
            '70-85%': 0,
            '85-100%': 0
        }
        
        for ticket in tickets:
            conf = ticket.ai_confidence * 100
            if conf < 50:
                confidence_ranges['0-50%'] += 1
            elif conf < 70:
                confidence_ranges['50-70%'] += 1
            elif conf < 85:
                confidence_ranges['70-85%'] += 1
            else:
                confidence_ranges['85-100%'] += 1
        
        return jsonify({
            'avg_confidence': round(avg_confidence * 100, 2),
            'total_predictions': len(tickets),
            'low_confidence_count': len(low_confidence),
            'category_distribution': category_dist,
            'confidence_distribution': confidence_ranges
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch model metrics', 'message': str(e)}), 500

@admin_bp.route('/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users with pagination and search"""
    try:
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        query = User.query.filter_by(role='user')
        
        if search:
            query = query.filter(
                (User.name.ilike(f'%{search}%')) |
                (User.email.ilike(f'%{search}%'))
            )
        
        query = query.order_by(User.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        users_data = []
        for user in pagination.items:
            user_dict = user.to_dict()
            user_dict['ticket_count'] = Ticket.query.filter_by(user_id=user.id).count()
            user_dict['open_tickets'] = Ticket.query.filter_by(user_id=user.id, status='open').count()
            users_data.append(user_dict)
        
        return jsonify({
            'users': users_data,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users', 'message': str(e)}), 500

@admin_bp.route('/admin/users/<user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """Update user (admin)"""
    try:
        admin_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        old_values = user.to_dict()
        
        # Update allowed fields
        if 'is_active' in data:
            user.is_active = bool(data['is_active'])
        if 'role' in data and data['role'] in ['user', 'admin']:
            user.role = data['role']
        
        db.session.commit()
        
        # Log action
        action = 'user_deactivated' if not user.is_active else 'user_updated'
        log_admin_action(
            admin_id,
            action,
            'user',
            user_id,
            {'old': old_values, 'new': user.to_dict()}
        )
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user', 'message': str(e)}), 500

@admin_bp.route('/admin/audit-logs', methods=['GET'])
@admin_required
def get_audit_logs():
    """Get audit logs with filtering"""
    try:
        action = request.args.get('action')
        target_type = request.args.get('target_type')
        admin_id = request.args.get('admin_id')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        query = AuditLog.query
        
        if action:
            query = query.filter_by(action=action)
        if target_type:
            query = query.filter_by(target_type=target_type)
        if admin_id:
            query = query.filter_by(admin_id=admin_id)
        
        query = query.order_by(AuditLog.timestamp.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        logs = [log.to_dict() for log in pagination.items]
        
        return jsonify({
            'logs': logs,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch audit logs', 'message': str(e)}), 500

@admin_bp.route('/admin/settings', methods=['GET'])
@admin_required
def get_settings():
    """Get system settings"""
    try:
        settings = SystemSettings.query.first()
        
        if not settings:
            # Create default settings
            settings = SystemSettings()
            db.session.add(settings)
            db.session.commit()
        
        return jsonify({'settings': settings.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch settings', 'message': str(e)}), 500

@admin_bp.route('/admin/settings', methods=['PUT'])
@admin_required
def update_settings():
    """Update system settings"""
    try:
        admin_id = get_jwt_identity()
        settings = SystemSettings.query.first()
        
        if not settings:
            settings = SystemSettings()
            db.session.add(settings)
        
        data = request.get_json()
        old_values = settings.to_dict()
        
        # Update settings
        for key, value in data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        
        settings.updated_by = admin_id
        db.session.commit()
        
        # Log action
        log_admin_action(
            admin_id,
            'settings_updated',
            'system',
            None,
            {'old': old_values, 'new': settings.to_dict()}
        )
        
        return jsonify({
            'message': 'Settings updated successfully',
            'settings': settings.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update settings', 'message': str(e)}), 500

@admin_bp.route('/admin/export/<export_type>', methods=['GET'])
@admin_required
def export_data(export_type):
    """Export data as CSV"""
    try:
        admin_id = get_jwt_identity()
        
        if export_type == 'tickets':
            tickets = Ticket.query.all()
            
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['ID', 'User Email', 'Title', 'Category', 'Priority', 'Status', 'AI Confidence', 'Created At'])
            
            for ticket in tickets:
                writer.writerow([
                    ticket.id,
                    ticket.user.email if ticket.user else 'Unknown',
                    ticket.title,
                    ticket.category,
                    ticket.priority,
                    ticket.status,
                    ticket.ai_confidence,
                    ticket.created_at.isoformat()
                ])
            
            output.seek(0)
            
            # Log action
            log_admin_action(admin_id, 'data_exported', 'system', None, {'type': 'tickets'})
            
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'tickets_export_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
            )
        
        elif export_type == 'users':
            users = User.query.filter_by(role='user').all()
            
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['ID', 'Name', 'Email', 'Company', 'Status', 'Tickets', 'Created At'])
            
            for user in users:
                writer.writerow([
                    user.id,
                    user.name,
                    user.email,
                    user.company or '',
                    'Active' if user.is_active else 'Inactive',
                    len(user.tickets),
                    user.created_at.isoformat()
                ])
            
            output.seek(0)
            
            # Log action
            log_admin_action(admin_id, 'data_exported', 'system', None, {'type': 'users'})
            
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'users_export_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
            )
        
        elif export_type == 'audit-logs':
            logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(1000).all()
            
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['ID', 'Admin', 'Action', 'Target Type', 'Target ID', 'Timestamp'])
            
            for log in logs:
                writer.writerow([
                    log.id,
                    log.admin.email if log.admin else 'Unknown',
                    log.action,
                    log.target_type,
                    log.target_id or '',
                    log.timestamp.isoformat()
                ])
            
            output.seek(0)
            
            # Log action
            log_admin_action(admin_id, 'data_exported', 'system', None, {'type': 'audit-logs'})
            
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'audit_logs_export_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
            )
        
        else:
            return jsonify({'error': 'Invalid export type'}), 400
    
    except Exception as e:
        return jsonify({'error': 'Failed to export data', 'message': str(e)}), 500

@admin_bp.route('/admin/notifications', methods=['GET'])
@admin_required
def get_notifications():
    """Get admin notifications"""
    try:
        admin_id = get_jwt_identity()
        
        notifications = AdminNotification.query.filter_by(admin_id=admin_id).order_by(
            AdminNotification.created_at.desc()
        ).limit(50).all()
        
        unread_count = AdminNotification.query.filter_by(admin_id=admin_id, is_read=False).count()
        
        return jsonify({
            'notifications': [n.to_dict() for n in notifications],
            'unread_count': unread_count
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch notifications', 'message': str(e)}), 500

@admin_bp.route('/admin/notifications/<notification_id>/read', methods=['PUT'])
@admin_required
def mark_notification_read(notification_id):
    """Mark notification as read"""
    try:
        notification = AdminNotification.query.get(notification_id)
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        notification.is_read = True
        db.session.commit()
        
        return jsonify({'message': 'Notification marked as read'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update notification', 'message': str(e)}), 500

