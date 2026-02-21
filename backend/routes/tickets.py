from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models import db
from models.ticket import Ticket
from models.user import User
from utils.helpers import token_required
from ml.predict import predict_ticket
from datetime import datetime

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/predict', methods=['POST'])
@token_required
def predict():
    """AI prediction for ticket"""
    try:
        data = request.get_json()
        
        if not data.get('description'):
            return jsonify({'error': 'Description is required'}), 400
        
        description = data['description']
        
        # Get AI prediction
        prediction = predict_ticket(description)
        
        return jsonify(prediction), 200
    
    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'message': str(e)}), 500

@tickets_bp.route('/create-ticket', methods=['POST'])
@token_required
def create_ticket():
    """Create new ticket"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'category', 'priority']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create ticket
        ticket = Ticket(
            user_id=user_id,
            title=data['title'].strip(),
            description=data['description'].strip(),
            category=data['category'],
            priority=data['priority'],
            ai_confidence=data.get('confidence', 0.0),
            status='open'
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        return jsonify({
            'message': 'Ticket created successfully',
            'ticket': ticket.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Ticket creation failed', 'message': str(e)}), 500

@tickets_bp.route('/tickets', methods=['GET'])
@token_required
def get_tickets():
    """Get user tickets"""
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        status = request.args.get('status')
        category = request.args.get('category')
        priority = request.args.get('priority')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Build query
        query = Ticket.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        if category:
            query = query.filter_by(category=category)
        if priority:
            query = query.filter_by(priority=priority)
        if search:
            query = query.filter(
                (Ticket.title.ilike(f'%{search}%')) | 
                (Ticket.description.ilike(f'%{search}%'))
            )
        
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

@tickets_bp.route('/ticket/<ticket_id>', methods=['GET'])
@token_required
def get_ticket(ticket_id):
    """Get ticket details"""
    try:
        user_id = get_jwt_identity()
        ticket = Ticket.query.get(ticket_id)
        
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        # Check ownership
        if ticket.user_id != user_id:
            user = User.query.get(user_id)
            if not user or user.role != 'admin':
                return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({'ticket': ticket.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch ticket', 'message': str(e)}), 500

@tickets_bp.route('/update-ticket', methods=['PUT'])
@token_required
def update_ticket():
    """Update ticket status"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        ticket_id = data.get('ticket_id')
        if not ticket_id:
            return jsonify({'error': 'Ticket ID is required'}), 400
        
        ticket = Ticket.query.get(ticket_id)
        
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        # Check ownership or admin
        user = User.query.get(user_id)
        if ticket.user_id != user_id and (not user or user.role != 'admin'):
            return jsonify({'error': 'Access denied'}), 403
        
        # Update status
        if 'status' in data:
            ticket.status = data['status']
            ticket.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Ticket updated successfully',
            'ticket': ticket.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Ticket update failed', 'message': str(e)}), 500

@tickets_bp.route('/analytics', methods=['GET'])
@token_required
def get_analytics():
    """Get analytics data"""
    try:
        user_id = get_jwt_identity()
        
        # Get all user tickets
        tickets = Ticket.query.filter_by(user_id=user_id).all()
        
        # Calculate statistics
        total_tickets = len(tickets)
        open_tickets = len([t for t in tickets if t.status == 'open'])
        in_progress_tickets = len([t for t in tickets if t.status == 'in_progress'])
        closed_tickets = len([t for t in tickets if t.status == 'closed'])
        high_priority = len([t for t in tickets if t.priority == 'high'])
        
        # Category distribution
        categories = {}
        for ticket in tickets:
            categories[ticket.category] = categories.get(ticket.category, 0) + 1
        
        # Priority distribution
        priorities = {
            'high': high_priority,
            'medium': len([t for t in tickets if t.priority == 'medium']),
            'low': len([t for t in tickets if t.priority == 'low'])
        }
        
        # Monthly trends (last 6 months)
        from collections import defaultdict
        monthly_data = defaultdict(int)
        for ticket in tickets:
            month_key = ticket.created_at.strftime('%Y-%m')
            monthly_data[month_key] += 1
        
        return jsonify({
            'stats': {
                'total': total_tickets,
                'open': open_tickets,
                'in_progress': in_progress_tickets,
                'closed': closed_tickets,
                'high_priority': high_priority
            },
            'categories': categories,
            'priorities': priorities,
            'monthly': dict(monthly_data)
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch analytics', 'message': str(e)}), 500
