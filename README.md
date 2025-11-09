# Flask Video Downloader

✨ **Overview**

This is a simple, web-based video downloader built using Flask (Python) for the backend and [yt-dlp](https://github.com/yt-dlp/yt-dlp) for handling the video extraction and downloading logic. It allows users to download videos from popular platforms like YouTube, Facebook, TikTok, X (Twitter), and Instagram by simply pasting the URL into a web form. The application features real-time download progress displayed directly in the user interface, improving user feedback for long-running downloads.

---

## 🚀 Features

- **Multi-Platform Support**: Download videos from YouTube, TikTok, Instagram, X/Twitter, and Facebook.
- **Real-Time Progress**: Uses AJAX polling to display download percentage, speed, and ETA.
- **Robust Downloading**: Utilizes the powerful yt-dlp library for best video quality extraction.
- **Timeout Protection**: Increased socket timeout for slow or large downloads.
- **Activity Logging**: Logs download start, finish, and failure events to `download_log.txt`.

---

## 💻 Installation and Setup

### 1. Dependencies

- Python 3.7 or higher.
- `yt-dlp` Python library.
- **FFmpeg**: Needed for video/audio merging and processing.
  - For Windows: Download FFmpeg binaries from [FFmpeg official site](https://ffmpeg.org/download.html) or trusted builds like [FFmpeg-Builds](https://github.com/GyanD/codexffmpeg/releases), and add the FFmpeg `bin` folder to your system PATH environment variable.
  - For Linux: Install via terminal with:


- Clone this repository and install the dependencies:

### a. Clone the repository
        git clone <repository-url>

### b. Navigate into the project directory
        cd video-downloader

### c. Create a virtual environment named 'venv'
        python -m venv venv

### d. Activate the virtual environment

        source venv/bin/activate  (linux/macOs)
        
    
        venv\Scripts\activate  (On windows)


#### e. Install the required Python packages
        pip install flask yt-dlp

---

### 2. Running the App

1. Run the Flask app:

        python app.py

2. Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ⚙️ Configuration & Details

- Make sure `yt-dlp` is properly installed; update it often for best results.
- Real-time progress is handled in `static/js/app.js` via periodic AJAX requests.
- Logs are stored in `download_log.txt` for basic tracking of download activities.
- The UI can be customized in `templates/index.html` and styled via `static/css/main.css`.

---

## 📝 Notes

- Downloading copyrighted content without permission may violate terms of service and copyright laws.
- This project is intended for education or personal use only.

---

## 📄 License

MIT License

---

## Credits

- [Flask](https://flask.palletsprojects.com/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)


