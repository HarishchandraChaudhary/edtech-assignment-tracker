const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
});

document.getElementById('logout-btn').addEventListener('click', () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    checkAuthStatus();
});

// --- NEW FUNCTION: Show a toast notification ---
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    toastContainer.appendChild(toast);

    // Show the toast
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);

    // Hide and remove the toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 500); // Wait for the fade-out transition
    }, 3000);
}

function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    document.querySelectorAll('.view').forEach(view => view.style.display = 'none');
    document.getElementById('logout-btn').style.display = 'none';

    if (token && role) {
        document.getElementById('logout-btn').style.display = 'block';
        if (role === 'teacher') {
            document.getElementById('teacher-view').style.display = 'block';
            fetchTeacherAssignments();
        } else if (role === 'student') {
            document.getElementById('student-view').style.display = 'block';
            fetchStudentAssignments();
        }
    } else {
        document.getElementById('login-signup-view').style.display = 'block';
    }
}

async function handleResponse(response) {
    if (!response.ok) {
        const errorData = await response.json();
        const errorMessage = errorData.detail || 'An unexpected error occurred.';
        throw new Error(errorMessage);
    }
    return response.json();
}

async function handleAuth(type) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;

    if (!username || !password) {
        showToast('Please fill in both fields.', 'error');
        return;
    }

    try {
        if (type === 'signup') {
            const response = await fetch(`${API_BASE_URL}/auth/signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password, role })
            });
            await handleResponse(response);
            showToast('Sign up successful! Now logging you in...');
            await handleAuth('login');
        } else if (type === 'login') {
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch(`${API_BASE_URL}/auth/token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData.toString()
            });
            const data = await handleResponse(response);
            localStorage.setItem('token', data.access_token);
            
            const userResponse = await fetch(`${API_BASE_URL}/users/me`, {
                headers: { 'Authorization': `Bearer ${data.access_token}` }
            });
            const userData = await handleResponse(userResponse);
            localStorage.setItem('role', userData.role);
            checkAuthStatus();
        }
    } catch (error) {
        console.error('Auth error:', error);
        showToast('Auth failed: ' + error.message, 'error');
    }
}

document.getElementById('create-assignment-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const title = document.getElementById('assignment-title').value;
    const description = document.getElementById('assignment-description').value;
    const due_date = document.getElementById('assignment-due-date').value;

    try {
        const response = await fetch(`${API_BASE_URL}/assignments/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ title, description, due_date })
        });
        await handleResponse(response);
        document.getElementById('create-assignment-form').reset();
        await fetchTeacherAssignments();
        showToast('Assignment created successfully!');
    } catch (error) {
        console.error('Create assignment error:', error);
        showToast(error.message, 'error');
    }
});

async function fetchTeacherAssignments() {
    const list = document.getElementById('teacher-assignments-list');
    list.innerHTML = '<h4>Loading...</h4>';

    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/assignments/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const assignments = await handleResponse(response);
        list.innerHTML = '';
        if (assignments.length === 0) {
            list.innerHTML = '<p>No assignments found.</p>';
        } else {
            assignments.forEach(assignment => {
                const card = document.createElement('div');
                card.className = 'assignment-card';
                card.innerHTML = `
                    <h4>${assignment.title}</h4>
                    <p>${assignment.description}</p>
                    <p>Due: ${new Date(assignment.due_date).toLocaleDateString()}</p>
                    <button onclick="viewSubmissions(${assignment.id}, this)">View Submissions</button>
                    <div id="submissions-for-${assignment.id}" style="display: none;"></div>
                `;
                list.appendChild(card);
            });
        }
    } catch (error) {
        console.error('Fetch assignments error:', error);
        list.innerHTML = `<h4>Failed to load assignments: ${error.message}</h4>`;
    }
}

async function viewSubmissions(assignmentId, button) {
    const token = localStorage.getItem('token');
    const submissionsDiv = document.getElementById(`submissions-for-${assignmentId}`);
    if (submissionsDiv.style.display === 'block') {
        submissionsDiv.style.display = 'none';
        button.textContent = 'View Submissions';
        return;
    }
    
    button.textContent = 'Loading...';
    submissionsDiv.style.display = 'block';

    try {
        const response = await fetch(`${API_BASE_URL}/assignments/${assignmentId}/submissions`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const submissions = await handleResponse(response);
        
        submissionsDiv.innerHTML = '<h5>Submissions:</h5>';
        if (submissions.length === 0) {
            submissionsDiv.innerHTML += '<p>No submissions yet.</p>';
        } else {
            submissions.forEach(sub => {
                const subCard = document.createElement('div');
                subCard.className = 'submission-card';
                subCard.innerHTML = `
                    <p><strong>Student ID:</strong> ${sub.student_id}</p>
                    <p><strong>Text:</strong> ${sub.submission_text}</p>
                    <p><strong>File:</strong> ${sub.submission_file ? `<a href="${'http://127.0.0.1:8000/' + sub.submission_file}" target="_blank">Download</a>` : 'None'}</p>
                    <small>Submitted at: ${new Date(sub.submitted_at).toLocaleString()}</small>
                `;
                submissionsDiv.appendChild(subCard);
            });
        }
        button.textContent = 'Hide Submissions';
    } catch (error) {
        console.error('View submissions error:', error);
        showToast(error.message, 'error');
        button.textContent = 'View Submissions';
        submissionsDiv.style.display = 'none';
    }
}

async function fetchStudentAssignments() {
    const list = document.getElementById('student-assignments-list');
    list.innerHTML = '<h4>Loading...</h4>';

    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/assignments/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const assignments = await handleResponse(response);
        list.innerHTML = '';
        if (assignments.length === 0) {
            list.innerHTML = '<p>No assignments found.</p>';
        } else {
            assignments.forEach(assignment => {
                const card = document.createElement('div');
                card.className = 'assignment-card';
                card.innerHTML = `
                    <h4>${assignment.title}</h4>
                    <p>${assignment.description}</p>
                    <p>Due: ${new Date(assignment.due_date).toLocaleDateString()}</p>
                    <button onclick="openSubmissionModal(${assignment.id}, '${assignment.title}')">Submit</button>
                `;
                list.appendChild(card);
            });
        }
    } catch (error) {
        console.error('Fetch assignments error:', error);
        list.innerHTML = `<h4>Failed to load assignments: ${error.message}</h4>`;
    }
}

let currentAssignmentId;

function openSubmissionModal(assignmentId, assignmentTitle) {
    currentAssignmentId = assignmentId;
    document.getElementById('modal-assignment-title').textContent = `Assignment: ${assignmentTitle}`;
    document.getElementById('submission-modal').style.display = 'flex';
}

document.querySelector('.close-button').addEventListener('click', () => {
    document.getElementById('submission-modal').style.display = 'none';
});

document.getElementById('submit-assignment-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const submissionText = document.getElementById('submission-text').value;
    const submissionFile = document.getElementById('submission-file').files[0];

    const formData = new FormData();
    formData.append('submission_text', submissionText);
    if (submissionFile) {
        formData.append('submission_file', submissionFile);
    }

    try {
        const response = await fetch(`${API_BASE_URL}/assignments/${currentAssignmentId}/submit`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });
        
        const data = await handleResponse(response);
        
        showToast(data.message);
        document.getElementById('submission-modal').style.display = 'none';
        document.getElementById('submit-assignment-form').reset();
    } catch (error) {
        console.error('Submission error:', error);
        showToast(error.message, 'error');
    }
});