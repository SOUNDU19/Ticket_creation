from flask import Blueprint, jsonify, request
from utils.helpers import token_required
from flask_jwt_extended import get_jwt_identity
from models.ticket import Ticket
from models.user import User
from collections import defaultdict
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)


def get_user_id_or_guest():
    user_id = get_jwt_identity()
    if not user_id:
        guest = User.query.filter_by(email='guest@nexoraai.com').first()
        return guest.id if guest else None
    return user_id


@analytics_bp.route('/user/analytics/overview', methods=['GET'])
@token_required
def overview():
    try:
        user_id = get_user_id_or_guest()
        if not user_id:
            return jsonify({'total': 0, 'open': 0, 'in_progress': 0, 'closed': 0, 'high_priority': 0, 'avg_confidence': 0}), 200

        tickets = Ticket.query.filter_by(user_id=user_id).all()
        total = len(tickets)
        open_t = sum(1 for t in tickets if t.status == 'open')
        in_prog = sum(1 for t in tickets if t.status == 'in_progress')
        closed = sum(1 for t in tickets if t.status in ('closed', 'resolved'))
        high = sum(1 for t in tickets if t.priority in ('high', 'critical'))
        avg_conf = round(sum(t.ai_confidence or 0 for t in tickets) / total * 100, 1) if total else 0

        return jsonify({
            'total': total, 'open': open_t, 'in_progress': in_prog,
            'closed': closed, 'high_priority': high, 'avg_confidence': avg_conf
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/user/analytics/activity', methods=['GET'])
@token_required
def activity():
    try:
        user_id = get_user_id_or_guest()
        if not user_id:
            return jsonify({'labels': [], 'data': []}), 200

        days = int(request.args.get('days', 30))
        since = datetime.utcnow() - timedelta(days=days)
        tickets = Ticket.query.filter(
            Ticket.user_id == user_id,
            Ticket.created_at >= since
        ).all()

        daily = defaultdict(int)
        for t in tickets:
            day = t.created_at.strftime('%Y-%m-%d')
            daily[day] += 1

        labels = [(datetime.utcnow() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days - 1, -1, -1)]
        data = [daily.get(l, 0) for l in labels]

        return jsonify({'labels': labels, 'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/user/analytics/category-distribution', methods=['GET'])
@token_required
def category_dist():
    try:
        user_id = get_user_id_or_guest()
        if not user_id:
            return jsonify({}), 200
        tickets = Ticket.query.filter_by(user_id=user_id).all()
        dist = defaultdict(int)
        for t in tickets:
            dist[t.category] += 1
        return jsonify(dict(dist)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/user/analytics/priority-distribution', methods=['GET'])
@token_required
def priority_dist():
    try:
        user_id = get_user_id_or_guest()
        if not user_id:
            return jsonify({}), 200
        tickets = Ticket.query.filter_by(user_id=user_id).all()
        dist = defaultdict(int)
        for t in tickets:
            dist[t.priority] += 1
        return jsonify(dict(dist)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/user/analytics/ai-insights', methods=['GET'])
@token_required
def ai_insights():
    try:
        user_id = get_user_id_or_guest()
        if not user_id:
            return jsonify({'avg_confidence': 0, 'low_confidence_count': 0, 'common_category': 'N/A'}), 200
        tickets = Ticket.query.filter_by(user_id=user_id).all()
        if not tickets:
            return jsonify({'avg_confidence': 0, 'low_confidence_count': 0, 'common_category': 'N/A'}), 200

        avg_conf = sum(t.ai_confidence or 0 for t in tickets) / len(tickets)
        low_conf = sum(1 for t in tickets if (t.ai_confidence or 0) < 0.7)
        cats = defaultdict(int)
        for t in tickets:
            cats[t.category] += 1
        common = max(cats, key=cats.get) if cats else 'N/A'

        return jsonify({
            'avg_confidence': round(avg_conf * 100, 1),
            'low_confidence_count': low_conf,
            'common_category': common
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/user/analytics/resolution-insights', methods=['GET'])
@token_required
def resolution_insights():
    return jsonify({'avg_resolution': '24h', 'fastest': '1h', 'longest_open': '72h', 'sla_rate': 85}), 200


@analytics_bp.route('/user/analytics/monthly-summary', methods=['GET'])
@token_required
def monthly_summary():
    try:
        user_id = get_user_id_or_guest()
        if not user_id:
            return jsonify({'created': 0, 'resolved': 0, 'critical': 0, 'avg_confidence': 0}), 200

        now = datetime.utcnow()
        start = now.replace(day=1, hour=0, minute=0, second=0)
        tickets = Ticket.query.filter(
            Ticket.user_id == user_id,
            Ticket.created_at >= start
        ).all()

        return jsonify({
            'created': len(tickets),
            'resolved': sum(1 for t in tickets if t.status in ('resolved', 'closed')),
            'critical': sum(1 for t in tickets if t.priority == 'critical'),
            'avg_confidence': round(sum(t.ai_confidence or 0 for t in tickets) / len(tickets) * 100, 1) if tickets else 0
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
