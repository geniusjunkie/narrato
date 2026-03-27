# 🎬 Narrato - AI Video Voiceover

Turn silent screen recordings into professional AI-narrated videos.

## ✨ Features

- 📤 **Upload** silent screen recordings
- 🤖 **AI Analysis** extracts key frames and understands your video
- ✍️ **Script Generation** writes professional narration
- 🎙️ **Voice Synthesis** using Microsoft Edge TTS (FREE)
- 🎬 **Auto-merge** video + audio with perfect sync
- 📥 **Download** your finished video

**Cost:** $0 (uses free API tiers)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd narrato
pip install -r requirements.txt
```

### 2. Set Up API Keys

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your keys
nano .env
```

**Get your free API keys:**
- **Groq:** https://console.groq.com → Sign up → API Keys → Create
- **Google AI:** https://aistudio.google.com/app/apikey → Create API Key

### 3. Run the Server

```bash
./start.sh
```

Or directly:
```bash
export GROQ_API_KEY="your-key-here"
export GOOGLE_API_KEY="your-key-here"
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Test the API

The API will be running at:
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs (interactive Swagger UI)

---

## 📡 API Endpoints

### Upload Video
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@your_video.mp4" \
  -F "voice=en-US-AriaNeural"
```

**Response:**
```json
{
  "job_id": "abc123",
  "status": "pending",
  "message": "Video uploaded successfully. Processing started.",
  "check_status": "/status/abc123"
}
```

### Check Status
```bash
curl "http://localhost:8000/status/abc123"
```

**Response:**
```json
{
  "job_id": "abc123",
  "status": "processing",
  "progress": 50,
  "message": "Generating voiceover script...",
  "output_url": null
}
```

### Download Video
```bash
curl "http://localhost:8000/download/abc123" -o output.mp4
```

### List Voices
```bash
curl "http://localhost:8000/voices"
```

---

## 🎙️ Available Voices

| Voice ID | Description | Language |
|----------|-------------|----------|
| `en-US-AriaNeural` | Professional Female (US) | English (US) |
| `en-US-GuyNeural` | Professional Male (US) | English (US) |
| `en-GB-SoniaNeural` | British Female | English (UK) |
| `en-GB-RyanNeural` | British Male | English (UK) |
| `en-AU-NatraNeural` | Australian Female | English (AU) |
| `en-IN-NeerjaNeural` | Indian Female | English (IN) |
| `es-ES-ElviraNeural` | Spanish Female | Spanish |
| `fr-FR-DeniseNeural` | French Female | French |

---

## 📁 Project Structure

```
narrato/
├── app/
│   ├── __init__.py
│   └── main.py              # FastAPI application
├── uploads/                 # Uploaded videos
├── outputs/                 # Processed videos
├── temp/                    # Temporary files
├── requirements.txt         # Python dependencies
├── start.sh                 # Startup script
├── test_api.py              # API test script
├── Dockerfile               # Docker configuration
├── .env.example             # Environment variables template
└── README.md                # This file
```

---

## 🔄 Processing Pipeline

1. **Upload** → Video saved to `uploads/`
2. **Frame Extraction** → 5 key frames extracted
3. **AI Analysis** → Gemini AI analyzes each frame
4. **Script Generation** → Groq AI writes narration
5. **Voice Synthesis** → Edge TTS generates audio
6. **Video Merge** → FFmpeg combines video + audio
7. **Download** → Final video in `outputs/`

**Typical processing time:** 2-3 minutes for a 2-minute video

---

## 🐛 Troubleshooting

### "API keys not configured"
Set your environment variables:
```bash
export GROQ_API_KEY="gsk_..."
export GOOGLE_API_KEY="AIza..."
```

### "Could not read video file"
- Ensure video format is MP4, MOV, AVI, or WebM
- Try re-encoding: `ffmpeg -i input.mov -c:v libx264 output.mp4`

### "FFmpeg not found"
Install FFmpeg:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Mac
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Processing takes too long
- Reduce video length (keep under 2 minutes)
- Lower `num_frames` parameter (default: 5)

---

## 🚀 Deploy to Render.com (FREE)

### 1. Push to GitHub

```bash
# Create a new GitHub repository
# Then push your code:
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/narrato.git
git push -u origin main
```

### 2. Deploy on Render

**Option A: Using render.yaml (Recommended)**

1. Go to https://dashboard.render.com
2. Click "New" → "Blueprint"
3. Connect your GitHub repo
4. Render will auto-detect `render.yaml`
5. Add environment variables:
   - `GROQ_API_KEY`
   - `GOOGLE_API_KEY`
6. Click "Apply"

**Option B: Manual Setup**

1. Go to https://dashboard.render.com
2. Click "New" → "Web Service"
3. Connect your GitHub repo
4. Settings:
   - **Name:** narrato
   - **Runtime:** Python 3
   - **Build Command:** `apt-get update && apt-get install -y ffmpeg libsm6 libxext6 libgl1 && pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `GROQ_API_KEY`
   - `GOOGLE_API_KEY`
6. Click "Create Web Service"

### 3. Your App is Live! 🎉

- **Frontend:** https://narrato-xxx.onrender.com
- **API:** https://narrato-xxx.onrender.com/docs

**Note:** Free tier spins down after 15 min inactivity. First request may take 30 seconds to wake up.

---

## Docker Deployment

```bash
docker build -t narrato .
docker run -p 8000:8000 -e GROQ_API_KEY=xxx -e GOOGLE_API_KEY=xxx narrato
```

---

## 💰 Cost Breakdown

| Service | Free Tier | Per Video |
|---------|-----------|-----------|
| Groq AI | 20 req/min | ~1 request |
| Google Gemini | 1,500 req/day | ~5 requests |
| Edge TTS | Unlimited | 1 request |
| **Total** | **FREE** | **$0** |

---

## 🎯 What's Built

| Component | Status |
|-----------|--------|
| ✅ Backend API | FastAPI with all endpoints |
| ✅ Frontend UI | Beautiful dark-themed web app |
| ✅ AI Pipeline | Frame analysis → Script → Voice → Merge |
| ✅ Render Deploy | `render.yaml` ready |
| ⏳ Custom Domain | Add narrato.geniusjunkie.net |
| ⏳ Payments | Stripe integration for subscriptions |

---

## 📝 License

MIT License - Build your video empire!

---

## 💡 Pro Tips

1. **Test locally first** — Make sure your API keys work
2. **Start with short videos** — Under 2 minutes for best results
3. **Use free tiers wisely** — Groq: 20 req/min, Google: 1,500/day
4. **Custom domain** — Point narrato.geniusjunkie.net to Render
5. **Monitor usage** — Add analytics before charging money

---

Built with ❤️ by Genius Junkie
