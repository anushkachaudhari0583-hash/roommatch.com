// Mobile Navigation Toggle
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    navToggle.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
    });
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar background change on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    const animateElements = document.querySelectorAll('.problem-card, .objective-card, .audience-card, .strategy-card, .step');
    animateElements.forEach(el => {
        observer.observe(el);
    });
});

// Button click animations
document.querySelectorAll('.btn-primary, .btn-secondary').forEach(button => {
    button.addEventListener('click', function(e) {
        // Create ripple effect
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Add ripple effect styles
const style = document.createElement('style');
style.textContent = `
    .btn-primary, .btn-secondary {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    const heroBg = document.querySelector('.hero-bg');
    
    if (hero && heroBg) {
        heroBg.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Counter animation for statistics (if you want to add them later)
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    }
    
    updateCounter();
}

// Typing effect for hero title (optional enhancement)
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Initialize typing effect on page load
document.addEventListener('DOMContentLoaded', () => {
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const originalText = heroTitle.textContent;
        // Uncomment the line below to enable typing effect
        // typeWriter(heroTitle, originalText, 50);
    }
});

// Form validation (for future contact forms)
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Add loading animation
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// Add loaded class styles
const loadedStyle = document.createElement('style');
loadedStyle.textContent = `
    body {
        opacity: 0;
        transition: opacity 0.5s ease-in-out;
    }
    
    body.loaded {
        opacity: 1;
    }
`;
document.head.appendChild(loadedStyle);

// Floating cards animation enhancement
document.addEventListener('DOMContentLoaded', () => {
    const floatingCards = document.querySelectorAll('.floating-card');
    
    floatingCards.forEach((card, index) => {
        // Add random delay to make animation more natural
        card.style.animationDelay = `${index * 0.5}s`;
        
        // Add hover effect
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.05)';
            card.style.transition = 'transform 0.3s ease';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Smooth reveal animation for sections
const revealElements = document.querySelectorAll('section');
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
});

revealElements.forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(30px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    revealObserver.observe(element);
});

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// API Helper Functions
const api = {
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'API request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    async register(userData) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },
    
    async login(email, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    },
    
    async joinWaitlist(email) {
        return this.request('/waitlist', {
            method: 'POST',
            body: JSON.stringify({ email })
        });
    },
    
    async getProfile(token) {
        return this.request('/profile', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
    },
    
    async createProfile(profileData, token) {
        return this.request('/profile', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(profileData)
        });
    }
};

// Authentication state
let currentUser = null;
let authToken = null;

// Load saved authentication
function loadAuth() {
    const savedToken = localStorage.getItem('roommatch_token');
    const savedUser = localStorage.getItem('roommatch_user');
    
    if (savedToken && savedUser) {
        authToken = savedToken;
        currentUser = JSON.parse(savedUser);
        updateUIForLoggedInUser();
    }
}

// Save authentication
function saveAuth(token, user) {
    authToken = token;
    currentUser = user;
    localStorage.setItem('roommatch_token', token);
    localStorage.setItem('roommatch_user', JSON.stringify(user));
}

// Clear authentication
function clearAuth() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('roommatch_token');
    localStorage.removeItem('roommatch_user');
    updateUIForLoggedOutUser();
}

// Update UI for logged in user
function updateUIForLoggedInUser() {
    const heroButtons = document.querySelector('.hero-buttons');
    if (heroButtons && currentUser) {
        heroButtons.innerHTML = `
            <button class="btn-primary" onclick="goToProfile()">Complete Profile</button>
            <button class="btn-secondary" onclick="logout()">Logout</button>
        `;
    }
}

// Update UI for logged out user
function updateUIForLoggedOutUser() {
    const heroButtons = document.querySelector('.hero-buttons');
    if (heroButtons) {
        heroButtons.innerHTML = `
            <button class="btn-primary" onclick="showLoginModal()">Find Your Match</button>
            <button class="btn-secondary" onclick="showWaitlistModal()">Join Waitlist</button>
        `;
    }
}

// Show login modal
function showLoginModal() {
    const modal = createModal(`
        <div class="auth-modal">
            <h2>Welcome to Roommatch</h2>
            <div class="auth-tabs">
                <button class="tab-btn active" onclick="switchTab('login')">Login</button>
                <button class="tab-btn" onclick="switchTab('register')">Register</button>
            </div>
            <div id="login-form" class="auth-form">
                <input type="email" id="login-email" placeholder="Email" required>
                <input type="password" id="login-password" placeholder="Password" required>
                <button class="btn-primary" onclick="handleLogin()">Login</button>
            </div>
            <div id="register-form" class="auth-form" style="display: none;">
                <input type="text" id="register-firstname" placeholder="First Name" required>
                <input type="text" id="register-lastname" placeholder="Last Name" required>
                <input type="email" id="register-email" placeholder="Email" required>
                <input type="password" id="register-password" placeholder="Password" required>
                <input type="tel" id="register-phone" placeholder="Phone (optional)">
                <button class="btn-primary" onclick="handleRegister()">Register</button>
            </div>
        </div>
    `);
    document.body.appendChild(modal);
}

// Show waitlist modal
function showWaitlistModal() {
    const modal = createModal(`
        <div class="waitlist-modal">
            <h2>Join Our Waitlist</h2>
            <p>Be the first to know when Roommatch launches!</p>
            <input type="email" id="waitlist-email" placeholder="Enter your email" required>
            <button class="btn-primary" onclick="handleWaitlist()">Join Waitlist</button>
        </div>
    `);
    document.body.appendChild(modal);
}

// Create modal
function createModal(content) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            ${content}
        </div>
    `;
    
    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    return modal;
}

// Close modal
function closeModal() {
    const modal = document.querySelector('.modal-overlay');
    if (modal) {
        modal.remove();
    }
}

// Switch between login and register tabs
function switchTab(tab) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const tabs = document.querySelectorAll('.tab-btn');
    
    tabs.forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    
    if (tab === 'login') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    }
}

// Handle login
async function handleLogin() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    if (!email || !password) {
        alert('Please fill in all fields');
        return;
    }
    
    try {
        const response = await api.login(email, password);
        saveAuth(response.access_token, response.user);
        closeModal();
        showSuccessMessage('Login successful! Welcome to Roommatch.');
    } catch (error) {
        alert('Login failed: ' + error.message);
    }
}

