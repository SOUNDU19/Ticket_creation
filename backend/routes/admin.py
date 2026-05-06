from flask import Blueprint, jsonify, request
from utils.helpers import admin_required
from flask_jwt_extended import get_jwt_identity
from models import db
from models.user import User
from models.ticket import Ticket
from models.admin import AuditLog, SystemSettings, AdminNotification

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/dashboard-stats', methods=['GET'])
@admin_required
def dashboard_stats():
    try:
        total_tickets = Ticket.query.count()
        open_tickets = Ticket.query.filter_by(status='open').count()
        in_progress = Ticket.query.filter_by(status='in_progress').count()
        resolved = Ticket.query.filter_by(status='resolved').count()
        total_users = User.query.filter_by(role='user').count()

        return jsonify({
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'in_progress': in_progress,
            'resolved': resolved,
            'total_users': total_users
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/admin/tickets', methods=['GET'])
@admin_required
def get_all_tickets():
    try:
        status = request.args.get('status')
        priority = request.args.get('priority')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        query = Ticket.query
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        if search:
            query = query.filter(
                Ticket.title.ilike(f'%{search}%') |
                Ticket.description.ilike(f'%{search}%')
            )

        query = query.order_by(Ticket.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'tickets': [t.to_dict() for t in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/admin/tickets/<ticket_id>', methods=['GET', 'PUT'])
@admin_required
def manage_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404

    if request.method == 'GET':
        return jsonify({'ticket': ticket.to_dict()}), 200

    data = request.get_json()
    if 'status' in data:
        ticket.status = data['status']
    if 'priority' in data:
        ticket.priority = data['priority']
    if 'category' in data:
        ticket.category = data['category']
    db.session.commit()
    return jsonify({'ticket': ticket.to_dict()}), 200


@admin_bp.route('/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    try:
        users = User.query.all()
        result = []
        for u in users:
            d = u.to_dict()
            d['ticket_count'] = Ticket.query.filter_by(user_id=u.id).count()
            result.append(d)
        return jsonify({'users': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/admin/analytics', methods=['GET'])
@admin_required
def get_analytics():
    try:
        tickets = Ticket.query.all()
        categories = {}
        priorities = {}
        statuses = {}
        for t in tickets:
            categories[t.category] = categories.get(t.category, 0) + 1
            priorities[t.priority] = priorities.get(t.priority, 0) + 1
            statuses[t.status] = statuses.get(t.status, 0) + 1

        return jsonify({
            'total': len(tickets),
            'categories': categories,
            'priorities': priorities,
            'statuses': statuses
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/admin/tickets/bulk-update', methods=['PUT'])
@admin_required
def bulk_update():
    try:
        data = request.get_json()
        ticket_ids = data.get('ticket_ids', [])
        updates = data.get('updates', {})
        for tid in ticket_ids:
            ticket = Ticket.query.get(tid)
            if ticket:
                for k, v in updates.items():
                    setattr(ticket, k, v)
        db.session.commit()
        return jsonify({'message': f'Updated {len(ticket_ids)} tickets'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/admin/model-metrics', methods=['GET'])
@admin_required
def model_metrics():
    return jsonify({'accuracy': 0.92, 'precision': 0.91, 'recall': 0.90, 'f1': 0.91}), 200


@admin_bp.route('/admin/audit-logs', methods=['GET'])
@admin_required
def audit_logs():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return jsonify({'logs': [l.to_dict() for l in logs]}), 200


@admin_bp.route('/admin/settings', methods=['GET', 'PUT'])
@admin_required
def settings():
    s = SystemSettings.query.first()
    if not s:
        s = SystemSettings()
        db.session.add(s)
        db.session.commit()

    if request.method == 'GET':
        return jsonify(s.to_dict()), 200

    data = request.get_json()
    field_map = {
        'sla_critical': 'sla_critical_hours',
        'sla_high': 'sla_high_hours',
        'sla_medium': 'sla_medium_hours',
        'sla_low': 'sla_low_hours',
        'ai_confidence_threshold': 'ai_confidence_threshold',
        'duplicate_detection_enabled': 'duplicate_detection_enabled'
    }
    for k, v in data.items():
        attr = field_map.get(k, k)
        if hasattr(s, attr):
            setattr(s, attr, v)
    db.session.commit()
    return jsonify(s.to_dict()), 200


@admin_bp.route('/admin/export/<export_type>', methods=['GET'])
@admin_required
def export_data(export_type):
    return jsonify({'message': f'Export {export_type} not implemented yet'}), 200


@admin_bp.route('/admin/notifications', methods=['GET'])
@admin_required
def get_notifications():
    notifs = AdminNotification.query.order_by(AdminNotification.created_at.desc()).limit(50).all()
    return jsonify({'notifications': [n.to_dict() for n in notifs]}), 200


@admin_bp.route('/admin/notifications/<notif_id>/read', methods=['PUT'])
@admin_required
def mark_read(notif_id):
    n = AdminNotification.query.get(notif_id)
    if n:
        n.is_read = True
        db.session.commit()
    return jsonify({'message': 'Marked as read'}), 200


@admin_bp.route('/admin/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def manage_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if request.method == 'GET':
        return jsonify({'user': user.to_dict()}), 200

    if request.method == 'PUT':
        data = request.get_json()
        for k in ['name', 'role', 'is_active']:
            if k in data:
                setattr(user, k, data[k])
        db.session.commit()
        return jsonify({'user': user.to_dict()}), 200

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
