"""
Narrato - FastAPI Backend
AI-powered video voiceover generation
"""

import os
import uuid
import asyncio
import base64
import io
import json
from typing import Optional
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, WebSocket
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Import frontend HTML
from app.frontend import FRONTEND_HTML

# Video processing imports
import cv2
from PIL import Image
from gtts import gTTS
import requests
from groq import Groq

# Configuration
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
TEMP_DIR = Path("temp")

# Create directories
for dir_path in [UPLOAD_DIR, OUTPUT_DIR, TEMP_DIR]:
    dir_path.mkdir(exist_ok=True)

# API Keys from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

app = FastAPI(
    title="Narrato API",
    description="AI-powered video voiceover generation",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job storage (use Redis in production)
jobs = {}

# Pydantic Models
class JobStatus(BaseModel):
    job_id: str
    status: str  # pending, processing, analyzing, scripting, voicing, merging, completed, failed
    progress: int = Field(0, ge=0, le=100)
    message: str
    created_at: str
    completed_at: Optional[str] = None
    output_url: Optional[str] = None
    error: Optional[str] = None


class ProcessRequest(BaseModel):
    voice: str = "en-US-AriaNeural"  # Default voice
    num_frames: int = 5


# Job Status Constants
class Status:
    PENDING = "pending"
    PROCESSING = "processing"
    ANALYZING = "analyzing"
    SCRIPTING = "scripting"
    VOICING = "voicing"
    MERGING = "merging"
    COMPLETED = "completed"
    FAILED = "failed"


# Helper Functions
def update_job(job_id: str, status: str, progress: int, message: str, error: str = None):
    """Update job status in memory store"""
    if job_id in jobs:
        update_data = {
            "status": status,
            "progress": max(0, min(100, progress)),  # Clamp between 0-100
            "message": message,
        }
        if error is not None:
            update_data["error"] = error
        if status == Status.COMPLETED:
            update_data["completed_at"] = datetime.now().isoformat()
            update_data["output_url"] = f"/download/{job_id}"
        jobs[job_id].update(update_data)


def extract_key_frames(video_path: str, num_frames: int = 5):
    """Extract evenly spaced frames from video"""
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0
    
    if total_frames == 0:
        cap.release()
        raise ValueError("Could not read video file")
    
    # Ensure num_frames is at least 2 to avoid division by zero
    num_frames = max(2, num_frames)
    
    # Calculate frame positions - avoid division by zero
    if num_frames == 1:
        frame_positions = [total_frames // 2]  # Middle frame
    else:
        frame_positions = [int(total_frames * i / (num_frames - 1)) for i in range(num_frames)]
    
    frames = []
    for pos in frame_positions:
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            frames.append(img)
    
    cap.release()
    return frames, duration


def analyze_frame_with_gemini(image: Image.Image, api_key: str) -> str:
    """Send frame to Gemini AI for analysis"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{
                "text": "Describe what is happening in this screen recording frame in one sentence. Be specific about any UI elements, buttons, or actions being shown."
            }, {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": img_str
                }
            }]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Frame shows part of the tutorial"
    except Exception as e:
        return f"Frame shows tutorial content"


def generate_script(descriptions: list, duration: float, api_key: str) -> str:
    """Generate narration script from frame descriptions"""
    client = Groq(api_key=api_key)
    
    context = "\n".join([f"Frame {i+1}: {desc}" for i, desc in enumerate(descriptions)])
    target_words = int(duration * 150 / 60)  # ~150 words per minute
    
    prompt = f"""You are a professional tutorial narrator. Write a clear, engaging voiceover script for a tutorial video.

Video frames description:
{context}

Target length: approximately {target_words} words (for a {duration:.0f} second video)

Write a natural-sounding narration that explains what's happening step by step. Use simple, clear language. Don't mention "frames" or "the video shows" - just narrate as if you're guiding someone through the process in real-time.

Format as clean paragraphs."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )
    
    return response.choices[0].message.content


async def generate_voiceover(text: str, voice: str, output_path: str):
    """Generate voice using Google TTS (FREE - works on all servers)"""
    import traceback
    
    # Map voice to language code (gTTS uses simple lang codes)
    lang_map = {
        "en-US-AriaNeural": "en",
        "en-US-GuyNeural": "en",
        "en-GB-SoniaNeural": "en",
        "en-GB-RyanNeural": "en",
        "en-AU-NatashaNeural": "en",
        "en-IN-NeerjaNeural": "en",
    }
    lang = lang_map.get(voice, "en")
    
    # Run gTTS in thread pool since it's blocking
    def _generate():
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(output_path)
            # Verify file was created
            if not os.path.exists(output_path):
                raise Exception("gTTS failed to create audio file")
            if os.path.getsize(output_path) == 0:
                raise Exception("gTTS created empty audio file")
            print(f"[INFO] Voiceover saved to {output_path} ({os.path.getsize(output_path)} bytes)")
        except Exception as e:
            print(f"[ERROR] gTTS failed: {e}")
            print(traceback.format_exc())
            raise
    
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _generate)


def merge_video_audio(video_path: str, audio_path: str, output_path: str):
    """Combine video and audio using ffmpeg (memory-efficient, streams instead of loading into RAM)"""
    import subprocess
    import traceback
    
    try:
        # Get video duration using ffprobe
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        video_duration = float(result.stdout.strip())
        
        # Get audio duration
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            audio_path
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        audio_duration = float(result.stdout.strip())
        
        print(f"[INFO] Video duration: {video_duration}s, Audio duration: {audio_duration}s")
        
        # Build ffmpeg command
        if audio_duration >= video_duration:
            # Audio is longer, just trim it
            cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',  # Copy video stream (no re-encoding)
                '-c:a', 'aac',
                '-t', str(video_duration),  # Trim to video duration
                '-shortest',
                '-movflags', '+faststart',  # Enable streaming
                output_path
            ]
        else:
            # Audio is shorter, loop it to match video duration
            cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-stream_loop', '-1',  # Loop audio infinitely
                '-i', audio_path,
                '-c:v', 'copy',  # Copy video stream (no re-encoding)
                '-c:a', 'aac',
                '-t', str(video_duration),  # Trim to video duration
                '-shortest',
                '-movflags', '+faststart',  # Enable streaming
                output_path
            ]
        
        print(f"[INFO] Running ffmpeg merge...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"[INFO] ffmpeg merge completed successfully")
        return output_path
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] ffmpeg failed: {e}")
        print(f"[ERROR] stdout: {e.stdout}")
        print(f"[ERROR] stderr: {e.stderr}")
        raise Exception(f"Video merge failed: {e.stderr}")
    except Exception as e:
        print(f"[ERROR] merge_video_audio failed: {e}")
        print(traceback.format_exc())
        raise


