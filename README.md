EdTech Assignment Tracker
This is a simple full-stack web application designed to help teachers manage assignments and students submit their work. The application features user authentication with two distinct roles: Teacher and Student.

Features
Teacher
Authentication: Secure signup and login to access the teacher dashboard.

Create Assignments: Easily create new assignments with a title, a detailed description, and a due date.

View Submissions: Access and view all submissions for any created assignment.

Student
Authentication: Secure signup and login to access the student dashboard.

View Assignments: See all assignments posted by teachers.

Submit Assignments: Submit assignments by providing a text response and optionally uploading a file.

Technologies Used
Backend: Python with the FastAPI framework.

Database: SQLAlchemy with SQLite for data persistence.

Authentication: JWT for secure token-based authentication.

Frontend: Plain HTML, CSS, and JavaScript.

UI/UX: Dynamic content loading and a responsive design without the need for external frameworks.

Setup and Installation
Prerequisites
Python 3.8+

pip (Python package installer)

1. Backend Setup
Clone the repository (if applicable) or create the following directory structure:

.
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       ├── users.py
│       └── assignments.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── js/
│       └── script.js
└── README.md
Install dependencies in your backend directory:

Bash

pip install fastapi "uvicorn[standard]" sqlalchemy "python-multipart" passlib[bcrypt] python-jose[cryptography]
Run the application:
From the backend directory, start the server using Uvicorn.

Bash

uvicorn main:app --reload
The server will run on http://127.0.0.1:8000.

2. Frontend Setup
The frontend is a static web application. You do not need a separate server to run it.

Open index.html in your web browser.

Usage
Open index.html in your web browser.

Sign Up: Create a new account and select your role (Teacher or Student).

Login: Use your newly created credentials to log in.

Teacher Dashboard:

Use the "Create New Assignment" form to post an assignment.

View your assignments and click "View Submissions" to see student work.

Student Dashboard:

The "Available Assignments" section will display all current assignments.

Click the "Submit" button on an assignment to submit your work via text or file upload.
