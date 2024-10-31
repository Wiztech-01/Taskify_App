# import os
from datetime import timedelta
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from Taskify_App.models import db, bcrypt,RevokedToken



from Taskify_App.auth import (
    UserRegistration,
    UserLogin,
    RefreshToken,
    Users,
    UserLogout
)

from Taskify_App.tasks import (
    Tasks,
    TaskDetail,
)
from Taskify_App.comment import (
    Comments,
    CommentDetail,
    CommentDetailProject
)
from Taskify_App.project import (
    Projects,
    ProjectDetail,
)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=2)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies'] 
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  
app.config['JWT_COOKIE_SECURE'] = False  
app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh'  
app.config['JWT_REFRESH_COOKIE_SECURE'] = False  
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False 

api = Api(app)
jwt = JWTManager(app)

# @app.route('/')
# def home():
#     return "Welcome to Taskify App!"  


@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    revoked_token = RevokedToken.query.filter_by(jti=jti).first()
    return revoked_token is not None


migrate = Migrate(app, db)
db.init_app(app)
bcrypt.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()


api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(RefreshToken, '/refresh')
api.add_resource(Users, '/user')
api.add_resource(Tasks, '/tasks')
api.add_resource(TaskDetail, '/tasks/<int:id>')
api.add_resource(Projects, '/projects')
api.add_resource(ProjectDetail, '/projects/<int:id>')
api.add_resource(Comments, '/comments')
api.add_resource(CommentDetail, '/comments/<int:id>')
api.add_resource(CommentDetailProject, '/projectcomments/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)