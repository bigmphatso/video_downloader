
import re
import yt_dlp
import os
import datetime

# --- LOGGING SETUP ---
LOG_FILE = "download_log.txt"

def log_event(message: str):
    """Writes a timestamped message to the log file."""
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} {message}\n")

# --- PROGRESS TRACKING ---
current_download_progress = {}

def progress_hook(d):
    """
    Hook function called by yt-dlp to report download progress.
    Updates the global progress dictionary with detailed metrics.
    """
    global current_download_progress
    
    current_download_progress['status'] = d['status']
    
    if d['status'] == 'downloading':
        # Capture and format detailed progress metrics
        current_download_progress['percent'] = f"{d['_percent_str'].strip()}"
        current_download_progress['speed'] = f"{d['_speed_str'].strip()}"
        current_download_progress['eta'] = f"{d['_eta_str'].strip()}"
        current_download_progress['downloaded_bytes'] = f"{d['_downloaded_bytes_str'].strip()}"
        current_download_progress['total_size'] = f"{d['_total_bytes_str'].strip() if d.get('_total_bytes_str') else 'N/A'}"
        
    elif d['status'] == 'finished':
        current_download_progress['percent'] = "100%"
        current_download_progress['speed'] = "N/A"
        current_download_progress['eta'] = "00:00"
        
    elif d['status'] == 'error':
        current_download_progress['percent'] = "N/A"
        # Log the critical error
        log_event(f"ERROR: Download failed for URL. Status: {d.get('error', 'Unknown Error')}")


# --- DOWNLOAD FUNCTION ---
def detect_platform(url: str) -> str:
    """Detects the video platform based on the URL using regex."""
    patterns = {
        "youtube": r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/",
        "tiktok": r"(https?://)?(www\.)?tiktok\.com/",
        "instagram": r"(https?://)?(www\.)?instagram\.com/",
        "facebook": r"(https?://)?(www\.)?facebook\.com/",
        "x": r"(https?://)?(www\.)?(x\.com|twitter\.com)/"
    }

    for platform, pattern in patterns.items():
        if re.search(pattern, url, re.IGNORECASE):
            return platform
    return "unknown"
    
def download_video(url: str, output_dir: str = "downloads"):
    global current_download_progress
    os.makedirs(output_dir, exist_ok=True)
    platform = detect_platform(url)

    # Log START
    log_event(f"START: Initiating download for URL: {url} (Platform: {platform})")
    current_download_progress = {"status": "starting", "percent": "0.0"}

    ydl_opts = {
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "format": "bestvideo+bestaudio/best",
        "socket_timeout": 300, 
        "progress_hooks": [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            title = info.get("title", "video")
            filename = ydl.prepare_filename(info)
            
            # Log FINISH
            log_event(f"FINISH: Successfully downloaded '{title}'. File: {os.path.basename(filename)}")
            
            return {"status": "success", "title": title, "file": os.path.basename(filename), "platform": platform}
            
    except Exception as e:
        # Log FAIL
        log_event(f"FAIL: Download failed for URL {url}. Reason: {str(e)}")
        current_download_progress['status'] = "error"
        return {"status": "error", "message": str(e)}

# --- NEW FUNCTION FOR FLASK TO POLL ---
def get_progress():
    """Returns the current download progress dictionary."""
    global current_download_progress
    return current_download_progress

