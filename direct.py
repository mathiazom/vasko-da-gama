import requests


def post_reminder(token, channel, reminder) -> bool:
    print(f"[INFO] Posting reminder:\n{reminder}")
    res = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={'Authorization': f'Bearer {token}'},
        json={
            "channel": channel,
            "text": reminder['text'],
            "attachments": reminder['attachments']
        })
    if not res.ok:
        print(f"[FAILED] Could not post reminder: {res.text}")
        return False
    try:
        res_data = res.json()
    except ValueError:
        print(f"[FAILED] Could not retrieve json of reminder request response")
        return False
    if not res_data['ok']:
        print(f"[FAILED] Could not post reminder: {res.text}")
        return False
    reminder_message_ts = res_data['ts']
    reminder_chores = reminder['chores']
    if reminder_chores:
        for text in reminder_chores:
            print(text)
            if not post_reminder_chores(token, channel, reminder_message_ts, text):
                return False
    print(f"[INFO] Reminder posted successfully.")
    return True


def post_reminder_chores(token, channel, parent_message_ts, text) -> bool:
    print(f"[INFO] Posting reminder chores: {text}")
    res = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={'Authorization': f'Bearer {token}'},
        json={
            "channel": channel,
            "thread_ts": parent_message_ts,
            "text": text
        })
    if not res.ok:
        print(f"[FAILED] Could not post reminder chores: {res.text}")
        return False
    print(f"[INFO] Reminder chores posted successfully.")
    return True
