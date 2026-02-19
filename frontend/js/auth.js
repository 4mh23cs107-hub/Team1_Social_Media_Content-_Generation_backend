const API_BASE = "http://127.0.0.1:8000";

// Handle Login
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const btn = document.getElementById('loginBtn');
        const loader = document.getElementById('loginLoader');
        const errorDiv = document.getElementById('loginError');

        btn.disabled = true;
        loader.classList.remove('hidden');
        errorDiv.textContent = '';

        try {
            const response = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('userEmail', email);
                window.location.href = 'dashboard.html';
            } else {
                errorDiv.textContent = data.detail || 'Login failed. Please check your credentials.';
            }
        } catch (err) {
            errorDiv.textContent = 'Network error. Is the backend running?';
        } finally {
            btn.disabled = false;
            loader.classList.add('hidden');
        }
    });
}

// Handle Signup
if (document.getElementById('signupForm')) {
    document.getElementById('signupForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const full_name = document.getElementById('fullName').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const btn = document.getElementById('signupBtn');
        const loader = document.getElementById('signupLoader');
        const errorDiv = document.getElementById('signupError');

        btn.disabled = true;
        loader.classList.remove('hidden');
        errorDiv.textContent = '';

        try {
            const response = await fetch(`${API_BASE}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ full_name, email, password })
            });

            const data = await response.json();

            if (response.ok) {
                // Auto login after signup
                const loginRes = await fetch(`${API_BASE}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const loginData = await loginRes.json();
                localStorage.setItem('token', loginData.access_token);
                localStorage.setItem('userEmail', email);
                window.location.href = 'dashboard.html';
            } else {
                errorDiv.textContent = data.detail || 'Registration failed.';
            }
        } catch (err) {
            errorDiv.textContent = 'Network error. Is the backend running?';
        } finally {
            btn.disabled = false;
            loader.classList.add('hidden');
        }
    });
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    window.location.href = 'login.html';
}
