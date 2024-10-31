from Taskify_App.app import app
from datetime import datetime
from Taskify_App.app import db, bcrypt   
from Taskify_App.models import User, Task, Project, Comment

def create_users():
    User.query.delete()
    users_data = [
        {'username': 'john_doe', 'email': 'john@example.com', 'password': 'password1', 'bio': 'John Doe is a software engineer.'},
        {'username': 'jane_smith', 'email': 'jane@example.com', 'password': 'password2', 'bio': 'Jane Smith is a project manager.'},
        {'username': 'alice_green', 'email': 'alice@example.com', 'password': 'password3', 'bio': 'Alice Green is a designer.'},
        {'username': 'bob_jones', 'email': 'bob@example.com', 'password': 'password4', 'bio': 'Bob Jones is a developer.'}
    ]

    for user_data in users_data:
        hashed_password = bcrypt.generate_password_hash(user_data['password']).decode("utf-8")
        user = User(username=user_data['username'], email=user_data['email'], password=hashed_password, bio=user_data['bio'])
        db.session.add(user)

    db.session.commit()

def create_projects():
    Project.query.delete()
    project1 = Project(name='Project Alpha', description='This is project Alpha.', start_date=datetime(2022,  1,  1), end_date=datetime(2022,  12,  31), user_id=1)
    project2 = Project(name='Project Beta', description='This is project Beta.', start_date=datetime(2023,  1,  1), end_date=datetime(2023,  12,  31), user_id=2)
    project3 = Project(name='Project Gamma', description='This is project Gamma.', start_date=datetime(2024,  1,  1), end_date=datetime(2024,  12,  31), user_id=3)
    project4 = Project(name='Project Socrates', description='This is project Socrates.', start_date=datetime(2025,  1,  1), end_date=datetime(2025,  12,  31), user_id=4)
    db.session.add_all([project1, project2, project3, project4])
    db.session.commit()
    return project1, project2, project3, project4

def create_tasks(project1, project2, project3, project4):
    Task.query.delete()
    task1 = Task(
        title='Task 1',
        description='This is task 1 for project Alpha.',
        due_date=datetime(2022,  6,  30),
        priority="High",
        status='Pending',
        user_id=1,
        category='Development',
        reminder_date=datetime(2022,  6,  29),
        recurrence_pattern='Weekly',
        project_id=project1.id
    )
    task2 = Task(
        title='Task 2',
        description='This is task 2 for project Beta.',
        due_date=datetime(2023,  3,  15),
        priority="Medium",
        status='In Progress',
        user_id=2,
        category='Design',
        reminder_date=datetime(2023,  3,  14),
        recurrence_pattern='Daily',
        project_id=project2.id
    )
    task3 = Task(
        title='Task 3',
        description='This is task 3 for project Alpha.',
        due_date=datetime(2022,  8,  15),
        priority="Low",
        status='Pending',
        user_id=3,
        category='Testing',
        reminder_date=datetime(2022,  8,  14),
        recurrence_pattern='Monthly',
        project_id=project1.id
    )
    task4 = Task(
        title='Task 4',
        description='This is task 4 for project Gamma.',
        due_date=datetime(2024,  5,  20),
        priority="High",
        status='Completed',
        user_id=4,
        category='Documentation',
        reminder_date=datetime(2024,  5,  19),
        recurrence_pattern='Daily',
        project_id=project3.id
    )
    db.session.add_all([task1, task2, task3, task4])
    db.session.commit()

def create_comments():
    Comment.query.delete()
    comment1 = Comment(text='This is a comment for task 1 by John Doe.', timestamp=datetime(2022,  6,  25), user_id=1, task_id=1, project_id=1)
    comment2 = Comment(text='This is a comment for task 2 by Jane Smith.', timestamp=datetime(2023,  3,  8), user_id=2, task_id=2, project_id=2)
    comment3 = Comment(text='This is a comment for task 3 by Alice Green.', timestamp=datetime(2022,  8,  14), user_id=3, task_id=3, project_id=3)
    comment4 = Comment(text='This is a comment for task 4 by Bob Jones.', timestamp=datetime(2024,  5,  18), user_id=4, task_id=4, project_id=4)
    db.session.add_all([comment1, comment2, comment3, comment4])
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        create_users()
        project1, project2, project3, project4 = create_projects()  
        create_tasks(project1, project2, project3, project4) 
        create_comments()