import requests


def post_reminder(token, channel, reminder):
    print(f"[INFO] Posting reminder:\n{reminder}")
    res = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={'Authorization': f'Bearer {token}'},
        json={
            "channel": channel,
            "text": reminder['text'],
            "attachments": reminder['attachments']
        })
    if not (res.ok and res.json()['ok']):
        print(f"[FAILED] Could not post reminder: {res.text}")
        return False
    print(f"[INFO] Reminder posted successfully.")
    return True
