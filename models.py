from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import validates, relationship
import re

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    serialize_rules = ('-tasks.user','-comments.user','-projects.user')
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)

    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', lazy=True, cascade='all, delete-orphan')
    projects = db.relationship('Project', backref='user', lazy=True, cascade='all, delete-orphan')
    

    @validates('password')
    def validate_password(self, key, password):
        assert len(password) >=  5, "Password must be at least  5 characters long."
        assert re.search(r'\d', password) and re.search(r'[a-zA-Z]', password), "Password must contain both letters and numbers."
        return password
    
    @validates('email')
    def validate_email(self, key, email):
        assert re.match(r'^[\w\.-]+@[\w\.-]+$', email), "Invalid email format."
        return email

class Task(db.Model, SerializerMixin):
    
    __tablename__ = 'tasks'

    serialize_rules = ('-user.tasks','-comments.user')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    category= db.Column(db.String(20), nullable = False)
    reminder_date = db.Column(db.DateTime, nullable=False)
    recurrence_pattern = db.Column(db.String(50))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=True)

    comments = db.relationship('Comment', backref='task', lazy='dynamic', cascade='all, delete-orphan')

    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': str(self.due_date),
            'priority': self.priority,
            'category': self.category,
            'reminder_date': str(self.reminder_date),
            'recurrence_pattern': self.recurrence_pattern,
            'status': self.status,
            'user_id': self.user_id,
            'project_id': self.project_id,
        }
    
    @validates('title')
    def validate_title(self, key, title):
        assert len(title.strip()) >  0, "Title cannot be empty."
        return title
    
    @validates('priority')
    def validate_priority(self, key, priority):
        allowed_priorities = ['High', 'Medium', 'Low']
        assert priority in allowed_priorities, "Priority must be either High, Medium, or Low."
        return priority
    
    @validates('recurrence_pattern')
    def validate_recurrence_pattern(self, key, pattern):
        allowed_patterns = ['Weekly', 'Monthly', 'Daily']
        assert pattern in allowed_patterns, f"Recurrence pattern must be one of {', '.join(allowed_patterns)}."
        return pattern
    

class Project(db.Model, SerializerMixin):
    __tablename__ = 'projects'

    serialize_rules = ('-tasks.project', '-comments.project')    

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
            'user_id': self.user_id,
        }
    
    @validates('start_date', 'end_date')
    def validate_date_range(self, key, end_date):
        if key == 'end_date':
            if end_date < self.start_date:
                raise ValueError("End date must be after the start date.")
        return end_date

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    serialize_rules = ('-user.comments','-task.comments','-task.user')    

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=True)
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'timestamp': str(self.timestamp),
            'task_id': self.task_id,
            'user_id': self.user_id,
            'project_id': self.project_id,
        }
    
    @validates('text')
    def validate_comment_text(self, key, text):
        assert len(text) <=  500, "Comment text cannot exceed  500 characters."
        return text

class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)

    def __init__(self, jti):
        self.jti = jti