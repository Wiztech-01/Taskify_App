# Taskify_App

# Flask Backend Task Management Application

This Flask backend application serves as a task management system where users can create, manage, and track their tasks, projects, and comments. It provides endpoints for user registration, login, task management, project management, comment management, and token management.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Evanny254/Taskify-Backend

2. Install dependencies: pip install -r requirements.txt
3. Configure the database connection in the app.py file.

## Database Models

### User
Attributes: id, username, email, password, bio
Relationships: Tasks, Comments, Projects
### Task
Attributes: id, title, description, due_date, priority, status, category, reminder_date, recurrence_pattern, user_id, project_id
Relationships: User, Project, Comments
### Project
Attributes: id, name, description, start_date, end_date, user_id
Relationships: User, Tasks, Comments
### Comment
Attributes: id, text, timestamp, task_id, user_id, project_id
Relationships: User, Task, Project
### RevokedToken
Attributes: id, jti

## API Endpoints

### User Registration
POST /register
User Login
POST /login
User Logout
POST /logout
Refresh Token
POST /refresh

### Get User Details
GET /user
Task Management
GET /tasks
POST /tasks
GET /tasks/<task_id>
PUT /tasks/<task_id>
DELETE /tasks/<task_id>

### Project Management
GET /projects
POST /projects
GET /projects/<project_id>
PUT /projects/<project_id>
DELETE /projects/<project_id>

### Comment Management
GET /comments
POST /comments
GET /comments/<comment_id>
PUT /comments/<comment_id>
DELETE /comments/<comment_id>

## Usage
Start the Flask server: flask run
Access the API endpoints using a REST client or HTTP requests.
