from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from Taskify_App.models import Project, db

class Projects(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        projects = Project.query.filter_by(user_id=current_user_id).all()
        return make_response(jsonify([project.to_dict() for project in projects]), 200)

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()

        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d")
        project = Project(
            name=data['name'],
            description=data['description'],
            start_date=start_date,
            end_date=end_date,
            user_id=current_user_id, 
        )
        db.session.add(project)
        db.session.commit()
        return make_response(jsonify(project.to_dict()), 201)

class ProjectDetail(Resource):
    @jwt_required()
    def get(self, id):
        current_user_id = get_jwt_identity()
        project = Project.query.filter_by(id=id, user_id=current_user_id).first()
        if project:
            return make_response(jsonify(project.to_dict()))
        else:
            return make_response(jsonify({'error': 'Project not found or unauthorized'}), 404)

    @jwt_required()
    def put(self, id):
        current_user_id = get_jwt_identity()
        project = Project.query.filter_by(id=id, user_id=current_user_id).first()
        if project:
            data = request.get_json()
            project.name = data.get('name', project.name)
            project.description = data.get('description', project.description)
            start_date_str = data.get('start_date')
            if start_date_str:
                project.start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            
            end_date_str = data.get('end_date')
            if end_date_str:
                project.end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            db.session.commit()
            response = make_response(jsonify(project.to_dict()), 201)
            return response
        else:
            return make_response(jsonify({'error': 'Project not found or unauthorized'}), 404)

    @jwt_required()
    def delete(self, id):
        current_user_id = get_jwt_identity()
        project = Project.query.filter_by(id=id, user_id=current_user_id).first()
        if project:
            db.session.delete(project)
            db.session.commit()
            return make_response(jsonify({'message': 'Project deleted successfully'}))
        else:
            return make_response(jsonify({'error': 'Project not found or unauthorized'}), 404)