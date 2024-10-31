from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required, get_jwt, get_jwt_identity,
    create_access_token, create_refresh_token
)
from Taskify_App.models import db, User, bcrypt, RevokedToken

class UserRegistration(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return {"error": "Username, email, and password are required."}, 400

            existing_user_username = User.query.filter_by(username=username).first()
            if existing_user_username:
                return {"error": "Username is already taken."}, 400

            existing_user_email = User.query.filter_by(email=email).first()
            if existing_user_email:
                return {"error": "Email is already registered."}, 400

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User registered successfully."}, 201
        except Exception as e:
            return {"error": "Failed to register user."}, 500

class UserLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            user = User.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            else:
                return {"error": "Invalid username or password."}, 401
        except Exception as e:
            return {"error": "Failed to login user."}, 500

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt()["jti"]
            revoked_token = RevokedToken(jti=jti)
            db.session.add(revoked_token)
            db.session.commit()
            return {"message": "Successfully logged out."}, 200
        except Exception as e:
            return {"error": "Failed to logout user."}, 500

class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            access_token = create_access_token(identity=current_user_id)
            return {"access_token": access_token}, 200
        except Exception as e:
            return {"error": "Failed to refresh token."}, 500

class Users(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)

            if user:
                return {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "bio": user.bio,
                    "tasks_count": len(user.tasks),
                    "comments_count": len(user.comments)
                }, 200
            else:
                return {"message": "User not found."}, 404
        except Exception as e:
            return {"error": "Failed to retrieve user data."}, 500
    @jwt_required()
    def put(self):
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if not user:
                return {"message": "User not found."}, 404

            data = request.get_json()
            for attr in data:
                setattr(user, attr, data[attr])

            db.session.commit()
            return {"message": "User details updated successfully."}, 200

        except Exception as e:
            return {"error": "Failed to update user details."}, 500