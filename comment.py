from flask import request, jsonify, make_response, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from Taskify_App.models import Comment,Task, Project, db

class Comments(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        comments = Comment.query.filter_by(user_id=current_user_id).all()
        return make_response(jsonify([comment.to_dict() for comment in comments]), 200)

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        comment = Comment(
            task_id=data['task_id'],
            project_id=data['project_id'],
            user_id=current_user_id,  
            text=data['text']
        )
        db.session.add(comment)
        db.session.commit()
        return make_response(jsonify(comment.to_dict()), 201)

class CommentDetail(Resource):
    @jwt_required()
    def get(self, id):
        try:
            current_user_id = get_jwt_identity()            
            if id:
                # Fetch comments by Task ID for the current user
                comments = Comment.query.filter_by(task_id=id, user_id=current_user_id).all()
                if comments:
                    return {'comments': [comment.to_dict() for comment in comments]}, 200
                else:
                    return {'message': 'No comments found for the specified task'}, 404
            else:
                return {'message': 'Please provide either task ID'}, 400
        except Exception as e:
            abort(500, message="Internal Server Error: {}".format(str(e)))

    @jwt_required()
    def delete(self, id):
        current_user_id = get_jwt_identity()
        comment = Comment.query.filter_by(id=id, user_id=current_user_id).first()
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return make_response(jsonify({'message': 'Comment deleted successfully'}))
        else:
            return make_response(jsonify({'error': 'Comment not found or unauthorized'}), 404)
class CommentDetailProject(Resource):
    @jwt_required()
    def get(self, id):
        try:
            current_user_id = get_jwt_identity()
            if id:
                # Fetch comments by Task ID for the current user
                comments = Comment.query.filter_by(project_id=id, user_id=current_user_id).all()
                if comments:
                    return {'comments': [comment.to_dict() for comment in comments]}, 200
                else:
                    return {'message': 'No comments found for the specified task'}, 404
            else:
                return {'message': 'Please provide project ID'}, 400
        except Exception as e:
            abort(500, message="Internal Server Error: {}".format(str(e)))