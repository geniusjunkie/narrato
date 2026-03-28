# Embedded frontend HTML (no external file needed)
FRONTEND_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Narrato — AI Video Voiceover</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-tertiary: #1a1a25;
            --accent-primary: #6366f1;
            --accent-secondary: #8b5cf6;
            --accent-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
            --text-primary: #fafafa;
            --text-secondary: #a1a1aa;
            --text-muted: #71717a;
            --success: #22c55e;
            --error: #ef4444;
            --border: rgba(255, 255, 255, 0.1);
            --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.3);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
        }
        .bg-gradient {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            z-index: -1;
            background: 
                radial-gradient(ellipse 80% 50% at 20% 40%, rgba(99, 102, 241, 0.15), transparent),
                radial-gradient(ellipse 60% 40% at 80% 60%, rgba(139, 92, 246, 0.1), transparent);
        }
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.5rem 3rem;
            border-bottom: 1px solid var(--border);
        }
        .logo {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.75rem;
            font-weight: 700;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .nav-auth {
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        .user-info {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: var(--text-secondary);
            font-size: 0.875rem;
        }
        .user-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: var(--accent-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.75rem;
            color: white;
        }
        .btn-nav {
            background: transparent;
            color: var(--text-secondary);
            border: 1px solid var(--border);
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 500;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-nav:hover {
            border-color: var(--accent-primary);
            color: var(--text-primary);
        }
        .hero {
            text-align: center;
            padding: 5rem 2rem 3rem;
            max-width: 900px;
            margin: 0 auto;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.3);
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            font-size: 0.875rem;
            color: var(--accent-primary);
            margin-bottom: 1.5rem;
        }
        .badge::before {
            content: '';
            width: 8px; height: 8px;
            background: var(--success);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .hero h1 {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 1.5rem;
        }
        .hero h1 span {
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .hero p {
            font-size: 1.25rem;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto 2rem;
        }
        .app-container {
            max-width: 800px;
            margin: 0 auto 4rem;
            padding: 0 2rem;
        }
        .auth-section {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 2.5rem;
            margin: 2rem auto;
            max-width: 400px;
            display: none;
        }
        .auth-section.active { display: block; }
        .auth-tabs {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 1rem;
        }
        .auth-tab {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 0.9375rem;
            font-weight: 500;
            padding: 0.5rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .auth-tab.active {
            color: var(--text-primary);
            border-bottom: 2px solid var(--accent-primary);
        }
        .auth-form {
            display: none;
        }
        .auth-form.active { display: block; }
        .form-group {
            margin-bottom: 1rem;
        }
        .form-group label {
            display: block;
            font-size: 0.875rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
        }
        .form-group input {
            width: 100%;
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            font-size: 0.9375rem;
        }
        .form-group input:focus {
            outline: none;
            border-color: var(--accent-primary);
        }
        .btn-primary {
            width: 100%;
            background: var(--accent-gradient);
            color: white;
            border: none;
            padding: 0.875rem;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 0.9375rem;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        .btn-primary:hover { opacity: 0.9; }
        .btn-primary:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .upload-zone {
            background: var(--bg-secondary);
            border: 2px dashed var(--border);
            border-radius: 1.5rem;
            padding: 3rem;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .upload-zone:hover, .upload-zone.dragover {
            border-color: var(--accent-primary);
            transform: translateY(-2px);
        }
        .upload-zone input { display: none; }
        .upload-icon {
            width: 80px; height: 80px;
            background: var(--bg-tertiary);
            border-radius: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.5rem;
            font-size: 2.5rem;
        }
        .upload-zone h3 { font-size: 1.25rem; margin-bottom: 0.5rem; }
        .upload-zone p { color: var(--text-muted); font-size: 0.875rem; }
        .settings-panel {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 1.5rem;
            margin-top: 1.5rem;
        }
        .settings-panel h4 {
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 1rem;
        }
        .settings-panel select {
            width: 100%;
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            font-size: 0.875rem;
            cursor: pointer;
        }
        .progress-section {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 2rem;
            margin-top: 1.5rem;
            display: none;
        }
        .progress-section.active { display: block; }
        .progress-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        .spinner {
            width: 20px; height: 20px;
            border: 2px solid var(--border);
            border-top-color: var(--accent-primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .progress-bar-container {
            background: var(--bg-tertiary);
            border-radius: 0.5rem;
            height: 8px;
            overflow: hidden;
            margin-bottom: 1rem;
        }
        .progress-bar {
            height: 100%;
            background: var(--accent-gradient);
            border-radius: 0.5rem;
            transition: width 0.5s ease;
            width: 0%;
        }
        .script-section {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 2rem;
            margin-top: 1.5rem;
            display: none;
        }
        .script-section.active { display: block; }
        .script-editor {
            width: 100%;
            min-height: 200px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            padding: 1rem;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            font-size: 0.9375rem;
            line-height: 1.6;
            resize: vertical;
            margin-bottom: 1rem;
        }
        .script-editor:focus {
            outline: none;
            border-color: var(--accent-primary);
        }
        .result-section {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 2rem;
            margin-top: 1.5rem;
            text-align: center;
            display: none;
        }
        .result-section.active { display: block; }
        .btn-group {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        .btn-secondary {
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border: 1px solid var(--border);
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
        }
        .btn-success {
            background: var(--success);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        .error-message {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid var(--error);
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 1rem;
            color: var(--error);
            font-size: 0.875rem;
            display: none;
        }
        .error-message.active { display: block; }
        .success-message {
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid var(--success);
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 1rem;
            color: var(--success);
            font-size: 0.875rem;
            display: none;
        }
        .success-message.active { display: block; }
        .login-prompt {
            text-align: center;
            padding: 3rem 2rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 1rem;
            margin: 2rem 0;
        }
        .login-prompt h3 {
            margin-bottom: 0.5rem;
            font-family: 'Space Grotesk', sans-serif;
        }
        .login-prompt p {
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
        }
        footer {
            border-top: 1px solid var(--border);
            padding: 2rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.875rem;
        }
    </style>
</head>
<body>
    <div class="bg-gradient"></div>
    <nav>
        <div class="logo">Narrato</div>
        <div class="nav-auth" id="navAuth">
            <!-- Auth buttons injected by JS -->
        </div>
    </nav>
    
    <section class="hero">
        <div class="badge">Free • No Credit Card Required</div>
        <h1>Turn Silent Videos Into <span>Professional Narrations</span></h1>
        <p>Upload your screen recording. Our AI analyzes the video, writes a script, and generates a natural voiceover.</p>
    </section>
    
    <main class="app-container">
        <!-- Auth Section (Login/Register) -->
        <div class="auth-section" id="authSection">
            <div class="auth-tabs">
                <button class="auth-tab active" data-tab="login">Sign In</button>
                <button class="auth-tab" data-tab="register">Create Account</button>
            </div>
            
            <div class="error-message" id="authError"></div>
            <div class="success-message" id="authSuccess"></div>
            
            <!-- Login Form -->
            <form class="auth-form active" id="loginForm">
                <div class="form-group">
                    <label for="loginEmail">Email</label>
                    <input type="email" id="loginEmail" placeholder="you@example.com" required>
                </div>
                <div class="form-group">
                    <label for="loginPassword">Password</label>
                    <input type="password" id="loginPassword" placeholder="••••••••" required minlength="8">
                </div>
                <button type="submit" class="btn-primary">Sign In</button>
            </form>
            
            <!-- Register Form -->
            <form class="auth-form" id="registerForm">
                <div class="form-group">
                    <label for="registerName">Name (optional)</label>
                    <input type="text" id="registerName" placeholder="Your name">
                </div>
                <div class="form-group">
                    <label for="registerEmail">Email</label>
                    <input type="email" id="registerEmail" placeholder="you@example.com" required>
                </div>
                <div class="form-group">
                    <label for="registerPassword">Password</label>
                    <input type="password" id="registerPassword" placeholder="Min 8 characters" required minlength="8">
                </div>
                <button type="submit" class="btn-primary">Create Account</button>
            </form>
        </div>
        
        <!-- Login Prompt (shown when not authenticated) -->
        <div class="login-prompt" id="loginPrompt">
            <h3>Get Started</h3>
            <p>Sign in or create a free account to start creating AI voiceovers.</p>
            <button class="btn-primary" id="showAuthBtn" style="width: auto; padding: 0.75rem 2rem;">Sign In / Register</button>
        </div>
        
        <!-- Main App (shown when authenticated) -->
        <div id="mainApp" style="display: none;">
            <div class="upload-zone" id="uploadZone">
                <input type="file" id="fileInput" accept="video/mp4,video/quicktime,video/x-msvideo,video/webm">
                <div class="upload-icon">📹</div>
                <h3>Drop your video here</h3>
                <p>or click to browse • MP4, MOV, AVI up to 100MB</p>
            </div>
            
            <div class="settings-panel">
                <h4>Settings</h4>
                <select id="voiceSelect">
                    <option value="en-US-AriaNeural">English (US) — Default</option>
                    <option value="en-GB-SoniaNeural">English (UK)</option>
                    <option value="en-AU-NatashaNeural">English (Australian)</option>
                    <option value="en-IN-NeerjaNeural">English (Indian)</option>
                </select>
                <div class="checkbox-group" style="margin-top: 1.5rem; padding: 1rem; background: var(--bg-tertiary); border-radius: 0.75rem; border: 1px solid var(--border);">
                    <label style="display: flex; align-items: center; gap: 0.75rem; cursor: pointer; color: var(--text-primary); font-size: 0.9375rem; font-weight: 500;">
                        <input type="checkbox" id="subtitlesCheckbox" style="width: 20px; height: 20px; cursor: pointer; accent-color: var(--accent-primary);">
                        <span>Add subtitles to video</span>
                    </label>
                    <p style="margin: 0.5rem 0 0 2rem; color: var(--text-secondary); font-size: 0.8rem; font-weight: normal;">Burn captions directly into your video</p>
                </div>
            </div>
            
            <div class="error-message" id="errorMessage"></div>
            
            <div class="progress-section" id="progressSection">
                <div class="progress-header">
                    <div style="display:flex;align-items:center;gap:0.75rem">
                        <div class="spinner"></div>
                        <span id="statusText">Processing your video...</span>
                    </div>
                    <span id="progressPercent">0%</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-bar" id="progressBar"></div>
                </div>
            </div>
            
            <div class="script-section" id="scriptSection">
                <h3>Review Your Script</h3>
                <p style="color: var(--text-secondary); margin-bottom: 1rem;">AI generated this narration based on your video. Edit it below, then click Generate Voiceover.</p>
                <textarea class="script-editor" id="scriptEditor" placeholder="Your script will appear here..."></textarea>
                <div class="btn-group">
                    <button class="btn-primary" id="generateVoiceoverBtn">Generate Voiceover</button>
                    <button class="btn-secondary" id="cancelBtn">Cancel</button>
                </div>
            </div>
            
            <div class="result-section" id="resultSection">
                <h3>Your video is ready!</h3>
                <p>AI voiceover added successfully</p>
                <div class="btn-group">
                    <a href="#" class="btn-success" id="downloadBtn">Download Video</a>
                    <button class="btn-secondary" id="createAnotherBtn">Create Another</button>
                </div>
            </div>
        </div>
    </main>
    
    <footer>
        <p>Built by Genius Junkie • Powered by Groq AI, Google Gemini, and Google TTS</p>
    </footer>
    
    <script>
        const API_URL = '';
        
        // Auth state
        let authToken = localStorage.getItem('narrato_token');
        let currentUser = null;
        
        // DOM Elements
        const navAuth = document.getElementById('navAuth');
        const authSection = document.getElementById('authSection');
        const loginPrompt = document.getElementById('loginPrompt');
        const mainApp = document.getElementById('mainApp');
        const authTabs = document.querySelectorAll('.auth-tab');
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');
        const authError = document.getElementById('authError');
        const authSuccess = document.getElementById('authSuccess');
        
        // App elements
        const uploadZone = document.getElementById('uploadZone');
        const fileInput = document.getElementById('fileInput');
        const voiceSelect = document.getElementById('voiceSelect');
        const subtitlesCheckbox = document.getElementById('subtitlesCheckbox');
        const progressSection = document.getElementById('progressSection');
        const scriptSection = document.getElementById('scriptSection');
        const resultSection = document.getElementById('resultSection');
        const errorMessage = document.getElementById('errorMessage');
        const progressBar = document.getElementById('progressBar');
        const statusText = document.getElementById('statusText');
        const progressPercent = document.getElementById('progressPercent');
        const scriptEditor = document.getElementById('scriptEditor');
        const generateVoiceoverBtn = document.getElementById('generateVoiceoverBtn');
        const cancelBtn = document.getElementById('cancelBtn');
        const downloadBtn = document.getElementById('downloadBtn');
        const createAnotherBtn = document.getElementById('createAnotherBtn');
        
        let currentJobId = null, pollInterval = null;
        
        // Initialize
        async function init() {
            if (authToken) {
                await loadUser();
            }
            updateUI();
        }
        
        // Load user from token
        async function loadUser() {
            try {
                const response = await fetch(`${API_URL}/auth/me`, {
                    headers: { 'Authorization': `Bearer ${authToken}` }
                });
                if (response.ok) {
                    currentUser = await response.json();
                } else {
                    // Token invalid
                    logout();
                }
            } catch (e) {
                console.error('Failed to load user:', e);
            }
        }
        
        // Update UI based on auth state
        function updateUI() {
            if (currentUser) {
                // Logged in
                navAuth.innerHTML = `
                    <div class="user-info">
                        <div class="user-avatar">${currentUser.name?.[0]?.toUpperCase() || currentUser.email[0].toUpperCase()}</div>
                        <span>${currentUser.name || currentUser.email}</span>
                    </div>
                    <button class="btn-nav" id="logoutBtn">Logout</button>
                `;
                document.getElementById('logoutBtn').addEventListener('click', logout);
                
                loginPrompt.style.display = 'none';
                authSection.classList.remove('active');
                mainApp.style.display = 'block';
            } else {
                // Not logged in
                navAuth.innerHTML = `
                    <button class="btn-nav" id="navLoginBtn">Sign In</button>
                    <button class="btn-primary" id="navRegisterBtn" style="width: auto; padding: 0.5rem 1rem;">Get Started</button>
                `;
                document.getElementById('navLoginBtn').addEventListener('click', () => showAuth('login'));
                document.getElementById('navRegisterBtn').addEventListener('click', () => showAuth('register'));
                
                loginPrompt.style.display = 'block';
                authSection.classList.remove('active');
                mainApp.style.display = 'none';
            }
        }
        
        // Show auth section
        function showAuth(tab) {
            loginPrompt.style.display = 'none';
            authSection.classList.add('active');
            switchAuthTab(tab);
        }
        
        // Switch auth tabs
        function switchAuthTab(tab) {
            authTabs.forEach(t => {
                t.classList.toggle('active', t.dataset.tab === tab);
            });
            if (tab === 'login') {
                loginForm.classList.add('active');
                registerForm.classList.remove('active');
            } else {
                loginForm.classList.remove('active');
                registerForm.classList.add('active');
            }
            hideAuthMessages();
        }
        
        // Auth tab click handlers
        authTabs.forEach(tab => {
            tab.addEventListener('click', () => switchAuthTab(tab.dataset.tab));
        });
        
        // Show auth prompt button
        document.getElementById('showAuthBtn').addEventListener('click', () => showAuth('login'));
        
        // Hide auth messages
        function hideAuthMessages() {
            authError.classList.remove('active');
            authSuccess.classList.remove('active');
        }
        
        // Show auth error
        function showAuthError(msg) {
            authError.textContent = msg;
            authError.classList.add('active');
            authSuccess.classList.remove('active');
        }
        
        // Show auth success
        function showAuthSuccess(msg) {
            authSuccess.textContent = msg;
            authSuccess.classList.add('active');
            authError.classList.remove('active');
        }
        
        // Login handler
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAuthMessages();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            try {
                const response = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    authToken = data.token;
                    currentUser = data.user;
                    localStorage.setItem('narrato_token', authToken);
                    showAuthSuccess('Login successful!');
                    setTimeout(() => {
                        updateUI();
                        resetApp();
                    }, 500);
                } else {
                    showAuthError(data.message || 'Login failed');
                }
            } catch (e) {
                showAuthError('Network error. Please try again.');
            }
        });
        
        // Register handler
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAuthMessages();
            
            const name = document.getElementById('registerName').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            
            try {
                const response = await fetch(`${API_URL}/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, password })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    authToken = data.token;
                    currentUser = data.user;
                    localStorage.setItem('narrato_token', authToken);
                    showAuthSuccess('Account created successfully!');
                    setTimeout(() => {
                        updateUI();
                        resetApp();
                    }, 500);
                } else {
                    showAuthError(data.message || 'Registration failed');
                }
            } catch (e) {
                showAuthError('Network error. Please try again.');
            }
        });
        
        // Logout
        function logout() {
            authToken = null;
            currentUser = null;
            localStorage.removeItem('narrato_token');
            updateUI();
            resetApp();
        }
        
        // Reset app state
        function resetApp() {
            clearInterval(pollInterval);
            currentJobId = null;
            fileInput.value = '';
            scriptEditor.value = '';
            subtitlesCheckbox.checked = false;
            progressSection.classList.remove('active');
            scriptSection.classList.remove('active');
            resultSection.classList.remove('active');
            uploadZone.style.display = 'block';
            document.querySelector('.settings-panel').style.display = 'block';
            progressBar.style.width = '0%';
            progressPercent.textContent = '0%';
            hideError();
        }
        
        // File upload handling
        uploadZone.addEventListener('click', () => fileInput.click());
        uploadZone.addEventListener('dragover', (e) => { e.preventDefault(); uploadZone.classList.add('dragover'); });
        uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault(); uploadZone.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
        });
        fileInput.addEventListener('change', (e) => { if (e.target.files.length > 0) handleFile(e.target.files[0]); });
        
        generateVoiceoverBtn.addEventListener('click', submitScript);
        cancelBtn.addEventListener('click', resetApp);
        createAnotherBtn.addEventListener('click', resetApp);
        
        function handleFile(file) {
            const allowedTypes = ['video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/webm'];
            if (!allowedTypes.includes(file.type)) { showError('Invalid file type. Please upload MP4, MOV, AVI, or WebM.'); return; }
            if (file.size > 100 * 1024 * 1024) { showError('File too large. Maximum size is 100MB.'); return; }
            hideError(); uploadFile(file);
        }
        
        async function uploadFile(file) {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('voice', voiceSelect.value);
            formData.append('num_frames', '5');
            formData.append('add_subtitles', subtitlesCheckbox.checked);
            progressSection.classList.add('active');
            uploadZone.style.display = 'none';
            document.querySelector('.settings-panel').style.display = 'none';
            scriptSection.classList.remove('active');
            try {
                const response = await fetch(`${API_URL}/upload`, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${authToken}` },
                    body: formData
                });
                if (!response.ok) { 
                    if (response.status === 401) {
                        logout();
                        showError('Session expired. Please sign in again.');
                        return;
                    }
                    const error = await response.json(); 
                    throw new Error(error.detail || 'Upload failed'); 
                }
                const data = await response.json();
                currentJobId = data.job_id;
                pollInterval = setInterval(() => checkStatus(currentJobId), 500);
            } catch (error) { showError(error.message); resetApp(); }
        }
        
        async function checkStatus(jobId) {
            try {
                const response = await fetch(`${API_URL}/status/${jobId}`, {
                    headers: { 'Authorization': `Bearer ${authToken}` }
                });
                const data = await response.json();
                updateProgress(data);
                
                if (data.status === 'waiting_for_approval') {
                    clearInterval(pollInterval);
                    showScriptEditor(data.script);
                }
                else if (data.status === 'completed') { 
                    clearInterval(pollInterval); 
                    showResult(jobId); 
                }
                else if (data.status === 'failed') { 
                    clearInterval(pollInterval); 
                    showError(data.error || 'Processing failed'); 
                    resetApp(); 
                }
            } catch (error) { console.error('Status check failed:', error); }
        }
        
        function updateProgress(data) {
            const progress = data.progress || 0;
            progressBar.style.width = `${progress}%`;
            progressPercent.textContent = `${progress}%`;
            statusText.textContent = data.message || 'Processing...';
        }
        
        function showScriptEditor(script) {
            progressSection.classList.remove('active');
            scriptSection.classList.add('active');
            scriptEditor.value = script || '';
        }
        
        async function submitScript() {
            if (!currentJobId) return;
            
            const script = scriptEditor.value.trim();
            if (!script) {
                showError('Please enter a script before generating voiceover.');
                return;
            }
            
            hideError();
            generateVoiceoverBtn.disabled = true;
            generateVoiceoverBtn.textContent = 'Submitting...';
            
            try {
                const response = await fetch(`${API_URL}/approve-script/${currentJobId}`, {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authToken}`
                    },
                    body: JSON.stringify({ script: script })
                });
                
                if (!response.ok) { 
                    if (response.status === 401) {
                        logout();
                        showError('Session expired. Please sign in again.');
                        return;
                    }
                    const error = await response.json(); 
                    throw new Error(error.detail || 'Failed to submit script'); 
                }
                
                scriptSection.classList.remove('active');
                progressSection.classList.add('active');
                pollInterval = setInterval(() => checkStatus(currentJobId), 500);
            } catch (error) { 
                showError(error.message); 
            } finally {
                generateVoiceoverBtn.disabled = false;
                generateVoiceoverBtn.textContent = 'Generate Voiceover';
            }
        }
        
        function showResult(jobId) {
            progressSection.classList.remove('active');
            scriptSection.classList.remove('active');
            resultSection.classList.add('active');
            
            // Store job ID for download
            downloadBtn.dataset.jobId = jobId;
        }
        
        // Handle download with auth header
        downloadBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            const jobId = downloadBtn.dataset.jobId;
            if (!jobId) return;
            
            downloadBtn.textContent = 'Downloading...';
            downloadBtn.disabled = true;
            
            try {
                const response = await fetch(`${API_URL}/download/${jobId}`, {
                    headers: { 'Authorization': `Bearer ${authToken}` }
                });
                
                if (!response.ok) {
                    if (response.status === 401) {
                        logout();
                        showError('Session expired. Please sign in again.');
                        return;
                    }
                    throw new Error('Download failed');
                }
                
                // Get the blob and create download link
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `narrato_${jobId}.mp4`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
            } catch (error) {
                showError('Download failed: ' + error.message);
            } finally {
                downloadBtn.textContent = 'Download Video';
                downloadBtn.disabled = false;
            }
        });
        
        function showError(message) { 
            errorMessage.textContent = message; 
            errorMessage.classList.add('active'); 
        }
        function hideError() { errorMessage.classList.remove('active'); }
        
        // Start
        init();
    </script>
</body>
</html>'''