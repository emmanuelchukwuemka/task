import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.task import Task, db
from models.user import User
from sqlalchemy import and_, or_
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

def validate_task_data(data, required_fields=None):
    """Validate task data."""
    if not data:
        return False, 'No data provided'
    
    if required_fields is None:
        required_fields = ['title']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f'{field} is required'
    
    # Validate status if provided
    if 'status' in data and data['status'] not in ['pending', 'in_progress', 'completed']:
        return False, 'Invalid status. Must be pending, in_progress, or completed'
    
    # Validate priority if provided
    if 'priority' in data and data['priority'] not in ['low', 'medium', 'high']:
        return False, 'Invalid priority. Must be low, medium, or high'
    
    # Validate due_date if provided
    if 'due_date' in data and data['due_date']:
        try:
            datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return False, 'Invalid due_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
    
    return True, None

@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    """Get all tasks with filtering and pagination."""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)  # Max 100 items per page
        
        # Filtering parameters
        status = request.args.get('status')
        priority = request.args.get('priority')
        search = request.args.get('search')
        
        # Build query
        query = Task.query
        
        # Apply filters
        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        if search:
            search_filter = or_(
                Task.title.contains(search),
                Task.description.contains(search)
            )
            query = query.filter(search_filter)
        
        # For non-admin users, only show their own tasks
        claims = get_jwt()
        user_role = claims.get('role', 'user')
        current_user_id = get_jwt_identity()
        
        if user_role != 'admin':
            query = query.filter(Task.user_id == current_user_id)
        
        # Order by creation date (newest first)
        query = query.order_by(Task.created_at.desc())
        
        # Paginate
        paginated_tasks = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'tasks': [task.to_dict() for task in paginated_tasks.items],
            'pagination': {
                'page': paginated_tasks.page,
                'pages': paginated_tasks.pages,
                'per_page': paginated_tasks.per_page,
                'total': paginated_tasks.total
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve tasks', 'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Get a specific task by ID."""
    try:
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'message': 'Task not found'}), 404
        
        # Check if user has permission to view this task
        claims = get_jwt()
        user_role = claims.get('role', 'user')
        current_user_id = get_jwt_identity()
        
        if user_role != 'admin' and task.user_id != current_user_id:
            return jsonify({'message': 'Access denied'}), 403
        
        return jsonify({'task': task.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve task', 'error': str(e)}), 500

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    """Create a new task."""
    try:
        data = request.get_json()
        
        # Validate data
        is_valid, error_message = validate_task_data(data)
        if not is_valid:
            return jsonify({'message': error_message}), 400
        
        # Create new task
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium'),
            user_id=get_jwt_identity()  # Assign to current user
        )
        
        # Set due_date if provided
        if 'due_date' in data and data['due_date']:
            task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Task created successfully',
            'task': task.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create task', 'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Update a specific task."""
    try:
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'message': 'Task not found'}), 404
        
        # Check if user has permission to update this task
        claims = get_jwt()
        user_role = claims.get('role', 'user')
        current_user_id = get_jwt_identity()
        
        if user_role != 'admin' and task.user_id != current_user_id:
            return jsonify({'message': 'Access denied'}), 403
        
        data = request.get_json()
        
        # Validate data (no required fields for updates)
        is_valid, error_message = validate_task_data(data, required_fields=[])
        if not is_valid:
            return jsonify({'message': error_message}), 400
        
        # Update fields if provided
        if 'title' in data:
            task.title = data['title']
        
        if 'description' in data:
            task.description = data['description']
        
        if 'status' in data:
            task.status = data['status']
        
        if 'priority' in data:
            task.priority = data['priority']
        
        if 'due_date' in data:
            if data['due_date']:
                task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            else:
                task.due_date = None
        
        task.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Task updated successfully',
            'task': task.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update task', 'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete a specific task."""
    try:
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'message': 'Task not found'}), 404
        
        # Check if user has permission to delete this task
        claims = get_jwt()
        user_role = claims.get('role', 'user')
        current_user_id = get_jwt_identity()
        
        if user_role != 'admin' and task.user_id != current_user_id:
            return jsonify({'message': 'Access denied'}), 403
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': 'Task deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete task', 'error': str(e)}), 500