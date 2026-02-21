from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity
from models.ticket import Ticket
from utils.helpers import token_required
from datetime import datetime, timedelta
from collections import defaultdict
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/user/analytics/overview', methods=['GET'])
@token_required
def get_overview():
    """Get user analytics overview"""
    try:
        user_id = get_jwt_identity()
        
        # Get all user tickets
        tickets = Ticket.query.filter_by(user_id=user_id).all()
        
        # Calculate statistics
        total_tickets = len(tickets)
        open_tickets = len([t for t in tickets if t.status == 'open'])
        in_progress = len([t for t in tickets if t.status == 'in_progress'])
        closed_tickets = len([t for t in tickets if t.status == 'closed'])
        high_priority_count = len([t for t in tickets if t.priority == 'high'])
        
        # Calculate average AI confidence
        confidences = [t.confidence for t in tickets if t.confidence]
        average_ai_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Calculate average resolution time
        resolved_tickets = [t for t in tickets if t.status == 'closed' and t.updated_at]
        if resolved_tickets:
            resolution_times = []
            for ticket in resolved_tickets:
                time_diff = ticket.updated_at - ticket.created_at
                resolution_times.append(time_diff.total_seconds() / 3600)  # hours
            avg_resolution_time_hours = sum(resolution_times) / len(resolution_times)
        else:
            avg_resolution_time_hours = 0
        
        return jsonify({
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'in_progress': in_progress,
            'closed_tickets': closed_tickets,
            'high_priority_count': high_priority_count,
            'average_ai_confidence': round(average_ai_confidence * 100, 2),
            'avg_resolution_time_hours': round(avg_resolution_time_hours, 2)
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch overview', 'message': str(e)}), 500

@analytics_bp.route('/user/analytics/activity', methods=['GET'])
@token_required
def get_activity():
    """Get user ticket activity over time"""
    try:
        user_id = get_jwt_identity()
        
        # Get tickets from last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        tickets = Ticket.query.filter(
            Ticket.user_id == user_id,
            Ticket.created_at >= thirty_days_ago
        ).all()
        
        # Group by date
        activity_data = defaultdict(int)
        for ticket in tickets:
            date_key = ticket.created_at.strftime('%Y-%m-%d')
            activity_data[date_key] += 1
        
        # Fill in missing dates with 0
        result = []
        for i in range(30):
            date = (datetime.utcnow() - timedelta(days=29-i)).strftime('%Y-%m-%d')
            result.append({
                'date': date,
                'count': activity_data.get(date, 0)
            })
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch activity', 'message': str(e)}), 500

@analytics_bp.route('/user/analytics/category-distribution', methods=['GET'])
@token_required
def get_category_distribution():
    """Get category distribution"""
    try:
        user_id = get_jwt_identity()
        
        tickets = Ticket.query.filter_by(user_id=user_id).all()
        
        # Count by category
        categories = defaultdict(int)
        for ticket in tickets:
            categories[ticket.category] += 1
        
        result = [
            {'category': category, 'count': count}
            for category, count in categories.items()
        ]
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch category distribution', 'message': str(e)}), 500

@analytics_bp.route('/user/analytics/priority-distribution', methods=['GET'])
@token_required
def get_priority_distribution():
    """Get priority distribution"""
    try:
        user_id = get_jwt_identity()
        
        tickets = Ticket.query.filter_by(user_id=user_id).all()
        
        # Count by priority
        priorities = defaultdict(int)
        for ticket in tickets:
            priorities[ticket.priority] += 1
        
        result = [
            {'priority': priority.capitalize(), 'count': count}
            for priority, count in priorities.items()
        ]
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch priority distribution', 'message': str(e)}), 500

@analytics_bp.route('/user/analytics/ai-insights', methods=['GET'])
@token_required
def get_ai_insights():
    """Get AI-related insights"""
    try:
        user_id = get_jwt_identity()
        
        tickets = Ticket.query.filter_by(user_id=user_id).all()
        
        if not tickets:
            return jsonify({
                'average_confidence': 0,
                'low_confidence_count': 0,
                'most_common_category': 'N/A',
                'confidence_trend': 'stable'
            }), 200
        
        # Calculate average confidence
        confidences = [t.confidence for t in tickets if t.confidence]
        average_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Count low confidence tickets (< 0.6)
        low_confidence_count = len([c for c in confidences if c < 0.6])
        
        # Most common category
        categories = defaultdict(int)
        for ticket in tickets:
            categories[ticket.category] += 1
        most_common_category = max(categories.items(), key=lambda x: x[1])[0] if categories else 'N/A'
        
        # Confidence trend (compare first half vs second half)
        if len(confidences) >= 4:
            mid = len(confidences) // 2
            first_half_avg = sum(confidences[:mid]) / mid
            second_half_avg = sum(confidences[mid:]) / (len(confidences) - mid)
            
            if second_half_avg > first_half_avg + 0.05:
                confidence_trend = 'improving'
            elif second_half_avg < first_half_avg - 0.05:
                confidence_trend = 'declining'
            else:
                confidence_trend = 'stable'
        else:
            confidence_trend = 'stable'
        
        return jsonify({
            'average_confidence': round(average_confidence * 100, 2),
            'low_confidence_count': low_confidence_count,
            'most_common_category': most_common_category,
            'confidence_trend': confidence_trend
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch AI insights', 'message': str(e)}), 500

@analytics_bp.route('/user/analytics/resolution-insights', methods=['GET'])
@token_required
def get_resolution_insights():
    """Get resolution time insights"""
    try:
        user_id = get_jwt_identity()
        
        tickets = Ticket.query.filter_by(user_id=user_id).all()
        closed_tickets = [t for t in tickets if t.status == 'closed' and t.updated_at]
        open_tickets = [t for t in tickets if t.status in ['open', 'in_progress']]
        
        if not closed_tickets:
            return jsonify({
                'average_resolution_hours': 0,
                'fastest_resolution_hours': 0,
                'longest_open_hours': 0,
                'sla_met_rate': 0
            }), 200
        
        # Calculate resolution times
        resolution_times = []
        for ticket in closed_tickets:
            time_diff = ticket.updated_at - ticket.created_at
            hours = time_diff.total_seconds() / 3600
            resolution_times.append(hours)
        
        average_resolution = sum(resolution_times) / len(resolution_times)
        fastest_resolution = min(resolution_times)
        
        # Longest open ticket
        if open_tickets:
            longest_open_times = []
            for ticket in open_tickets:
                time_diff = datetime.utcnow() - ticket.created_at
                hours = time_diff.total_seconds() / 3600
                longest_open_times.append(hours)
            longest_open = max(longest_open_times)
        else:
            longest_open = 0
        
        # SLA met rate (assuming 48 hours SLA)
        sla_hours = 48
        sla_met = len([t for t in resolution_times if t <= sla_hours])
        sla_met_rate = (sla_met / len(resolution_times)) * 100 if resolution_times else 0
        
        return jsonify({
            'average_resolution_hours': round(average_resolution, 2),
            'fastest_resolution_hours': round(fastest_resolution, 2),
            'longest_open_hours': round(longest_open, 2),
            'sla_met_rate': round(sla_met_rate, 2)
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch resolution insights', 'message': str(e)}), 500

@analytics_bp.route('/user/analytics/monthly-summary', methods=['GET'])
@token_required
def get_monthly_summary():
    """Get current month summary with comparison"""
    try:
        user_id = get_jwt_identity()
        
        now = datetime.utcnow()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        
        # Current month tickets
        current_month_tickets = Ticket.query.filter(
            Ticket.user_id == user_id,
            Ticket.created_at >= current_month_start
        ).all()
        
        # Last month tickets
        last_month_tickets = Ticket.query.filter(
            Ticket.user_id == user_id,
            Ticket.created_at >= last_month_start,
            Ticket.created_at < current_month_start
        ).all()
        
        # Current month stats
        current_created = len(current_month_tickets)
        current_resolved = len([t for t in current_month_tickets if t.status == 'closed'])
        current_critical = len([t for t in current_month_tickets if t.priority == 'high'])
        
        current_confidences = [t.confidence for t in current_month_tickets if t.confidence]
        current_avg_confidence = sum(current_confidences) / len(current_confidences) if current_confidences else 0
        
        # Last month stats
        last_created = len(last_month_tickets)
        last_resolved = len([t for t in last_month_tickets if t.status == 'closed'])
        last_critical = len([t for t in last_month_tickets if t.priority == 'high'])
        
        last_confidences = [t for t in last_month_tickets if t.confidence]
        last_avg_confidence = sum(last_confidences) / len(last_confidences) if last_confidences else 0
        
        # Calculate changes
        def calculate_change(current, last):
            if last == 0:
                return 0 if current == 0 else 100
            return round(((current - last) / last) * 100, 1)
        
        return jsonify({
            'current_month': {
                'created': current_created,
                'resolved': current_resolved,
                'critical': current_critical,
                'avg_confidence': round(current_avg_confidence * 100, 2)
            },
            'changes': {
                'created': calculate_change(current_created, last_created),
                'resolved': calculate_change(current_resolved, last_resolved),
                'critical': calculate_change(current_critical, last_critical),
                'confidence': round((current_avg_confidence - last_avg_confidence) * 100, 2)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to fetch monthly summary', 'message': str(e)}), 500
