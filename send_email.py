import requests

def send_failure_email(video_id, error_msg):
    print("[EMAIL] Sending failure notification...")

    payload = {
        "to": "alert@example.com",
        "subject": f"[Download Failure] Video ID: {video_id}",
        "body": f"""
Download failed for video ID: {video_id}

Error Message:
--------------
{error_msg}
"""
    }

    # Sample dummy API endpoint (replace with your actual email API like SendGrid, Mailgun, etc.)
    api_url = "https://jsonplaceholder.typicode.com/posts"  # Replace with real email service
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        if response.status_code == 201:
            print("[EMAIL] Alert sent successfully.")
        else:
            print(f"[EMAIL] Failed to send email. Status: {response.status_code}")
    except Exception as e:
        print(f"[EMAIL] Exception while sending alert: {e}")
