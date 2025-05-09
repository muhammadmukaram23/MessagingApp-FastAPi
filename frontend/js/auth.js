class Auth {
    constructor() {
        this.token = localStorage.getItem('token') || 'mysecrettoken123'; // Default token
        this.userId = localStorage.getItem('userId');
        this.username = localStorage.getItem('username');
        this.email = localStorage.getItem('email');
        this.apiBaseUrl = 'http://127.0.0.1:8001';
        
        this.setupAuthUI();
    }

    setupAuthUI() {
        // Toggle between login and register forms
        const loginToggle = document.getElementById('loginToggle');
        const registerToggle = document.getElementById('registerToggle');
        const loginFormContainer = document.getElementById('loginFormContainer');
        const registerFormContainer = document.getElementById('registerFormContainer');

        loginToggle.addEventListener('click', () => {
            loginToggle.classList.add('active');
            registerToggle.classList.remove('active');
            loginFormContainer.classList.remove('d-none');
            registerFormContainer.classList.add('d-none');
        });

        registerToggle.addEventListener('click', () => {
            registerToggle.classList.add('active');
            loginToggle.classList.remove('active');
            registerFormContainer.classList.remove('d-none');
            loginFormContainer.classList.add('d-none');
        });

        // Login form handler
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleLogin();
        });

        // Register form handler
        document.getElementById('registerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleRegister();
        });
    }

    async handleLogin() {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const formData = new FormData();
            formData.append('email', email);
            formData.append('password', password);

            const response = await fetch(`${this.apiBaseUrl}/login/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                },
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Login failed');
            }

            const data = await response.json();
            this.setUserData(data);
            this.showMainApp();
        } catch (error) {
            alert(error.message || 'Login failed. Please check your credentials.');
        }
    }

    async handleRegister() {
        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;

        try {
            const response = await fetch(`${this.apiBaseUrl}/users/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Registration failed');
            }

            // After successful registration, log the user in
            await this.handleLogin();
        } catch (error) {
            alert(error.message || 'Registration failed. Please try again.');
        }
    }

    setUserData(data) {
        this.userId = data.user_id;
        this.username = data.username;
        this.email = data.email;

        // Store in localStorage
        localStorage.setItem('userId', this.userId);
        localStorage.setItem('username', this.username);
        localStorage.setItem('email', this.email);
    }

    showMainApp() {
        // Update UI
        document.getElementById('userName').textContent = this.username;
        document.getElementById('userEmail').textContent = this.email;
        
        // Show main app and hide auth section
        document.getElementById('authSection').classList.add('d-none');
        document.getElementById('mainApp').classList.remove('d-none');
        
        // Initialize contacts and messages
        contacts.loadContacts();
        messages.startPolling();
    }

    logout() {
        this.userId = null;
        this.username = null;
        this.email = null;

        localStorage.removeItem('userId');
        localStorage.removeItem('username');
        localStorage.removeItem('email');

        // Show auth section and hide main app
        document.getElementById('authSection').classList.remove('d-none');
        document.getElementById('mainApp').classList.add('d-none');
    }

    isAuthenticated() {
        return !!this.userId;
    }

    getAuthHeader() {
        return {
            'Authorization': `Bearer ${this.token}`
        };
    }
}

// Initialize auth
const auth = new Auth(); 