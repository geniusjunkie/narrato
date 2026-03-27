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
        .form-group { margin-bottom: 1rem; }
        .form-group label {
            display: block;
            font-size: 0.875rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
        }
        .form-group select {
            width: 100%;
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            font-size: 0.875rem;
            cursor: pointer;
        }
        .form-group select:focus {
            outline: none;
            border-color: var(--accent-primary);
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
        .progress-steps {
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: var(--text-muted);
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
        .error-message {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid var(--error);
            border-radius: 0.75rem;
            padding: 1rem;
            margin-top: 1rem;
            color: var(--error);
            display: none;
        }
        .error-message.active { display: block; }
        .features {
            padding: 4rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        .features h2 {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2rem;
            text-align: center;
            margin-bottom: 3rem;
        }
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
        }
        .feature-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 1.5rem;
        }
        .feature-icon {
            width: 48px; height: 48px;
            background: var(--bg-tertiary);
            border-radius: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: 1rem;
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
    </nav>
    <section class="hero">
        <div class="badge">Free • No Credit Card Required</div>
        <h1>Turn Silent Videos Into <span>Professional Narrations</span></h1>
        <p>Upload your screen recording. Our AI analyzes the video, writes a script, and generates a natural voiceover.</p>
    </section>
    <main class="app-container">
        <div class="upload-zone" id="uploadZone">
            <input type="file" id="fileInput" accept="video/mp4,video/quicktime,video/x-msvideo,video/webm">
            <div class="upload-icon">📹</div>
            <h3>Drop your video here</h3>
            <p>or click to browse • MP4, MOV, AVI up to 100MB</p>
        </div>
        <div class="settings-panel">
            <h4>Voice Settings</h4>
            <div class="form-group">
                <label for="voiceSelect">Select Voice</label>
                <select id="voiceSelect">
                    <option value="en-US-AriaNeural">Aria — US Female (Professional)</option>
                    <option value="en-US-GuyNeural">Guy — US Male (Professional)</option>
                    <option value="en-GB-SoniaNeural">Sonia — UK Female</option>
                    <option value="en-GB-RyanNeural">Ryan — UK Male</option>
                    <option value="en-AU-NatashaNeural">Natasha — Australian Female</option>
                    <option value="en-IN-NeerjaNeural">Neerja — Indian Female</option>
                </select>
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
        <div class="result-section" id="resultSection">
            <h3>Your video is ready!</h3>
            <p>AI voiceover added successfully</p>
            <div class="btn-group">
                <a href="#" class="btn-success" id="downloadBtn" download>Download Video</a>
                <button class="btn-secondary" id="createAnotherBtn">Create Another</button>
            </div>
        </div>
    </main>
    <section class="features">
        <h2>How It Works</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">📤</div>
                <h3>1. Upload</h3>
                <p>Upload any silent screen recording. No audio required.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3>2. AI Analysis</h3>
                <p>Our AI extracts key frames and understands your video.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">✍️</div>
                <h3>3. Script Generation</h3>
                <p>AI writes a professional narration script.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎙️</div>
                <h3>4. Voice Synthesis</h3>
                <p>Choose from professional AI voices. Free and unlimited.</p>
            </div>
        </div>
    </section>
    <footer>
        <p>Built by Genius Junkie • Powered by Groq AI, Google Gemini, and Microsoft Edge TTS</p>
    </footer>
    <script>
        const API_URL = '';
        const uploadZone = document.getElementById('uploadZone');
        const fileInput = document.getElementById('fileInput');
        const voiceSelect = document.getElementById('voiceSelect');
        const progressSection = document.getElementById('progressSection');
        const resultSection = document.getElementById('resultSection');
        const errorMessage = document.getElementById('errorMessage');
        const progressBar = document.getElementById('progressBar');
        const statusText = document.getElementById('statusText');
        const progressPercent = document.getElementById('progressPercent');
        const downloadBtn = document.getElementById('downloadBtn');
        const createAnotherBtn = document.getElementById('createAnotherBtn');
        let currentJobId = null, pollInterval = null;
        
        uploadZone.addEventListener('click', () => fileInput.click());
        uploadZone.addEventListener('dragover', (e) => { e.preventDefault(); uploadZone.classList.add('dragover'); });
        uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault(); uploadZone.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
        });
        fileInput.addEventListener('change', (e) => { if (e.target.files.length > 0) handleFile(e.target.files[0]); });
        
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
            progressSection.classList.add('active');
            uploadZone.style.display = 'none';
            document.querySelector('.settings-panel').style.display = 'none';
            try {
                const response = await fetch(`${API_URL}/upload`, { method: 'POST', body: formData });
                if (!response.ok) { const error = await response.json(); throw new Error(error.detail || 'Upload failed'); }
                const data = await response.json();
                currentJobId = data.job_id;
                pollInterval = setInterval(() => checkStatus(currentJobId), 2000);
            } catch (error) { showError(error.message); resetUI(); }
        }
        
        async function checkStatus(jobId) {
            try {
                const response = await fetch(`${API_URL}/status/${jobId}`);
                const data = await response.json();
                updateProgress(data);
                if (data.status === 'completed') { clearInterval(pollInterval); showResult(jobId); }
                else if (data.status === 'failed') { clearInterval(pollInterval); showError(data.error || 'Processing failed'); resetUI(); }
            } catch (error) { console.error('Status check failed:', error); }
        }
        
        function updateProgress(data) {
            const progress = data.progress || 0;
            progressBar.style.width = `${progress}%`;
            progressPercent.textContent = `${progress}%`;
            statusText.textContent = data.message || 'Processing...';
        }
        
        function showResult(jobId) {
            progressSection.classList.remove('active');
            resultSection.classList.add('active');
            downloadBtn.href = `${API_URL}/download/${jobId}`;
        }
        
        function resetUI() {
            progressSection.classList.remove('active');
            resultSection.classList.remove('active');
            uploadZone.style.display = 'block';
            document.querySelector('.settings-panel').style.display = 'block';
            progressBar.style.width = '0%';
            progressPercent.textContent = '0%';
        }
        
        function showError(message) { errorMessage.textContent = message; errorMessage.classList.add('active'); }
        function hideError() { errorMessage.classList.remove('active'); }
        createAnotherBtn.addEventListener('click', () => { resetUI(); fileInput.value = ''; hideError(); });
    </script>
</body>
</html>'''