// Handle registration
async function handleRegister() {
    const firstname = document.getElementById('register-firstname').value;
    const lastname = document.getElementById('register-lastname').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const phone = document.getElementById('register-phone').value;
    
    if (!firstname || !lastname || !email || !password) {
        alert('Please fill in all required fields');
        return;
    }
    
    try {
        const response = await api.register({
            first_name: firstname,
            last_name: lastname,
            email: email,
            password: password,
            phone: phone
        });
        saveAuth(response.access_token, response.user);
        closeModal();
        showSuccessMessage('Registration successful! Welcome to Roommatch.');
    } catch (error) {
        alert('Registration failed: ' + error.message);
    }
}

// Handle waitlist signup
async function handleWaitlist() {
    const email = document.getElementById('waitlist-email').value;
    
    if (!email) {
        alert('Please enter your email');
        return;
    }
    
    try {
        await api.joinWaitlist(email);
        closeModal();
        showSuccessMessage('Successfully joined the waitlist! We\'ll notify you when Roommatch launches.');
    } catch (error) {
        alert('Waitlist signup failed: ' + error.message);
    }
}

// Show success message
function showSuccessMessage(message) {
    const notification = document.createElement('div');
    notification.className = 'success-notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Go to profile (placeholder)
function goToProfile() {
    alert('Profile management coming soon! Complete your profile to start matching.');
}

// Logout
function logout() {
    clearAuth();
    showSuccessMessage('Logged out successfully');
}

// Add click handlers for CTA buttons
document.querySelectorAll('.btn-primary').forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Add your signup/matching logic here
        if (button.textContent.includes('Find Your Match')) {
            if (currentUser) {
                goToProfile();
            } else {
                showLoginModal();
            }
        } else if (button.textContent.includes('Join Waitlist')) {
            showWaitlistModal();
        } else if (button.textContent.includes('Try Roommatch Beta')) {
            if (currentUser) {
                goToProfile();
            } else {
                showLoginModal();
            }
        }
    });
});

// Initialize authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    loadAuth();
});

// Add hover effects for cards
document.querySelectorAll('.problem-card, .objective-card, .audience-card, .strategy-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.15)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.1)';
    });
});

// Add scroll progress indicator (optional)
function createScrollProgress() {
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, #8B5CF6, #A855F7);
        z-index: 9999;
        transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset;
        const docHeight = document.body.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        progressBar.style.width = scrollPercent + '%';
    });
}

// Initialize scroll progress
createScrollProgress();