async def process_video_job(job_id: str, video_path: str, voice: str, num_frames: int):
    """Background task to process video - ALL blocking ops run in thread pool"""
    loop = asyncio.get_event_loop()
    
    try:
        # Validate API keys
        if not GROQ_API_KEY or not GOOGLE_API_KEY:
            raise ValueError("API keys not configured. Set GROQ_API_KEY and GOOGLE_API_KEY environment variables.")
        
        # Step 1: Extract frames (CPU-intensive, run in thread)
        update_job(job_id, Status.ANALYZING, 5, "Extracting frames from video...")
        frames, duration = await loop.run_in_executor(
            None, extract_key_frames, video_path, num_frames
        )
        
        # Step 2: Analyze frames (network calls, run in thread)
        update_job(job_id, Status.ANALYZING, 10, f"Analyzing {len(frames)} video frames with AI...")
        frame_descriptions = []
        for i, frame in enumerate(frames):
            desc = await loop.run_in_executor(
                None, analyze_frame_with_gemini, frame, GOOGLE_API_KEY
            )
            frame_descriptions.append(desc)
            # Progress increases from 10% to 35% based on frame analysis
            progress = 10 + int((i + 1) / len(frames) * 25)
            update_job(job_id, Status.ANALYZING, progress, f"Analyzed frame {i+1}/{len(frames)}")
        
        # Step 3: Generate script (network call, run in thread)
        update_job(job_id, Status.SCRIPTING, 40, "Generating voiceover script...")
        script = await loop.run_in_executor(
            None, generate_script, frame_descriptions, duration, GROQ_API_KEY
        )
        
        # Save script for reference (file I/O, run in thread)
        script_path = OUTPUT_DIR / f"{job_id}_script.txt"
        def _save_script():
            with open(script_path, 'w') as f:
                f.write(script)
        await loop.run_in_executor(None, _save_script)
        
        # Step 4: Generate voiceover (already async with thread pool inside)
        update_job(job_id, Status.VOICING, 60, "Generating AI voiceover...")
        audio_path = str(TEMP_DIR / f"{job_id}_voiceover.mp3")
        await generate_voiceover(script, voice, audio_path)
        
        # Verify audio file was created
        def _verify_audio():
            if not os.path.exists(audio_path):
                raise Exception(f"Audio file not found: {audio_path}")
            size = os.path.getsize(audio_path)
            if size == 0:
                raise Exception("Audio file is empty")
            return size
        
        audio_size = await loop.run_in_executor(None, _verify_audio)
        print(f"[INFO] Audio file verified: {audio_size} bytes")
        
        # Step 5: Merge video and audio (CPU-intensive, run in thread)
        update_job(job_id, Status.MERGING, 85, "Merging video and audio...")
        output_path = str(OUTPUT_DIR / f"{job_id}_final.mp4")
        await loop.run_in_executor(
            None, merge_video_audio, video_path, audio_path, output_path
        )
        
        # Verify output file was created
        def _verify_output():
            if not os.path.exists(output_path):
                raise Exception(f"Output video not found: {output_path}")
            size = os.path.getsize(output_path)
            if size == 0:
                raise Exception("Output video is empty")
            return size
        
        output_size = await loop.run_in_executor(None, _verify_output)
        print(f"[INFO] Output video verified: {output_size} bytes")
        
        # Cleanup temp files (run in thread)
        def _cleanup():
            try:
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                    print(f"[INFO] Cleaned up temp audio: {audio_path}")
            except Exception as e:
                print(f"[WARN] Failed to cleanup audio file: {e}")
        await loop.run_in_executor(None, _cleanup)
        
        # Mark complete
        update_job(job_id, Status.COMPLETED, 100, "Video processing complete!")
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"[ERROR] Job {job_id} failed: {error_msg}")
        print(traceback.format_exc())
        # Preserve the last progress instead of resetting to 0
        current_progress = jobs.get(job_id, {}).get("progress", 0)
        update_job(job_id, Status.FAILED, current_progress, f"Failed at {current_progress}%: {error_msg}", error=error_msg)


# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend HTML"""
    return FRONTEND_HTML


@app.post("/upload")
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    voice: str = "en-US-AriaNeural",
    num_frames: int = 5
):
    """Upload a video and start processing"""
    
    # Validate file type
    allowed_types = ['video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/webm']
    if file.content_type not in allowed_types:
        raise HTTPException(400, f"Invalid file type. Allowed: {allowed_types}")
    
    # Generate job ID
    job_id = str(uuid.uuid4())[:8]
    
    # Save uploaded file
    file_ext = file.filename.split('.')[-1]
    video_path = str(UPLOAD_DIR / f"{job_id}.{file_ext}")
    
    with open(video_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Create job entry
    jobs[job_id] = {
        "job_id": job_id,
        "status": Status.PENDING,
        "progress": 0,
        "message": "Video uploaded, starting processing...",
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "output_url": None,
        "error": None,
        "video_path": video_path
    }
    
    # Start background processing
    background_tasks.add_task(process_video_job, job_id, video_path, voice, num_frames)
    update_job(job_id, Status.PROCESSING, 5, "Starting video analysis...")
    
    return {
        "job_id": job_id,
        "status": Status.PENDING,
        "message": "Video uploaded successfully. Processing started.",
        "check_status": f"/status/{job_id}"
    }


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """Get processing status"""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    
    job = jobs[job_id]
    return {
        "job_id": job_id,
        "status": job["status"],
        "progress": job["progress"],
        "message": job["message"],
        "created_at": job["created_at"],
        "completed_at": job.get("completed_at"),
        "output_url": job.get("output_url"),
        "error": job.get("error")
    }


@app.get("/download/{job_id}")
async def download_video(job_id: str):
    """Download processed video"""
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    
    job = jobs[job_id]
    if job["status"] != Status.COMPLETED:
        raise HTTPException(400, f"Video not ready. Status: {job['status']}")
    
    output_path = OUTPUT_DIR / f"{job_id}_final.mp4"
    if not output_path.exists():
        raise HTTPException(404, "Output file not found")
    
    return FileResponse(
        path=output_path,
        filename=f"narrato_{job_id}.mp4",
        media_type="video/mp4"
    )


@app.get("/voices")
async def list_voices():
    """List available voices"""
    return {
        "voices": [
            {"id": "en-US-AriaNeural", "name": "Aria (US Female)", "language": "English (US)"},
            {"id": "en-US-GuyNeural", "name": "Guy (US Male)", "language": "English (US)"},
            {"id": "en-GB-SoniaNeural", "name": "Sonia (UK Female)", "language": "English (UK)"},
            {"id": "en-GB-RyanNeural", "name": "Ryan (UK Male)", "language": "English (UK)"},
            {"id": "en-AU-NatashaNeural", "name": "Natasha (AU Female)", "language": "English (Australia)"},
            {"id": "en-IN-NeerjaNeural", "name": "Neerja (IN Female)", "language": "English (India)"},
            {"id": "es-ES-ElviraNeural", "name": "Elvira (Spanish Female)", "language": "Spanish"},
            {"id": "fr-FR-DeniseNeural", "name": "Denise (French Female)", "language": "French"},
            {"id": "de-DE-KatjaNeural", "name": "Katja (German Female)", "language": "German"},
        ]
    }


# WebSocket for real-time updates (optional)
@app.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await websocket.accept()
    
    if job_id not in jobs:
        await websocket.send_json({"error": "Job not found"})
        await websocket.close()
        return
    
    # Send current status
    await websocket.send_json(jobs[job_id])
    
    # Keep connection open and poll for updates
    last_status = jobs[job_id]["status"]
    last_progress = jobs[job_id].get("progress", 0)
    
    while last_status not in [Status.COMPLETED, Status.FAILED]:
        await asyncio.sleep(1)
        if job_id in jobs:
            current = jobs[job_id]
            current_progress = current.get("progress", 0)
            # Check if status or progress changed
            if current["status"] != last_status or current_progress != last_progress:
                await websocket.send_json(current)
                last_status = current["status"]
                last_progress = current_progress
    
    # Send final status
    if job_id in jobs:
        await websocket.send_json(jobs[job_id])
    
    await websocket.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
