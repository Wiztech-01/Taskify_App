from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from Taskify_App.models import Task, db

class Tasks(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=current_user_id).all()
        return make_response(jsonify([task.to_dict() for task in tasks]), 200)

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        due_date = datetime.strptime(data['due_date'], "%Y-%m-%d").date()
        reminder_date = datetime.strptime(data['reminder_date'], "%Y-%m-%d").date()
        task = Task(
            title=data['title'],
            description=data['description'],
            due_date=due_date,
            priority=data['priority'],
            category=data['category'],
            reminder_date=reminder_date,
            recurrence_pattern=data['recurrence_pattern'],
            status=data['status'],
            user_id=current_user_id,
            project_id=data['project_id']
        )
        
        db.session.add(task)
        db.session.commit()
        return make_response(jsonify(task.to_dict()), 201)

class TaskDetail(Resource):
    @jwt_required()
    def get(self, id):
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=id, user_id=current_user_id).first()
        if task:
            return make_response(jsonify(task.to_dict()))
        else:
            return make_response(jsonify({'error': 'Task not found or unauthorized'}), 404)
        
    @jwt_required()
    def put(self, id):
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=id, user_id=current_user_id).first()
        if not task:
            return make_response(jsonify({"error": "Task not found or unauthorized"}),  404)

        data = request.get_json()

        for attr, value in data.items():
            if attr in ['due_date', 'reminder_date']:
                try:
                    value = datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    return make_response(jsonify({"error": "Invalid date format"}),  400)

            if hasattr(task, attr):
                setattr(task, attr, value)
            else:
                return make_response(jsonify({"error": f"Invalid attribute: {attr}"}),  400)

        db.session.commit()

        return make_response(jsonify(task.to_dict()),  200)
    
    @jwt_required()
    def delete(self, id):
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=id, user_id=current_user_id).first()
        if task:
            db.session.delete(task)
            db.session.commit()
            return make_response(jsonify({'message': 'Task deleted successfully'}))
        else:
            return make_response(jsonify({'error': 'Task not found or unauthorized'}), 404)