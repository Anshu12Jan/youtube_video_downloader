import os
import random
import time
import yt_dlp
import retrieve_proxy
import db_
from send_email import send_failure_email

USER_AGENTS = [
    "Mozilla/5.0 *******************************************",
    "Mozilla/5.0 *******************************************",
    "Mozilla/5.0 *******************************************",
]

_last_download_time = [0]

def throttle(min_interval=5):
    now = time.time()
    elapsed = now - _last_download_time[0]
    if elapsed < min_interval:
        wait_time = min_interval - elapsed
        print(f"[THROTTLE] Sleeping for {wait_time:.2f}s to throttle requests.")
        time.sleep(wait_time)
    _last_download_time[0] = time.time()

def get_random_cookie_file():
    cookie_files = [f for f in os.listdir(".") if f.startswith("cookies") and f.endswith(".txt")]
    return f"/{random.choice(cookie_files)}" if cookie_files else None

def download_video_dl(video_id):
    input_url = f'https://www.youtube.com/watch?v={video_id}'
    video_path = f'Video/{video_id}.mp4'

    def get_ydl_opts(proxy=None):
        cookie_file = get_random_cookie_file()
        user_agent = random.choice(USER_AGENTS)
        print(f"[INFO] Using cookie file: {cookie_file}")
        print(f"[INFO] Using user-agent: {user_agent}")
        opts = {
            'retries': 1,
            'outtmpl': video_path,
            'cookiefile': cookie_file,
            'format': 'mp4',
            'quiet': True,
            "nocheckcertificate": True,
            'throttled_rate': '100K',
            'sleep_interval': random.randint(2, 10),
            'max_sleep_interval': random.randint(10, 15),
            "http_headers": {"User-Agent": user_agent},
        }
        if proxy:
            opts['proxy'] = proxy
        return opts

    try:
        print("[$] Downloading without proxy")
        throttle(min_interval=random.randint(2, 15))
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            ydl.download([input_url])
        return {"url": video_path, 'statusCode': 200}
    except Exception as e:
        print("[$] Non-proxy download failed. Switching to proxy...")
        send_failure_email(video_id, str(e))
        try:
            proxy_url = retrieve_proxy.retrive_proxy()['https']
            print(f"[$] Retrying with proxy: {proxy_url}")
            throttle(min_interval=random.randint(2, 15))
            with yt_dlp.YoutubeDL(get_ydl_opts(proxy=proxy_url)) as ydl:
                ydl.download([input_url])
            return {"url": video_path, 'statusCode': 200}
        except Exception as proxy_error:
            print(f"[X] Proxy download failed: {proxy_error}")
            return {"url": str(proxy_error), 'statusCode': 400}

if __name__ == "__main__":
    video_id = os.environ.get("video_id")

    if not video_id:
        print("[X] Missing video_id environment variable.")
        exit(1)

    for attempt in range(2):
        try:
            sleep_time = random.randint(2, 15)
            print(f"[THROTTLE] Sleeping {sleep_time}s before download attempt {attempt + 1}.")
            time.sleep(sleep_time)

            resp = download_video_dl(video_id)

            if resp['statusCode'] == 200:
                db_.update_video_url(
                    vid_id=str(video_id),
                    pre_url=resp['url'],
                    negative_keyword=None,
                    brand=None
                )
                print(f"[SUCCESS] Download completed for video {video_id}")
                break
            else:
                print(f"[WARN] Attempt {attempt+1} failed with status {resp['statusCode']}")
        except Exception as e:
            print(f"[ERROR] Download attempt {attempt + 1} failed: {e}")
    else:
        db_.update_video_url(str(video_id), "Download failed after 2 attempts")
        print(f"[FAILURE] All download attempts failed for video {video_id}")
