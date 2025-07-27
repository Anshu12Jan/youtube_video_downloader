# YouTube Video Downloader with Proxy Fallback

This script downloads YouTube videos using `yt-dlp`, with request throttling, cookie/user-agent rotation, and proxy fallback support.

---

## ✅ Features

- Simple download via `yt-dlp`
- Randomized delay to mimic human behavior
- Proxy fallback for blocked IPs
- Cookie and user-agent rotation for obfuscation
- Database update after each attempt

---

## 📦 Requirements

- Python 3.7+
- Modules:
  - `yt-dlp`
  - `retrieve_proxy`, `db_`, `send_email` (custom modules)

---

## 🛠️ Usage

1. Set the `video_id` environment variable:
```bash
export video_id=dQw4w9WgXcQ
