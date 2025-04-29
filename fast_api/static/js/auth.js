/**
 * Authentication module for handling user login
 * API Endpoint: https://keidotapi.azurewebsites.net/api/Login/login
 */
document.addEventListener('DOMContentLoaded', function() {
    // References to DOM elements
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const loginButton = document.getElementById('loginButton');
    const loginSpinner = document.getElementById('loginSpinner');
    const loginIcon = document.getElementById('loginIcon');
    const loginAlert = document.getElementById('loginAlert');

    // Check if user is already logged in
    checkAuthStatus();

    // Add event listener for form submission
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    /**
     * Handles the login form submission
     * @param {Event} event - The form submission event
     */
    async function handleLogin(event) {
        event.preventDefault();
        
        // Hide any previous alerts and show loading state
        setLoading(true);
        hideAlert();
        
        // Validate form
        if (!validateForm()) {
            setLoading(false);
            return;
        }
        
        // Get form data
        const email = emailInput.value.trim();
        const password = passwordInput.value;
        
        try {
            // Make API request
            const response = await fetch('https://keidotapi.azurewebsites.net/api/Login/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });
            
            // Process response
            if (!response.ok) {
                throw new Error(`Error de autenticación (${response.status})`);
            }
            
            const data = await response.json();
            
            // Check for error in response data
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Store authentication data
            storeAuthData(data);
            
            // Show success message and redirect
            showAlert('Inicio de sesión exitoso. Redirigiendo...', 'success');
            
            // Redirect after a small delay
            setTimeout(() => {
                if (data.is_worker) {
                    window.location.href = '/dashboard';  // Redirect to dashboard after login
                } else {
                    window.location.href = '/payment-page';  // Redirect to payment page for regular users
                }
            }, 1500);
            
        } catch (error) {
            console.error('Error de inicio de sesión:', error);
            showAlert(error.message || 'Error al iniciar sesión. Por favor intente nuevamente.', 'danger');
            setLoading(false);
        }
    }
    
    /**
     * Validate form inputs
     * @returns {boolean} - True if form is valid, false otherwise
     */
    function validateForm() {
        let isValid = true;
        
        // Validate email
        if (!emailInput.value.trim()) {
            emailInput.classList.add('is-invalid');
            isValid = false;
        } else {
            emailInput.classList.remove('is-invalid');
        }
        
        // Validate password
        if (!passwordInput.value) {
            passwordInput.classList.add('is-invalid');
            isValid = false;
        } else {
            passwordInput.classList.remove('is-invalid');
        }
        
        return isValid;
    }
    
    /**
     * Store authentication data in local storage
     * @param {Object} data - The authentication data
     */
    function storeAuthData(data) {
        localStorage.setItem('auth_token', data.token);
        localStorage.setItem('user_id', data.id);
        localStorage.setItem('user_name', data.name);
        localStorage.setItem('is_worker', data.is_worker);
        localStorage.setItem('token_expiration', data.expiration);
    }
    
    /**
     * Check if user is already logged in and redirect if necessary
     */
    function checkAuthStatus() {
        const token = localStorage.getItem('auth_token');
        const expiration = localStorage.getItem('token_expiration');
        
        if (token && expiration) {
            // Check if token is still valid
            const expirationDate = new Date(expiration);
            const now = new Date();
            
            if (expirationDate > now) {
                // Token is still valid, redirect to appropriate page
                const isWorker = localStorage.getItem('is_worker') === 'true';
                
                // Only redirect if on login page
                if (window.location.pathname === '/login' || window.location.pathname === '/') {
                    if (isWorker) {
                        window.location.href = '/dashboard';
                    } else {
                        window.location.href = '/payment-page';
                    }
                }
            } else {
                // Token expired, clear storage
                clearAuthData();
            }
        }
    }
    
    /**
     * Clear authentication data from local storage
     */
    function clearAuthData() {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_id');
        localStorage.removeItem('user_name');
        localStorage.removeItem('is_worker');
        localStorage.removeItem('token_expiration');
    }
    
    /**
     * Show an alert message
     * @param {string} message - The message to display
     * @param {string} type - The type of alert (success, danger, warning, info)
     */
    function showAlert(message, type = 'danger') {
        loginAlert.textContent = message;
        loginAlert.className = `alert alert-${type}`;
        loginAlert.classList.remove('d-none');
    }
    
    /**
     * Hide the alert message
     */
    function hideAlert() {
        loginAlert.classList.add('d-none');
    }
    
    /**
     * Set loading state for the login button
     * @param {boolean} isLoading - Whether the form is in a loading state
     */
    function setLoading(isLoading) {
        if (isLoading) {
            loginButton.disabled = true;
            loginSpinner.classList.remove('d-none');
            loginIcon.classList.add('d-none');
        } else {
            loginButton.disabled = false;
            loginSpinner.classList.add('d-none');
            loginIcon.classList.remove('d-none');
        }
    }

    // Expose functions for potential use by other scripts
    window.authModule = {
        logout: function() {
            clearAuthData();
            window.location.href = '/';  // Redirect to root (login page)
        },
        getToken: function() {
            return localStorage.getItem('auth_token');
        },
        getUserId: function() {
            return localStorage.getItem('user_id');
        },
        getUserName: function() {
            return localStorage.getItem('user_name');
        },
        isAuthenticated: function() {
            const token = localStorage.getItem('auth_token');
            const expiration = localStorage.getItem('token_expiration');
            
            if (token && expiration) {
                const expirationDate = new Date(expiration);
                const now = new Date();
                return expirationDate > now;
            }
            
            return false;
        },
        isWorker: function() {
            return localStorage.getItem('is_worker') === 'true';
        }
    };
});