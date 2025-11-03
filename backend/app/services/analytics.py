import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_sqlalchemy import SQLAlchemy
from models.task import Task
from models.user import User
from sqlalchemy import func
from datetime import datetime, timedelta

def get_task_statistics(db: SQLAlchemy):
    """
    Get overall task statistics.
    
    Returns:
        dict: Statistics including total tasks, completed tasks, pending tasks, etc.
    """
    total_tasks = db.session.query(func.count(Task.id)).scalar()
    completed_tasks = db.session.query(func.count(Task.id)).filter(Task.status == 'completed').scalar()
    pending_tasks = db.session.query(func.count(Task.id)).filter(Task.status == 'pending').scalar()
    in_progress_tasks = db.session.query(func.count(Task.id)).filter(Task.status == 'in_progress').scalar()
    
    # Calculate completion percentage
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completion_rate': round(completion_rate, 2)
    }

def get_user_task_statistics(db: SQLAlchemy, user_id: int):
    """
    Get task statistics for a specific user.
    
    Args:
        db (SQLAlchemy): Database instance
        user_id (int): User ID
        
    Returns:
        dict: User-specific task statistics
    """
    total_tasks = db.session.query(func.count(Task.id)).filter(Task.user_id == user_id).scalar()
    completed_tasks = db.session.query(func.count(Task.id)).filter(
        Task.user_id == user_id, 
        Task.status == 'completed'
    ).scalar()
    pending_tasks = db.session.query(func.count(Task.id)).filter(
        Task.user_id == user_id, 
        Task.status == 'pending'
    ).scalar()
    in_progress_tasks = db.session.query(func.count(Task.id)).filter(
        Task.user_id == user_id, 
        Task.status == 'in_progress'
    ).scalar()
    
    # Calculate completion percentage
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return {
        'user_id': user_id,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completion_rate': round(completion_rate, 2)
    }

def get_tasks_by_priority(db: SQLAlchemy):
    """
    Get task count grouped by priority.
    
    Returns:
        dict: Task counts by priority level
    """
    priority_counts = db.session.query(
        Task.priority, 
        func.count(Task.id)
    ).group_by(Task.priority).all()
    
    return {priority: count for priority, count in priority_counts}

def get_tasks_by_status(db: SQLAlchemy):
    """
    Get task count grouped by status.
    
    Returns:
        dict: Task counts by status
    """
    status_counts = db.session.query(
        Task.status, 
        func.count(Task.id)
    ).group_by(Task.status).all()
    
    return {status: count for status, count in status_counts}