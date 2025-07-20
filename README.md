# EdTech Assignment Tracker

A simple, full-stack web application for managing and submitting assignments for teachers and students.

<br>

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- **Python 3.8+**: The backend is built with Python.
- **Node.js & npm (Optional)**: If you were to add frontend dependencies in the future.
- **A modern web browser**: To run the frontend.

### Installation

1.  **Clone the repository** (or set up the files as discussed):
    ```bash
    git clone <your-repo-url>
    cd edtech-assignment-tracker
    ```

2.  **Backend Setup**:
    Navigate to the `backend` directory and install the required Python packages.
    ```bash
    cd backend/
    pip install "fastapi[all]" "uvicorn[standard]" sqlalchemy "python-multipart" passlib[bcrypt] python-jose[cryptography]"
    ```

3.  **Run the Backend Server**:
    From the `backend` directory, start the FastAPI server with auto-reload for development.
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

4.  **Frontend Setup**:
    The frontend is a static application. Simply open the `index.html` file in your preferred web browser.

## 📁 Project Structure

The project is organized into two main directories:

-   `backend/`: Contains all the Python code for the API, including routers, database models, and schemas.
-   `frontend/`: Contains all the static files for the user interface (HTML, CSS, JavaScript).

├── backend/
│   ├── main.py            # Main FastAPI application entry point
│   ├── database.py        # SQLAlchemy database engine and session
│   ├── models.py          # Database models (User, Assignment, Submission)
│   ├── schemas.py         # Pydantic schemas for data validation
│   └── routers/           # API endpoint definitions
│       ├── init.py
│       ├── users.py
│       └── assignments.py
├── frontend/
│   ├── index.html         # Main application page
│   ├── styles.css         # Styling for the application
│   └── js/
│       └── script.js      # Frontend logic and API calls
└── README.md


## ✨ Features

-   **User Authentication**: Secure signup and login with role-based access control (Student/Teacher).
-   **Assignment Management**: Teachers can create, view, and manage assignments.
-   **Assignment Submission**: Students can submit assignments with a text response and an optional file upload.
-   **File Storage**: Submitted files are stored on the server.
-   **Dynamic UI**: The frontend dynamically loads content and switches between views without page reloads.
-   **Modern Feedback**: User actions (e.g., submission success) are confirmed with clean toast notifications instead of distracting alerts.

## 🖥️ API Endpoints

The backend exposes a RESTful API. Below are the primary endpoints:

| Endpoint                          | Method | Description                                    | Role       |
| --------------------------------- | ------ | ---------------------------------------------- | ---------- |
| `/api/v1/auth/signup`             | `POST`   | Creates a new user account.                    | Public     |
| `/api/v1/auth/token`              | `POST`   | Authenticates a user and returns a JWT token.  | Public     |
| `/api/v1/users/me`                | `GET`    | Retrieves the current authenticated user's info. | Authenticated |
| `/api/v1/assignments/`            | `POST`   | Creates a new assignment.                      | Teacher    |
| `/api/v1/assignments/`            | `GET`    | Retrieves all assignments.                     | Authenticated |
| `/api/v1/assignments/{id}/submit` | `POST`   | Submits an assignment for a specific ID.       | Student    |
| `/api/v1/assignments/{id}/submissions` | `GET`    | Views all submissions for an assignment.     | Teacher    |

## 🤝 Contributing

Contributions are welcome! If you find a bug or have a feature request, please feel free to open an issue or submit a pull request.

## 📄 License

This project is open source and available under the MIT License.
