import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.analytics import (
    get_task_statistics, 
    get_user_task_statistics, 
    get_tasks_by_priority, 
    get_tasks_by_status
)
from models.task import db

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/statistics', methods=['GET'])
@jwt_required()
def task_statistics():
    """Get overall task statistics."""
    try:
        # Check if user is admin
        claims = get_jwt()
        user_role = claims.get('role', 'user')
        
        if user_role != 'admin':
            # Return user-specific statistics
            current_user_id = get_jwt_identity()
            stats = get_user_task_statistics(db, current_user_id)
        else:
            # Return overall statistics
            stats = get_task_statistics(db)
        
        return jsonify({
            'statistics': stats
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve statistics', 'error': str(e)}), 500

@analytics_bp.route('/priority', methods=['GET'])
@jwt_required()
def tasks_by_priority():
    """Get task count grouped by priority."""
    try:
        stats = get_tasks_by_priority(db)
        
        return jsonify({
            'priority_stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve priority statistics', 'error': str(e)}), 500

@analytics_bp.route('/status', methods=['GET'])
@jwt_required()
def tasks_by_status():
    """Get task count grouped by status."""
    try:
        stats = get_tasks_by_status(db)
        
        return jsonify({
            'status_stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve status statistics', 'error': str(e)}), 500